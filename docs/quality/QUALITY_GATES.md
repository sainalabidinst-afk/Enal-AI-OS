# Quality Gate Policy — Enal Cognitive Platform

**Status:** 🟢 **Active**  
**Applies to:** All pull requests targeting `main` or `release/*` branches  
**Enforcement:** CI/CD pipeline (see `scripts/gate0_validate.py`)

---

## Purpose

This document defines the **minimum objective standards** that every change must meet before being merged into the production codebase. These gates are non-negotiable and enforced by CI/CD.

The goal is not to prevent change, but to ensure every change maintains or improves the engineering baseline.

---

## Gate Table

| # | Gate | Requirement | Severity | Enforcement |
|---|------|-------------|----------|-------------|
| 1 | **MyPy** | `0 errors` on `apps/ backend/ benchmarks/ tests/ sdk/` | 🔴 BLOCKER | `mypy apps/ backend/ benchmarks/ tests/` |
| 2 | **Ruff Lint** | `0 blockers`. Warnings must be justified in PR description | 🟡 WARNING | `ruff check apps/ backend/` |
| 3 | **Ruff Format** | `0 files would be reformatted` | 🟡 WARNING | `ruff format --check apps/ backend/` |
| 4 | **Tests** | `≥95% pass rate` (baseline: 426 passing) | 🔴 BLOCKER | `pytest --tb=short -q` |
| 5 | **Test Stability** | Flaky tests = blocker. `--reruns 3` must not hide failures | 🔴 BLOCKER | `pytest --reruns 3 -q` |
| 6 | **API Contract** | All public API signatures must be backward compatible | 🔴 BLOCKER | Manual review + type checker |
| 7 | **ADR** | Architecture changes require approved ADR before implementation | 🔴 BLOCKER | Manual review |
| 8 | **No Circular Imports** | `0` new circular imports introduced | 🟡 WARNING | `ruff check --select RUF011` |
| 9 | **No Mutable Defaults** | `0` new RUF012 violations | 🟡 WARNING | `ruff check --select RUF012` |
| 10 | **No Blind Exceptions** | New `except Exception:` requires explicit justification | 🟡 WARNING | Manual review + `ruff check --select BLE001` |
| 11 | **Python 3.11 Compat** | No f-string backslash escapes in production code | 🔴 BLOCKER | `compile()` scan (see `tools/audit/`) |
| 12 | **Type Safety** | No `type: ignore` comments without documented reason | 🟡 WARNING | Manual review |

---

## Gate Details

### Gate 1 — MyPy (🔴 BLOCKER)

```bash
python -m mypy apps/ backend/ benchmarks/ tests/
```

Zero errors required. `type: ignore` is permitted only with an inline comment explaining why:

```python
# type: ignore[attr-defined] — Vendor model does not expose this field
```

### Gate 2 — Ruff Lint (🟡 WARNING)

```bash
python -m ruff check apps/ backend/
```

If warnings exist, each must be justified in the PR description. Example justification:

> "BLE001 at line 142 is intentional: this is a top-level handler that must catch all exceptions to prevent crash."

### Gate 4 — Tests (🔴 BLOCKER)

```bash
python -m pytest --tb=short -q --coverage
```

Requirements:
- ≥95% of baseline tests must pass (baseline: 426)
- New code must include corresponding tests
- Test coverage must not decrease below 80% (overall)

### Gate 7 — ADR (🔴 BLOCKER)

Architecture changes include:
- Adding new core modules
- Changing event bus interface
- Modifying capability pack contract
- Replacing infrastructure components (database, cache, etc.)
- Changing runtime execution model

These require:
1. ADR filed in `docs/adr/` before implementation begins
2. At least one decider review (Chief Architect, Senior Engineer)
3. ADR status: ✅ Accepted

---

## Exception Process

Any gate may be overridden via **Exception Request**:

1. File an issue with label `quality-gate-override`
2. Include:
   - Gate violated
   - Reason for override
   - Mitigation plan
   - Expiration date (if temporary)
3. Requires approval from 2 deciders

**No exception** is permanent. All exceptions must have a path to compliance.

---

## Escalation

If a gate blocks a critical fix:

1. **First:** Fix the issue (preferred)
2. **Second:** File Exception Request (temporary)
3. **Third:** Escalate to Chief Architect

Production-critical hotfixes may bypass gates only with explicit approval from 2 deciders AND must be retroactively fixed within 24 hours.

---

## Enforcement in CI/CD

See `scripts/gate0_validate.py` for CI/CD implementation.

Current script validates:
- MyPy: 0 errors
- Ruff: scan
- Test collection

The full gate table should be implemented in CI/CD as the next engineering priority after baseline freeze.

---

## Relationship to Engineering Baseline

This document extends the Engineering Baseline (`docs/ENGINEERING_BASELINE.md`).

The baseline defines the **state** of the codebase at freeze time.
The quality gates define the **process** to maintain that state going forward.

Both are required for engineering governance.

