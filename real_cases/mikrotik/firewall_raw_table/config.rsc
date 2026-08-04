# MikroTik RouterOS Raw Firewall Table
/ip firewall raw
    add chain=prerouting action=accept protocol=tcp dst-port=22         src-address=192.168.1.0/24
    add chain=prerouting action=drop protocol=tcp dst-port=23         src-address=0.0.0.0/0
    add chain=postrouting action=accept protocol=icmp
/ip firewall filter
    add chain=input action=accept connection-state=established,related
    add chain=input action=accept protocol=icmp
    add chain=input action=drop
/interface ethernet
    set ether1 name=WAN
