<!-- BILINGUAL_DOCS_START -->
## Bahasa Indonesia / English

### Ringkasan / Summary

Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.
> Terjemahan Indonesia: Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.

- Bahasa Indonesia: konten utama tetap dipertahankan dalam dokumen asli, dan bagian ini memberi konteks ringkas dalam bahasa Indonesia.
- English: the main content remains in the original document, and this section provides a concise bilingual context for international readers.

### Informasi Dokumen / Document Info
- File: `docs/RELEASE_CRITERIA.md`
- Judul: Release Criteria
- Status: bilingual header added

<!-- BILINGUAL_DOCS_END -->

<!-- DOCUMENT_METADATA_START -->
**Owner:** Documentation Team
**Canonical Owner:** Documentation Governance Lead
**Last Verified:** 2026-08-02
**Version:** 1.0.0
**Status:** Active
**SSOT:** Release conditions, quality gates, Definition of Done, and benchmark targets
<!-- DOCUMENT_METADATA_END -->

# ECP Release Criteria

**Version:** 1.0.0
**Effective:** 2026-08-02
**Parent:** `GOVERNANCE_CHARTER.md`
**Purpose:** Defines release conditions, quality gates, and Definition of Done for ECP releases and Capability Packs.

---

## 1. Success Criteria — v1.0.0-dev

ECP v1.0.0-dev is successful if and only if:
> Terjemahan Indonesia: ECP v1.0.0-dev adalah successful if dan only if:

1. ✅ **13 Capability Packs** exist and are registered in Capability Graph
2. ✅ **Golden Test Suite** passes with ≥80% pass rate
3. ✅ **CI/CD Pipeline** blocks merges on any failure
4. ✅ **Documentation** covers getting started, SDK, contracts, and Architecture
5. ✅ **No Framework Trap** — Core remains stable while Capability Packs evolve
6. ✅ **Architecture Governance** active: Core is frozen, Capability First Rule enforced, all changes require ADR when impacting multiple packs

---

## 2. Golden Test Set

The Golden Test Suite (`benchmarks/golden_test_set.py`) contains:
> Terjemahan Indonesia: Golden Test Suite (benchmarks/golden_test_set.py) contains:

- 50 simple tasks (basic reasoning, coding, explanation)
- 50 medium tasks (API design, database schema, configuration)
- 50 complex tasks (full-stack apps, distributed systems)
- 50 domain-specific tasks (networking, trading, DevOps, research, self-development)

**Pass Threshold:** ≥80% (160/200 tests)

---

## 3. CI/CD Pipeline

Every PR must pass:
> Terjemahan Indonesia: Setiap PR harus lulus:

1. **Lint & Format** — ruff + black
2. **Type Check** — mypy with strict mode
3. **Unit Tests** — pytest with ≥80% coverage
4. **Architecture Test** — package boundary enforcement
5. **Benchmarks** — performance and quality benchmarks
6. **SDK Compatibility** — imports and basic functionality
7. **Plugin Compatibility** — all plugins load correctly
8. **Golden Tests** — full Golden Test Suite
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
> Terjemahan Indonesia: Certification requires each kapabilitas Pack untuk meet or exceed following benchmark scores:

| Capability | Target Score | Grade |
|------------|--------------|-------|
| Network Engineer | ≥90 | A |
| Code Engineer | ≥85 | A- |
| Research Assistant | ≥85 | A- |
| DevOps Assistant | ≥80 | B+ |
| Trading Analyst | ≥80 | B+ (must also pass Certification) |
| Self Development | ≥90 | A |
| Decision Intelligence | ≥90 | A (91.25% benchmark — RFC-0007) |
| System Architect | ≥90 | A (RFC-0011) |
| Security Engineer | ≥85 | A- (RFC-0008) |
| Data Engineer | ≥85 | A- (RFC-0009) |
| Database Engineer | ≥85 | A- (RFC-0010) |
| QA Engineer | ≥90 | A (RFC-0012) |
| Business Analyst | ≥85 | A- (RFC-0013) |

All scores are measured by the 6-dimension Capability Benchmark framework (Accuracy, Completeness, Explainability, Safety, Efficiency, Consistency).
> Terjemahan Indonesia: All scores adalah measured oleh 6-dimension kapabilitas Benchmark kerangka kerja (Accuracy, Completeness, Explainability, Safety, Efficiency, Consistency).

---

## 6. Definition of Done — Standard Template

Each Capability Pack's Definition of Done uses this standard template. A pack fills in its specific values.
> Terjemahan Indonesia: Each kapabilitas Pack's Definition dari Done uses ini standard template. sebuah pack fills dalam its specific values.

