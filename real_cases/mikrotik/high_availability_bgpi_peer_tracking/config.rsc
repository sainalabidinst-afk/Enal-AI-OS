/interface ethernet
set ether1 disable-running-check=no name=WAN-Primary

/routing bgp peer
add name=peer1 remote-address=10.0.0.2 remote-as=65002 multihop=no

/system health
set cpu-overtemp-check=yes

/system watchdog
set watch-address=8.8.8.8 watchdog-time=1m send-timeout=1s