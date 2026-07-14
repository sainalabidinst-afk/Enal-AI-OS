/interface ethernet
set [ find default-name=ether1 ] name=wan
set [ find default-name=ether2 ] name=lan1
set [ find default-name=ether3 ] name=lan2
set [ find default-name=ether4 ] name=dmz

/interface bridge
add name=bridge1

/interface bridge port
add bridge=bridge1 interface=lan1
add bridge=bridge1 interface=lan2

/ip address
add address=10.0.1.1/24 interface=lan1 network=10.0.1.0
add address=10.0.2.1/24 interface=lan2 network=10.0.2.0
add address=10.0.99.1/24 interface=dmz network=10.0.99.0

/ip dhcp-server
add address-pool=dhcp_lan1 interface=lan1 name=dhcp1
add address-pool=dhcp_lan2 interface=lan2 name=dhcp2

/ip pool
add name=dhcp_lan1 ranges=10.0.1.100-10.0.1.200
add name=dhcp_lan2 ranges=10.0.2.100-10.0.2.200

/ip firewall nat
add action=masquerade chain=srcnat out-interface=wan

/ip firewall filter
add action=accept chain=input connection-state=established,related,untracked
add action=drop chain=input connection-state=invalid
add action=accept chain=input protocol=icmp
add action=accept chain=input connection-state=new in-interface=lan1
add action=accept chain=input connection-state=new in-interface=lan2
add action=drop chain=input
add action=accept chain=forward connection-state=established,related,untracked
add action=drop chain=forward connection-state=invalid
add action=accept chain=forward protocol=icmp
add action=drop chain=forward

/system identity
set name=office-router
