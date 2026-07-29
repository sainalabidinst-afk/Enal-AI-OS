# Network Engineer Capability Specification

## Version: 2.0.0
## Status: Draft (v2.0 expanding to network consultant)

---

## 1. Purpose

Deliver vendor-agnostic network intelligence untuk:
- Configuration parsing & validation
- Security compliance auditing
- Risk analysis & recommendations
- Configuration generation & simulation
- Design review (topology-level analysis and scoring)
- Troubleshooting (structured evidence → hypothesis → root cause)
- Migration planning (cross-vendor with risk, rollback, downtime)
- Network advisory (high-level design questions with explainable designs)

---

## 2. Scope

### In Scope
- Vendor support: MikroTik RouterOS, Cisco IOS, Fortinet, Juniper (planned)
- File format: .rsc, .conf, .txt
- Analysis types: Security, Best Practice, Compliance, Design Review, Troubleshooting
- Output: Findings, Risk Score, Recommendations, Documentation, Migration Plans, Design Proposals

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
  "type": "text|topology|symptom|query",
  "content": "string (raw config, topology JSON, symptom description, or design question)",
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
  "risk_score": "float 0-1",
  "design_review": {
    "network_score": "float 0-100",
    "availability_grade": "A|B+|B|C|D|F",
    "security_grade": "A|B+|B|C|D|F",
    "scalability_grade": "A|B+|B|C|D|F",
    "performance_grade": "A|B+|B|C|D|F",
    "issues": []
  },
  "troubleshooting": {
    "session_id": "string",
    "hypotheses": [],
    "root_cause": {}
  },
  "migration_plan": {
    "source_vendor": "string",
    "target_vendor": "string",
    "phases": [],
    "estimated_downtime_minutes": "int"
  },
  "advisory": {
    "proposals": []
  }
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

### Design Review Rules
| Rule ID | Category | Description |
|---------|----------|-------------|
| DR-001 | Availability | Single Point of Failure detected |
| DR-002 | Performance | Potential bandwidth bottleneck |
| DR-003 | Security | Management interface exposure |
| DR-004 | Scalability | Flat segment with too many devices |
| DR-005 | Performance | High latency links |
| DR-006 | Security | VLAN leak / overly broad VLAN |

### Troubleshooting Patterns
| Pattern ID | Symptom | Hypotheses |
|------------|---------|------------|
| TSH-001 | Ping timeout | Downstream unreachable, routing blackhole, firewall block |
| TSH-002 | Intermittent connectivity | Interface flapping, routing instability |
| TSH-003 | Slow network | Bandwidth saturation, DNS latency |

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
- Design review requires manual topology input for multi-device scenarios
- Migration planner estimates are heuristic-based
- Troubleshooting engine requires structured evidence input

---

## 8. Network Engineer 2.0 Roadmap

### N1 — Deep Network Knowledge
- Expanded ontology: TCP/IP, Routing, Switching, MPLS, BGP, OSPF, IS-IS, VXLAN, EVPN, SD-WAN, WiFi, IPv6, DNS, DHCP, QoS, Multicast, NAT, Firewall, Zero Trust
- Concept-level explanations with RFC references
- Cross-vendor concept mapping

### N2 — Design Review
- Topology-level analysis for SPOF, bottleneck, routing loop, asymmetric routing, VLAN leak, security gap, scalability
- Graded scoring: Network Score (0-100), Availability, Security, Scalability, Performance

### N3 — Troubleshooting Engine
- Structured workflow: symptom → collect evidence → hypothesis → counter hypothesis → verification → root cause
- Pattern matching for common network symptoms
- Confidence-weighted hypothesis ranking

### N4 — Migration Planner
- Cross-vendor migration plans with phased execution
- Risk assessment, rollback steps, downtime estimation, validation checkpoints
- Vendor alignment mapping (Cisco ↔ MikroTik ↔ Fortinet)

### N5 — Network Advisor
- Natural language design queries: "500 branches", "HA datacenter", "Zero Trust", "SD-WAN"
- Explainable design proposals with architecture summary, components, recommendations, and risks

---

## 9. Dataset Coverage Target

| Milestone | Cases | Vendors Covered | Domains Covered |
|-----------|-------|-----------------|-----------------|
| 5A.1 | 25 | MikroTik: 10, Cisco: 10, Fortinet: 5 | Security: 15, Best Practice: 10 |
| 5A.2 | 50 | Balanced distribution | Security: 25, HA: 10, QoS: 5, Wireless: 5, Monitoring: 5 |
| 5A.3 | 100 | All 3 vendors × 25+ cases | Full coverage |

---

## 10. Evaluation Metrics

### Golden Tests
- ✅ Must pass 100% before merge
- Test cases stored in `benchmarks/golden/`

### Real Cases
- Benchmark pass rate minimum 95%
- Evaluated via `make benchmark-network`

### Performance
- Execution time logged via telemetry
- Alert if >2s average
