# MikroTik RouterOS SSTP VPN Server
/interface sstp-server
    set enabled=yes
/ppp profile
    add name=SSTP-PROFILE local-address=10.0.0.1 remote-address=VPN-POOL         dns-server=8.8.8.8,1.1.1.1
/ip pool
    add name=VPN-POOL ranges=10.0.100.10-10.0.100.250
/ppp secret
    add name=vpnuser password=VPNpass123! profile=SSTP-PROFILE         service=sstp
/certificate
    add name=CA common-name="VPN-CA" key-usage=key-cert-sign
    add name=CLIENT-CERT common-name="VPN-CLIENT" key-usage=tls-client
/ip firewall filter
    add chain=input action=accept protocol=tcp dst-port=443 src-address=0.0.0.0/0
