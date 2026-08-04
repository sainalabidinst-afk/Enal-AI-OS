# MikroTik RouterOS Queue Tree QoS
/queue tree
    add name="VOIP-Priority" parent=global-out limit-at=512k max-limit=1M         priority=1
    add name="Video-Medium" parent=global-out limit-at=2M max-limit=10M         priority=3
    add name="Bulk-Low" parent=global-out limit-at=1M max-limit=5M         priority=8
/queue simple
    add name="Guest-Limit" target=10.0.50.0/24 max-limit=512k/512k
/ip firewall mangle
    add chain=prerouting action=mark-connection new-connection-mark=VOIP         protocol=udp dst-port=5060,16384-16394 passthrough=yes
    add chain=prerouting action=mark-packet new-packet-mark=VOIP         connection-mark=VOIP passthrough=no
