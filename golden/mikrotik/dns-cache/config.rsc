/interface ethernet
set [ find default-name=ether1 ] name=wan
set [ find default-name=ether2 ] name=lan1

/ip address
add address=192.168.1.1/24 interface=lan1 network=192.168.1.0

/ip dns
set servers=8.8.8.8,1.1.1.1 cache-size=2048

/system identity
set name=dns-cache-router
