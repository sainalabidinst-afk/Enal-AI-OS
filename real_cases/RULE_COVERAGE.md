<!-- BILINGUAL_DOCS_START -->
## Bahasa Indonesia / English

### Ringkasan / Summary
Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.
> Terjemahan Indonesia: Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.

- Bahasa Indonesia: konten utama tetap dipertahankan dalam dokumen asli, dan bagian ini memberi konteks ringkas dalam bahasa Indonesia.
- English: the main content remains in the original document, and this section provides a concise bilingual context for international readers.

### Informasi Dokumen / Document Info
- File: `real_cases/RULE_COVERAGE.md`
- Judul: Rule Coverage
- Status: bilingual header added

<!-- BILINGUAL_DOCS_END -->

# RULE COVERAGE

<!-- DOCUMENT_METADATA_START -->
**Owner:** Documentation Team
**Canonical Owner:** Documentation Governance Lead
**Last Verified:** 2026-08-02
**Version:** 1.0.0
**Status:** Active
**SSOT:** Real case study documentation
<!-- DOCUMENT_METADATA_END -->
# Network Engineer Analyzer

## Summary
| Metric | Before | After |
|--------|--------|-------|
| Total Rules | 40 | 55 |
| MikroTik Rules | 40 | 43 |
| Cisco Rules | 0 | 3 |
| Fortinet Rules | 0 | 3 |
| Vendor-Agnostic Rules | 0 | 9 |

## Coverage by Vendor
| Vendor | Rules | Coverage % |
|--------|-------|------------|
| MikroTik | 43 | 100% |
| Cisco | 3 | 7% |
| Fortinet | 3 | 7% |

## Coverage by Domain
| Domain | Rules | Cases Covered | Notes |
|--------|-------|---------------|-------|
| Routing | 6 | 3 (MikroTik) | 6/9 cases covered |
| Firewall | 9 | 4 (all vendors) | Full coverage |
| NAT | 3 | 3 (MikroTik) | Cisco/Fortinet patterns need parser |
| VPN | 5 | 3 (all vendors) | Added Cisco/Fortinet IPSec |
| QoS | 3 | 3 (MikroTik) | Cisco/Fortinet patterns need parser |
| Wireless | 4 | 3 (MikroTik) | Added WPA/WEP checks |
| Services | 4 | 3 (MikroTik) | SNMP/WPA2 support added |
| Security | 15 | 10 (all vendors) | Added Telnet detection |
| Switching | 1 | 3 (MikroTik) | Cisco/Fortinet patterns need parser |
| High Availability | 4 | 3 (all vendors) | Added HSRP/HA support |

## Coverage by Severity
| Severity | Count |
|----------|-------|
| CRITICAL | 23 |
| WARNING | 18 |
| INFO | 10 |
| SUGGESTION | 4 |

## Coverage by Dataset
All 30 real cases can be analyzed (raw_lines based rules work on all vendors).
> Terjemahan Indonesia: All 30 real cases dapat menjadi analyzed (raw_lines based rules work pada all vendors).
