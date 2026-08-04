# MikroTik RouterOS L3 Switch with VLANs
/interface bridge
    add name=bridge-local protocol-mode=rstp vlan-filtering=yes
/interface ethernet
    set ether1 name=trunk1 master-port=bridge-local
    set ether2 name=trunk2 master-port=bridge-local
    set ether3 name=access1 master-port=bridge-local
/interface bridge vlan
    add bridge=bridge-local vlan=10 tagged=trunk1,trunk2 untagged=access1
    add bridge=bridge-local vlan=20 tagged=trunk1,trunk2
/ip address
    add address=192.168.10.1/24 interface=bridge-local network=192.168.10.0         vlan=10
    add address=192.168.20.1/24 interface=bridge-local network=192.168.20.0         vlan=20
