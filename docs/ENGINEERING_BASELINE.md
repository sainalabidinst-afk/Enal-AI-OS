# Engineering Baseline — v1.0.0-engineering-baseline

**Status:** 🟢 **Frozen**  
**Tag:** `v1.0.0-engineering-baseline`  
**Date:** 2024

---

## Purpose

This document records the exact engineering state of the Enal Cognitive Platform at the point the engineering baseline was frozen. After this point:

- **No new architecture changes or large refactors** without documented cross-domain need
- **No redesigns** of core components
- Focus shifts to:
  1. Documentation of actual code state
  2. Product development on stable foundation

---

## Baseline Qualification

| Check | Result | Evidence |
|-------|--------|----------|
| MyPy strict | ✅ **0 errors** | All 27+ files fixed across sprints |
| Pylance Severity 8 | ✅ **0** | Clean type resolution |
| VS Code Problems | ✅ **0** | No remaining diagnostics |
| Test Suite | ✅ **426 passing** | All tests pass |
| Python 3.11 f-string | ✅ **0 issues in production** | Verified via `compile()` scan |
| Ruff hygiene | ⚠️ Residual warnings | `ruff check --fix` and `ruff format` pending (auto-fixable) |
| Architecture consistency | ✅ Validated | AR-001 through AR-017 pass |
| API contract consistency | ✅ Validated | All signatures match |
| No circular imports | ✅ Resolved | knowledge, task_planner, meeting |
| No mutable defaults | ✅ Addressed | RUF012 fixed across codebase |
| No blind exceptions | ⚠️ 45 locations | Accepted tech debt — review per case in future sprint |

---

## Repository Structure (Post-Hardening)

```
enal-ai-os/
├── apps/               # 6 Capability Packs (network, code, research, devops, trading, self)
├── backend/            # API, core, studio, models
├── benchmarks/         # Performance, capability, golden test benchmarks
├── docs/               # Architecture, API, quality gates, roadmap
│   ├── adr/            # Architecture Decision Records
│   └── quality/        # Quality Gate Policy
├── examples/           # Custom agent, custom workflow
├── frontend/           # Next.js frontend
├── golden/             # Cisco, Fortinet, MikroTik golden configs
├── plugins/            # MikroTik plugin
├── real_cases/         # Real-world test datasets
├── scripts/            # CI/CD, gate validation, release readiness
├── sdk/                # Python SDK
├── tests/              # Unit tests (426 passing)
├── tools/
│   └── audit/          # Utility scripts (hygiene, mypy fixing, f-string scanning)
└── workspace/          # Runtime workspace
```

---

## Files Modified During Hardening (27 core + utilities)

### Core Production Files (27)

| File | Fix Applied |
|------|-------------|
| `adaptive_runtime.py` | Rewritten with proper types |
| `reflection.py` | No await on sync calls |
| `cognitive_kernel.py` | DecisionService returns dict |
| `unified_orchestrator.py` | Budget estimate is sync |
| `orchestrator_v2.py` | Use orchestrate_goal instead of process_request |
| `code_engineer/__init__.py` | ArchitectureReader str\|None fix |
| `conversation_manager.py` | Added _persist_artifact method |
| `reasoning_engine.py` | No await on sync calls |
| `strategic_planner.py` | No await on sync calls |
| `world_model.py` | No await on sync calls |
| `decision_engine.py` | Returns dict instead of DecisionResult |
| `vendor/models.py` | Added NATRule.in_interface, BridgeConfig.comment |
| `routeros_parser.py` | Added missing dataclass fields |
| `profiles.py` | Fixed vendor model checks |
| `enricher.py` | Fixed evidence building |
| `attachments/pipeline.py` | Fixed InfrastructureAST fields |
| `attachments/models.py` | Fixed type breaks |
| `execution_session.py` | Fixed constructor params |
| `memory_layer.py` | Fixed constructor issues |
| `workspace_service.py` | Fixed create_workspace signature |
| `artifact_service.py` | Fixed create_artifact signature |
| `config.py` | Fixed settings types |
| `event_bus.py` | Fixed Redis type annotations |
| `detector.py` | Fixed VendorFamily\|None type |
| `voice_vision_agent.py` | Fixed None defaults |
| `execution.py` | Fixed Artifact vs ExecutionArtifact |
| `society.py` | Fixed SubtaskResult type |

