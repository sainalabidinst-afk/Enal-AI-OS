# ECP Architecture Overview - Platform RC (2026-07-27)

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
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                      Runtime Layer                           │
│  ┌──────────────┬──────────────┬──────────────────────────┐ │
│  │ Event Bus    │ Task Queue   │ Distributed Runtime      │ │
│  └──────────────┴──────────────┴──────────────────────────┘ │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    Infrastructure Layer                        │
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
- **Perception** (`backend/app/core/perception_engine.py`) - Input processing, entity/intent extraction
- **Planner** (`apps/organization/ai_planner.py`) - Goal decomposition, cost/risk estimation  
- **Memory** (`backend/app/core/memory_layer.py`) - 7 memory layers with consolidation
- **Executor** (`apps/organization/workflow_executor.py`) - Workflow execution, checkpoint, retry
- **Learning** (`backend/app/core/cognitive/continuous_learning.py`) - RL, human feedback
- **Governance** (`backend/app/core/governance.py`) - Approval workflow, tenant isolation

Orchestrated by `backend/app/agents/orchestrator_v2.py`.

---

## Architecture Rule (2026-07-27)

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
    └── self_development/     # Self-development reference app
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

```
Contract v1.x → Stable, backward-compatible
Contract v2.x → Breaking changes, migration guide provided
```

> **Policy Change (2026-07-27):** All public API contracts are frozen. Internal changes allowed; public signature changes require review.

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