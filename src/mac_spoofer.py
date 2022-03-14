import re
import subprocess


class MACSpoofer:
    def __init__(self, interface, process):
        self.interface = interface
        self.process = process

    def get_current_mac(self):
        # ifconfig_result = subprocess.check_output(f"ifconfig {self.interface}", shell=True).decode()
        get_mac_result = subprocess.check_output(f"macchanger -s {self.interface}", shell=True).decode()
        mac_address_pattern = re.compile(r"Current MAC:\s\s\s(..:){5}..")
        search = mac_address_pattern.search(get_mac_result)
        # mac_address_pattern = re.compile(r"(\w\w:){5}\w\w")
        # search = mac_address_pattern.search(ifconfig_result)
        if search:
            self.process.emit("[+] " + search.group(0))
        else:
            self.process.emit("[-] Could not find MAC address. Please check your interface!")

    def change_mac(self, new_mac):
        self.process.emit(f"[+] Changing MAC address >> {new_mac} for {self.interface}")
        subprocess.run(f"ifconfig {self.interface} down", shell=True)
        mac_changer_process = subprocess.run(f"macchanger -m {new_mac} {self.interface}",
                                             shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        # subprocess.run(f"ifconfig {self.interface} hw ether {new_mac}", shell=True)
        subprocess.run(f"ifconfig {self.interface} up", shell=True)
        self.process.emit(mac_changer_process.stderr.decode())

