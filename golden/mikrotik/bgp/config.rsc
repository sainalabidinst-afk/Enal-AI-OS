/interface ethernet
set [ find default-name=ether1 ] name=wan1

/ip address
add address=203.0.113.2/24 interface=wan1 network=203.0.113.0

/routing bgp
set enabled=yes as=65530 router-id=10.0.0.1

/routing bgp peer
add name=isp-peer remote-address=203.0.113.1 remote-as=65530

/ip route
add dst-address=0.0.0.0/0 gateway=203.0.113.1

/system identity
set name=bgp-router
