/interface ethernet
set [ find default-name=ether1 ] name=wan1
set [ find default-name=ether2 ] name=wan2
set [ find default-name=ether3 ] name=lan1
set [ find default-name=ether4 ] name=lan2
set [ find default-name=ether5 ] name=lan3

/interface bridge
add name=bridge1

/interface bridge port
add bridge=bridge1 interface=lan1
add bridge=bridge1 interface=lan2
add bridge=bridge1 interface=lan3

/ip address
add address=10.10.1.1/24 interface=bridge1 network=10.10.1.0
add address=10.10.2.1/24 interface=lan2 network=10.10.2.0
add address=10.10.3.1/24 interface=lan3 network=10.10.3.0

/ip pool
add name=isp_pool1 ranges=10.10.1.100-10.10.1.250
add name=isp_pool2 ranges=10.10.2.100-10.10.2.200

/ip dhcp-server
add address-pool=isp_pool1 interface=bridge1 name=dhcp1
add address-pool=isp_pool2 interface=lan2 name=dhcp2

/ip dhcp-server network
add address=10.10.1.0/24 gateway=10.10.1.1 dns-nameserver=8.8.8.8
add address=10.10.2.0/24 gateway=10.10.2.1 dns-nameserver=8.8.8.8

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
add action=accept chain=input connection-state=new in-interface=lan2
add action=drop chain=input
add action=accept chain=forward connection-state=established,related,untracked
add action=drop chain=forward connection-state=invalid

/ip route
add dst-address=0.0.0.0/0 gateway=203.0.113.1 distance=1
add dst-address=0.0.0.0/0 gateway=203.0.113.2 distance=2

/system identity
set name=isp-large-gw

/system ntp client
set enabled=yes
