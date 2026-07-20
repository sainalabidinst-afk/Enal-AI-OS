# DATASET VALIDATION
# Network Engineer Real Cases

## Validation Results
| Check | Status |
|-------|--------|
| Config files available | ✅ All 30 cases have config.rsc or config.txt |
| Expected.json available | ✅ All 30 cases have expected.json |
| Metadata complete | ✅ All have description, tags, source |
| Format valid | ✅ All valid JSON |
| No broken files | ✅ All readable |

## Case Validation Details
```
mikrotik:
  - firewall_input_filter_strict: config.rsc + expected.json ✅
  - high_availability_bgpi_peer_tracking: config.rsc + expected.json ✅
  - qos_traffic_shaping_enterprise: config.rsc + expected.json ✅
  - routing_static_route_default: config.rsc + expected.json ✅
  - security_insecure_defaults: config.rsc + expected.json ✅
  - services_dhcp_dns_server: config.rsc + expected.json ✅
  - switching_vlan_switch: config.rsc + expected.json ✅
  - vpn_pptp_remote_access: config.rsc + expected.json ✅
  - wireless_wlan_corporate: config.rsc + expected.json ✅
  - nat_masquerade_portal: config.rsc + expected.json ✅
  - sample_hotspot: config.rsc + expected.json ✅

cisco:
  - firewall_asa_acl_strict: config.txt + expected.json ✅
  - routing_ospf_enterprise: config.txt + expected.json ✅
  - nat_pat_dmz: config.txt + expected.json ✅
  - vpn_site_to_site_ipsec: config.txt + expected.json ✅
  - qos_voice_priority: config.txt + expected.json ✅
  - wireless_corporate_ssid: config.txt + expected.json ✅
  - services_dns_ntp_snmp: config.txt + expected.json ✅
  - security_ssh_hardened: config.txt + expected.json ✅
  - switching_vlan_trunking: config.txt + expected.json ✅
  - high_availability_hsrp_router: config.txt + expected.json ✅

fortinet:
  - firewall_policy_dmz: config.txt + expected.json ✅
  - routing_static_bgp_ha: config.txt + expected.json ✅
  - nat_virtual_ip_nat: config.txt + expected.json ✅
  - vpn_ipsec_site_to_site: config.txt + expected.json ✅
  - qos_traffic_shaping: config.txt + expected.json ✅
  - wireless_employee_wifi: config.txt + expected.json ✅
  - services_dns_ntp_mgmt: config.txt + expected.json ✅
  - security_admin_exposed: config.txt + expected.json ✅
  - switching_managed_vlan: config.txt + expected.json ✅
  - high_availability_active_passive: config.txt + expected.json ✅
```

## Summary
- Total cases validated: 30
- Valid cases: 30 (100%)
- Invalid cases: 0