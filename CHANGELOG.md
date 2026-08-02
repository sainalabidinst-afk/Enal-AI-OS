<!-- BILINGUAL_DOCS_START -->
## Bahasa Indonesia / English


### Ringkasan / Summary
Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.
> Terjemahan Indonesia: Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.

- Bahasa Indonesia: konten utama tetap dipertahankan dalam dokumen asli, dan bagian ini memberi konteks ringkas dalam bahasa Indonesia.
- English: the main content remains in the original document, and this section provides a concise bilingual context for international readers.

### Informasi Dokumen / Document Info
- File: `CHANGELOG.md`
- Judul: Changelog
- Status: bilingual header added

<!-- BILINGUAL_DOCS_END -->

# Changelog

All notable changes to Enal Cognitive Platform (ECP) will be documented in this file.
> Terjemahan Indonesia: All notable changes untuk Enal kognitif platform (ECP) akan menjadi documented dalam ini file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
> Terjemahan Indonesia: Format adalah based pada Keep sebuah Changelog, dan ini proyek adheres untuk Semantic Versioning.

## [1.0.0-engineering-baseline] - 2024


### Engineering Baseline — Frozen 🧊


This tag marks the official **Engineering Baseline** of the Enal Cognitive Platform.
> Terjemahan Indonesia: Ini tag marks official rekayasa dasar dari Enal kognitif platform.

**Status:** 🟢 Engineering Baseline Stable

#### What was accomplished


- **Type Safety (MyPy):** 0 errors across entire codebase (27+ files fixed)
- **Python 3.11 Compatibility:** Verified with `compile()` — 0 issues in production code
- **Pylance Severity 8:** 0 remaining diagnostics
- **VS Code Problems:** 0 remaining issues
- **Test Suite:** 426 tests passing
- **Architecture Consistency:** All structural contracts validated
- **API Contract Consistency:** All signatures verified

#### Housekeeping

- Utility scripts (`_audit_hygiene.py`, `_fix_*.py`, `_run_*.py`) moved to `tools/audit/`
- Root repository cleaned of helper/tooling files
- `tools/audit/__init__.py` created with clear purpose documentation

#### Post-Baseline Rules

- No new large-scale refactoring without documented cross-domain need
- No architecture redesigns
- Focus shifts to:
  1. Documentation (architecture, module dependency, runtime flow, API, quality gates)
  2. Product development on stable foundation
> Terjemahan Indonesia: Dokumentasi (arsitektur, module dependency, runtime flow, API, kualitas gates) Product development pada stable foundation

#### Engineering Final Assessment


| Area | Status |
|------|--------|
| Architecture Consistency | ✅ |
| API Contract Consistency | ✅ |
| Type Safety (MyPy) | ✅ 0 Error |
| Python 3.11 Compatibility | ✅ |
| Pylance Severity 8 | ✅ 0 |
| VS Code Problems | ✅ 0 |
| Test Suite | ✅ 426 Passed |
| Engineering Hardening | ✅ Complete |
| Engineering Baseline | ✅ **Stable** |

---

## [1.0.0-release-candidate] - 2026-07-27


### Added
- Engineering Hardening Phase complete - All Severity 8+ type issues resolved
- Cognitive pipeline fully integrated (Perception → Planner → Memory → Executor)
- Checkpoint/Resume/Retry support in WorkflowExecutor
- SessionMemory and ProjectMemory for cross-execution context

### Fixed
- Circular imports: `knowledge/__init__.py`, `task_planner.py`, `meeting.py`
- Missing vendor model imports: `UniversalBGP`, `UniversalMPLS`, `UniversalCAPsMAN`, `UniversalWireGuard` in cisco_ios.py, mikrotik.py
- `Team` dataclass missing `team_id` field
- `create_checkpoint`, `resume_from_checkpoint`, `execute_with_retry` moved inside `WorkflowExecutor` class
- Duplicate `PerceptionInput` removed, now imports from `perception_engine.py`
- CodeEngineerApp `generate_patch()` rewritten with correct signature
- IntentRouter `max()` key function corrected
- API optional access patterns hardened with `_safe_get` helpers

### Status
- Runtime tests: 426 passing
- Static analysis: 0 Severity 8+ issues (down from 366)
- Architecture: 92/100 - Platform Release Candidate

---

## [1.0.0-dev] - 2026-07-08


### Added
- Strategic rebrand from "Enal AI OS" to "Enal Cognitive Platform (ECP)"
- v1.0.0-dev roadmap with 6 Official Capability Packs
- CI/CD pipeline with 8 automated checks (lint, type check, unit tests, architecture, benchmarks, SDK compatibility, plugin compatibility, golden tests)
- Golden Test Suite with 200 test cases across 4 categories
- 13 Capability Packs scaffolded:
  - Network Engineer
  - Code Engineer
  - Research Assistant
  - DevOps Assistant
  - Trading Analyst
  - Self Development
> Terjemahan Indonesia: Insinyur Jaringan, Insinyur Kode, Asisten Peneliti, Asisten DevOps, Analis Perdagangan, Pengembangan Diri
- Version management (VERSION file, pyproject.toml updated to 1.0.0-dev)
- v1 roadmap document with success criteria and metrics

### Changed
- Repository restructured for ecosystem readiness (kernel, runtime, sdk, studio, marketplace, capability_packs, apps, plugins, examples, docs, benchmarks)
- All Phase 1-6 components integrated into cohesive platform
- Documentation updated to reflect product positioning

### Governance
- No new engines without real use case
- Kernel must remain under 5000 lines
- All plugins require manifest and security validation
- Golden tests must pass with ≥80% rate

---

## [0.1.0] - 2026-07-08

### Added
- Phase 1: AI Core (model router, memory, planner, tool calling, RAG)
- Phase 2: AI Software Engineer (coding agents, QA, DevOps)
- Phase 3: AI Enterprise Platform (organization, reputation, experience, observability)
- Phase 4: Cognitive Architecture (reasoning, debate, simulation, verification)
- Phase 5: Adaptive Cognitive OS (adaptive runtime, decision engine, meta-cognition)
- Phase 6: Ecosystem (SDK, contracts, marketplace, studio, distributed runtime)
- Stable contracts for all core interfaces
- Plugin manifest and security model
- Package boundary enforcement
- Benchmark suite
- Comprehensive documentation
