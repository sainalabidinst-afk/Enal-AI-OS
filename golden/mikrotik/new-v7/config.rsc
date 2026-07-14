/interface ethernet
set [ find default-name=ether1 ] name=wan
set [ find default-name=ether2 ] name=lan

/ip address
add address=192.168.88.1/24 interface=lan network=192.168.88.0

/ip pool
add name=dhcp_pool ranges=192.168.88.10-192.168.88.250

/ip dhcp-server
add address-pool=dhcp_pool interface=lan name=dhcp1

/ip dhcp-server network
add address=192.168.88.0/24 gateway=192.168.88.1

/ip firewall nat
add action=masquerade chain=srcnat out-interface=wan

/system identity
set name=new-v7-router
