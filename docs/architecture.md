<!-- BILINGUAL_DOCS_START -->
## Bahasa Indonesia / English

### Ringkasan / Summary

Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.
> Terjemahan Indonesia: Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.

- Bahasa Indonesia: konten utama tetap dipertahankan dalam dokumen asli, dan bagian ini memberi konteks ringkas dalam bahasa Indonesia.
- English: the main content remains in the original document, and this section provides a concise bilingual context for international readers.

### Informasi Dokumen / Document Info
- File: `docs/architecture.md`
- Judul: Architecture
- Status: bilingual header added

<!-- BILINGUAL_DOCS_END -->

<!-- DOCUMENT_METADATA_START -->
**Owner:** Documentation Team
**Canonical Owner:** Documentation Governance Lead
**Last Verified:** 2026-08-02
**Version:** 1.0.0
**Status:** Active
**SSOT:** System architecture overview and component interactions
<!-- DOCUMENT_METADATA_END -->

# ECP Architecture Overview — Platform RC (2026-08-02)

## System Architecture (Live)

```
┌─────────────────────────────────────────────────────────────┐
│                         USER                                 │
└───────────────────────────┬─────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────┐
│                   Gateway API (FastAPI)                      │
└───────────────────────────┬─────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────┐
│              Adaptive Cognitive Runtime                        │
│  Meta-Cognition: Choose pipeline, optimize budget             │
└───────────────────────────┬─────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────┐
│                    Cognitive Kernel (INTEGRATED)               │
│  ┌─────────┬─────────┬─────────┬─────────┬──────────────┐  │
│  │Perception│ Memory  │Reasoning│Planning │  Decision    │  │
│  └─────────┴─────────┴─────────┴─────────┴──────────────┘  │
│  ┌─────────┬─────────┬─────────┬─────────┬──────────────┐  │
│  │ Action  │Reflection│ Learning │ Debate │ Simulation  │  │
│  └─────────┴─────────┴─────────┴─────────┴──────────────┘  │
└────────────────────────────┬────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      Runtime Layer                           │
│  ┌──────────────┬──────────────┬──────────────────────────┐ │
│  │ Event Bus    │ Task Queue   │ Distributed Runtime      │ │
│  └──────────────┴──────────────┴──────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Infrastructure Layer                       │
│  ┌──────────┬──────────┬──────────┬──────────┬────────────┐ │
│  │  Redis   │PostgreSQL│  Qdrant  │MinIO    │  Ollama    │ │
│  └──────────┴──────────┴──────────┴──────────┴────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

## Cognitive Pipeline (Active)

```
Input → Perception → Planner → Memory → Executor → Learning → Governance
```

Each layer is implemented and tested:
> Terjemahan Indonesia: Each layer adalah implemented dan tested:
- **Perception** (`backend/app/core/perception_engine.py`) - Input processing, entity/intent extraction
- **Planner** (`apps/organization/ai_planner.py`) - Goal decomposition, cost/risk estimation
- **Memory** (`backend/app/core/memory_layer.py`) - 7 memory layers with consolidation
- **Executor** (`apps/organization/workflow_executor.py`) - Workflow execution, checkpoint, retry
- **Learning** (`backend/app/core/cognitive/continuous_learning.py`) - RL, human feedback
- **Governance** (`backend/app/core/governance.py`) - Approval workflow, tenant isolation

Orchestrated by `backend/app/agents/orchestrator_v2.py`.
> Terjemahan Indonesia: Orchestrated oleh backend/app/agen/orchestrator_v2.py.

---

## Architecture Rule (2026-08-02)

> **Core Cognitive Services Decoupling Rule:**
> No Core Cognitive Service may call another directly without going through service interface or orchestration layer.

**Enforce:** Memory ↔ Planner ↔ Executor ↔ Learning communicate through contracts only.

---

## Package Structure

```
backend/
└── app/
    ├── main.py                 # FastAPI application entry point
    ├── api/                    # Route handlers (REST endpoints)
    │   ├── chat.py            # Chat + SSE streaming
    │   ├── execution.py       # Execution CRUD + progress
    │   ├── workspace.py       # Workspace CRUD + files
    │   ├── artifact.py        # Artifact CRUD + versions
    │   ├── model_gateway.py   # Model provider health/status
    │   ├── capability_discovery.py  # Capability registry lookup
    │   └── ...                 # Other route modules
    ├── core/                   # Canonical services (source of truth)
    │   ├── perception_engine.py # NEW: Input processing + NLP
    │   ├── memory_layer.py    # Memory layers (working, conversation, knowledge, long-term, session, project)
    │   ├── cognitive_kernel.py # Cognitive service orchestration
    │   ├── cognitive/        # Cognitive primitives
    │   │   ├── planner.py      # Plan creation + result review
    │   │   ├── reasoning_engine.py
    │   │   ├── debate_engine.py
    │   │   ├── self_verification.py
    │   │   ├── simulation_engine.py
    │   │   ├── world_model.py
    │   │   ├── strategic_planner.py
    │   │   └── continuous_learning.py
    │   ├── adaptive_runtime.py # Dynamic pipeline composition
    │   ├── evaluation.py       # QualityGate + benchmark framework
    │   ├── governance.py       # Approval + tenant isolation
    │   ├── security_model.py   # RBAC + audit logging
    │   └── ...                 # Other core services
    └── agents/                 # Agent implementations
        └── orchestrator_v2.py # Primary orchestrator (integrated pipeline)
