import subprocess
import argparse
import os
import signal
import time


# Disable IP forwarding and flush IPTables rule
class FakeAccessPoint:
    def __init__(self, wireless_interface, ssid, network_interface):
        self.wireless_interface = wireless_interface
        self.ssid = ssid
        self.network_interface = network_interface

    def init_hostapd(self):
        configurations = [
            f"interface={self.wireless_interface}\n",
            "driver=nl80211\n", 
            f"ssid={self.ssid}\n", 
            "hw_mode=g\n", 
            "channel=5\n", 
            "macaddr_acl=0\n", 
            "ignore_broadcast_ssid=0\n"
            ]
        hostapd_conf = open("src/fap/hostapd.conf", "w+")
        hostapd_conf.writelines(configurations)
        hostapd_conf.close()

    def init_dnsmasq(self):
        configurations = [
            f"interface={self.wireless_interface} \n",
            "dhcp-range=192.168.1.2, 192.168.1.30, 255.255.255.0, 12h \n",
            "dhcp-option=3, 192.168.1.1 \n",
            "dhcp-option=6, 192.168.1.1 \n",
            "server=8.8.8.8 \n",
            "log-queries \n",
            "log-dhcp \n",
            "listen-address=127.0.0.1 \n" 
        ]
        dnsmasq_conf = open("src/fap/dnsmasq.conf", "w+")
        dnsmasq_conf.writelines(configurations)
        dnsmasq_conf.close()

    def interface_setup(self):
        configurations = [
            f"ifconfig {self.wireless_interface} up 192.168.1.1 netmask 255.255.255.0 \n",
            "route add -net 192.168.1.0 netmask 255.255.255.0 gw 192.168.1.1 \n"
        ]
        interface_setup_script = open("src/fap/interface_setup.sh", "w+")
        interface_setup_script.writelines(configurations)
        interface_setup_script.close()

    def network_setup(self):
        configurations = [
            f"iptables --table nat --append POSTROUTING --out-interface {self.network_interface} -j MASQUERADE \n",
            f"iptables --append FORWARD --in-interface {self.wireless_interface} -j ACCEPT \n",
            "echo 1 > /proc/sys/net/ipv4/ip_forward \n"
        ]
        network_setup_script = open("src/fap/enable_network.sh", "w+")
        network_setup_script.writelines(configurations)
        network_setup_script.close()

    def run(self):
        self.init_hostapd()
        self.init_dnsmasq()
        self.interface_setup()
        if self.network_interface != "emptynullnone":
            self.network_setup()

        self.hostapd_process = subprocess.Popen(
            "hostapd src/fap/hostapd.conf",
            shell=True, preexec_fn=os.setsid
            )
        self.dnsmasq_process = subprocess.Popen(
            "dnsmasq -C src/fap/dnsmasq.conf -d",
            shell=True, preexec_fn=os.setsid, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
        subprocess.run("src/fap/interface_setup.sh", shell=True)
        if self.network_interface != "emptynullnone":
            subprocess.run("src/fap/enable_network.sh", shell=True)
        
    def stop(self):
        #self.hostapd_process.send_signal(signal.SIGINT)
        #self.dnsmasq_process.send_signal(signal.SIGINT)
        os.killpg(os.getpgid(self.hostapd_process.pid), signal.SIGINT)
        os.killpg(os.getpgid(self.dnsmasq_process.pid), signal.SIGINT)

#def get_arguments():
    #parser = argparse.ArgumentParser()
    #parser.add_argument("-w", "--wireless", dest="wireless_interface", help="The wireless interface to be used")
    #parser.add_argument("-s", "--ssid", dest="ssid", help="The SSID of the fake access point")
    #parser.add_argument("-n", "--network", dest="network_interface", help="The interface that provide network connectivity")
    #options = parser.parse_args()

    #return options


#options = get_arguments()

#wireless_interface = options.wireless_interface
#ssid = options.ssid
#network_interface = options.network_interface
#fap = FakeAccessPoint(wireless_interface, ssid, network_interface)
#fap.run()
