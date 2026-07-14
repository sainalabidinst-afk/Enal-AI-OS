/interface ethernet
set [ find default-name=ether1 ] name=wan
set [ find default-name=ether2 ] name=lan1

/interface eoip
add name=eoip1 tunnel-id=1 remote-address=203.0.113.1 local-address=203.0.113.2

/ip address
add address=10.255.255.2/30 interface=eoip1 network=10.255.255.0
add address=192.168.1.1/24 interface=lan1 network=192.168.1.0

/system identity
set name=eoip-router
