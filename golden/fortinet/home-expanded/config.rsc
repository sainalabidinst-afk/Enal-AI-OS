config system global
    set hostname fortinet-home-expanded
    set timezone Asia/Jakarta
end

config system interface
    edit "wan"
        set ip 203.0.113.2 255.255.255.0
        set type physical
        set alias "WAN Uplink"
        set status up
    next
    edit "lan"
        set ip 192.168.1.1 255.255.255.0
        set type physical
        set alias "LAN Downlink"
        set status up
    next
    edit "mgmt"
        set ip 10.0.0.1 255.255.255.0
        set type physical
        set status up
    next
end

config system vlan
    edit 10
        set interface "lan"
    next
    edit 20
        set interface "lan"
        set ip 192.168.20.1 255.255.255.0
    next
end

config router static
    edit 1
        set gateway 203.0.113.1
        set device "wan"
    next
    edit 2
        set dst 10.0.0.0 255.255.255.0
        set gateway 192.168.1.254
        set device "lan"
    next
end

config system dhcp server
    edit 1
        set default-gateway 192.168.1.1
        set lease-time 86400
    next
end

config system dns
    set primary 8.8.8.8
    set secondary 1.1.1.1
end

config system ntp
    set ntpsync enable
    set server "0.pool.ntp.org"
end

config log syslogd setting
    set status enable
    set server "10.0.0.100"
end

config firewall policy
    edit 1
        set srcintf "lan"
        set dstintf "wan"
        set srcaddr "all"
        set dstaddr "all"
        set action accept
        set service "ALL"
        set schedule "always"
        set logtraffic all
    next
    edit 2
        set srcintf "wan"
        set dstintf "lan"
        set srcaddr "all"
        set dstaddr "all"
        set action accept
        set service "HTTP"
        set schedule "always"
    next
    edit 3
        set srcintf "wan"
        set dstintf "lan"
        set srcaddr "all"
        set dstaddr "all"
        set action deny
        set service "ALL"
        set schedule "always"
    next
end

config vpn ipsec phase1-interface
    edit "vpn-tunnel"
        set remote-gw 203.0.113.10
        set psksecret ENC
    next
end

config vpn ipsec phase2-interface
    edit "vpn-tunnel"
        set dst-addr 10.0.0.0/24
    next
end

config system local
    edit "admin"
        set type local
        set passwd ENC
    next
    edit "operator"
        set type local
        set passwd ENC
    next
end

config system ha
    set mode a-p
    set group-name "FGT-CLUSTER"
    set priority 200
end

config system ntp
    set ntpsync enable
    set server "0.pool.ntp.org"
end
