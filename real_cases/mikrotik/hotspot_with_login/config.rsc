# MikroTik RouterOS Hotspot with login page
/interface ethernet
    set ether1 name=WAN
    set ether2 name=LAN
/ip pool
    add name=HOTSPOT-POOL ranges=10.0.0.10-10.0.0.250
/ip dhcp-server
    add name=HOTSPOT-DHCP interface=LAN address-pool=HOTSPOT-POOL         lease-time=1h
/ip hotspot
    add name=hotspot1 interface=LAN profile=default
/ip hotspot profile
    add name=default hotspot-address=10.0.0.1 dns-name=hotspot.local         rate-limit=1M/1M
/ip dns
    set allow-remote-requests=yes servers=8.8.8.8,1.1.1.1
