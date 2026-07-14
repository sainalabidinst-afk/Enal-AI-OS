/interface ethernet
set [ find default-name=ether1 ] name=wan
set [ find default-name=ether2 ] name=lan1
set [ find default-name=ether3 ] name=wlan1

/interface wireless
set wlan1 name=wifi-guest band=2ghz-b/g/n channel-width=20/40mhz-XX country=indonesia disabled=no frequency=auto

/interface wireless security-profiles
set [ find default=yes ] name=guest-profile mode=dynamic-keys authentication-types=wpa2-psk wpa2-pre-shared-key=hotel2024

/interface wireless access-list
add mac-address=AA:BB:CC:DD:EE:FF interface=wlan1

/ip hotspot
add name=hotspot1 interface=lan1 profile=hsprof1 address-pool=hs_pool1

/ip hotspot profile
add name=hsprof1 dns-name=hotel.local hotspot-address=192.168.88.1

/ip pool
add name=hs_pool1 ranges=192.168.88.10-192.168.88.250

/ip address
add address=192.168.88.1/24 interface=lan1 network=192.168.88.0
add address=10.0.0.1/24 interface=wlan1 network=10.0.0.0

/ip dhcp-server
add address-pool=hs_pool1 interface=lan1 name=dhcp1

/ip firewall nat
add action=masquerade chain=srcnat out-interface=wan

/ip firewall filter
add action=accept chain=input connection-state=established,related,untracked
add action=drop chain=input connection-state=invalid
add action=accept chain=input protocol=icmp
add action=accept chain=input connection-state=new in-interface=lan1
add action=drop chain=input
add action=accept chain=forward connection-state=established,related,untracked
add action=drop chain=forward connection-state=invalid

/system identity
set name=hotel-gateway

/system clock
set time-zone-name=Asia/Jakarta
