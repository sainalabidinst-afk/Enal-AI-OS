# MikroTik RouterOS IPv6 6to4 Tunnel
/interface 6to4
    add name=6to4-TUN keepalive=10s mtu=1472
/ipv6 route
    add dst-address=2000::/3 gateway=6to4-TUN
/ipv6 address
    add address=2002:c000:0201::1/48 interface=6to4-TUN advertise=yes
/interface ethernet
    set ether1 name=WAN
