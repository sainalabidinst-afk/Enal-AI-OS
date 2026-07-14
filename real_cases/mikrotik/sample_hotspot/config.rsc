/interface bridge
add name=bridge1
/interface bridge port
add bridge=bridge1 interface=ether2
add bridge=bridge1 interface=ether3
/ip address
add address=192.168.1.1/24 interface=bridge1 network=192.168.1.0
/ip dhcp-client
add interface=ether1 disabled=no
/ip firewall filter
add action=accept chain=input protocol=icmp
add action=accept chain=input connection-state=established,related
add action=drop chain=input
