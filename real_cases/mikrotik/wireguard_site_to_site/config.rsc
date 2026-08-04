# MikroTik RouterOS WireGuard VPN
/interface wireguard
    add name=wg0 listen-port=13231 private-key="<private-key>"
/ip address
    add address=10.10.0.1/24 interface=wg0 network=10.10.0.0
/interface wireguard peer
    add interface=wg0 public-key="<public-key>" endpoint-address=203.0.113.2         endpoint-port=13231 allowed-address=10.20.0.0/24 persistent-keepalive=25s
/ip firewall filter
    add chain=input action=accept protocol=udp port=13231 src-address=203.0.113.0/24
    add chain=forward action=accept src-address=10.10.0.0/24 dst-address=10.20.0.0/24
