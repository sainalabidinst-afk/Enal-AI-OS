/interface wireguard
add name=wg0

/interface wireguard peers
add interface=wg0 public-key="ABC123" allowed-address=10.0.0.2/32

/ip address
add address=10.0.0.1/24 interface=wg0 network=10.0.0.0

/system identity
set name=wireguard-server
