hostname cisco-home-router
!
interface GigabitEthernet0/0
 ip address 192.168.1.1 255.255.255.0
 no shutdown
!
interface GigabitEthernet0/1
 ip address 203.0.113.2 255.255.255.0
 no shutdown
!
ip route 0.0.0.0 0.0.0.0 203.0.113.1
!
access-list 101 permit tcp any host 192.168.1.1 eq 22
access-list 101 deny ip any any
!
ip nat inside source list 101 interface GigabitEthernet0/1 overload
!
end
