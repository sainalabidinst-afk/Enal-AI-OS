# MikroTik RouterOS Wireless Security
/interface wireless
    set [ find default-name=wlan1 ] mode=ap ssid=Corp-WiFi         security-profile=CORP-SEC
/interface wireless security
    add name=CORP-SEC mode=dynamic-keys authentication-types=wpa2-psk         wpa2-pre-shared-key=MyWiFiPass123 unicast-ciphers=aes-ccm group-ciphers=aes-ccm
/interface wireless access-list
    add mac-address=00:00:00:00:00:01 comment="Allowed Device"
/interface bridge
    add name=bridge-local
/interface bridge port
    add bridge=bridge-local interface=wlan1
