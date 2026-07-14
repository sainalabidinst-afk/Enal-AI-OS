/interface ethernet
set [ find default-name=ether1 ] name=wan
set [ find default-name=ether2 ] name=lan1

/ip address
add address=192.168.1.1/24 interface=lan1 network=192.168.1.0

/queue simple
add name=client1 target=192.168.1.100 max-limit=10M/5M
add name=client2 target=192.168.1.101 max-limit=5M/2M

/system identity
set name=simple-queue-router
