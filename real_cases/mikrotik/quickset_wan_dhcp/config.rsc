# MikroTik RouterOS QuickSet WAN DHCP
/interface ethernet
    set ether1 name=WAN
    set ether2 name=LAN
/ip address
    add address=dhcp interface=WAN
    add address=192.168.88.1/24 interface=LAN network=192.168.88.0
/ip pool
    add name=LAN-POOL ranges=192.168.88.10-192.168.88.254
/ip dhcp-server
    add name=LAN-DHCP interface=LAN address-pool=LAN-POOL lease-time=1d
/ip firewall nat
    add chain=srcnat action=masquerade out-interface=WAN
/ip firewall filter
    add chain=input action=accept protocol=icmp
    add chain=input action=accept connection-state=established,related
    add chain=input action=drop
