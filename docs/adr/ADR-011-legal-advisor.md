# ADR-011: Legal Advisor Capability Pack

| Field | Value |
|-------|-------|
| **ADR ID** | ADR-011 |
| **Status** | Proposed |
| **Date** | 2026-10-02 |
| **Decision Maker** | Pending Platform Architecture Board review |
| **Related RFC** | RFC-0031 |

## Context

Legal Advisor is proposed as a conditional pack. Legal analysis depends on
jurisdiction, effective dates, approved sources, and qualified legal judgment.
Document inputs may also be privileged or confidential.

## Decision

Propose that, if project demand is confirmed:

1. The pack resides in `apps/legal_advisor/` and owns its legal-domain engine,
   schemas, and tools.
2. All Core services are accessed through `backend.app.runtime`; direct Core
   internal imports and cross-pack imports are prohibited.
3. Rules and playbooks are project-approved, versioned data, not hard-coded
   universal legal conclusions.
4. Source and clause references, jurisdiction, effective date, uncertainty, and
   human-review status are retained in outputs.
5. Activation requires qualified legal review, ten benchmark scenarios, golden
   tests, and governance checks.

## Consequences

- No runtime behavior is approved by this proposal.
- Output is assistive only and cannot represent legal advice or approval.
- Access, retention, redaction, and source licensing require project-specific
  approval.
- Draft scenarios cannot be treated as authoritative statements of law.

## Cross-Capability Proof

No cross-pack dependency is proposed. Future integrations must use approved
runtime contracts, be reviewed for confidentiality, and preserve the
Capability First Rule.
