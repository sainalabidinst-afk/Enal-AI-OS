# Domain Expert vs Certification Status

## Implementation Maturity vs Certification

ENAL AI OS uses two distinct status systems that are often confused. Understanding the difference is important for governance and communication.

## Domain Expert (Implementation Maturity)

**Definition:** A capability that has completed implementation according to ENAL AI OS development standards.

**Criteria:**
- Core engine implemented
- Domain knowledge encoded
- Basic tests exist
- Documentation written
- Integrated with platform contracts

**Status Levels:**
| Level | Description |
|-------|-------------|
| Concept | Idea stage, no implementation |
| Prototype | Proof of concept, not integrated |
| Development | Active development, incomplete |
| Domain Expert | Implementation complete, integrated with platform |
| Certified | Passed formal certification audit |

**Key Point:** "Domain Expert" means the capability **has been built**, not that it has been **validated**.

## Certification Status (Quality Validation)

**Definition:** A capability that has passed formal audit, benchmark, golden test, real case validation, and production readiness review.

**Criteria:**
- Phase 1.1 — Capability Audit: ≥80% score, no critical findings
- Phase 1.2 — Benchmark Audit: Meets performance targets
- Phase 1.3 — Golden Tests: All categories passing
- Phase 1.4 — Real Cases: Real-world scenarios validated
- Phase 1.5 — Production Readiness: Cross-cutting checks passed
- Phase 1.6 — Certification Review: Final approval

**Certification Levels:**
| Level | Description |
|-------|-------------|
| Experimental | Not certified, major rework required |
| Provisional | Conditional certification, re-audit required |
| Certified | Full certification, meets all standards |
| Deprecated | Certification revoked or expired |

**Key Point:** "Certified" means the capability has been **independently validated** against objective criteria.

## Relationship

```
Implementation
    │
    ▼
Domain Expert ──────┐
                    │
                    ▼
              Certification
                    │
                    ▼
               Certified
```

A capability can be:
1. **Domain Expert but not Certified** — Built but not yet audited (most common)
2. **Domain Expert and Certified** — Built and validated (target state)
3. **Not Domain Expert and not Certified** — In development

## Current State

As of Sprint 11:
- **22 capabilities** are at Domain Expert level (implementation complete)
- **0 capabilities** are Certified (formal validation pending)
- **22 capabilities** are Provisional (audit score 73-77%, corrective actions in progress)

## Why This Matters

- **Development teams** should target Domain Expert as the implementation milestone
- **Governance teams** should target Certification as the quality milestone
- **Users** should understand that Domain Expert means "available" while Certified means "validated"

Mixing these two statuses creates confusion about capability readiness. Keeping them separate ensures that:
1. Development progress is tracked independently from quality validation
2. Certification has clear, objective criteria
3. Stakeholders have accurate information about capability maturity
