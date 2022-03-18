import scapy.all as scapy
import requests
import time


class NetworkScanner:
    def __init__(self, update_progress):
        self.ip_range = None
        self.interface = None
        self.count = None
        self.update_progress = update_progress

    def set_ip_range(self, ip_range):
        self.ip_range = ip_range

    def set_interface(self, interface):
        self.interface = interface

    def set_count(self, count):
        self.count = count

    def scan(self):
        arp_request = scapy.ARP(pdst=self.ip_range)
        broadcast = scapy.Ether(dst="FF:FF:FF:FF:FF:FF:FF")
        arp_request_broadcast = broadcast / arp_request

        clients_list = []

        for i in range(self.count):
            answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False, iface=self.interface)[0]
            print(f"\r[+] {self.count - 1 - i} scan left", end="")
            # Update scan progress bar
            self.update_progress.emit((i + 1) / self.count * 100 - i * 4)
            for element in answered_list:
                client_dict = {"ip": element[1].psrc, "mac": element[1].hwsrc, "ven": "Unknown"}
                if client_dict not in clients_list:
                    clients_list.append(client_dict)

        for x in clients_list:
            url = "http://api.macvendors.com/" + x["mac"]
            connection_error = True
            while connection_error: 
                try:
                    vendor_request = requests.get(url)
                    if vendor_request.ok:
                        x["ven"] = vendor_request.text
                    time.sleep(0.5)
                    connection_error = False
                except requests.exceptions.ConnectionError as e:
                    pass
        self.update_progress.emit(100)
        return clients_list
