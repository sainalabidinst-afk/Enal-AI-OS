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
| wireless_wlan_corporate | ✓ | ✓ | ✓ | VALID |
| vpn_pptp_remote_access | ✓ | ✓ | ✓ | VALID |
| switching_vlan_switch | ✓ | ✓ | ✓ | VALID |
| services_dhcp_dns_server | ✓ | ✓ | ✓ | VALID |
| security_insecure_defaults | ✓ | ✓ | ✓ | VALID |
| sample_hotspot | ✓ | ✓ | ✓ | VALID |
| routing_static_route_default | ✓ | ✓ | ✓ | VALID |
| qos_traffic_shaping_enterprise | ✓ | ✓ | ✓ | VALID |
| nat_masquerade_portal | ✓ | ✓ | ✓ | VALID |
| high_availability_bgpi_peer_tracking | ✓ | ✓ | ✓ | VALID |

### Cisco Cases

| Case | Config File | Has Expected JSON | Has Metadata | Status |
|------|-------------|-----------------|--------------|--------|
| wireless_corporate_ssid | ✓ | ✓ | ✓ | VALID |
| routing_ospf_enterprise | ✓ | ✓ | ✓ | VALID |
| vpn_site_to_site_ipsec | ✓ | ✓ | ✓ | VALID |
| services_dns_ntp_snmp | ✓ | ✓ | ✓ | VALID |
| qos_voice_priority | ✓ | ✓ | ✓ | VALID |
| switching_vlan_trunking | ✓ | ✓ | ✓ | VALID |
| security_ssh_hardened | ✓ | ✓ | ✓ | VALID |
| nat_pat_dmz | ✓ | ✓ | ✓ | VALID |
| firewall_asa_acl_strict | ✓ | ✓ | ✓ | VALID |
| high_availability_hsrp_router | ✓ | ✓ | ✓ | VALID |

### Fortinet Cases

| Case | Config File | Has Expected JSON | Has Metadata | Status |
|------|-------------|-----------------|--------------|--------|
| wireless_employee_wifi | ✓ | ✓ | ✓ | VALID |
| vpn_ipsec_site_to_site | ✓ | ✓ | ✓ | VALID |
| switching_managed_vlan | ✓ | ✓ | ✓ | VALID |
| services_dns_ntp_mgmt | ✓ | ✓ | ✓ | VALID |
| security_admin_exposed | ✓ | ✓ | ✓ | VALID |
| routing_static_bgp_ha | ✓ | ✓ | ✓ | VALID |
| firewall_policy_dmz | ✓ | ✓ | ✓ | VALID |
| qos_traffic_shaping | ✓ | ✓ | ✓ | VALID |
| nat_virtual_ip_nat | ✓ | ✓ | ✓ | VALID |
| high_availability_active_passive | ✓ | ✓ | ✓ | VALID |

## Format Validation

All config files are readable text files. All expected.json files are valid JSON with required fields:
- vendor
- expected (with critical, high, medium, low counts)
- metadata (with description, tags)

## Missing Items

None. All 30 real cases have complete required files.