/interface ethernet
set [ find default-name=ether1 ] name=wan
set [ find default-name=ether2 ] name=lan1

/interface vrrp
add name=vrrp1 interface=lan1 virtual-address=192.168.1.1 priority=100

/ip address
add address=192.168.1.2/24 interface=lan1 network=192.168.1.0

/system identity
set name=vrrp-router
