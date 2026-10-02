# RFC-0032: HSE Specialist Capability Pack

| Field | Value |
|-------|-------|
| **RFC ID** | RFC-0032 |
| **Status** | Draft |
| **Version** | 0.1.0 |
| **Capability Pack** | HSE Specialist |
| **Capability ID** | `hse-specialist` |
| **Category** | Health, Safety, Environment |
| **Related ADR** | ADR-012 |

## Summary

Add an optional HSE Specialist pack to structure hazard identification, risk
assessment, incident learning, and environmental compliance evidence. It is
conditional and does not replace qualified safety professionals, site
procedures, or emergency response.

## Motivation

Industrial projects need consistent, traceable safety and environmental
reviews. A bounded pack can organize supplied evidence and simulate scenarios
to support, not substitute for, competent human decisions.

## Scope

- Identify hazards from supplied task, site, and process descriptions.
- Produce a risk register using a project-approved likelihood/severity matrix.
- Compare proposed controls with a configurable hierarchy-of-controls checklist.
- Analyze incident narratives for contributing factors and corrective actions.
- Map supplied evidence to versioned HSE requirements and report gaps.

Out of scope: autonomous permit-to-work approval, declaring a site safe,
emergency response instructions, exposure-limit determinations without
validated inputs, and certification or compliance claims.

## Detailed Design

### Engine

`HSESpecialistEngine` should expose `hazard_analysis`, `risk_register`,
`control_review`, `incident_analysis`, and `compliance_gap_check`. Every risk
rating must identify the configured matrix and underlying assumptions. Incident
analysis should focus on system factors and evidence, not blame. Unknown or
contradictory site conditions require an explicit escalation.

### Tools and contracts

- `HazardTaxonomy`: maps hazards to a project-approved, versioned taxonomy.
- `RiskMatrix`: computes ratings from validated likelihood and severity scales;
  it must not invent missing values.
- `ControlHierarchyReviewer`: identifies proposed controls by elimination,
  substitution, engineering, administrative, and PPE categories.
- `IncidentFactorAnalyzer`: organizes evidence, timeline, contributing factors,
  and corrective-action candidates with source links.
- `HSERequirementMapper`: evaluates supplied evidence against configured
  jurisdiction- and date-specific requirements.
- All integrations are read-only by default. Site sensors or operational
  controls require separate review, authorization, and safety case.

### Governance and boundaries

- Future pack code imports Core services only from `backend.app.runtime`, never
  `backend.app.core` internals.
- No direct imports from other capability packs; cross-pack work uses approved
  runtime contracts.
- Before activation, add standard registration and boundary checks,
  `apps/hse_specialist/`, benchmark/golden assets, and authorized,
  de-identified `real_cases/` examples.
- Review `docs/GOVERNANCE_CHARTER.md`, `docs/GOVERNANCE.md`, package boundaries,
  operational safety, privacy, and environmental data policies before merge.

### Benchmark and golden baseline

Ten draft baseline scenarios are listed in
`benchmarks/vertical_industry_scenarios.json` and detailed in
`golden_tests/hse_specialist/golden_test_suite.json`. These specifications are
not measured scores or safety certification. A runnable benchmark requires
domain-owner review and an approved implementation.

## Alternatives Considered

1. Generic risk scoring — rejected because matrices and acceptance thresholds
   are site- and project-specific.
2. Automated operational control — rejected because an incorrect action can
   create immediate physical harm.
3. Train on unreviewed incident data — rejected because reports may be
   sensitive, biased, or unsuitable as normative ground truth.

## Compatibility

This is a draft only; no engine, tools, registration, or runtime contracts are
added. Future implementation must be opt-in and versioned.

## Security and Safety Considerations

Treat site and incident records as sensitive. Restrict access, minimize
retention, redact personal information, and preserve provenance. Surface
uncertainty and escalate imminent hazards to established site procedures and
qualified personnel; the pack must never represent generated output as a
substitute for emergency response or competent safety approval.

## Testing Strategy

- Validate the ten scenario references and suite structure.
- On implementation, test missing/contradictory conditions, matrix boundaries,
  escalation behavior, source traceability, and reproducibility.
- Have a qualified HSE owner review the taxonomy, matrix, scenarios, and any
  thresholds before CI certification.

## Governance Checklist

- [ ] Confirm project demand, operating context, jurisdiction, and HSE owner.
- [ ] Review this RFC and ADR-012 through the documented process.
- [ ] Approve hazard taxonomy, risk matrix, data sources, and escalation policy.
- [ ] Verify Runtime-facade-only Core access and package boundaries.
- [ ] Review all scenarios with qualified HSE professionals before certification.
- [ ] Keep the pack advisory; do not connect control systems without a separate
  safety case and explicit authorization.

## Timeline

Draft and benchmark specification only. Implementation is conditional on
project demand and completion of the governance checklist.

## References

- [Governance Charter](../GOVERNANCE_CHARTER.md)
- [Governance](../GOVERNANCE.md)
- [RFC process](README.md)
- [ADR-012](../adr/ADR-012-hse-specialist.md)
