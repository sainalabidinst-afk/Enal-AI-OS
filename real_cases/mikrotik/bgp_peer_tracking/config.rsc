# MikroTik RouterOS BGP with peer tracking
/routing bgp instance
    set default name=default as=65001 router-id=10.0.0.1
/routing bgp peer
    add name=peer-to-isp remote-address=203.0.113.2 remote-as=65002 multihop=no         ttl=255
    add name=peer-to-transit remote-address=10.0.1.2 remote-as=65003 multihop=no         ttl=255
/ip firewall filter
    add chain=forward action=accept protocol=tcp dst-port=179 src-address=10.0.0.0/24
    add chain=input action=accept protocol=tcp dst-port=179 src-address=10.0.0.0/24
