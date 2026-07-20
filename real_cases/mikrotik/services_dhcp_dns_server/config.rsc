/ip address
add address=192.168.100.1/24 interface=ether1 network=192.168.100.0

/ip dhcp-server
add name=dhcp1 interface=ether1 address-pool=pool1 lease-time=1h disabled=no

/ip pool
add name=pool1 ranges=192.168.100.10-192.168.100.250

/ip dhcp-server network
add address=192.168.100.0/24 gateway=192.168.100.1 dns-server=8.8.8.8,8.8.4.4

/ip dns
set servers=8.8.8.8,8.8.4.4 allow-remote-requests=no