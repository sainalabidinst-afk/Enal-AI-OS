/ip ssh
set allow-none-cipher=yes strong-crypto=no

/user
add name=admin password=admin123 group=full

/ip service
set telnet disabled=no
set ftp disabled=no
set ssh address=0.0.0.0/0