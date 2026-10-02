# ADR-010: Finance Analyst Capability Pack

| Field | Value |
|-------|-------|
| **ADR ID** | ADR-010 |
| **Status** | Proposed |
| **Date** | 2026-10-02 |
| **Decision Maker** | Pending Platform Architecture Board review |
| **Related RFC** | RFC-0030 |

## Context

Finance Analyst is proposed as a conditional vertical pack. Its calculations
must be reproducible, its source data sensitive, and its results must not be
presented as investment or audit advice.

## Decision

Propose that, if project demand is confirmed:

1. The pack resides in `apps/finance_analyst/` and owns its financial domain
   engine, schemas, and tools.
2. All Core services are accessed through `backend.app.runtime`; direct Core
   internal imports and cross-pack imports are prohibited.
3. Arithmetic is deterministic and input-driven; generated explanations do
   not replace calculation or evidence.
4. External data access is separately approved, permission-scoped, provenance
   preserving, and read-only by default.
5. Activation requires domain review, ten benchmark scenarios, golden tests,
   and governance checks.

## Consequences

- No runtime behavior is approved by this proposal.
- Financial conclusions remain advisory and require human review.
- Missing, ambiguous, or stale data must be surfaced rather than silently
  defaulted.
- The RFC, benchmark matrix, and golden suite remain drafts until approval.

## Cross-Capability Proof

No cross-pack dependency is proposed. Any future integration must use approved
runtime contracts and demonstrate a project need without violating the
Capability First Rule.
