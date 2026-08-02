<!-- BILINGUAL_DOCS_START -->
## Bahasa Indonesia / English

### Ringkasan / Summary
Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.
> Terjemahan Indonesia: Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.

- Bahasa Indonesia: konten utama tetap dipertahankan dalam dokumen asli, dan bagian ini memberi konteks ringkas dalam bahasa Indonesia.
- English: the main content remains in the original document, and this section provides a concise bilingual context for international readers.

### Informasi Dokumen / Document Info
- File: `real_cases/analyzer_rules_mapping.md`
- Judul: Analyzer Rules Mapping
- Status: bilingual header added

<!-- BILINGUAL_DOCS_END -->

# Network Engineer Analyzer Rules - Domain Classification

<!-- DOCUMENT_METADATA_START -->
**Owner:** Documentation Team
**Canonical Owner:** Documentation Governance Lead
**Last Verified:** 2026-08-02
**Version:** 1.0.0
**Status:** Active
**SSOT:** Real case study documentation
<!-- DOCUMENT_METADATA_END -->
# Generated from apps/network_engineer/analyzer.py
# Total: 36 rules across 8 domains

## Domain: Routing (6 rules)
- _check_route_without_gateway - Route without gateway configuration
- _check_default_route_missing - Default route missing
- _check_missing_ntp - NTP not configured
- _check_missing_loopback - No loopback interface
- _check_overlapping_networks - Overlapping network addresses
- _check_duplicate_ip_addresses - Duplicate IP addresses

## Domain: Firewall (9 rules)
- _check_missing_firewall_input - No input chain rules
- _check_missing_firewall_forward - Forward chain missing with NAT
- _check_missing_icmp_accept - ICMP not explicitly allowed
- _check_firewall_without_stateful - No stateful inspection
- _check_missing_connection_tracking - No connection tracking rules
- _check_firewall_rule_order - Firewall rule order issues
- _check_masquerade_on_lan - Masquerade on LAN interface
- _check_bridge_without_stp - Bridge no STP (also HA)
- _check_bridge_loop_risk - Bridge with loop risk (also HA)

## Domain: NAT (3 rules)
- _check_missing_masquerade - No masquerade rule
- _check_duplicate_nat - Multiple NAT rules detected
- _check_missing_masquerade (duplicate check)

## Domain: VPN (2 rules)
- _check_ppp_without_encryption - PPP without encryption

## Domain: QoS (3 rules)
- _check_missing_fasttrack - FastTrack not enabled
- _check_queue_without_limit - Queue missing max limit
- _check_queue_simple_duplicate - Duplicate queue targets

## Domain: Wireless (1 rule)
- _check_wireless_open_security - Wireless default security

## Domain: Services (4 rules)
- _check_dns_without_upstream - No DNS servers
- _check_dhcp_pool_exhaustion - DHCP without pool
- _check_hotspot_without_profile - Hotspot no profile
- _check_hotspot_dns_unsafe - Hotspot unsafe DNS

## Domain: Security (14 rules)
- _check_default_password - Default/weak password
- _check_unrestricted_winbox - Winbox open to world
- _check_unrestricted_ssh - SSH open to world
- _check_unrestricted_www - Web open to world
- _check_unrestricted_api - API open to world
- _check_user_without_password - No user password
- _check_service_without_restriction - Service unrestricted
- _check_weak_password_in_comment - Password in comment
- _check_unencrypted_protocols - Telnet/HTTP enabled
- _check_mgmt_from_untrusted - Management from anywhere
- _check_high_risk_ports_open - High-risk ports exposed
- _check_certificate_expired - Expired certificate
- _check_radius_without_backup - RADIUS no backup

## Domain: Switching (1 rule)
- _check_unused_interfaces - Unused interfaces enabled

## Domain: High Availability (2 rules)
- _check_bridge_without_stp - Bridge no STP (covered above)
- _check_bridge_loop_risk - Bridge with loop risk (covered above)
