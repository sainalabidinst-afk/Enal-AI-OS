# MikroTik RouterOS L2TP VPN Server
/interface l2tp-server
    set enabled=yes
/ppp profile
    add name=L2TP-PROFILE local-address=10.0.0.1 remote-address=VPN-POOL         dns-server=8.8.8.8,1.1.1.1
/ip pool
    add name=VPN-POOL ranges=10.0.100.10-10.0.100.250
/ppp secret
    add name=vpnuser password=VPNpass123! profile=L2TP-PROFILE         service=l2tp
/ip firewall filter
    add chain=input action=accept protocol=udp dst-port=1701 src-address=0.0.0.0/0
    add chain=input action=accept protocol=ipsec-esp src-address=0.0.0.0/0
