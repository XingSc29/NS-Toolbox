iptables --table nat --append POSTROUTING --out-interface eth0 -j MASQUERADE 
iptables --append FORWARD --in-interface wlan0 -j ACCEPT 
echo 1 > /proc/sys/net/ipv4/ip_forward 
