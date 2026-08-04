# MikroTik RouterOS PPTP VPN
/interface pptp-server
    set enabled=yes
/ppp profile
    add name=VPN-PROFILE local-address=10.0.0.1 remote-address=VPN-POOL         dns-server=8.8.8.8,1.1.1.1
/ip pool
    add name=VPN-POOL ranges=10.0.100.10-10.0.100.250
/ppp secret
    add name=vpnuser password=VPNpass123! profile=VPN-PROFILE         service=pptp
/ip firewall filter
    add chain=input action=accept protocol=tcp dst-port=1723 src-address=0.0.0.0/0
    add chain=input action=accept protocol=gre src-address=0.0.0.0/0
