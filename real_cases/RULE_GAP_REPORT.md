

# RULE GAP REPORT

<!-- DOCUMENT_METADATA_START -->
**Owner:** Documentation Team
**Canonical Owner:** Documentation Governance Lead
**Last Verified:** 2026-08-02
**Version:** 1.0.0
**Status:** Active
**SSOT:** Real case study documentation
<!-- DOCUMENT_METADATA_END -->
# Network Engineer Analyzer vs Real Cases

## Case Analysis Summary
- Total cases: 30
- MikroTik cases: 10
- Cisco cases: 10
- Fortinet cases: 10

## Gap Classification

### A. Cases Without Rule Coverage
All Cisco and Fortinet cases have NO rule coverage - analyzer only detects MikroTik patterns.

| Case | Category | Vendor | Status |
|------|----------|--------|--------|
| cisco:routing_ospf_enterprise | routing | cisco | NO RULES - OSPF not detected |
| cisco:firewall_asa_acl_strict | firewall | cisco | PARTIAL - Telnet blocked but not detected |
| cisco:nat_pat_dmz | nat | cisco | NO RULES - PAT syntax not detected |
| cisco:vpn_site_to_site_ipsec | vpn | cisco | NO RULES - IPSec not detected |
| cisco:qos_voice_priority | qos | cisco | NO RULES - Policy-map not detected |
| cisco:wireless_corporate_ssid | wireless | cisco | NO RULES - dot11 not detected |
| cisco:services_dns_ntp_snmp | services | cisco | NO RULES - SNMP not detected |
| cisco:security_ssh_hardened | security | cisco | PARTIAL - weak password detected |
| cisco:switching_vlan_trunking | switching | cisco | NO RULES - VLAN not detected |
| cisco:high_availability_hsrp | high_availability | cisco | NO RULES - HSRP not detected |
| fortinet:routing_static_bgp_ha | routing | fortinet | NO RULES - Fortinet syntax |
| fortinet:firewall_policy_dmz | firewall | fortinet | NO RULES - Fortinet syntax |
| fortinet:nat_virtual_ip_nat | nat | fortinet | NO RULES - Fortinet syntax |
| fortinet:vpn_ipsec_site_to_site | vpn | fortinet | NO RULES - Fortinet syntax |
| fortinet:qos_traffic_shaping | qos | fortinet | NO RULES - Fortinet syntax |
| fortinet:wireless_employee_wifi | wireless | fortinet | NO RULES - Fortinet syntax |
| fortinet:services_dns_ntp_mgmt | services | fortinet | NO RULES - Fortinet syntax |
| fortinet:security_admin_exposed | security | fortinet | PARTIAL - weak password detected |
| fortinet:switching_managed_vlan | switching | fortinet | NO RULES - Fortinet syntax |
| fortinet:high_availability_active_passive | high_availability | fortinet | NO RULES - Fortinet syntax |

### B. Rule Overlap Analysis
Rules that detect overlapping patterns:
- _check_firewall_without_stateful overlaps with _check_missing_connection_tracking (both check connection-state)
- _check_missing_fasttrack could be considered part of Performance not NAT

### C. Missing Vendor Patterns
Cisco patterns needed:
- `telnet disabled=no` - should trigger unencrypted protocols (same as MikroTik telnet)
- `ip ssh version 2` - should indicate secure SSH configuration
- `standby` - HSRP/VRRP detection
- `ospf` / `bgp` - routing protocol detection
- `policy-map` / `class-map` - QoS policy detection
- `vlan` / `switchport` - switching detection
- `crypto isakmp` / `vpn ipsec` - IPSec detection
- `dot11` / `ssid` - wireless detection

Fortinet patterns needed:
- `config firewall` - Fortinet firewall base
- `config vpn ipsec` - IPSec
- `config system ha` - HA
- `config wireless-controller` - wireless

### D. Duplicate Rule Detection
NO duplicate rule IDs found. Rules are uniquely named by function.

### E. Summary
| Metric | Count |
|--------|-------|
| Cases with full coverage | 10 (MikroTik only) |
| Cases with partial coverage | 2 (security patterns) |
| Cases with no coverage | 18 (Cisco/Fortinet) |
| Missing vendor patterns | 18 |

