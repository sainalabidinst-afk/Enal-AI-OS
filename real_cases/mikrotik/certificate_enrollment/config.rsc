# MikroTik RouterOS Certificate
/certificate
    add name=my-ca common-name="My-CA" key-usage=key-cert-sign         tls-version=1.3
    add name=server-cert common-name="router.local" key-usage=digital-signature         tls-version=1.3 subject-alt-name="DNS:router.local"
/ip service
    set www disabled=yes
    set www-ssl port=443 certificate=server-cert
    set ssh disabled=no port=22
