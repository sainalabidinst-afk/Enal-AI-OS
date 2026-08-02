

# Dataset Validation Report

<!-- DOCUMENT_METADATA_START -->
**Owner:** Documentation Team
**Canonical Owner:** Documentation Governance Lead
**Last Verified:** 2026-08-02
**Version:** 1.0.0
**Status:** Active
**SSOT:** Real case study documentation
<!-- DOCUMENT_METADATA_END -->

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
| wireless_wlan_corporate | config.rsc | âœ“ | âœ“ | VALID |
| vpn_pptp_remote_access | config.rsc | âœ“ | âœ“ | VALID |
| switching_vlan_switch | config.rsc | âœ“ | âœ“ | VALID |
| services_dhcp_dns_server | config.rsc | âœ“ | âœ“ | VALID |
| security_insecure_defaults | config.rsc | âœ“ | âœ“ | VALID |
| sample_hotspot | config.rsc | âœ“ | âœ“ | VALID |
| routing_static_route_default | config.rsc | âœ“ | âœ“ | VALID |
| qos_traffic_shaping_enterprise | config.rsc | âœ“ | âœ“ | VALID |
| nat_masquerade_portal | config.rsc | âœ“ | âœ“ | VALID |
| high_availability_bgpi_peer_tracking | config.rsc | âœ“ | âœ“ | VALID |

### Cisco Cases (config.txt format)

| Case | Config File | Has Expected JSON | Has Metadata | Status |
|------|-------------|-----------------|--------------|--------|
| wireless_corporate_ssid | config.txt | âœ“ | âœ“ | VALID |
| routing_ospf_enterprise | config.txt | âœ“ | âœ“ | VALID |
| vpn_site_to_site_ipsec | config.txt | âœ“ | âœ“ | VALID |
| services_dns_ntp_snmp | config.txt | âœ“ | âœ“ | VALID |
| qos_voice_priority | config.txt | âœ“ | âœ“ | VALID |
| switching_vlan_trunking | config.txt | âœ“ | âœ“ | VALID |
| security_ssh_hardened | config.txt | âœ“ | âœ“ | VALID |
| nat_pat_dmz | config.txt | âœ“ | âœ“ | VALID |
| firewall_asa_acl_strict | config.txt | âœ“ | âœ“ | VALID |
| high_availability_hsrp_router | config.txt | âœ“ | âœ“ | VALID |

### Fortinet Cases (config.txt format)

| Case | Config File | Has Expected JSON | Has Metadata | Status |
|------|-------------|-----------------|--------------|--------|
| wireless_employee_wifi | config.txt | âœ“ | âœ“ | VALID |
| vpn_ipsec_site_to_site | config.txt | âœ“ | âœ“ | VALID |
| switching_managed_vlan | config.txt | âœ“ | âœ“ | VALID |
| services_dns_ntp_mgmt | config.txt | âœ“ | âœ“ | VALID |
| security_admin_exposed | config.txt | âœ“ | âœ“ | VALID |
| routing_static_bgp_ha | config.txt | âœ“ | âœ“ | VALID |
| firewall_policy_dmz | config.txt | âœ“ | âœ“ | VALID |
| qos_traffic_shaping | config.txt | âœ“ | âœ“ | VALID |
| nat_virtual_ip_nat | config.txt | âœ“ | âœ“ | VALID |
| high_availability_active_passive | config.txt | âœ“ | âœ“ | VALID |

## Format Validation

All config files are readable text files. All expected.json files are valid JSON with required fields:
- vendor
- expected (with critical, high, medium, low counts)
- metadata (with description, tags)

## Missing Items

None. All 30 real cases have complete required files.