apps/
    ├── organization/           # Organization runtime
    │   ├── ai_planner.py      # Planner with cost/risk estimation
    │   └── workflow_executor.py # Executor with checkpoint/resume/retry
    ├── society/               # Society runtime
    │   └── intent_router.py   # Intent routing + domain hints
    ├── network_engineer/      # Network reference app
    ├── code_engineer/         # Code reference app
    ├── research/             # Research reference app
    ├── devops/               # DevOps reference app
    ├── trading/              # Trading reference app
    ├── self_development/     # Self-development reference app
    ├── decision_intelligence/     # Decision Intelligence (RFC-0007)
    ├── system_architect/          # System Architect (RFC-0011)
    ├── security_engineer/         # Security Engineer (RFC-0008)
    ├── data_engineer/             # Data Engineer (RFC-0009)
    ├── database_engineer/         # Database Engineer (RFC-0010)
    ├── qa_engineer/               # QA Engineer (RFC-0012)
    └── business_analyst/          # Business Analyst (RFC-0013)
benchmarks/                   # Performance + quality benchmarks
```

---

## Status: Platform Release Candidate (92/100)

| Layer | Status | Notes |
|-------|--------|-------|
| Core Platform | ✅ Complete | 90 |
| Cognitive Services | ✅ Integrated | 91 |
| Capability Packs | ✅ Production Ready | 90 |
| Operational Layer | ✅ Implemented | 90 |
| Security | ✅ RBAC + Isolation | 89 |
| Testing | ✅ 426 tests pass | 92 |

---

## Dependency Rules

```
apps → sdk → kernel
apps → runtime → kernel
studio → runtime → kernel
marketplace → runtime → kernel
plugins → kernel
```

**Forbidden:**
- kernel → runtime, sdk, apps, capability_packs
- runtime → apps, sdk, capability_packs

---

## Contract Versioning

All contracts are versioned and backward-compatible within major versions.
> Terjemahan Indonesia: All contracts adalah versioned dan backward-compatible within major versions.

```
Contract v1.x → Stable, backward-compatible
Contract v2.x → Breaking changes, migration guide provided
```

> **Policy Change (2026-08-02):** All public API contracts are frozen. Internal changes allowed; public signature changes require review.

---

## Next Sprints (Revised Priority)

### Sprint A — Engineering Hardening
- 0 Pylance Severity 8
- 100% Public API Typed
- Async consistency

### Sprint B — AES Documentation
- Architecture Specification
- Engineering Specification
- Behavioral contracts

### Sprint C — Reflection + Evaluation
```
Generate → Evaluate → Reflect → Improve → Verify
```

### Sprint D — Evidence Layer
```
Search → Retrieve → Extract → Normalize → Rank → Evidence → Citation
```

### Sprint E — Debate Engine
