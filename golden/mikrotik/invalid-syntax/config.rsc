/interface ethernet
set [ find default-name=ether1 ] name=wan
invalid line here
/ip address
add address=192.168.1.1/24 interface=lan1 network=192.168.1.0
