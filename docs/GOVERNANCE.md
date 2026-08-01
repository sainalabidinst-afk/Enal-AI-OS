# ECP Governance — Operational Rules

**Version:** 1.0.0
**Status:** Ratified
**Effective:** 2026-08-01
**Authority:** Chief Architect
**Parent:** `GOVERNANCE_CHARTER.md`
**Purpose:** Operational rules that all RFCs, ADRs, Capability Packs, and releases must satisfy.

---

## 1. Capability First Rule

> **No Core change is allowed to improve a single Capability Pack.**

- If one Capability Pack needs a different behavior, the change must stay inside that Capability Pack.
- If 2 or more Capability Packs need the same behavior, an ADR may be submitted with proof from both packs.
- Core changes require ADR approval and cross-capability proof.

---

## 2. No New Engines Without Use Case

Any new engine, module, or abstraction must:

1. Be required by at least two Capability Packs.
2. Have a golden test case.
3. Be documented in architecture docs.

If no Capability Pack improves, no benchmark increases, and no journey becomes better — **do not build**.

---

## 3. Architecture Freeze Policy

> **Core may only change if all of the following are satisfied:**

| # | Condition | Evidence |
|---|-----------|----------|
| 1 | Used by at least two Capability Packs | Cross-capability proof document |
| 2 | Has an approved ADR | ADR in `docs/adr/` + entry in `ARCHITECTURE_DECISIONS.md` |
| 3 | Passes benchmark | Benchmark result persisted in `benchmarks/` |
| 4 | Passes regression tests | Full test suite green (CI/CD) |

**Process for a Core change:**

1. Identify the Core change needed.
2. Document which Capability Packs require it.
3. If fewer than 2 packs require it → the change belongs in the Capability Pack, not Core.
4. If 2+ packs require it → submit an RFC with test cases from both packs.
5. RFC accepted → submit ADR with impact analysis.
6. ADR approved → implement with benchmark + regression proof.
7. Merge only after all four Architecture Freeze conditions pass.

**Explicitly forbidden without the above process:**

- Adding a new Runtime, Planner, Kernel, or architectural Layer.
- Modifying Core to improve a single Capability Pack.
- Breaking Core contracts without a 2-release grace period and migration guide.

---

## 4. Kernel Stability

The kernel (`backend/app/core/`) must:

- Remain under 5,000 lines of code.
- Have zero external dependencies beyond stdlib + pydantic.
- Maintain backward-compatible contracts.
- Pass all tests on every commit.

---

## 5. Capability Pack Independence

Capability Packs must **not** import other Capability Pack engines directly.

All cross-pack communication flows through **Execution Runtime and shared contracts only**.

**Forbidden:**

```python
# FORBIDDEN
from apps.trading_analyst import engine as trading_engine
trading_engine.analyze(...)
```

**Allowed:**

```python
# ALLOWED
task = {
    "domain": "research",
    "intent": "Analyze market sentiment for AAPL",
}
result = await execution_runtime.execute(task)
```

---

## 6. Architecture Decision Records (ADR)

- All significant architecture decisions require an ADR.
- ADRs live in `docs/adr/` and are aggregated in `ARCHITECTURE_DECISIONS.md`.
- Changes to frozen ADRs require:
  - RFC process with extended review period
  - Migration plan for all affected components
  - Approval by project architecture authority

### What Requires an ADR

- Adding a new Runtime
- Adding a new Planner
- Adding a new Kernel
- Adding a new architectural Layer
- Modifying Core for any reason

All require: cross-capability proof (≥2 packs), RFC with impact analysis, and architecture authority approval.

---

## 7. CI/CD Enforcement of Governance

CI/CD must block merges that violate governance:

| Check | Fails When |
|-------|------------|
| Architecture Test | Package boundary violated (pack imports pack engine directly) |
| Core Change Guard | Core modified without a referenced approved ADR |
| ADR Reference Check | Change impacting multiple packs lacks ADR |
| Benchmark Gate | Benchmark score below pack threshold |
| Golden Tests | Golden test suite below pass threshold |

**Merge Policy:** All checks must pass. No exceptions.

---

## 8. Capability Changelog

Each Capability Pack maintains its own changelog. The changelog records knowledge additions, benchmark improvements, and reasoning enhancements. It does **not** record Core changes.

### Format

```markdown
## <Capability Pack> v<version>

### Added
- <knowledge/topic>

### Improved
- <aspect>

### Fixed
- <issue>

### Benchmark
- <dimension>: <before> → <after>
```

### Example

```markdown
## Network v1.1

### Added
- BGP path selection analysis
- MPLS forwarding rules
- IPv6 dual-stack patterns

### Improved
- Firewall explanation depth
- Risk scoring accuracy: 85% → 92%

### Fixed
- VLAN false positive on trunk interfaces

### Benchmark
- Accuracy: 89% → 92%
- Explainability: B → A-
```

---

## 9. Exception Handling

Any exception to the rules in this document must be proposed as an RFC, reviewed, and approved by the architecture authority. Exceptions are recorded in the ADR log and this document is updated accordingly.

---

## 10. Approval

| Role | Status | Date |
|------|--------|------|
| Chief Architect | Approved | 2026-08-01 |

