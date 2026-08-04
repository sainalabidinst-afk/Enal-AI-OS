# MikroTik RouterOS VRRP High Availability
/interface ethernet
    set ether1 name=WAN
    set ether2 name=LAN
/ip address
    add address=192.168.1.2/24 interface=LAN network=192.168.1.0
/ipv6 address
    add address=2001:db8::2/64 interface=LAN network=2001:db8::0
/vrrp
    add name=VRRP-LAN interface=LAN id=1 priority=100         address=192.168.1.1 authentication=12345678
    add name=VRRP-IPV6 interface=LAN id=2 priority=100         address=2001:db8::1 authentication=12345678
/ip firewall filter
    add chain=input action=accept protocol=vrrp interface=LAN
