import subprocess
import argparse
import os
import signal
import time
import shutil


# Disable IP forwarding and flush IPTables rule
class CaptivePortal:
    def __init__(self, wireless_interface, ssid, login_page):
        self.wireless_interface = wireless_interface
        self.ssid = ssid
        self.login_page = login_page

    def init_hostapd(self):
        configurations = [
            f"interface={self.wireless_interface}\n",
            "driver=nl80211\n", 
            f"ssid={self.ssid}\n", 
            "channel=5\n", 
            ]
        hostapd_conf = open("src/captive_portal/hostapd.conf", "w+")
        hostapd_conf.writelines(configurations)
        hostapd_conf.close()

    def init_dnsmasq(self):
        if self.login_page == "TM Unifi Login":
            shutil.copyfile("src/captive_portal/tmlogin.html", "/var/www/html/index.html")
            try:
                shutil.copytree("src/captive_portal/digitalme - self sovereign identity for everyone_files", "/var/www/html/digitalme - self sovereign identity for everyone_files")
            except FileExistsError as e:
                pass

        configurations = [
            f"interface={self.wireless_interface} \n",
            "dhcp-range=192.168.1.10,192.168.1.100,12h \n",
            "dhcp-option=3, 192.168.1.1 \n",
            "dhcp-option=6, 192.168.1.1 \n",
            f"address=/#/192.168.1.1 \n" 
        ]
        dnsmasq_conf = open("src/captive_portal/dnsmasq.conf", "w+")
        dnsmasq_conf.writelines(configurations)
        dnsmasq_conf.close()

    def conf_network(self):
        configurations = [
            f"ifconfig {self.wireless_interface} 192.168.1.1 netmask 255.255.255.0 \n",
            "echo 1 > /proc/sys/net/ipv4/ip_forward \n",
            "iptables --flush \n",
            "iptables --table nat --flush \n",
            "iptables --delete-chain \n",
            "iptables --table nat --delete-chain \n",
            "iptables -P FORWARD ACCEPT \n"
        ]
        interface_setup_script = open("src/captive_portal/network_conf.sh", "w+")
        interface_setup_script.writelines(configurations)
        interface_setup_script.close()

    def run(self):
        self.init_hostapd()
        self.init_dnsmasq()
        self.conf_network()

        subprocess.run("service NetworkManager stop", shell=True)
        self.hostapd_process = subprocess.Popen(
            "hostapd src/captive_portal/hostapd.conf",
            shell=True, preexec_fn=os.setsid
            )
        self.dnsmasq_process = subprocess.Popen(
            "dnsmasq -C src/captive_portal/dnsmasq.conf -d",
            shell=True, preexec_fn=os.setsid, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL 
        )
        subprocess.run("src/captive_portal/network_conf.sh", shell=True)
        
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
