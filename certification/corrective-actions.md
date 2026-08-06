# Corrective Action Plan — Phase 1.1 Re-Audit

## Objective

Raise all capabilities from current baseline to **≥80%** and eliminate Grade D before entering Benchmark Audit.

## Priority Tiers

### 🔴 Tier 1 — Grade D (Must Fix Before Re-Audit)

| Capability | Score | Grade | Blocking Issues |
|------------|-------|-------|-----------------|
| integration | 95 | D | Missing docs, missing tests, missing schemas |
| organization | 98 | D | Missing docs, missing tests, missing schemas |
| society | 95 | D | Missing docs, missing tests, missing schemas |

**Common corrective actions:**
1. Create `docs/capabilities/{slug}.md`
2. Create `tests/test_{name}.py`
3. Create or identify schema/contract module
4. Re-run audit

### 🟡 Tier 2 — Grade C, Score <75%

No capabilities currently in this tier. Current Grade C range: 106–116.

### 🟢 Tier 3 — Grade C, Score 75–79%

No capabilities currently in this tier. All Grade C capabilities are above 75%.

## Corrective Actions Detail

### CA-001: integration — Documentation
- **File:** `docs/capabilities/integration.md`
- **Action:** Create capability documentation
- **Owner:** Automated scaffolding + human review
- **Status:** Pending

### CA-002: integration — Tests
- **File:** `tests/test_integration.py`
- **Action:** Create baseline test suite
- **Owner:** Automated scaffolding
- **Status:** Pending

### CA-003: integration — Schemas
- **File:** `apps/integration/schemas.py` or identify existing schema module
- **Action:** Create or map schema definitions
- **Owner:** Automated scaffolding
- **Status:** Pending

### CA-004: organization — Documentation
- **File:** `docs/capabilities/organization.md`
- **Action:** Create capability documentation
- **Status:** Pending

### CA-005: organization — Tests
- **File:** `tests/test_organization.py`
- **Action:** Create baseline test suite
- **Status:** Pending

### CA-006: organization — Schemas
- **File:** `apps/organization/schemas.py` or identify existing schema module
- **Action:** Create or map schema definitions
- **Status:** Pending

### CA-007: society — Documentation
- **File:** `docs/capabilities/society.md`
- **Action:** Create capability documentation
- **Status:** Pending

### CA-008: society — Tests
- **File:** `tests/test_society.py`
- **Action:** Create baseline test suite
- **Status:** Pending

### CA-009: society — Schemas
- **File:** `apps/society/schemas.py` or identify existing schema module
- **Action:** Create or map schema definitions
- **Status:** Pending

## Execution Order

1. Run corrective actions for Tier 1 capabilities
2. Re-run Phase 1.1 audit
3. Verify no Grade D remains
4. Verify all capabilities ≥80%
5. Proceed to Phase 1.2 — Benchmark Audit

## Notes

- Corrective actions are limited to filling gaps in existing implementation.
- No new capability features or architectural changes.
- All artifacts must follow platform conventions.
