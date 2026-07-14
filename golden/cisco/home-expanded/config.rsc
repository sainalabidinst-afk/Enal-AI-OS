hostname cisco-home-router
!
interface GigabitEthernet0/0
 description LAN Interface
 ip address 192.168.1.1 255.255.255.0
 no shutdown
!
interface GigabitEthernet0/1
 description WAN Interface
 ip address 203.0.113.2 255.255.255.0
 no shutdown
!
vlan 10
 name Management
!
vlan 20
 name Users
!
spanning-tree mode rapid-pvst
spanning-tree vlan 10 priority 24576
!
ip route 0.0.0.0 0.0.0.0 203.0.113.1
ip route 10.0.0.0 255.255.255.0 192.168.1.254
!
access-list 101 permit tcp any host 192.168.1.1 eq 22
access-list 101 deny ip any any
!
ip nat inside source list 101 interface GigabitEthernet0/1 overload
!
ip dhcp pool LAN
 network 192.168.1.0 255.255.255.0
 default-router 192.168.1.1
 dns-server 8.8.8.8
 lease 86400
!
router ospf 1
 network 192.168.1.0 0.0.0.255 area 0
!
standby 1 ip 192.168.1.254
standby 1 priority 110
!
aaa new-model
aaa authentication login default local
!
snmp-server community public RO
!
ntp server 0.pool.ntp.org
!
logging 10.0.0.1
!
username admin privilege 15 secret 5 $1$hash
username operator privilege 1 secret 5 $1$hash2
!
enable secret 5 $1$enable$hash
!
ip name-server 8.8.8.8 1.1.1.1
!
line vty 0 4
 transport input ssh
 login local
 exec-timeout 5 0
!
end
