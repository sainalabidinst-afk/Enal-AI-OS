# Benchmark Inventory

## Summary
- Total real cases: 30
- MikroTik cases: 10
- Cisco cases: 10
- Fortinet cases: 9
- Other: 1

## Benchmark Components

| Component | Location | Status |
|-----------|----------|--------|
| Benchmark Runner | `benchmarks/network_engineer_benchmark.py` | Present |
| Benchmark Harness | `real_cases/benchmark.py` | Present |
| Expected Results | `real_cases/*/expected.json` | Present (30 files) |
| Real Cases Dataset | `real_cases/` | Present (30 cases) |
| Report Generator | `benchmarks/network_engineer_benchmark.py:_write_report` | Present |
| Summary Printer | `benchmarks/network_engineer_benchmark.py:print_summary` | Present |

## Real Cases Inventory

### MikroTik (10 cases)
| Case | Config File | Expected Findings Source |
|------|-------------|------------------------|
| mikrotik:wireless_wlan_corporate | config.rsc | tags: wireless, ssid |
| mikrotik:vpn_pptp_remote_access | config.rsc | tags: vpn, pptp |
| mikrotik:switching_vlan_switch | config.rsc | tags: vlan, switching |
| mikrotik:services_dhcp_dns_server | config.rsc | tags: dhcp, services |
| mikrotik:security_insecure_defaults | config.rsc | tags: security, telnet |
| mikrotik:sample_hotspot | sample_hotspot.txt | tags: hotspot, bridge |
| mikrotik:routing_static_route_default | config.rsc | tags: routing |
| mikrotik:qos_traffic_shaping_enterprise | config.rsc | tags: qos |
| mikrotik:nat_masquerade_portal | config.rsc | tags: nat |
| mikrotik:high_availability_bgpi_peer_tracking | config.rsc | tags: ha, bgp |

### Cisco (10 cases)
| Case | Config File | Expected Findings Source |
|------|-------------|------------------------|
| cisco:wireless_corporate_ssid | config.rsc | tags: wireless, ssid |
| cisco:routing_ospf_enterprise | config.rsc | tags: routing, ospf |
| cisco:vpn_site_to_site_ipsec | config.rsc | tags: vpn |
| cisco:services_dns_ntp_snmp | config.rsc | tags: services |
| cisco:qos_voice_priority | config.rsc | tags: qos |
| cisco:switching_vlan_trunking | config.rsc | tags: vlan, switching |
| cisco:security_ssh_hardened | config.rsc | tags: security, ssh |
| cisco:nat_pat_dmz | config.rsc | tags: nat |
| cisco:firewall_asa_acl_strict | config.rsc | tags: firewall, acl |
| cisco:high_availability_hsrp_router | config.rsc | tags: ha, hsrp |

### Fortinet (10 cases)
| Case | Config File | Expected Findings Source |
|------|-------------|------------------------|
| fortinet:wireless_employee_wifi | config.rsc | tags: wireless |
| fortinet:vpn_ipsec_site_to_site | config.rsc | tags: vpn |
| fortinet:switching_managed_vlan | config.rsc | tags: vlan |
| fortinet:services_dns_ntp_mgmt | config.rsc | tags: services |
| fortinet:security_admin_exposed | config.rsc | tags: security |
| fortinet:routing_static_bgp_ha | config.rsc | tags: routing, ha |
| fortinet:firewall_policy_dmz | config.rsc | tags: firewall |
| fortinet:qos_traffic_shaping | config.rsc | tags: qos |
| fortinet:nat_virtual_ip_nat | config.rsc | tags: nat |
| fortinet:high_availability_active_passive | config.rsc | tags: ha |