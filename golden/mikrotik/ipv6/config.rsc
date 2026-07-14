/interface ethernet
set [ find default-name=ether1 ] name=wan
set [ find default-name=ether2 ] name=lan1

/ipv6 address
add address=fd00::1/64 interface=lan1

/ipv6 pool
add name=ipv6_pool ranges=fd00::100-fd00::200

/ipv6 dhcp-server
add name=dhcp6 interface=lan1 address-pool=ipv6_pool

/system identity
set name=ipv6-router
