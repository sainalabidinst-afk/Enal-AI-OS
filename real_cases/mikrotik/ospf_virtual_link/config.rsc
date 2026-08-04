# MikroTik RouterOS OSPF Virtual Link
/routing ospf instance
    set default name=default router-id=1.1.1.1 distribute-default=never
/routing ospf area
    add name=backbone area-id=0.0.0.0
    add name=remote-area area-id=0.0.0.1
/routing ospf virtual-link
    add instance=default neighbor-id=2.2.2.2 interface=ether1
/ip address
    add address=10.0.1.1/24 interface=ether1 network=10.0.1.0
/interface ethernet
    set ether1 name=CORE-LINK
