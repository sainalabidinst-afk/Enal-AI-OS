/interface ethernet
set [ find default-name=ether1 ] name=wan
set [ find default-name=ether2 ] name=lan1

/interface pppoe-client
add name=pppoe1 interface=wan user=isp-username password=isp-password

/ip address
add address=192.168.1.1/24 interface=lan1 network=192.168.1.0

/ip pool
add name=pppoe_pool ranges=192.168.1.100-192.168.1.200

/ip dhcp-server
add address-pool=pppoe_pool interface=lan1 name=dhcp1

/ip firewall nat
add action=masquerade chain=srcnat out-interface=pppoe1

/system identity
set name=pppoe-router
