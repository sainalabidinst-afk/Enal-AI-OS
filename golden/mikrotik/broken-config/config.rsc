/interface ethernet
set [ find default-name=ether1 ] name=wan
set [ find default-name=ether2 ] name=lan1

/ip address
add address=192.168.1.1/24 interface=lan1 network=192.168.1.0

/ip firewall filter
add action=accept chain=input
add action=drop chain=input

/system identity
set name=broken-router
