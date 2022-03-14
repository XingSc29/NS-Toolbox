ifconfig wlan0 up 192.168.1.1 netmask 255.255.255.0 
route add -net 192.168.1.0 netmask 255.255.255.0 gw 192.168.1.1 
