# ECP Release Criteria

**Version:** 1.0.0
**Effective:** 2026-08-01
**Parent:** `GOVERNANCE_CHARTER.md`
**Purpose:** Defines release conditions, quality gates, and Definition of Done for ECP releases and Capability Packs.

---

## 1. Success Criteria — v1.0.0-dev

ECP v1.0.0-dev is successful if and only if:

1. ✅ **6 Capability Packs** exist and are registered in Capability Graph
2. ✅ **Golden Test Suite** passes with ≥80% pass rate
3. ✅ **CI/CD Pipeline** blocks merges on any failure
4. ✅ **Documentation** covers getting started, SDK, contracts, and architecture
5. ✅ **No Framework Trap** — Core remains stable while Capability Packs evolve
6. ✅ **Architecture Governance** active: Core is frozen, Capability First Rule enforced, all changes require ADR when impacting multiple packs

---

## 2. Golden Test Set

The golden test suite (`benchmarks/golden_test_set.py`) contains:

- 50 simple tasks (basic reasoning, coding, explanation)
- 50 medium tasks (API design, database schema, configuration)
- 50 complex tasks (full-stack apps, distributed systems)
- 50 domain-specific tasks (networking, trading, DevOps, research, self-development)

**Pass Threshold:** ≥80% (160/200 tests)

---

## 3. CI/CD Pipeline

Every PR must pass:

1. **Lint & Format** — ruff + black
2. **Type Check** — mypy with strict mode
3. **Unit Tests** — pytest with ≥80% coverage
4. **Architecture Test** — package boundary enforcement
5. **Benchmarks** — performance and quality benchmarks
6. **SDK Compatibility** — imports and basic functionality
7. **Plugin Compatibility** — all plugins load correctly
8. **Golden Tests** — full golden test suite
9. **Governance Checks** — Core change guard, ADR reference, Capability First (see `GOVERNANCE.md`)

**Merge Policy:** All checks must pass. No exceptions.

---

## 4. Metrics to Track

| Metric | Target | Measurement |
|--------|--------|-------------|
| Golden Test Pass Rate | ≥80% | benchmarks/golden_test_set.py |
| Test Coverage | ≥80% | pytest-cov |
| Type Safety | 0 errors | mypy --strict |
| Architecture Violations | 0 | benchmarks/package_boundaries.py |
| SDK Import Time | <100ms | sdk/benchmarks |
| Capability Quality Score | ≥85% | benchmarks/capability_benchmark.py |
| Improvement Velocity | >0 real cases/week per pack | real_cases/<capability_id>/ |
| Documentation Coverage | 100% | docs/ |

---

## 5. Developer Preview Quality Targets

Certification requires each Capability Pack to meet or exceed the following benchmark scores:

| Capability | Target Score | Grade |
|------------|--------------|-------|
| Network | ≥90 | A |
| Code | ≥85 | A- |
| Research | ≥85 | A- |
| DevOps | ≥80 | B+ |
| Trading | ≥80 | B+ (must also pass Certification) |
| Self Development | ≥90 | A |

All scores are measured by the 6-dimension Capability Benchmark framework (Accuracy, Completeness, Explainability, Safety, Efficiency, Consistency).

---

## 6. Definition of Done — Standard Template

Each Capability Pack's Definition of Done uses this standard template. A pack fills in its specific values.

```text
Definition of Done

Functional
- [ ] <functional requirement>

Benchmark
- [ ] Benchmark score ≥ <threshold> (grade <grade>)

Golden Tests
- [ ] All pack golden test scenarios pass (100%)

Real Cases
- [ ] ≥ <N> real cases logged in real_cases/<capability_id>/
- [ ] Evaluation notes recorded for each case

Documentation
- [ ] Capability Guide updated
- [ ] API reference / contract updated

SDK
- [ ] Pack accessible via SDK without Core changes

Performance
- [ ] Response within target latency budget

Security
- [ ] No known P0/P1 security issues

Regression
- [ ] No regression in existing benchmark dimensions
- [ ] Benchmark reproducible (documented command + persisted result)

Release Notes
- [ ] Capability Changelog updated
```

