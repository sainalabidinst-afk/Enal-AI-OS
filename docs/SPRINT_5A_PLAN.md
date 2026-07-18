# Sprint 5A — Network Engineer: Production Ready

**Goal:** Bring Network Engineer capability to production-ready status with measurable quality gates.

**Definition of Done:**
- Accuracy: ≥95%
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
| Parser (RouterOS, Cisco, Fortinet) | ✅ Mature |
| Analyzer (47 rules) | ✅ Mature |
| Graph Builder | ✅ Present |
| Recommendation Engine | ✅ Present |
| Generator | ✅ Present |
| Simulator | ✅ Present |
| Verification Engine | ✅ Present |
| Risk Scorer | ✅ Present |
| Controlled Deployment | ✅ Present |
| NIC (Knowledge + Inference) | ✅ Present |
| Golden Tests | ⚠️ 1 sample case |
| Real Cases | ⚠️ 1 sample case |

---

## Week 1 — Golden Tests Expansion

Target: 100+ golden test cases covering:
- MikroTik RouterOS: ACL, BGP, OSPF, HSRP, NAT, AAA, SNMP, QoS, VPN, MPLS
- Cisco IOS: ACL, BGP, OSPF, HSRP, NAT, AAA, SNMP, QoS, VPN, MPLS
- Fortinet: Policies, NAT, VPN, Routing, HA

Each golden test must have:
- `config.rsc` / `config.txt` — actual configuration snippet
- `expected.json` — expected findings, risk score, compliance score
- `metadata.yaml` — vendor, device role, complexity, tags
- `report.md` — human-readable expected report

Location: `real_cases/mikrotik/`, `real_cases/cisco/`, `real_cases/fortinet/`

---

## Week 2 — Benchmark Automation

Target: Automated benchmark runner that:
1. Loads all real cases from disk
2. Runs each case through the analyzer
3. Compares actual vs expected findings
4. Computes accuracy, false positive, false negative, latency
5. Generates capability score breakdown
6. Exports results to JSON/CSV

Location: `benchmarks/network_engineer_benchmark.py`

Integration:
- `make benchmark-network` target in Makefile
- CI job: `python benchmarks/network_engineer_benchmark.py`

---

## Week 3 — Coverage Expansion

Target: Add missing rule coverage:
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

## Week 4 — Integration & Telemetry

Target:
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
