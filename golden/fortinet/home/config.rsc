config system global
    set hostname fortinet-home
end

config system interface
    edit "wan"
        set ip 203.0.113.2 255.255.255.0
    next
    edit "lan"
        set ip 192.168.1.1 255.255.255.0
    next
end

config firewall policy
    edit 1
        set action accept
        set srcintf "lan"
        set dstintf "wan"
        set srcaddr "all"
        set dstaddr "all"
        set schedule "always"
        set service "ALL"
        set logtraffic all
    next
    edit 2
        set action accept
        set srcintf "wan"
        set dstintf "lan"
        set srcaddr "all"
        set dstaddr "all"
        set schedule "always"
        set service "ALL"
    next
end

config system ntp
    set ntpsync enable
end
