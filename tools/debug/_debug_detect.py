import sys
sys.path.insert(0, '.')

config_text = open('real_cases/fortinet/wireless_employee_wifi/config.txt').read()

from apps.network_engineer.vendor.cisco_ios import CiscoIOSAdapter
from apps.network_engineer.vendor.mikrotik import MikroTikAdapter
from apps.network_engineer.vendor.fortinet import FortiOSAdapter

cisco = CiscoIOSAdapter()
mikrotik = MikroTikAdapter()
fortinet = FortiOSAdapter()

print("Cisco detect:", cisco.detect(config_text))
print("MikroTik detect:", mikrotik.detect(config_text))
print("Fortinet detect:", fortinet.detect(config_text))

# Check which Cisco indicator matches
indicators = [
    "interface GigabitEthernet",
    "interface FastEthernet",
    "interface TenGigabitEthernet",
    "interface Dot11Radio",
    "interface BVI",
    "access-list ",
    "ip nat inside source",
    "line vty",
    "enable password",
    "router bgp ",
    "ip route ",
    "dot11 ssid",
    "switchport mode",
    "vlan ",
    "policy-map",
    "class-map",
    "router ospf",
    "snmp-server",
    "hostname ",
]
for ind in indicators:
    if ind in config_text:
        print(f"Cisco matched: {ind!r}")
