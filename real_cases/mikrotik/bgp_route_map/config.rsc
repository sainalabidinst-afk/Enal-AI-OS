# MikroTik RouterOS BGP with route maps
/routing bgp instance
    set default name=default as=65001 router-id=10.0.0.1
/routing bgp peer
    add name=peer-to-isp remote-address=203.0.113.2 remote-as=65002         multihop=no ttl=255
/routing bgp network
    add network=10.1.0.0/16 synchronize=yes
/routing filter
    add chain=bgp-out action=accept prefix=10.1.0.0/16         prefix-length=16-24
/ip firewall filter
    add chain=forward action=accept protocol=tcp dst-port=179
