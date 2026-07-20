/ip firewall filter
add chain=input action=drop protocol=tcp dst-port=22,23,80,443,8291 src-address=0.0.0.0/0 comment="Block management ports from WAN"
add chain=input action=accept protocol=tcp dst-port=22 src-address=192.168.1.0/24
add chain=input action=accept protocol=tcp dst-port=443 src-address=192.168.1.0/24
add chain=input action=drop protocol=tcp dst-port=22,23,80,443,8291
add chain=forward action=drop
add chain=input action=accept connection-state=established,related
add chain=input action=accept protocol=icmp
add chain=output action=accept