### Utility Scripts moved to `tools/audit/`

```
tools/audit/
├── __init__.py
├── audit_hygiene.py
├── find_fstring_backslash.py
├── fix_6_remaining.py
├── fix_all_remaining.py
├── fix_final_batch.py
├── fix_final_mypy.py
├── fix_mypy_errors.py
├── fix_remaining_4.py
├── fix_remaining_mypy.py
├── fix_self_verification.py
├── run_ruff.py
├── run_scans.py
├── run_scans_and_mypy.py
└── apply_mypy_fixes.py
```

---

## Python 3.11 Compatibility — Verification Detail

- **Method:** `compile(content, path, 'exec', flags=0)` for every `.py` file in the repository
- **Result:** 0 f-string backslash issues in `apps/`, `backend/`, `benchmarks/`, `tests/`
- **One exception:** `_fix_final_mypy.py:93` — utility script, NOT production code

Pattern verified as non-existent:
```python
# ❌ This pattern does NOT exist in production code:
f"{expr_with_backslash}"

# ✅ All f-strings use pre-computed variables:
fixed = value.replace('\\n', '')
f"{fixed}"
```

---

## Build Environment

| Component | Version |
|-----------|---------|
| Python | 3.11.9 |
| Node.js | Not installed in current environment (defined in `frontend/package.json`: Next.js 14.2.0, React 18.2.0, TypeScript 5.3.0) |
| npm | Not installed in current environment |
| Docker | 29.6.2 |
| Git | 2.55.0.windows.3 |
| OS | Windows 11 |

---

## Dependency Snapshot

### Backend (`backend/pyproject.toml`)

| Dependency | Version Requirement |
|------------|-------------------|
| fastapi | >=0.109.0 |
| uvicorn[standard] | >=0.27.0 |
| sqlalchemy | >=2.0.0 |
| qdrant-client | >=1.7.0 |
| redis | >=5.0.0 |
| pydantic | >=2.6.0 |
| pydantic-settings | >=2.0.0 |
| litellm | >=1.40.0 |
| langchain-openai | >=0.1.0 |
| langchain-core | >=0.1.0 |
| httpx | >=0.26.0 |
| pyyaml | >=6.0 |
| aiohttp | >=3.9.0 |
| python-multipart | >=0.0.9 |
| psycopg2-binary | >=2.9.0 |

### Backend Dev Dependencies

| Dependency | Version Requirement |
|------------|-------------------|
| pytest | >=8.0.0 |
| pytest-asyncio | >=0.23.0 |
| ruff | >=0.4.0 |
| black | >=24.4.0 |
| mypy | >=1.8.0 |

### Frontend (`frontend/package.json`)

| Dependency | Version |
|------------|---------|
| next | 14.2.0 |
| react | ^18.2.0 |
| react-dom | ^18.2.0 |
| zustand | ^5.0.14 |
| lucide-react | ^0.378.0 |
| tailwindcss (dev) | ^3.4.0 |
| typescript (dev) | ^5.3.0 |

### SDK (`sdk/pyproject.toml`)

See `sdk/` directory for SDK-specific dependencies.

---

## Baseline Engineering Principles

These principles form the "constitution" of engineering for this project. Every architectural decision, code review, and implementation must align with these principles.

