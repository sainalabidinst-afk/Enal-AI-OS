/interface ethernet
set [ find default-name=ether1 ] name=wan1
set [ find default-name=ether2 ] name=lan1

/ip address
add address=10.0.0.1/24 interface=lan1 network=10.0.0.0
add address=10.0.1.1/24 interface=wan1 network=10.0.1.0

/routing ospf
set enabled=yes router-id=10.0.0.1

/routing ospf interface
add interface=lan1 network-type=broadcast
add interface=wan1 network-type=point-to-point

/routing ospf area
add area-id=0.0.0.0 name=backbone

/ip route
add dst-address=0.0.0.0/0 gateway=203.0.113.1

/system identity
set name=ospf-router
