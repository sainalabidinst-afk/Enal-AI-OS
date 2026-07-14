/interface ethernet
set [ find default-name=ether1 ] name=wan
set [ find default-name=ether2 ] name=lan-core
set [ find default-name=ether3 ] name=dmz

/interface bridge
add name=bridge1

/interface bridge port
add bridge=bridge1 interface=lan-core

/ip address
add address=10.10.1.1/24 interface=bridge1 network=10.10.1.0
add address=10.10.99.1/24 interface=dmz network=10.10.99.0

/ip firewall filter
add action=accept chain=input connection-state=established,related,untracked
add action=drop chain=input connection-state=invalid
add action=accept chain=input protocol=icmp
add action=accept chain=input connection-state=new in-interface=bridge1 src-address=10.10.1.0/24
add action=drop chain=input

add action=accept chain=forward connection-state=established,related,untracked
add action=drop chain=forward connection-state=invalid
add action=accept chain=forward protocol=icmp
add action=accept chain=forward src-address=10.10.1.0/24 dst-address=10.10.99.0/24
add action=drop chain=forward

/ip firewall nat
add action=masquerade chain=srcnat out-interface=wan

/system identity
set name=enterprise-fw
