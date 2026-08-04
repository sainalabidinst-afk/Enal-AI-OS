# MikroTik RouterOS HTB QoS
/queue tree
    add name="HIGH-PRIORITY" parent=global-out limit-at=512k max-limit=1M         priority=1
    add name="MEDIUM-PRIORITY" parent=global-out limit-at=2M max-limit=10M         priority=3
    add name="BEST-EFFORT" parent=global-out limit-at=1M max-limit=5M         priority=8
/ip firewall mangle
    add chain=prerouting action=mark-connection new-connection-mark=HIGH         protocol=tcp dst-port=22,443 passthrough=yes
    add chain=prerouting action=mark-packet new-packet-mark=HIGH         connection-mark=HIGH passthrough=no
