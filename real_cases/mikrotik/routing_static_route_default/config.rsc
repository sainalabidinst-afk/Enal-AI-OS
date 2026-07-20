/ip address
add address=192.168.10.1/24 interface=ether1 network=192.168.10.0
add address=10.0.0.1/30 interface=ether2 network=10.0.0.0

/ip route
add dst-address=0.0.0.0/0 gateway=10.0.0.2 distance=1
add dst-address=172.16.0.0/12 gateway=10.0.0.2
add dst-address=10.10.0.0/16 gateway=192.168.10.254 distance=2

/ip route cache
set memory-lines=1024

/routing bgp instance
set default as=65001 router-id=10.0.0.1 redistribute-connected=yes