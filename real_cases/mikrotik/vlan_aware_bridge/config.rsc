# MikroTik RouterOS VLAN-aware bridge
/interface bridge
    add name=bridge-local vlan-filtering=yes
/interface bridge vlan
    add bridge=bridge-local vlan=10 tagged=ether1,ether2 untagged=ether3
    add bridge=bridge-local vlan=20 tagged=ether1,ether2 untagged=ether4
/interface ethernet
    set ether1 name=TRUNK1
    set ether2 name=TRUNK2
    set ether3 name=ACCESS1
    set ether4 name=ACCESS2
/ip address
    add address=192.168.10.1/24 interface=bridge-local network=192.168.10.0
