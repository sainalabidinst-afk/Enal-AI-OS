# ADR-012: HSE Specialist Capability Pack

| Field | Value |
|-------|-------|
| **ADR ID** | ADR-012 |
| **Status** | Proposed |
| **Date** | 2026-10-02 |
| **Decision Maker** | Pending Platform Architecture Board review |
| **Related RFC** | RFC-0032 |

## Context

HSE Specialist is proposed as a conditional pack for safety and environmental
analysis. Incorrect or overconfident outputs could affect people, operations,
or the environment; matrices, requirements, and escalation paths are
project-specific.

## Decision

Propose that, if project demand is confirmed:

1. The pack resides in `apps/hse_specialist/` and owns its domain engine,
   schemas, and tools.
2. All Core services are accessed through `backend.app.runtime`; direct Core
   internal imports and cross-pack imports are prohibited.
3. Risk ratings use an explicit, approved matrix and validated evidence;
   missing values remain unknown.
4. Site-control and sensor integrations are excluded by default and require an
   independent safety case and explicit authorization.
5. Activation requires qualified HSE review, ten benchmark scenarios, golden
   tests, and governance checks.

## Consequences

- No runtime behavior or operational control is approved by this proposal.
- Outputs are advisory and cannot certify a site safe or replace emergency
  procedures or competent personnel.
- Incident data must be authorized, minimized, de-identified where feasible,
  and provenance-preserving.
- Draft scenarios and scores are not a safety certification.

## Cross-Capability Proof

No cross-pack dependency is proposed. Any future integration must use approved
runtime contracts, include safety and privacy review, and preserve the
Capability First Rule.
