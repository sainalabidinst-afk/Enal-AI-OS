/interface ethernet
set [ find default-name=ether1 ] name=wan1
set [ find default-name=ether2 ] name=wan2
set [ find default-name=ether3 ] name=lan-core

/interface bridge
add name=bridge1

/interface bridge port
add bridge=bridge1 interface=lan-core

/ip address
add address=10.0.0.1/24 interface=bridge1 network=10.0.0.0
add address=10.1.0.1/24 interface=lan-core network=10.1.0.0

/ip pool
add name=mpls_pool1 ranges=10.0.0.100-10.0.0.250

/ip dhcp-server
add address-pool=mpls_pool1 interface=bridge1 name=dhcp1

/mpls
set enabled=yes

/mpls ldp
set enabled=yes

/mpls ldp interface
add interface=bridge1

/ip route
add dst-address=0.0.0.0/0 gateway=203.0.113.1

/system identity
set name=mpls-router
