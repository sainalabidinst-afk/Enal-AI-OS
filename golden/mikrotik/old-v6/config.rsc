/interface ethernet
set [ find default-name=ether1 ] name=ether1
set [ find default-name=ether2 ] name=ether2

/ip address
add address=192.168.1.1/24 interface=ether1 network=192.168.1.0

/ip firewall nat
add action=masquerade chain=srcnat

/system identity
set name=old-v6-router