---

## 7. Definition of Done per Capability Pack

### 7.1 Network Engineer

| DoD Item | Criterion |
|----------|-----------|
| Golden Benchmark | ≥95% accuracy (grade A) |
| Real Cases | ≥100 real cases in `real_cases/network/` |
| Regression | No regression across all 6 benchmark dimensions |
| Documentation | `CAPABILITY_GUIDE.md` and contract updated |
| Reproducibility | Benchmark reproducible via documented command; results persisted |
| Changelog | Capability Changelog updated |

### 7.2 Code Engineer

| DoD Item | Criterion |
|----------|-----------|
| Golden Benchmark | ≥90% code quality score |
| Real Cases | ≥100 real repositories in `real_cases/code/` |
| Regression | No regression across all 6 benchmark dimensions |
| Documentation | `CAPABILITY_GUIDE.md` and contract updated |
| Reproducibility | Benchmark reproducible; results persisted |
| Changelog | Capability Changelog updated |

### 7.3 Research Assistant

| DoD Item | Criterion |
|----------|-----------|
| Golden Benchmark | ≥85% citation accuracy |
| Real Cases | ≥100 research questions in `real_cases/research/` |
| Regression | No regression across all 6 benchmark dimensions |
| Documentation | `CAPABILITY_GUIDE.md` and contract updated |
| Reproducibility | Benchmark reproducible; results persisted |
| Changelog | Capability Changelog updated |

### 7.4 DevOps Assistant

| DoD Item | Criterion |
|----------|-----------|
| Golden Benchmark | ≥85% correctness on generated configs |
| Real Cases | ≥100 infrastructure scenarios in `real_cases/devops/` |
| Regression | No regression across all 6 benchmark dimensions |
| Documentation | `CAPABILITY_GUIDE.md` and contract updated |
| Reproducibility | Benchmark reproducible; results persisted |
| Changelog | Capability Changelog updated |

### 7.5 Trading Analyst

| DoD Item | Criterion |
|----------|-----------|
| Golden Benchmark | ≥80% (grade B+) and Certification passed |
| Real Cases | ≥100 market scenarios in `real_cases/trading/` |
| Regression | No regression across all 6 benchmark dimensions |
| Documentation | `CAPABILITY_GUIDE.md` and contract updated |
| Reproducibility | Benchmark reproducible; results persisted |
| Changelog | Capability Changelog updated |

### 7.6 Self Development

| DoD Item | Criterion |
|----------|-----------|
| Golden Benchmark | ≥90% (grade A) |
| Real Cases | ≥10 real projects in `real_cases/self_development/` |
| Regression | No regression across all 6 benchmark dimensions |
| Documentation | `CAPABILITY_GUIDE.md` and contract updated |
| Reproducibility | Benchmark reproducible; results persisted |
| Changelog | Capability Changelog updated |

---

## 8. Release Definition of Done

A release is complete when:

- [ ] All target Capability Packs meet their Definition of Done (Section 7)
- [ ] Golden Test Suite ≥80% (160/200)
- [ ] Test coverage ≥80%
- [ ] mypy --strict: 0 errors
- [ ] Architecture violations: 0
- [ ] All governance checks pass (Core change guard, ADR reference)
- [ ] Release notes and changelog updated
- [ ] Metrics recorded and benchmark results persisted

---

## 9. Post-Release Review

After each release:

1. Compare actual benchmark scores vs targets.
2. Log lessons learned into the Continuous Learning cycle.
3. Update `CAPABILITY_STRATEGY.md` grade table.
4. Update `ROADMAP.md` based on actual velocity.

---

## 10. Approval

| Role | Status | Date |
|------|--------|------|
| Chief Product Officer | Approved | 2026-08-01 |

