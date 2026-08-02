<!-- BILINGUAL_DOCS_START -->
## Bahasa Indonesia / English

### Ringkasan / Summary
Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.
> Terjemahan Indonesia: Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.

- Bahasa Indonesia: konten utama tetap dipertahankan dalam dokumen asli, dan bagian ini memberi konteks ringkas dalam bahasa Indonesia.
- English: the main content remains in the original document, and this section provides a concise bilingual context for international readers.

### Informasi Dokumen / Document Info
- File: `docs/quality/QUALITY_GATES.md`
- Judul: Quality Gates
- Status: bilingual header added

<!-- BILINGUAL_DOCS_END -->

# Quality Gate Policy â€” Enal Cognitive Platform

<!-- DOCUMENT_METADATA_START -->
**Owner:** Documentation Team
**Canonical Owner:** Documentation Governance Lead
**Last Verified:** 2026-08-02
**Version:** 1.0.0
**Status:** Active
**SSOT:** Quality documentation for QUALITY_GATES
<!-- DOCUMENT_METADATA_END -->

**Status:** ðŸŸ¢ **Active**  
**Applies to:** All pull requests targeting `main` or `release/*` branches  
**Enforcement:** CI/CD pipeline (see `scripts/gate0_validate.py`)

---

## Purpose

This document defines the **minimum objective standards** that every change must meet before being merged into the production codebase. These gates are non-negotiable and enforced by CI/CD.
> Terjemahan Indonesia: Ini dokumen defines minimum objective standards itu every change must meet before being merged into production codebase. These gates adalah non-negotiable dan enforced oleh CI/CD.

The goal is not to prevent change, but to ensure every change maintains or improves the engineering baseline.
> Terjemahan Indonesia: Goal adalah not untuk prevent change, but untuk ensure every change maintains or improves rekayasa dasar.

---

## Gate Table

| # | Gate | Requirement | Severity | Enforcement |
|---|------|-------------|----------|-------------|
| 1 | **MyPy** | `0 errors` on `apps/ backend/ benchmarks/ tests/ sdk/` | ðŸ”´ BLOCKER | `mypy apps/ backend/ benchmarks/ tests/` |
| 2 | **Ruff Lint** | `0 blockers`. Warnings must be justified in PR description | ðŸŸ¡ WARNING | `ruff check apps/ backend/` |
| 3 | **Ruff Format** | `0 files would be reformatted` | ðŸŸ¡ WARNING | `ruff format --check apps/ backend/` |
| 4 | **Tests** | `â‰¥95% pass rate` (baseline: 426 passing) | ðŸ”´ BLOCKER | `pytest --tb=short -q` |
| 5 | **Test Stability** | Flaky tests = blocker. `--reruns 3` must not hide failures | ðŸ”´ BLOCKER | `pytest --reruns 3 -q` |
| 6 | **API Contract** | All public API signatures must be backward compatible | ðŸ”´ BLOCKER | Manual review + type checker |
| 7 | **ADR** | Architecture changes require approved ADR before implementation | ðŸ”´ BLOCKER | Manual review |
| 8 | **No Circular Imports** | `0` new circular imports introduced | ðŸŸ¡ WARNING | `ruff check --select RUF011` |
| 9 | **No Mutable Defaults** | `0` new RUF012 violations | ðŸŸ¡ WARNING | `ruff check --select RUF012` |
| 10 | **No Blind Exceptions** | New `except Exception:` requires explicit justification | ðŸŸ¡ WARNING | Manual review + `ruff check --select BLE001` |
| 11 | **Python 3.11 Compat** | No f-string backslash escapes in production code | ðŸ”´ BLOCKER | `compile()` scan (see `tools/audit/`) |
| 12 | **Type Safety** | No `type: ignore` comments without documented reason | ðŸŸ¡ WARNING | Manual review |

---

## Gate Details

### Gate 1 â€” MyPy (ðŸ”´ BLOCKER)

