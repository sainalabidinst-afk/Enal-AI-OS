# MikroTik RouterOS Cloud and DNS
/ip cloud
    set ddns-enabled=yes ddns-update-interval=1m
    set ddns-use-ip-ssl=yes
/ip dns
    set allow-remote-requests=yes servers=8.8.8.8,1.1.1.1
    set use-doh=yes doh-server=https://dns.google/dns-query
/system ntp client
    set enabled=yes server-address=time.google.com
/system logging
    add topics=info action=memory
