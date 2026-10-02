# ADR-014: Cybersecurity Analyst Capability Pack

| Field | Value |
|-------|-------|
| **ADR ID** | ADR-014 |
| **Status** | Proposed |
| **Date** | 2026-10-02 |
| **Decision Maker** | Pending Platform Architecture Board review |
| **Related RFC** | RFC-0034 |
| **Target Version** | ECP v2.4.0 |

## Context

Cybersecurity Analyst is proposed as a conditional pack providing threat modeling,
vulnerability assessment, incident detection, and compliance mapping. Incorrect or
overconfident outputs could affect security posture; threat models, vulnerability
classifications, and incident analyses are inherently based on supplied inputs and
must remain advisory. Matrices, thresholds, and baselines are project-specific.

## Decision

Propose that, if project demand is confirmed:

1. The pack resides in `apps/cybersecurity_analyst/` and owns its domain engine,
   schemas, and tools.
2. All Core services are accessed through `backend.app.runtime`; direct Core
   internal imports and cross-pack imports are prohibited.
3. Threat models, vulnerability assessments, and incident detections are
   deterministic and input-driven; missing values remain unknown.
4. All outputs are advisory: `incident_detection_claim = false`,
   `root_cause_attribution = false`, and `compliance_certification_claim = false`.
5. Activation requires cybersecurity domain review, ten benchmark scenarios,
   golden tests, and governance checks.

## Consequences

- No runtime behavior, operational control, or security certification is approved
  by this proposal.
- Outputs are advisory and cannot certify a system secure or replace incident
  response.
- Threat model inputs, vulnerability records, alert data, and compliance evidence
  must be authorized, minimized, de-identified where feasible, and provenance-
  preserving.
- Draft scenarios and scores are not benchmark results.

## Cross-Capability Proof

No cross-pack dependency is proposed. Any future integration must use approved
runtime contracts, include platform and data-handling review, and preserve the
Capability First Rule.
