/interface bridge
add name=bridge-core vlan-filtering=yes protocol-mode=stp

/interface bridge port
add bridge=bridge-core interface=ether1 pvid=10
add bridge=bridge-core interface=ether2 pvid=20
add bridge=bridge-core interface=ether3 pvid=30

/interface bridge vlan
add bridge=bridge-core vlan-id=10 tagged=ether1,ether2 untagged=ether3