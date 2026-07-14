/interface ethernet
set [ find default-name=ether1 ] name=wan
set [ find default-name=ether2 ] name=lan1
set [ find default-name=ether3 ] name=lan2

/interface bridge
add name=bridge1 vlan-filtering=yes

/interface bridge port
add bridge=bridge1 interface=lan1
add bridge=bridge1 interface=lan2

/interface bridge vlan
add bridge=bridge1 tagged=bridge1 vlan-ids=10
add bridge=bridge1 tagged=bridge1 vlan-ids=20

/ip address
add address=192.168.10.1/24 interface=bridge1 network=192.168.10.0
add address=192.168.20.1/24 interface=bridge1 network=192.168.20.0

/ip pool
add name=vlan10_pool ranges=192.168.10.100-192.168.10.200
add name=vlan20_pool ranges=192.168.20.100-192.168.20.200

/ip dhcp-server
add address-pool=vlan10_pool interface=bridge1 name=dhcp10
add address-pool=vlan20_pool interface=bridge1 name=dhcp20

/ip firewall nat
add action=masquerade chain=srcnat out-interface=wan

/system identity
set name=vlan-router
