/interface pptp-server server
set enabled=yes default-profile=default

/ppp secret
add name=vpnuser password=vpnpass123 service=pptp profile=default

/ip firewall filter
add chain=input action=accept protocol=tcp dst-port=1723
add chain=input action=accept protocol=gre