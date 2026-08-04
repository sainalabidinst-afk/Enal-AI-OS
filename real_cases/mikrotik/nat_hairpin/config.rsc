# MikroTik RouterOS NAT Hairpin
/ip firewall nat
    add chain=srcnat action=masquerade src-address=192.168.1.0/24         out-interface=ether1
    add chain=dstnat action=dnat to-addresses=192.168.1.10 to-ports=80         dst-address=192.168.1.10 protocol=tcp dst-port=80 in-interface=ether2
/ip address
    add address=192.168.1.1/24 interface=ether2 network=192.168.1.0
/interface ethernet
    set ether1 name=WAN
    set ether2 name=LAN
