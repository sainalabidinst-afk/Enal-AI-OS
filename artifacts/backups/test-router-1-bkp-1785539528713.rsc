/interface ethernet
set [ find default-name=ether1 ] name=wan
set [ find default-name=ether2 ] name=lan1
set [ find default-name=ether3 ] name=lan2
set [ find default-name=ether4 ] name=lan3

/interface bridge
add name=bridge1

/interface bridge port
add bridge=bridge1 interface=lan1
add bridge=bridge1 interface=lan2
add bridge=bridge1 interface=lan3

/ip address
add address=10.10.1.1/24 interface=bridge1 network=10.10.1.0

/ip dhcp-server
add address-pool=campus_pool interface=bridge1 name=dhcp1

/ip pool
add name=campus_pool ranges=10.10.1.100-10.10.1.250

/ip dns
set servers=8.8.8.8,1.1.1.1

/ip firewall nat
add action=masquerade chain=srcnat out-interface=wan

/ip firewall filter
add action=accept chain=input connection-state=established,related,untracked
add action=drop chain=input connection-state=invalid
add action=accept chain=input protocol=icmp
add action=accept chain=input connection-state=new in-interface=bridge1
add action=drop chain=input

/ip route
add dst-address=0.0.0.0/0 gateway=10.0.0.1

/system identity
set name=campus-gateway

/system ntp client
set enabled=yes

/system clock
set time-zone-name=Asia/Jakarta
