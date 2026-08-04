# MikroTik RouterOS CAPsMAN
/caps-man
    set enabled=yes
/caps-man manager
    set enabled=yes
/caps-man datapath
    add name=datapath1 bridge=bridge-local
/caps-man security
    add name=security1 authentication-types=wpa2-psk         wpa2-pre-shared-key=MyWiFiPass123
/caps-man configuration
    add name=config1 datapath=datapath1 security=security1 ssid=Corp-WiFi         channel-width=20/40mhz
/caps-man interface
    add name=ap1 master-interface=ether1 configuration=config1
