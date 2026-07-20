/interface wireless
set wlan1 ssid=CorpWiFi frequency=2412 band=2ghz-b/g/n mode=ap-bridge

/interface wireless security-profiles
set [find default=yes] authentication-types=wpa2-psk wpa2-pre-shared-key=wifi12345

/ip hotspot profile
add name=hsprof1 dns-name=wifi.corp.local hotspot-address=192.168.20.1