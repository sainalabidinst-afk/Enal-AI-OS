/interface ethernet
set [ find default-name=ether1 ] name=lan1
set [ find default-name=ether2 ] name=wlan1

/capsman
set enabled=yes

/capsman interface
add name=caps1 master-interface=wlan1

/capsman security
set name=default authentication-types=wpa2-psk wpa2-pre-shared-key=change-me

/capsman configuration
set name=default ssid=MyWifi

/ip address
add address=192.168.88.1/24 interface=lan1 network=192.168.88.0

/system identity
set name=capsman-ap
