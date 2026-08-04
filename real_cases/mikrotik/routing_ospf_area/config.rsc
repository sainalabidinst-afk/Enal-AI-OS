# MikroTik RouterOS OSPF
/routing ospf instance
    set default name=default router-id=1.1.1.1 distribute-default=never
/routing ospf area
    add name=backbone area-id=0.0.0.0
/routing ospf interface
    add interface=ether1 network-type=broadcast area=backbone
    add interface=ether2 network-type=broadcast area=backbone
/ip address
    add address=10.0.1.1/24 interface=ether1 network=10.0.1.0
    add address=10.0.2.1/24 interface=ether2 network=10.0.2.0
/routing ospf network
    add network=10.0.0.0/8 area=backbone