| # | Principle | Description |
|---|-----------|-------------|
| 1 | **Architecture Freeze** | No new large-scale refactors, redesigns, or architecture changes without documented cross-domain need validated through ADR |
| 2 | **Backward Compatibility** | All public APIs and interfaces must maintain backward compatibility. Breaking changes require ADR, deprecation period, and migration path |
| 3 | **Strong Typing** | All code must pass MyPy strict checking. No `Any` types in public interfaces. Use `X \| None` over `Optional[X]` |
| 4 | **No Hidden Dependencies** | All dependencies must be explicitly declared in `pyproject.toml` or `package.json`. No reliance on transitive or system-level packages |
| 5 | **Test First** | Every change must include or update tests. Baseline: 426 tests passing. No regression below 95% pass rate |
| 6 | **Observability First** | All runtime operations must emit telemetry events. Every execution path must be traceable via `record_execution_event` |
| 7 | **Event Driven** | Cross-module communication must use the Event Bus. No direct coupling between capability packs or core modules |
| 8 | **Plugin First** | Extend functionality through plugins, not by modifying core. Plugins require manifest and security validation |

---

## Architecture Decision Records (ADR)

ADRs are stored in `docs/adr/`. Each ADR records a significant architectural decision, its context, alternatives considered, and the rationale for the chosen approach.

| ADR | Title | Description |
|-----|-------|-------------|
| ADR-001 | Event Bus Architecture | Why Event Bus was chosen for cross-module communication |
| ADR-002 | Capability Pack Architecture | Why capability packs are the unit of extension |
| ADR-003 | Universal AST Design | Why Universal AST was chosen for multi-vendor network configuration |
| ADR-004 | Debate Engine Architecture | Why debate-based reasoning was chosen for self-verification |

See `docs/adr/` for full decision records.

---

## Quality Gate Policy

See `docs/quality/QUALITY_GATES.md` for the complete Quality Gate Policy.

Every pull request targeting `main` or `release/*` must pass:

| Gate | Requirement | Severity |
|------|-------------|----------|
| MyPy | 0 errors | 🔴 BLOCKER |
| Tests | ≥95% pass (baseline: 426) | 🔴 BLOCKER |
| API Contract | Backward compatible | 🔴 BLOCKER |
| ADR | Required for architecture changes | 🔴 BLOCKER |
| Ruff Lint | No blockers | 🟡 WARNING |
| Ruff Format | 0 files reformatted | 🟡 WARNING |
| No Blind Exceptions | New ones justified | 🟡 WARNING |

Exceptions require documented approval. See full policy for exception process.

---

## Known Accepted Tech Debt

| Issue | Count | Severity | Decision |
|-------|-------|----------|----------|
| Blind `except Exception:` | 45 | Low | Accept for now. Review per case in future sprint |
| `subprocess.run` without `check=False` | 5 | Low | All in utility scripts. Fix when actively maintaining tooling |
| `ruff check --fix` pending | ~50 auto-fixable | Low | Run when committing next round of changes |
| `ruff format` pending | ~10 files | Low | Run when committing next round of changes |

---

## Next Steps

1. **Phase 2: AES Documentation** — Document actual code state:
   - Architecture overview
   - Module dependency graph
   - Runtime flow
   - Event flow
   - Public API
   - Quality gates
   - Testing strategy
   - Coding standards

2. **Phase 3: Reference Architecture** — Elevate AES to reference architecture for all applications built on ECP
3. **Phase 4: Application Development Guide** — Coding standards, capability pack development guide
4. **Phase 5: Product Development** — Feature development on stable foundation

---

## Document Inventory

| Document | Path |
|----------|------|
| Engineering Baseline | `docs/ENGINEERING_BASELINE.md` |
| Quality Gate Policy | `docs/quality/QUALITY_GATES.md` |
| ADR-001: Event Bus | `docs/adr/ADR-001-event-bus-architecture.md` |
| ADR-002: Capability Pack | `docs/adr/ADR-002-capability-pack-architecture.md` |
| ADR-003: Universal AST | `docs/adr/ADR-003-universal-ast-design.md` |
| ADR-004: Debate Engine | `docs/adr/ADR-004-debate-engine-architecture.md` |
| Architecture Overview | `docs/architecture.md` |
| Quality Gate | `docs/QUALITY_GATE.md` |
| Sprint Hardening Summary | `SPRINT_HARDENING_SUMMARY.md` |

