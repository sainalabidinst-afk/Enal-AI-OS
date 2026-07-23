# Dataset Validation Report

## Validation Summary

| Status | Count |
|--------|-------|
| Valid Config Files | 30 |
| Valid Expected JSON | 30 |
| Complete Metadata | 30 |
| Total Cases | 30 |

## Case-by-Case Validation

### MikroTik Cases

| Case | Config File | Has Expected JSON | Has Metadata | Status |
|------|-------------|-----------------|--------------|--------|
| wireless_wlan_corporate | config.rsc | ✓ | ✓ | VALID |
| vpn_pptp_remote_access | config.rsc | ✓ | ✓ | VALID |
| switching_vlan_switch | config.rsc | ✓ | ✓ | VALID |
| services_dhcp_dns_server | config.rsc | ✓ | ✓ | VALID |
| security_insecure_defaults | config.rsc | ✓ | ✓ | VALID |
| sample_hotspot | config.rsc | ✓ | ✓ | VALID |
| routing_static_route_default | config.rsc | ✓ | ✓ | VALID |
| qos_traffic_shaping_enterprise | config.rsc | ✓ | ✓ | VALID |
| nat_masquerade_portal | config.rsc | ✓ | ✓ | VALID |
| high_availability_bgpi_peer_tracking | config.rsc | ✓ | ✓ | VALID |

### Cisco Cases (config.txt format)

| Case | Config File | Has Expected JSON | Has Metadata | Status |
|------|-------------|-----------------|--------------|--------|
| wireless_corporate_ssid | config.txt | ✓ | ✓ | VALID |
| routing_ospf_enterprise | config.txt | ✓ | ✓ | VALID |
| vpn_site_to_site_ipsec | config.txt | ✓ | ✓ | VALID |
| services_dns_ntp_snmp | config.txt | ✓ | ✓ | VALID |
| qos_voice_priority | config.txt | ✓ | ✓ | VALID |
| switching_vlan_trunking | config.txt | ✓ | ✓ | VALID |
| security_ssh_hardened | config.txt | ✓ | ✓ | VALID |
| nat_pat_dmz | config.txt | ✓ | ✓ | VALID |
| firewall_asa_acl_strict | config.txt | ✓ | ✓ | VALID |
| high_availability_hsrp_router | config.txt | ✓ | ✓ | VALID |

### Fortinet Cases (config.txt format)

| Case | Config File | Has Expected JSON | Has Metadata | Status |
|------|-------------|-----------------|--------------|--------|
| wireless_employee_wifi | config.txt | ✓ | ✓ | VALID |
| vpn_ipsec_site_to_site | config.txt | ✓ | ✓ | VALID |
| switching_managed_vlan | config.txt | ✓ | ✓ | VALID |
| services_dns_ntp_mgmt | config.txt | ✓ | ✓ | VALID |
| security_admin_exposed | config.txt | ✓ | ✓ | VALID |
| routing_static_bgp_ha | config.txt | ✓ | ✓ | VALID |
| firewall_policy_dmz | config.txt | ✓ | ✓ | VALID |
| qos_traffic_shaping | config.txt | ✓ | ✓ | VALID |
| nat_virtual_ip_nat | config.txt | ✓ | ✓ | VALID |
| high_availability_active_passive | config.txt | ✓ | ✓ | VALID |

## Format Validation

All config files are readable text files. All expected.json files are valid JSON with required fields:
- vendor
- expected (with critical, high, medium, low counts)
- metadata (with description, tags)

## Missing Items

None. All 30 real cases have complete required files.