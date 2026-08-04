# MikroTik RouterOS IPv6 DHCPv6 Server
/ipv6
    set accept-redirects=yes accept-router-advertisements=yes
/ipv6 pool
    add name=DHCPv6-POOL prefix=2001:db8:1::/64
/ipv6 dhcp-server
    add name=DHCPv6-SERVER interface=ether1 address-pool=DHCPv6-POOL         lease-time=1d
/ipv6 nd
    set interface=ether1 advertise-dns=yes
/interface ethernet
    set ether1 name=LAN
