# Code Audit Report - Sprint 5A.4

## Audit Date: 2026-07-24

---

## STEP 1: Source Code Audit

### TODO/FIXME found
None found in attachments codebase.

### Dead code found
None found.

### Duplicate logic found
- `_text_contains_any` and `_find_evidence` exist in `compliance.py` and could be extracted to shared utility

### Unreachable code found
None found.

### Inconsistent error handling
- Fixed: `registry.py` - added logging to exception handlers (was bare except blocks)

### Silent exception
- Fixed: `registry.py` - now logs parser loading failures at debug level
- Fixed: `benchmark/runner.py` - now logs expected.json parse errors at warning level

### Resource leak
None found.

---

## STEP 2: Error Handling

### Bare except blocks
- All fixed - now have logging

### Exception with clear messages
All explicit exceptions have clear messages.

---

## STEP 3: Input Validation

### None dereference risks
- `analyzer.py:55` - `getattr(analysis.ast, "to_dict", None)` safe but could be cleaner
- All parser `can_parse` methods use `meta.vendor` comparison which is safe

### Index error risks
None found - all index access properly bounds-checked.

### Key error risks
- `compliance.py:131-134` - `ast.system` access assumes dict structure exists
- `compliance.py:144-147` - `ast.get("compliance_score")` safe via method

---

## STEP 4: Logging Review

### Missing logging in critical paths
- Now fixed in registry.py and benchmark/runner.py

---

## STEP 5: Performance Review

### Inefficient loops
- `compliance.py:_text_contains_any` - iterates over all AST sections each time called
- `reasoning.py` - iterates over findings multiple times for different breakdowns

### Object allocation
- `report.py` - creates many intermediate lists for markdown output

---

## STEP 6: Test Stabilization

Cannot execute tests due to environment limitations (no Python runtime).

---

## STEP 7: Documentation

No behavior changes required for documentation.

---

## Files Changed in Sprint 5A.4

| File | Change Type |
|------|-------------|
| `backend/app/core/attachments/parsers/registry.py` | Added logging to exception handlers |
| `backend/app/core/benchmark/runner.py` | Added logging to expected.json parse error |
| `backend/app/core/telemetry/__init__.py` | Created (was missing) |
| `backend/app/core/telemetry/service.py` | Created (was missing) |
| `backend/app/core/telemetry/aggregator.py` | Created (was missing) |

---

## Summary

| Metric | Value |
|--------|-------|
| Critical bugs found | 0 |
| Observability improvements | 2 locations |
| Files modified | 2 |
| Files created | 3 |

---

## Recommendations for 5A.5
1. Consider extracting shared compliance utilities
2. Add input validation for archive size limits
3. Add rate limiting on benchmark endpoints