/interface ethernet
set [ find default-name=ether1 ] name=wan1
set [ find default-name=ether2 ] name=wan2
set [ find default-name=ether3 ] name=lan1

/ip address
add address=192.168.1.1/24 interface=lan1 network=192.168.1.0
add address=203.0.113.2/24 interface=wan1 network=203.0.113.0

/ip firewall nat
add action=masquerade chain=srcnat out-interface=wan1

/ip route
add dst-address=0.0.0.0/0 gateway=203.0.113.1 distance=1
add dst-address=0.0.0.0/0 gateway=198.51.100.1 distance=2

/tool netwatch
add host=8.8.8.8 interval=10s

/system identity
set name=failover-router
