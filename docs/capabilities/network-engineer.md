# Network Engineer Capability Specification

## Version: 1.0.0
## Status: Draft (v1.0 ready for implementation)

---

## 1. Purpose

Deliver vendor-agnostic network intelligence untuk:
- Configuration parsing & validation
- Security compliance auditing
- Risk analysis & recommendations
- Configuration generation & simulation

---

## 2. Scope

### In Scope
- Vendor support: MikroTik RouterOS, Cisco IOS, Fortinet
- File format: .rsc, .conf, .txt
- Analysis types: Security, Best Practice, Compliance
- Output: Findings, Risk Score, Recommendations, Documentation

### Out of Scope
- Direct device configuration push
- Real-time monitoring
- Traffic simulation
- Cross-vendor translation (future roadmap)

---

## 3. Contract

### Input
```json
{
  "type": "text",
  "content": "string (raw config)",
  "vendor_hint": "mikrotik|cisco|fortinet|auto-detect"
}
```

### Output
```json
{
  "device": "string",
  "vendor": "string",
  "summary": "string",
  "issues": [{"severity": "critical|high|medium|low", "category": "string", "description": "string"}],
  "recommendations": [{"priority": "high|medium|low", "problem": "string", "why": "string", "recommendation": "string"}],
  "risk_score": "float 0-1"
}
```

---

## 4. Analyzer Rules (Target 200+)

### Security Rules
| Rule ID | Category | Vendor | Description |
|---------|----------|--------|-------------|
| SEC-001 | Firewall | All | Default policies must be restrictive |
| SEC-002 | Authentication | All | Weak authentication detected |
| SEC-003 | Services | All | Unnecessary services exposed |
| SEC-004 | SNMP | All | SNMP community strings exposed |

### Best Practice Rules
| Rule ID | Category | Vendor | Description |
|---------|----------|--------|-------------|
| BP-001 | Logging | All | Logging not configured for critical events |
| BP-002 | NTP | All | Time source not configured |
| BP-003 | SSH | All | SSH hardening not applied |

---

## 5. Benchmark Requirements

### Target Metrics
| Metric | Target | Pass Criteria |
|--------|--------|---------------|
| Accuracy | ≥95% | Correct findings ≥95% |
| Precision | ≥95% | False positive ≤5% |
| Recall | ≥95% | True positive ≥95% |
| Latency | <2s | Avg response <2 seconds |
| Coverage | ≥90% | Code path coverage ≥90% |

---

## 6. Supported Vendors

| Vendor | Format | Parser Status | Analyzer Status |
|--------|--------|---------------|----------------|
| MikroTik | .rsc, .conf | ✅ | ⏳ |
| Cisco IOS | .conf, .txt | ✅ | ⏳ |
| Fortinet | .conf | ✅ | ⏳ |

---

## 7. Known Limitations

- Timeout 60s untuk file > 10MB
- Hanya mendukung single-config analysis (bukan template)
- Belum ada diff analysis
- Network context awareness terbatas

---

## 8. Dataset Coverage Target

| Milestone | Cases | Vendors Covered | Domains Covered |
|-----------|-------|-----------------|-----------------|
| 5A.1 | 25 | MikroTik: 10, Cisco: 10, Fortinet: 5 | Security: 15, Best Practice: 10 |
| 5A.2 | 50 | Balanced distribution | Security: 25, HA: 10, QoS: 5, Wireless: 5, Monitoring: 5 |
| 5A.3 | 100 | All 3 vendors × 25+ cases | Full coverage |

---

## 9. Evaluation Metrics

### Golden Tests
- ✅ Must pass 100% before merge
- Test cases stored in `benchmarks/golden/`

### Real Cases
- Benchmark pass rate minimum 95%
- Evaluated via `make benchmark-network`

### Performance
- Execution time logged via telemetry
- Alert if >2s average