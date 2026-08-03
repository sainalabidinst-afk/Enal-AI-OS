/interface ethernet
set [ find default-name=ether1 ] name=wan
set [ find default-name=ether2 ] name=lan1

/ip address
add address=192.168.1.1/24 interface=lan1 network=192.168.1.0

/ip dhcp-client
add disabled=no interface=wan

/ip dhcp-server
add address-pool=dhcp_pool1 interface=lan1 name=dhcp1

/ip pool
add name=dhcp_pool1 ranges=192.168.1.100-192.168.1.200

/ip firewall nat
add action=masquerade chain=srcnat out-interface=wan

/ip firewall filter
add action=accept chain=input comment="defconf: accept established,related,untracked" connection-state=established,related,untracked
add action=drop chain=input comment="defconf: drop all" connection-state=invalid
add action=accept chain=input protocol=icmp
add action=accept chain=input connection-state=new in-interface=lan1
add action=drop chain=input

/system identity
set name=home-router

/system clock
set time-zone-name=Asia/Jakarta
