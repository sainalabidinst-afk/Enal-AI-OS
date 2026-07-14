# ECP Architecture Overview

## System Architecture

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
│              Adaptive Cognitive Runtime                      │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  Meta-Cognition: Choose pipeline, optimize budget     │  │
│  └───────────────────────────────────────────────────────┘  │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    Cognitive Kernel                          │
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
│                    Infrastructure Layer                      │
│  ┌──────────┬──────────┬──────────┬──────────┬────────────┐ │
│  │  Redis   │PostgreSQL│  Qdrant  │MinIO    │  Ollama    │ │
│  └──────────┴──────────┴──────────┴──────────┴────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

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
    │   ├── __init__.py
    │   ├── config.py           # Configuration singleton
    │   ├── contracts.py        # Stable contracts & schemas
    │   ├── model_router.py     # LLM execution (canonical, 15 callers)
    │   ├── model_gateway.py    # Health/status API (auxiliary)
    │   ├── artifact_service.py # Artifact CRUD + versioning (canonical)
    │   ├── workspace_service.py # Workspace CRUD + memory (canonical)
    │   ├── tool_registry.py    # Tool registration + schema export
    │   ├── event_bus.py        # Pub/sub event system
    │   ├── task_queue.py       # Async task execution
    │   ├── memory_layer.py     # Memory layers (working, conversation, knowledge, long-term)
    │   ├── memory.py           # Redis-backed conversation store (migrated from modules/)
    │   ├── vector_store.py     # Qdrant-backed document retrieval (extracted from modules/)
    │   ├── cognitive_kernel.py # Cognitive service orchestration
    │   ├── cognitive/          # Cognitive primitives
    │   │   ├── planner.py      # Plan creation + result review
    │   │   ├── reasoning_engine.py
    │   │   ├── debate_engine.py
    │   │   ├── self_verification.py
    │   │   ├── simulation_engine.py
    │   │   ├── world_model.py
    │   │   ├── strategic_planner.py
    │   │   └── continuous_learning.py
    │   ├── adaptive_runtime.py # Dynamic pipeline composition
    │   ├── execution_session.py # Execution session lifecycle
    │   ├── execution_integration.py # Execution + artifact integration
    │   ├── goal_engine.py      # Goal tracking
    │   ├── workflow_engine.py  # DAG execution
    │   ├── long_task.py        # Resumable workflows
    │   ├── background_tasks.py # Async job queue
    │   ├── decision_engine.py  # Option selection
    │   ├── cost_optimizer.py   # Model cost selection
    │   ├── meta_cognition.py   # Pipeline selection + optimization
    │   ├── agent_reputation.py # Agent scoring
    │   ├── experience.py       # Experience learning
    │   ├── organization.py     # Organization tree
    │   ├── governance.py       # Policy engine
    │   ├── observability.py    # Tracing + metrics
    │   ├── state_recovery.py   # Checkpointing
    │   ├── evaluation.py       # Benchmark framework
    │   ├── mcp_registry.py     # MCP tool registry
    │   ├── notification_service.py # Notification dispatch
    │   ├── plugin_marketplace.py  # Plugin CRUD
    │   ├── semantic_graph.py   # Knowledge graph
    │   ├── skill_registry.py   # Skill registration
    │   ├── sandbox.py          # Code execution sandbox
    │   └── security_model.py   # Security policy model
    └── agents/                 # Agent implementations
        ├── orchestrator_v2.py  # Primary orchestrator
        └── meta_planner.py     # Meta-planning
frontend/                       # Next.js frontend (not yet started)
apps/                            # Capability pack consumers
benchmarks/                      # Performance + quality benchmarks
```

## Dependency Rules

```
apps → sdk → kernel
apps → runtime → kernel
studio → runtime → kernel
marketplace → runtime → kernel
plugins → kernel
capability_packs → apps → sdk → kernel
capability_packs → runtime → kernel
```

**Forbidden:**
- kernel → runtime, sdk, apps, capability_packs
- runtime → apps, sdk, capability_packs
- sdk → runtime
- capability_packs → kernel

## Contract Versioning

All contracts are versioned and backward-compatible within major versions.

```
Contract v1.x → Stable, backward-compatible
Contract v2.x → Breaking changes, migration guide provided
```

## Plugin Manifest Format

```yaml
name: my-plugin
version: 1.0.0
description: Plugin description
author: Author Name
license: MIT
capabilities:
  - networking
  - mikrotik
permissions:
  - read
  - execute
required_contracts:
  - tool: >=1.0.0
  - capability: >=1.0.0
required_runtime: ">=1.0.0"
security_level: safe
dependencies: []
tags:
  - networking
  - mikrotik
```

## Security Model

1. **Declaration**: Capability Pack / Plugin declares required permissions
2. **Validation**: Platform validates against security policies
3. **Sandbox**: Plugin/capability pack runs in isolated environment
4. **Approval**: Privileged operations require manual approval
5. **Monitoring**: All actions are audited

## Capability Excellence

Capability Excellence is the state where each Capability Pack can solve real-world problems consistently, explainably, safely, and measurably through both synthetic and real-world benchmarks, without requiring any changes to the Core Platform.

All Capability Pack improvements must originate from:
1. Documented real usage in `real_cases/<capability_id>/`
2. Benchmark measurements across 6 dimensions: Accuracy, Completeness, Explainability, Safety, Efficiency, Consistency
3. Objective evaluation, not assumptions

The Core is frozen. Capability Packs evolve.
