/interface ethernet
set [ find default-name=ether1 ] name=wan
set [ find default-name=ether2 ] name=lan1

/ip address
add address=192.168.1.1/24 interface=lan1 network=192.168.1.0

/queue tree
add name=download parent=global priority=1
add name=upload parent=global priority=8

/system identity
set name=queue-tree-router
