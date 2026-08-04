# MikroTik RouterOS MPLS with LDP
/mpls ldp
    set enabled=yes lsr-id=1.1.1.1 transport-address=1.1.1.1
/mpls ldp interface
    add interface=ether1
    add interface=ether2
/interface ethernet
    set ether1 name=MPLS-CORE-1
    set ether2 name=MPLS-CORE-2
/ip address
    add address=10.0.1.1/30 interface=MPLS-CORE-1 network=10.0.1.0
    add address=10.0.2.1/30 interface=MPLS-CORE-2 network=10.0.2.0
/routing ospf area
    add area-id=0.0.0.0
