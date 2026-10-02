# RFC-0034: Cybersecurity Analyst Capability Pack

| Field | Value |
|-------|-------|
| **RFC ID** | RFC-0034 |
| **Status** | Draft |
| **Version** | 0.1.0 |
| **Capability Pack** | Cybersecurity Analyst |
| **Capability ID** | `cybersecurity-analyst` |
| **Category** | Security |
| **Target Version** | ECP v2.4.0 |
| **Related ADR** | ADR-014 |
| **Target Quality** | A (≥90) |

## Summary

Add a Cybersecurity Analyst pack that provides threat modeling (STRIDE),
vulnerability assessment (CVSS-based), incident detection (baseline deviation),
and compliance mapping (requirement-coverage analysis). The pack is advisory and
opt-in: it does not certify systems secure, does not execute operational control,
and does not replace incident response procedures.

## Motivation

Security is a cross-cutting concern for every deployment, yet many teams lack a
repeatable, traceable way to:

1. **Threat Modeling** — systematically enumerate STRIDE threats against a system
   description, assets, and trust boundaries.
2. **Vulnerability Assessment** — classify and prioritize findings using CVSS
   scores and produce remediation guidance.
3. **Incident Detection** — detect anomalies by comparing current activity to a
   baseline and triage alert severity.
4. **Compliance Mapping** — map evidence to requirements and report coverage for
   frameworks such as ISO 27001, SOC 2, and NIST CSF.

The Cybersecurity Analyst pack provides a bounded, deterministic analysis layer
with explicit assumptions, source provenance, and documented limitations.

## Scope

- Normalize supplied threat-model inputs, vulnerability records, alert/event data,
  and compliance evidence.
- Generate STRIDE threat findings with mitigations per identified category.
- Classify vulnerabilities by CVSS score into critical / high / medium / low.
- Detect incident anomalies from baseline deviation and alert severity.
- Map evidence to compliance requirements and compute coverage percentages.
- Produce traceable summaries with formulae, input lineage, and limitations.

Out of scope: live penetration testing, automated remediation or operational
control, root-cause attribution, compliance certification claims, and claims of
system security. The pack must not fabricate findings or silently default missing
inputs.

## Detailed Design

### Engine

`CybersecurityAnalystEngine` is a deterministic orchestration layer that delegates
to `CybersecurityAnalysisEngine` for:

- `threat_model` — STRIDE analysis over system description, assets, and trust
  boundaries.
- `vulnerability_assess` — CVSS-based severity classification.
- `incident_detect` — anomaly detection via baseline deviation and alert analysis.
- `compliance_map` — evidence-to-requirement mapping with coverage percentage.

All calculations use explicit inputs and declared formulae; LLM output may explain
results but must not be the source of arithmetic. Outputs expose formulae, input
lineage, and limitations.

### Tools and contracts

- `ThreatModeler`: enumerates STRIDE threats from a system description, assets,
  data flows, and trust boundaries; produces findings with mitigations.
- `VulnerabilityAssessor`: classifies vulnerabilities by CVSS score, aggregates
  severity counts, and surfaces remediation guidance.
- `IncidentDetector`: compares current event counts to a baseline, flags anomalies
  above a configurable threshold, and analyzes alert severity.
- `ComplianceMapper`: maps evidence to framework requirements, reports gaps, and
  computes coverage percentage.
- Define request/response schemas in the pack; tool calls must be allowlisted and
  auditable and read-only by default. External connectors require separate project
  approval and provenance metadata.

### Governance and boundaries

- Any future pack code imports permitted Core services only through
  `backend.app.runtime`; no imports from `backend.app.core` internals.
- No direct imports from other capability packs. Cross-pack work uses approved
  runtime contracts.
- Before activation, add the pack to the standard registration and boundary checks,
  provide an `apps/cybersecurity_analyst/` package, benchmark/golden assets, and a
  `real_cases/cybersecurity_analyst/` directory with approved examples.
- Review `docs/GOVERNANCE_CHARTER.md`, `docs/GOVERNANCE.md`, package boundaries,
  capability-first rules, data handling, and the relevant ADR before merging.
- Threat models, vulnerability assessments, and incident detections are advisory;
  they cannot certify a system secure or trigger operational control without a
  separate safety case and explicit authorization.

### Benchmark and golden baseline

`benchmarks/cybersecurity_analyst_benchmark.py` defines ten baseline scenarios
across six dimensions. The executable-shaped golden suite is
`golden_tests/cybersecurity_analyst/golden_test_suite.json`; each benchmark
scenario maps one-to-one to a golden test. These are acceptance specifications,
not measured results. A runnable benchmark and CI gate require domain-owner review
and an approved implementation.

## Alternatives Considered

1. Reuse the Security Engineer pack for all cybersecurity tasks — rejected because
   it conflates security hardening with structured threat modeling and compliance
   mapping ownership.
2. Automated remediation on incident detection — rejected because automated
   operational control requires a separate safety case and can worsen incidents.
3. Use an LLM for all analysis — rejected because security outputs require
   reproducible logic and auditable assumptions.

## Compatibility

This is a proposal and adds no runtime behavior or public API. Existing packs
remain unaffected. Future schemas must be versioned and opt-in under
`apps/cybersecurity_analyst/`.

## Security and Safety Considerations

Treat threat models, vulnerability records, and compliance evidence as sensitive.
Minimize retention, redact identifiers in logs, validate external inputs, and keep
data sources read-only unless separately authorized. Clearly distinguish analysis
results, mitigations, and assumptions; require human review for consequential
decisions.

## Testing Strategy

- Validate all ten scenario-to-golden-test references and suite structure.
- On implementation, add deterministic unit tests for STRIDE analysis, vulnerability
  classification, anomaly detection, compliance mapping, invalid and missing
  inputs, reproducibility, provenance, and advisory-only behavior.
- Require domain-owner review of scenario data and thresholds before CI
  certification. Do not present draft scores as benchmark results.

## Governance Checklist

- [ ] Confirm project demand and a cybersecurity domain owner.
- [ ] Review this RFC and ADR-014 through the documented RFC/ADR process.
- [ ] Verify Runtime-facade-only Core access and package boundaries.
- [ ] Approve data sources, retention, jurisdiction, and human-review policy.
- [ ] Implement at least ten reviewed scenarios and a runnable golden-test gate.
- [ ] Add real cases only with documented provenance and authorization.

## Timeline

Draft and benchmark specification only. Implementation is conditional on project
demand and completion of the governance checklist.

## References

- [Governance Charter](../GOVERNANCE_CHARTER.md)
- [Governance](../GOVERNANCE.md)
- [RFC process](README.md)
- [ADR-014](../adr/ADR-014-cybersecurity-analyst.md)