```text
Definition of Done

Functional
- [ ] <functional requirement>

Benchmark
- [ ] Benchmark score ≥ <threshold> (grade <grade>)

Golden Tests
- [ ] All pack Golden Test scenarios pass (100%)

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

### 7.7 Decision Intelligence

| DoD Item | Criterion |
|----------|-----------|
| Golden Benchmark | ≥90% (grade A — benchmark overall 91.25%) |
| Real Cases | (Shared reasoning layer — real cases tracked per consuming pack) |
| Regression | No regression across all 8 benchmark dimensions |
| Documentation | `docs/capabilities/decision-intelligence.md` updated |
| Reproducibility | Benchmark reproducible via `benchmarks/decision_intelligence_benchmark.py`; results persisted |
| Changelog | Capability Changelog updated |

### 7.8 System Architect

| DoD Item | Criterion |
|----------|-----------|
| Golden Benchmark | ≥90% (grade A) |
| Real Cases | Real cases tracked via architecture review history in `real_cases/system_architect/` |
| Regression | No regression across all 8 benchmark dimensions |
| Documentation | `docs/capabilities/system-architect.md` and `docs/CAPABILITY_GUIDE.md` updated |
| Reproducibility | Benchmark reproducible via `benchmarks/system_architect_benchmark.py`; results persisted |
| Changelog | Capability Changelog updated |

### 7.9 Security Engineer

| DoD Item | Criterion |
|----------|-----------|
| Golden Benchmark | ≥85% (grade A-) |
| Real Cases | ≥20 security analysis cases in `real_cases/security_engineer/` |
| Regression | No regression across all 9 benchmark dimensions |
| Documentation | `docs/capabilities/security-engineer.md` and `docs/CAPABILITY_GUIDE.md` updated |
| Reproducibility | Benchmark reproducible via `benchmarks/security_engineer_benchmark.py`; results persisted |
| Changelog | Capability Changelog updated |

### 7.10 Data Engineer

| DoD Item | Criterion |
|----------|-----------|
| Golden Benchmark | ≥85% (grade A-) |
| Real Cases | ≥20 data pipeline cases in `real_cases/data_engineer/` |
| Regression | No regression across all 8 benchmark dimensions |
| Documentation | `docs/capabilities/data-engineer.md` and `docs/CAPABILITY_GUIDE.md` updated |
| Reproducibility | Benchmark reproducible via `benchmarks/data_engineer_benchmark.py`; results persisted |
| Changelog | Capability Changelog updated |

### 7.11 Database Engineer

| DoD Item | Criterion |
|----------|-----------|
| Golden Benchmark | ≥85% (grade A-) |
| Real Cases | ≥20 database analysis cases in `real_cases/database_engineer/` |
| Regression | No regression across all 8 benchmark dimensions |
| Documentation | `docs/capabilities/database-engineer.md` and `docs/CAPABILITY_GUIDE.md` updated |
| Reproducibility | Benchmark reproducible via `benchmarks/database_engineer_benchmark.py`; results persisted |
| Changelog | Capability Changelog updated |

### 7.12 QA Engineer

| DoD Item | Criterion |
|----------|-----------|
| Golden Benchmark | ≥90% (grade A) |
| Real Cases | ≥20 QA analysis cases in `real_cases/qa_engineer/` |
| Regression | No regression across all 9 benchmark dimensions |
| Documentation | `docs/capabilities/qa-engineer.md` and `docs/CAPABILITY_GUIDE.md` updated |
| Reproducibility | Benchmark reproducible via `benchmarks/qa_engineer_benchmark.py`; results persisted |
| Changelog | Capability Changelog updated |

### 7.13 Business Analyst

| DoD Item | Criterion |
|----------|-----------|
| Golden Benchmark | ≥85% (grade A-) |
| Real Cases | ≥20 business analysis cases in `real_cases/business_analyst/` |
| Regression | No regression across all 9 benchmark dimensions |
| Documentation | `docs/capabilities/business-analyst.md` and `docs/CAPABILITY_GUIDE.md` updated |
| Reproducibility | Benchmark reproducible via `benchmarks/business_analyst_benchmark.py`; results persisted |
| Changelog | Capability Changelog updated |

---

## 8. Release Definition of Done

A release is complete when:
> Terjemahan Indonesia: Sebuah rilis adalah complete when:

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
> Terjemahan Indonesia: After each rilis:

1. Compare actual benchmark scores vs targets.
2. Log lessons learned into the Continuous Learning cycle.
3. Update `CAPABILITY_STRATEGY.md` grade table.
4. Update `ROADMAP.md` based on actual velocity.

---

## 10. Approval

| Role | Status | Date |
|------|--------|------|
| Chief Product Officer | Approved | 2026-08-02 |
