# MikroTik RouterOS IPv6 with DHCPv6
/ipv6
    set accept-redirects=yes accept-router-advertisements=yes
/ipv6 address
    add address=2001:db8::1/64 interface=ether1 advertise=yes
/ipv6 dhcp-server
    add name=DHCPv6-SERVER interface=ether1 address-pool=POOL-V6         lease-time=1d prefix-length=64
/ipv6 pool
    add name=POOL-V6 ranges=2001:db8:1::100-2001:db8:1::200
/ipv6 nd
    set interface=ether1 advertise-dns=yes
