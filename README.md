# NS-Toolbox

A GUI-based network hacking tool developed by a student. 

Many modules such as network scanner, ARP spoofer and MAC spoofer do not meet the standard. For example, I did not implement Nmap for the network scanner. Instead of using Nmap, I used the Python scapy library to create these modules. This is because the entire project is for my own educational purpose only.

## Installation

Run these with root privilege:  
```
./installation  
pip3 install -r requirement.txt
```

## Modules

| Layer 2                  | TCP/IP       | DNS          | HTTP              | WiFi                          |
| :----------------------: | :----------: | :----------: | :---------------: | :---------------------------: |
| Network Scanner          | Port Scanner | DNS Spoofer  | Password Sniffer  | Network Scanner (airodump-ng) |
| ARP Spoofer              | SSL stripper |              | Download Replacer | Handshake Snooper             |
| MAC Spoofer              |              |              | Code Injector     | Deauther                      |
| DHCP Starvation          |              |              | Web Crawler       | WPA/WPA2 Cracking             |
|                          |              |              |                   | Evil Twin Attack (Fake access point & Captive portal) 

## PyQt Error Messages

You might find some error messages in your terminal while performing actions on the GUI.   
Those are some known bugs of Qt, you do not need to worry about them if the program works fine.

## xterm Properties

Press [Ctrl] + [left/right mouse button] to change the properties of the terminals.

## Video demo

[URL](https://www.youtube.com/watch?v=CV4zWTlTe7w)
