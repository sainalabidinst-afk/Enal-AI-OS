<!-- BILINGUAL_DOCS_START -->
## Bahasa Indonesia / English

### Ringkasan / Summary
Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.
> Terjemahan Indonesia: Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.

- Bahasa Indonesia: konten utama tetap dipertahankan dalam dokumen asli, dan bagian ini memberi konteks ringkas dalam bahasa Indonesia.
- English: the main content remains in the original document, and this section provides a concise bilingual context for international readers.

### Informasi Dokumen / Document Info
- File: `docs/SPRINT_5A_PLAN.md`
- Judul: Sprint 5A Plan
- Status: bilingual header added

<!-- BILINGUAL_DOCS_END -->

# Sprint 5A â€” Network Engineer: Production Ready

<!-- DOCUMENT_METADATA_START -->
**Owner:** Documentation Team
**Canonical Owner:** Documentation Governance Lead
**Last Verified:** 2026-08-02
**Version:** 1.0.0
**Status:** Active
**SSOT:** Documentation for SPRINT_5A_PLAN
<!-- DOCUMENT_METADATA_END -->

**Goal:** Bring Network Engineer capability to production-ready status with measurable quality gates.

**Definition of Done:**
- Accuracy: â‰¥95%
- False Positive: <5%
- False Negative: <5%
- Latency: <2s per analysis
- Coverage: >90% of known issue classes
- Golden Tests: 100% pass
- Real Cases: 100+ cases with benchmark results
- Documentation: Complete

---

## Current State

| Component | Status |
|-----------|--------|
| Parser (RouterOS, Cisco, Fortinet) | âœ… Mature |
| Analyzer (47 rules) | âœ… Mature |
| Graph Builder | âœ… Present |
| Recommendation Engine | âœ… Present |
| Generator | âœ… Present |
| Simulator | âœ… Present |
| Verification Engine | âœ… Present |
| Risk Scorer | âœ… Present |
| Controlled Deployment | âœ… Present |
| NIC (Knowledge + Inference) | âœ… Present |
| Golden Tests | âš ï¸ 1 sample case |
| Real Cases | âš ï¸ 1 sample case |

---

## Week 1 â€” Golden Tests Expansion

Target: 100+ golden test cases covering:
> Terjemahan Indonesia: Target: 100+ kasus uji emas yang mencakup:
- MikroTik RouterOS: ACL, BGP, OSPF, HSRP, NAT, AAA, SNMP, QoS, VPN, MPLS
- Cisco IOS: ACL, BGP, OSPF, HSRP, NAT, AAA, SNMP, QoS, VPN, MPLS
- Fortinet: Policies, NAT, VPN, Routing, HA

Each golden test must have:
> Terjemahan Indonesia: Each golden test must memiliki:
- `config.rsc` / `config.txt` â€” actual configuration snippet
- `expected.json` â€” expected findings, risk score, compliance score
- `metadata.yaml` â€” vendor, device role, complexity, tags
- `report.md` â€” human-readable expected report

Location: `real_cases/mikrotik/`, `real_cases/cisco/`, `real_cases/fortinet/`
> Terjemahan Indonesia: Lokasi: real_cases/mikrotik/, real_cases/cisco/, real_cases/fortinet/

---

## Week 2 â€” Benchmark Automation

Target: Automated benchmark runner that:
> Terjemahan Indonesia: Target: Automated benchmark runner itu:
1. Loads all real cases from disk
2. Runs each case through the analyzer
3. Compares actual vs expected findings
4. Computes accuracy, false positive, false negative, latency
5. Generates capability score breakdown
6. Exports results to JSON/CSV

Location: `benchmarks/network_engineer_benchmark.py`
> Terjemahan Indonesia: Lokasi: benchmarks/network_engineer_benchmark.py

Integration:
> Terjemahan Indonesia: Integrasi:
- `make benchmark-network` target in Makefile
- CI job: `python benchmarks/network_engineer_benchmark.py`

---

## Week 3 â€” Coverage Expansion

Target: Add missing rule coverage:
> Terjemahan Indonesia: Target: Tambahkan cakupan aturan yang hilang:
- VLAN security
- STP/RSTP
- BGP security (prefix filtering, TTL security)
- OSPF security (authentication)
- IPsec/VPN validation
- QoS policy validation
- SNMPv3 vs SNMPv1/v2c
- AAA/TACACS+/RADIUS validation
- Logging and syslog
- NTP configuration
- DNS security

---

## Week 4 â€” Integration & Telemetry

Target:
> Terjemahan Indonesia: Target:
- Wire telemetry recording into analyzer
- Track per-rule execution time
- Track vendor detection accuracy
- Track capability usage per session
- Dashboard-ready metrics endpoint

---

## Execution Plan

1. Create golden test cases (batch 1: 20 MikroTik cases)
2. Create golden test cases (batch 2: 20 Cisco cases)
3. Create golden test cases (batch 3: 20 Fortinet cases)
4. Create golden test cases (batch 4: 40 mixed advanced cases)
5. Benchmark automation
6. Coverage expansion
7. Integration testing
8. Documentation
