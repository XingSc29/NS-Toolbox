import re
import nmap
from prettytable import PrettyTable
import argparse
import yaml


class PortScanner:
    def __init__(self, ip_address, scan_type):
        self.ip_address = ip_address
        self.scan_type = scan_type
        self.port_scanner = nmap.PortScanner()

    def run(self):
        host_script = True
        os_detection = True
        port_script = True
        port_scan = True
        if self.scan_type == "Intense scan":
            self.port_scanner.scan(self.ip_address, arguments="-v -T4 -A")

        elif self.scan_type == "Intense scan plus UDP":
            print("[+] UDP scan is enabled, it might take very long depending on the host range.")
            self.port_scanner.scan(self.ip_address, arguments="-v -sS -sU -T4 -A")

        elif self.scan_type == "Intense scan, all TCP ports":
            self.port_scanner.scan(self.ip_address, "1-65535", "-v -T4 -A")

        elif self.scan_type == "Intense scan, no ping":
            self.port_scanner.scan(self.ip_address, arguments="-v -T4 -A -Pn")

        elif self.scan_type == "Ping scan":
            self.port_scanner.scan(self.ip_address, arguments="-v -sn")
            host_script = False
            os_detection = False
            port_script = False
            port_scan = False

        elif self.scan_type == "Quick scan":
            self.port_scanner.scan(self.ip_address, arguments="-T4 -F")
            host_script = False
            os_detection = False
            port_script = False

        elif self.scan_type == "Quick scan plus":
            self.port_scanner.scan(self.ip_address, arguments="-sV -T4 -O -F --version-light")
            host_script = False
            port_script = False

        elif self.scan_type == "Regular scan":
            self.port_scanner.scan(self.ip_address, arguments="-sS")
            host_script = False
            port_script = False
            os_detection = False

        # elif self.scan_type == "Quick traceroute":
        #     self.port_scanner.scan(self.ip_address, arguments="-sn --traceroute")
        #     host_script = False
        #     os_detection = False

        # Print host information
        self.print_host_information(host_script, os_detection, port_script)
        # Print port info
        if port_scan:
            self.print_port_info_table()

    def print_host_information(self, host_script, os_detection, port_script):
        print("[+] Showing maximum obtained information...")
        hosts_list = self.port_scanner.all_hosts()
        for host in hosts_list:
            status = self.port_scanner[host].state()
            if status == "down":
                continue

            print("\n\n===================================================== Host ====================================================")
            print("IP address:", self.port_scanner[host]["addresses"]["ipv4"])
            print("Status:", status)
            try:
                print("MAC address:", self.port_scanner[host]["addresses"]["mac"])
                print("Vendor:", self.port_scanner[host]["vendor"][self.port_scanner[host]["addresses"]["mac"]])
            except KeyError:
                pass

            # If OS detection is enabled
            if os_detection:
                try:
                    osmatches = self.port_scanner[host]["osmatch"]
                    os_guess_table = PrettyTable(["OS detection", "Accuracy"])
                    for osmatch in osmatches:
                        os_guess_table.add_row([osmatch["name"], osmatch["accuracy"]])
                    print(str(os_guess_table) + "\n")
                except KeyError:
                    pass

            # if host script is done
            if host_script:
                try:
                    hostscript_dic = self.port_scanner[host]["hostscript"]
                    print("------------------------------------------------- Host Script -------------------------------------------------")
                    # Pretty print the hostscript nested dictionary
                    print("Host script:")
                    print(yaml.dump(hostscript_dic, default_flow_style=False).replace("\\", ""))
                except KeyError:
                    pass
            # if port script is done
            if port_script:
                try:
                    ports_list = self.port_scanner[host]["tcp"].keys()
                    # Check if port script is found or not
                    port_script_found = False
                    for port in ports_list:
                        try:
                            port_script_dic = self.port_scanner[host]["tcp"][port]["script"]
                            port_script_found = True
                        except KeyError:
                            pass
                    if port_script_found:
                        print("------------------------------------------------ Port Scripts -------------------------------------------------")

                    # Pretty print port script
                    for port in ports_list:
                        try:
                            port_script_dic = self.port_scanner[host]["tcp"][port]["script"]
                            # Pretty print the port script nested dictionary
                            print(f"Port scripts ({port}):")
                            print(yaml.dump(port_script_dic, default_flow_style=False).replace("\n\n", "\n").replace("\\", ""))
                        except KeyError:
                            pass
                except KeyError:
                    pass

    # Print port info in a prettytable for all hosts
    def print_port_info_table(self):
        print("\n==================================================== Ports ====================================================")
        ports_csv = self.port_scanner.csv().split("\n")
        # Get Headers
        csv_headers = ports_csv[0].split(";")
        csv_headers[12] = csv_headers[12].replace("\r", "")  # Remove "\r"
        del ports_csv[0]  # Remove headers from ports_csv
        del ports_csv[-1]  # Remove last empty line from ports_csv
        # Create header for PrettyTable
        port_info_table = PrettyTable([csv_headers[0], csv_headers[3], csv_headers[4], csv_headers[5], csv_headers[6],
                                       csv_headers[7], csv_headers[8], csv_headers[10], csv_headers[12]])
        # Append port info into pretty table
        for port_info in ports_csv:
            port_info = port_info.split(";")
            port_info[12] = port_info[12].replace("\r", "")  # Remove "\r"
            # print(port_info)  # Check (delete it later)
            for i in range(len(port_info)):
                if port_info[i] == "":
                    port_info[i] = "-"
            port_info_table.add_row([port_info[0], port_info[3], port_info[4], port_info[5], port_info[6], port_info[7],
                                     port_info[8], port_info[10], port_info[12]])
        print("Port info:")
        print(str(port_info_table))


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--scan", dest="scan_type", help="The scan type to be used")
    parser.add_argument("-t", "--target", dest="target", help="The target to be scanned")
    options = parser.parse_args()

    return options


# Get arguments
options = get_arguments()
scan_type = options.scan_type
target_ip = options.target
# Initialize port scanner and run
scanner = PortScanner(target_ip, scan_type)
scanner.run()
