/queue simple
add name="VoIP-High" target=192.168.10.100/32 max-limit=1M/1M priority=1
add name="Video-Med" target=192.168.10.0/24 max-limit=10M/10M priority=3
add name="General-Low" target=0.0.0.0/0 max-limit=512k/512k priority=8

/queue tree
add name="Download-Limit" parent=global-out limit-at=1M max-limit=10M
add name="Upload-Limit" parent=global-in limit-at=512k max-limit=5M