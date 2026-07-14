/interface ethernet
set [ find default-name=ether1 ] name=wan
set [ find default-name=ether2 ] name=lan1
set [ find default-name=ether3 ] name=lan2

/interface bridge
add name=bridge1

/interface bridge port
add bridge=bridge1 interface=lan1
add bridge=bridge1 interface=lan2

/ip address
add address=192.168.1.1/24 interface=bridge1 network=192.168.1.0

/ip dhcp-server
add address-pool=pool1 interface=bridge1 name=dhcp1

/ip pool
add name=pool1 ranges=192.168.1.100-192.168.1.200

/ip firewall nat
add action=masquerade chain=srcnat out-interface=wan

/ip firewall filter
add action=accept chain=input connection-state=established,related,untracked
add action=drop chain=input connection-state=invalid
add action=accept chain=input protocol=icmp
add action=accept chain=input connection-state=new in-interface=bridge1
add action=drop chain=input

/system identity
set name=rt-rw-net