```bash
python -m mypy apps/ backend/ benchmarks/ tests/
```

Zero errors required. `type: ignore` is permitted only with an inline comment explaining why:
> Terjemahan Indonesia: Zero errors required. type: ignore adalah permitted only dengan sebuah inline comment explaining why:

```python
# type: ignore[attr-defined] â€” Vendor model does not expose this field
```

### Gate 2 â€” Ruff Lint (ðŸŸ¡ WARNING)

```bash
python -m ruff check apps/ backend/
```

If warnings exist, each must be justified in the PR description. Example justification:
> Terjemahan Indonesia: If warnings exist, each must menjadi justified dalam PR description. Example justification:

> "BLE001 at line 142 is intentional: this is a top-level handler that must catch all exceptions to prevent crash."

### Gate 4 â€” Tests (ðŸ”´ BLOCKER)

```bash
python -m pytest --tb=short -q --coverage
```

Requirements:
> Terjemahan Indonesia: Persyaratan:
- â‰¥95% of baseline tests must pass (baseline: 426)
- New code must include corresponding tests
- Test coverage must not decrease below 80% (overall)

### Gate 7 â€” ADR (ðŸ”´ BLOCKER)

Architecture changes include:
> Terjemahan Indonesia: Arsitektur changes include:
- Adding new core modules
- Changing event bus interface
- Modifying capability pack contract
- Replacing infrastructure components (database, cache, etc.)
- Changing runtime execution model

These require:
> Terjemahan Indonesia: Ini memerlukan:
1. ADR filed in `docs/adr/` before implementation begins
2. At least one decider review (Chief Architect, Senior Engineer)
3. ADR status: âœ… Accepted

---

## Exception Process

Any gate may be overridden via **Exception Request**:
> Terjemahan Indonesia: Any gate may menjadi overridden via Exception Request:

1. File an issue with label `quality-gate-override`
2. Include:
   - Gate violated
   - Reason for override
   - Mitigation plan
   - Expiration date (if temporary)
> Terjemahan Indonesia: Gate violated Reason untuk override Mitigation plan Expiration date (if temporary)
3. Requires approval from 2 deciders

**No exception** is permanent. All exceptions must have a path to compliance.

---

## Escalation

If a gate blocks a critical fix:
> Terjemahan Indonesia: If sebuah gate blocks sebuah critical fix:

1. **First:** Fix the issue (preferred)
2. **Second:** File Exception Request (temporary)
3. **Third:** Escalate to Chief Architect

Production-critical hotfixes may bypass gates only with explicit approval from 2 deciders AND must be retroactively fixed within 24 hours.
> Terjemahan Indonesia: Production-critical hotfixes may bypass gates only dengan explicit approval dari 2 deciders dan must menjadi retroactively fixed within 24 hours.

---

## Enforcement in CI/CD

See `scripts/gate0_validate.py` for CI/CD implementation.
> Terjemahan Indonesia: See scripts/gate0_validate.py untuk CI/CD implementation.

Current script validates:
> Terjemahan Indonesia: Skrip saat ini memvalidasi:
- MyPy: 0 errors
- Ruff: scan
- Test collection

The full gate table should be implemented in CI/CD as the next engineering priority after baseline freeze.
> Terjemahan Indonesia: Full gate table should menjadi implemented dalam CI/CD as next rekayasa priority after dasar freeze.

---

## Relationship to Engineering Baseline

This document extends the Engineering Baseline (`docs/ENGINEERING_BASELINE.md`).
> Terjemahan Indonesia: Ini dokumen extends rekayasa dasar (docs/ENGINEERING_BASELINE.MD).

The baseline defines the **state** of the codebase at freeze time.
The quality gates define the **process** to maintain that state going forward.
> Terjemahan Indonesia: Dasar defines state dari codebase at freeze time. kualitas gates define process untuk maintain itu state going forward.

Both are required for engineering governance.
> Terjemahan Indonesia: Both adalah required untuk rekayasa tata kelola.
