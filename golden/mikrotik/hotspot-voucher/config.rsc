/interface ethernet
set [ find default-name=ether1 ] name=wan
set [ find default-name=ether2 ] name=lan1

/ip hotspot
add name=hotspot1 interface=lan1 profile=hsprof1 address-pool=hs_pool1

/ip hotspot profile
add name=hsprof1 dns-name=hotel.local hotspot-address=192.168.88.1

/ip pool
add name=hs_pool1 ranges=192.168.88.10-192.168.88.250

/ip dhcp-server
add address-pool=hs_pool1 interface=lan1 name=dhcp1

/ip firewall nat
add action=masquerade chain=srcnat out-interface=wan

/system identity
set name=hotel-gateway
