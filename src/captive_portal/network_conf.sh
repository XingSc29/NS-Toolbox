ifconfig wlan0 192.168.1.1 netmask 255.255.255.0 
echo 1 > /proc/sys/net/ipv4/ip_forward 
iptables --flush 
iptables --table nat --flush 
iptables --delete-chain 
iptables --table nat --delete-chain 
iptables -P FORWARD ACCEPT 
