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

/ip pool
add name=isp_pool1 ranges=10.0.0.100-10.0.0.250

/ip dhcp-server
add address-pool=isp_pool1 interface=bridge1 name=dhcp1

/ip dns
set servers=8.8.8.8,1.1.1.1

/ip firewall nat
add action=masquerade chain=srcnat out-interface=wan1
add action=masquerade chain=srcnat out-interface=wan2

/ip firewall filter
add action=accept chain=input connection-state=established,related,untracked
add action=drop chain=input connection-state=invalid
add action=accept chain=input protocol=icmp
add action=accept chain=input connection-state=new in-interface=bridge1
add action=drop chain=input

/ip route
add dst-address=0.0.0.0/0 gateway=203.0.113.1 distance=1
add dst-address=0.0.0.0/0 gateway=203.0.113.2 distance=2

/system identity
set name=isp-medium-gw

/system ntp client
set enabled=yes

/system clock
set time-zone-name=Asia/Jakarta
