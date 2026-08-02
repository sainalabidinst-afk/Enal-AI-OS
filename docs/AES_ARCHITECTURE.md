<!-- BILINGUAL_DOCS_START -->
## Bahasa Indonesia / English


### Ringkasan / Summary
Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.
> Terjemahan Indonesia: Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.

- Bahasa Indonesia: konten utama tetap dipertahankan dalam dokumen asli, dan bagian ini memberi konteks ringkas dalam bahasa Indonesia.
- English: the main content remains in the original document, and this section provides a concise bilingual context for international readers.

### Informasi Dokumen / Document Info
- File: `docs/AES_ARCHITECTURE.md`
- Judul: Aes Architecture
- Status: bilingual header added

<!-- BILINGUAL_DOCS_END -->

# AES — Architecture Engineering Specification


**Document Version:** 1.0.0  
**Baseline Tag:** `v1.0.0-engineering-baseline`  
**Classification:** Internal — Engineering Reference  

---

## Table of Contents

1. [System Overview](#1-system-overview)
2. [Layer Architecture](#2-layer-architecture)
3. [Module Dependency Graph](#3-module-dependency-graph)
4. [Runtime Flow](#4-runtime-flow)
5. [Event Flow](#5-event-flow)
6. [Public API Contracts](#6-public-api-contracts)
7. [Memory Architecture](#7-memory-architecture)
8. [Cognitive Pipeline](#8-cognitive-pipeline)
9. [Capability Pack Architecture](#9-capability-pack-architecture)
10. [Quality Gates](#10-quality-gates)
11. [Testing Strategy](#11-testing-strategy)
12. [Coding Standards](#12-coding-standards)

---

## 1. System Overview

ECP (Enal Cognitive Platform) is a multi-agent cognitive operating system that orchestrates domain-specific capability packs through a unified cognitive pipeline. The architecture follows an event-driven, layered design with strict dependency rules.
> Terjemahan Indonesia: ECP (Enal kognitif platform) adalah sebuah multi-agen kognitif sistem operasi itu orchestrates domain-specific kapabilitas packs through sebuah unified kognitif jalur. arsitektur follows sebuah event-driven, layered design dengan strict dependency rules.

### Architectural Principles


- **Layered isolation:** Each layer communicates only with adjacent layers
- **Event-driven:** Cross-module communication via Event Bus
- **Pipeline execution:** Cognitive services execute in ordered pipelines determined by task complexity
- **Plugin-first:** Capability packs extend functionality without modifying core
- **Memory hierarchy:** 7 memory layers with automatic consolidation

### High-Level Architecture Diagram


```
┌──────────────────────────────────────────────────────────────────┐
│                        USER INTERFACE                            │
│  (REST API / WebSocket / CLI)                                    │
└────────────────────────────┬─────────────────────────────────────┘
                             │
┌────────────────────────────▼─────────────────────────────────────┐
│                     API LAYER (FastAPI)                          │
│  backend/app/api/ — 15 route modules                             │
│  - chat, execution, workspace, artifact, telemetry,              │
│    benchmark, model_gateway, capability_discovery, etc.          │
└────────────────────────────┬─────────────────────────────────────┘
                             │
┌────────────────────────────▼─────────────────────────────────────┐
│                  ORCHESTRATION LAYER                             │
│  ┌──────────────────┐  ┌──────────────────┐  ┌────────────────┐ │
│  │  AIOrchestrator  │  │ UnifiedOrch.     │  │ AdaptiveRuntime│ │
│  │(orchestrator_v2) │  │(unified_orch.)   │  │(adaptive_rt.)  │ │
│  └────────┬─────────┘  └────────┬─────────┘  └───────┬────────┘ │
└───────────┼──────────────────────┼──────────────────────┼────────┘
            │                      │                      │
┌───────────▼──────────────────────▼──────────────────────▼────────┐
│                   COGNITIVE KERNEL                               │
│  ┌──────────┬──────────┬──────────┬──────────┬──────────────┐   │
│  │Perception│  Memory  │Reasoning │ Planning │   Decision    │   │
│  └──────────┴──────────┴──────────┴──────────┴──────────────┘   │
│  ┌──────────┬──────────┬──────────┬──────────┬──────────────┐   │
│  │  Action  │Reflection│ Learning │  Debate  │  Simulation  │   │
│  └──────────┴──────────┴──────────┴──────────┴──────────────┘   │
└────────────────────────────┬─────────────────────────────────────┘
                             │
┌────────────────────────────▼─────────────────────────────────────┐
│                      RUNTIME LAYER                               │
│  ┌──────────────┬─────────────────┬──────────────────────────┐  │
│  │  Event Bus   │   Task Queue     │  Execution Integration  │  │
│  │ (Redis Pub/  │ (in-memory async)│  (scheduler + progress) │  │
│  │  Sub+Streams)│                  │                          │  │
│  └──────────────┴─────────────────┴──────────────────────────┘  │
│  ┌──────────────┬─────────────────┬──────────────────────────┐  │
│  │Model Router  │  Cost Optimizer │   State Recovery         │  │
│  │(LLM routing) │  (budget-aware) │   (checkpoint/restore)   │  │
│  └──────────────┴─────────────────┴──────────────────────────┘  │
└────────────────────────────┬─────────────────────────────────────┘
                             │
┌────────────────────────────▼─────────────────────────────────────┐
│                    INFRASTRUCTURE LAYER                          │
│  ┌──────────┬──────────┬──────────┬──────────┬────────────────┐ │
│  │  Redis   │PostgreSQL│  Qdrant  │ File Sys │  External LLM  │ │
│  │(cache/   │(metadata)│(vectors) │(memory)  │  (LiteLLM)     │ │
│  │ events)  │          │          │          │                │ │
│  └──────────┴──────────┴──────────┴──────────┴────────────────┘ │
└──────────────────────────────────────────────────────────────────┘
```

---

## 2. Layer Architecture

### 2.1 API Layer — `backend/app/api/`


**Purpose:** HTTP/REST interface for external consumers. No business logic.

| Module | Endpoints | Auth |
|--------|-----------|------|
| `chat.py` | `POST /chat`, WebSocket `/ws/chat` | Session token |
| `execution.py` | `POST /execute`, `GET /execute/{id}`, WebSocket progress | API key |
| `workspace.py` | CRUD `/workspaces` | API key |
| `artifact.py` | CRUD `/artifacts` | API key |
| `telemetry.py` | `GET /telemetry/metrics`, `GET /telemetry/traces` | Internal |
| `health.py` | `GET /health` | None |
| `model_gateway.py` | `GET /models`, `POST /models/{id}/test` | API key |
| `capability_discovery.py` | `GET /capabilities` | API key |
| `benchmark.py` | `POST /benchmark/run`, `GET /benchmark/results` | Internal |
| `notifications.py` | WebSocket `/ws/notifications` | Session token |
| `orchestrator_v2.py` | `POST /orchestrate` | API key |
| `attachments.py` | `POST /attachments/upload` | API key |

### 2.2 Orchestration Layer


Three orchestrators exist with distinct responsibilities:
> Terjemahan Indonesia: Three orchestrators exist dengan distinct responsibilities:

| Orchestrator | File | Responsibility |
|---|---|---|
| **AIOrchestrator** | `agents/orchestrator_v2.py` | Top-level: goal → perception → plan → execute. Single-entry point for external consumers |
| **UnifiedOrchestrator** | `core/unified_orchestrator.py` | Multi-mode: DIRECT, COGNITIVE, MULTI_AGENT, WORKFLOW. Dynamic team formation |
| **AdaptiveCognitiveRuntime** | `core/adaptive_runtime.py` | Pipeline-based: selects cognitive pipeline based on task complexity budget |

**Resolution order:** AIOrchestrator → UnifiedOrchestrator → AdaptiveCognitiveRuntime → CognitiveKernel

### 2.3 Cognitive Kernel — `backend/app/core/cognitive_kernel.py`


8 cognitive services executed in ordered pipelines:
> Terjemahan Indonesia: 8 kognitif services executed dalam ordered pipelines:

| Service | Class | Responsibility |
|---|---|---|
| Perception | `PerceptionService` | Input processing, entity/intent extraction, memory retrieval |
| Memory | `MemoryService` | Relevant memory search across layers |
| Reasoning | `ReasoningService` | Hypothesis generation, reasoning chains, decision logic |
| Planning | `PlanningService` | Strategic roadmap creation |
| Decision | `DecisionService` | Multi-option evaluation and selection |
| Action | `ActionService` | Action plan formulation |
| Reflection | `ReflectionService` | Self-review of decisions and outputs |
| Learning | `LearningService` | Quality scoring, learning signal extraction |

### 2.4 Runtime Layer

| Component | File | Technology |
|---|---|---|
| Event Bus | `core/event_bus.py` | Redis Streams + in-memory subscribers |
| Task Queue | `core/task_queue.py` | In-memory asyncio queue |
| Execution Integration | `core/execution_integration.py` | Custom scheduler + progress |
| Model Router | `core/model_router.py` | LiteLLM-based routing |
| Cost Optimizer | `core/cost_optimizer.py` | Token budget estimation |
| State Recovery | `core/state_recovery.py` | Checkpoint/restore |

### 2.5 Infrastructure Layer


| Component | Purpose | Access Pattern |
|---|---|---|
| Redis | Event Bus streams, cache, working memory | `redis.asyncio` |
| PostgreSQL | Execution sessions, artifacts metadata | SQLAlchemy async |
| Qdrant | Vector search for knowledge memory | `qdrant-client` |
| File System | Memory persistence (knowledge, long-term, episodic, session, project) | JSON files in `workspace/memory/` |
| LLM Providers | OpenAI, Anthropic, Ollama, etc. | LiteLLM unified interface |

---

## 3. Module Dependency Graph


### 3.1 Dependency Rules (Enforced)


```
apps/ ──────────► backend/app/core/ ──────────► infrastructure
   │                      │
   └──► backend/app/api/  └──► backend/app/agents/
```

**Strict rules:**

1. `apps/*` → `backend.app.core.*` : Allowed (via imports)
2. `backend.app.api.*` → `backend.app.core.*` : Allowed
3. `backend.app.agents.*` → `backend.app.core.*` : Allowed
4. `backend.app.core.*` → `apps.*` : **FORBIDDEN**
5. `backend.app.core.*` → `backend.app.api.*` : **FORBIDDEN**
6. `apps/network_engineer` → `apps/code_engineer` : **FORBIDDEN** (cross-capability)
7. All cross-module communication: must use Event Bus

### 3.2 Actual Dependency Map


```
main.py
  ├── api/chat.py ────────────► core/cognitive_kernel.py
  │                              ├── core/memory_layer.py
  │                              ├── core/decision_engine.py
  │                              ├── core/cognitive/reasoning_engine.py
  │                              ├── core/cognitive/strategic_planner.py
  │                              ├── core/cognitive/world_model.py
  │                              ├── core/reflection.py
  │                              └── core/model_router.py
  ├── api/execution.py ───────► core/execution_integration.py
  │                              ├── core/execution_session.py
  │                              ├── core/artifact_service.py
  │                              ├── core/workspace_service.py
  │                              └── core/notification_service.py
  ├── api/workspace.py ───────► core/workspace_service.py
  ├── api/artifact.py ────────► core/artifact_service.py
  ├── agents/orchestrator_v2.py
  │    ├── core/perception_engine.py
  │    └── apps/organization/ai_planner.py
  ├── core/unified_orchestrator.py
  │    ├── core/cognitive_kernel.py
  │    ├── core/adaptive_runtime.py
  │    ├── core/organization.py
  │    ├── apps/organization/ai_planner.py
  │    └── apps/organization/multi_agent.py
  └── core/adaptive_runtime.py
       ├── core/cognitive_kernel.py
       ├── core/cognitive_budget.py
       ├── core/cost_optimizer.py
       └── core/model_router.py
```

### 3.3 Lazy Singleton Pattern


To prevent circular imports at module load time, core components use lazy singletons:
> Terjemahan Indonesia: Untuk prevent circular imports at module load time, core components use lazy singletons:

```python
# Pattern used in: unified_orchestrator.py, event_bus.py
_unified_orchestrator = None

def get_unified_orchestrator() -> UnifiedOrchestrator:
    global _unified_orchestrator
    if _unified_orchestrator is None:
        _unified_orchestrator = UnifiedOrchestrator()
    return _unified_orchestrator
```

Components using this pattern:
> Terjemahan Indonesia: Components using ini pattern:
- `UnifiedOrchestrator` (lazy)
- `EventBus` (module-level instance)
- `CognitiveKernel` (module-level `cognitive_kernel`)
- `MemoryManager` (module-level `memory_manager`)
- `AdaptiveCognitiveRuntime` (module-level `adaptive_runtime`)

---

## 4. Runtime Flow

### 4.1 Request Lifecycle


```
1. HTTP Request ──► FastAPI Router
                         │
2.                      │
                  ┌──────▼──────┐
                  │ Parse input │  ← chat.py / execution.py
                  │ Validate    │
                  └──────┬──────┘
                         │
3.                      │
                  ┌──────▼──────────┐
                  │ Orchestration   │  ← AIOrchestrator
                  │ (goal → plan)   │     or UnifiedOrchestrator
                  └──────┬──────────┘
                         │
4.                      │
                  ┌──────▼────────────┐
                  │ Pipeline Selection│  ← AdaptiveCognitiveRuntime
                  │ (complexity-based)│     budget.estimate(task)
                  └──────┬────────────┘
                         │
5.                      │
                  ┌──────▼────────────┐
                  │ Cognitive Pipeline│  ← CognitiveKernel
                  │ 8 services in     │     execute_pipeline()
                  │ ordered sequence  │
                  └──────┬────────────┘
                         │
6.                      │
                  ┌──────▼────────────┐
                  │ Result Aggregation│
                  │ + Artifact         │  ← artifact_service
                  │ + Notification     │  ← notification_service
                  └──────┬────────────┘
                         │
7. HTTP Response ◄────────┘
```

### 4.2 Pipeline Selection Logic


```python
PIPELINE_PRESETS = {
    TRIVIAL:    ["perception", "memory", "decision", "action"],
    SIMPLE:     ["perception", "memory", "reasoning", "decision", "action"],
    MEDIUM:     ["perception", "memory", "planning", "reasoning",
                 "decision", "reflection", "action"],
    COMPLEX:    ["perception", "memory", "planning", "reasoning",
                 "debate", "simulation", "decision", "verification",
                 "reflection", "learning"],
    VERY_COMPLEX: ["perception", "memory", "planning", "reasoning",
                   "debate", "simulation", "decision", "verification",
                   "reflection", "learning"],
}
```

Each pipeline service consumes the previous service's output (`context`) and produces enriched output. The chain is:
> Terjemahan Indonesia: Each jalur layanan consumes previous layanan's output (context) dan produces enriched output. chain adalah:

```
context = {"input": user_input}
→ perception (adds entities, intents, memories)
→ memory     (adds relevant_memories)
→ reasoning  (adds hypotheses, chain, decision)
→ planning   (adds roadmap)
→ decision   (adds selected_option, confidence)
→ action     (adds action plan)
→ reflection (adds review, score)
→ learning   (adds quality_score, suggestions)
```

### 4.3 Execution Session Flow


```
POST /execute ──► ExecutionIntegration.execute()
                     │
               ┌─────▼─────┐
               │ Create     │  ← execution_session_manager
               │ Session    │
               └─────┬─────┘
                     │
               ┌─────▼─────┐
               │ Build      │  ← ExecutionGraph (DAG of tasks)
               │ Graph      │     understand → plan → execute → verify
               └─────┬─────┘
                     │
               ┌─────▼─────┐
               │ Submit     │  ← ExecutionScheduler
               │ Queue      │
               └─────┬─────┘
                     │
               ┌─────▼──────────┐
               │ × N tasks      │
               │  Each: run →   │
               │  complete/fail │
               └─────┬──────────┘
                     │
               ┌─────▼──────┐
               │ Create      │  ← artifact_service
               │ Artifact    │
               └─────┬──────┘
                     │
               ┌─────▼────────┐
               │ Notify       │  ← WebSocket / notification
               │ Complete     │
               └─────┬────────┘
                     │
               Return ExecutionSession ◄──
```

---

## 5. Event Flow

### 5.1 Event System Architecture


```
┌─────────────────────────────────────────────┐
│                 EventBus                      │
│  ┌──────────────────────────────────────┐   │
│  │         Redis Streams                 │   │
│  │  enal:events:task.created            │   │
│  │  enal:events:execution.progress      │   │
│  │  enal:events:memory.consolidated     │   │
│  │  enal:events:notification.sent       │   │
│  └──────────────────────────────────────┘   │
│  ┌──────────────────────────────────────┐   │
│  │      In-Memory Subscribers            │   │
│  │  {event_type: [handler_fn, ...]}     │   │
│  └──────────────────────────────────────┘   │
└─────────────────────────────────────────────┘
```

### 5.2 Event Data Model

```python
@dataclass
class Event:
    event_type: str           # e.g., "task.completed"
    payload: dict[str, Any]   # Event-specific data
    source: str               # Publisher component
    target: str = "*"         # Subscriber filter
    timestamp: datetime       # UTC
    correlation_id: str | None = None  # Trace ID
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class EventEnvelope:
    event: Event
    stream: str               # Redis stream name
    id: str | None = None     # Unique envelope ID
```

### 5.3 Known Event Types


| Event Type | Publisher | Consumer(s) | Payload |
|---|---|---|---|
| `task.created` | ExecutionScheduler | NotificationService, Telemetry | `{task_id, name, session_id}` |
| `task.completed` | ExecutionScheduler | NotificationService, ArtifactService | `{task_id, result}` |
| `task.failed` | ExecutionScheduler | NotificationService, StateRecovery | `{task_id, error}` |
| `memory.consolidated` | MemoryManager | LearningService | `{block_id, source_layer, summary}` |
| `execution.progress` | ExecutionIntegration | WebSocket clients | `{session_id, progress, status}` |
| `notification.sent` | NotificationService | Telemetry | `{recipient, channel, message}` |

### 5.4 Publish-Subscribe Pattern


```python
# Publishing
await event_bus.publish(Event(
    event_type="task.completed",
    payload={"task_id": "task-1", "result": {...}},
    source="execution_scheduler",
    correlation_id=session.correlation_id,
))

# Subscribing
event_bus.subscribe("task.completed", my_handler)
```

---

## 6. Public API Contracts


### 6.1 REST API Endpoints


| Method | Path | Request | Response | Status |
|---|---|---|---|---|
| `POST` | `/chat` | `{message, session_id, project_id?}` | `{reply, session_id, artifacts[]}` | ✅ Stable |
| `POST` | `/execute` | `{goal, workspace_id, conversation_id?}` | `{session_id, status}` | ✅ Stable |
| `GET` | `/execute/{id}` | — | `ExecutionSession` | ✅ Stable |
| `GET` | `/execute/{id}/stream` | WebSocket | Progress events (SSE) | ✅ Stable |
| `POST` | `/workspaces` | `{name, description?}` | `Workspace` | ✅ Stable |
| `GET` | `/workspaces` | — | `Workspace[]` | ✅ Stable |
| `GET` | `/workspaces/{id}` | — | `Workspace` | ✅ Stable |
| `POST` | `/artifacts` | `{workspace_id, name, type, content}` | `Artifact` | ✅ Stable |
| `GET` | `/artifacts/{id}` | — | `Artifact` | ✅ Stable |
| `GET` | `/capabilities` | `?query=` | `Capability[]` | ✅ Stable |
| `POST` | `/orchestrate` | `{goal, mode?, context?}` | `{session_id, plan_id, steps}` | ✅ Stable |
| `GET` | `/health` | — | `{status, version, uptime}` | ✅ Stable |
| `POST` | `/attachments/upload` | Multipart file | `{attachment_id, parsed?}` | ✅ Stable |
| `GET` | `/telemetry/metrics` | `?range=` | `Metrics` | ⚠️ Internal |

### 6.2 WebSocket Endpoints


| Path | Direction | Message Format |
|---|---|---|
| `/ws/chat/{session_id}` | Bidirectional | JSON `{type, content, metadata}` |
| `/ws/execution/{session_id}` | Server → Client | JSON `{type, status, progress, data}` |
| `/ws/notifications/{user_id}` | Server → Client | JSON `{type, message, timestamp, metadata}` |

### 6.3 Internal Interfaces


| Interface | Provider | Consumer | Method |
|---|---|---|---|
| `CognitiveService.process(context)` | 8 service classes | `CognitiveKernel` | `async` |
| `MemoryLayer.store/retrieve/search/delete` | 7 memory layers | `MemoryManager` | `async` |
| `EventBus.publish/subscribe/consume` | `EventBus` | All modules | `async` |
| `ModelRouter.complete/embed/generate` | `ModelRouter` | All cognitive services | `sync` |

---

## 7. Memory Architecture


### 7.1 Memory Layers

| Layer | Class | Backend | TTL | Purpose |
|---|---|---|---|---|
| **Working** | `WorkingMemory` | Redis | 1 hour | Short-lived session state |
| **Conversation** | `ConversationMemory` | Redis | 24 hours | Chat history |
| **Knowledge** | `KnowledgeMemory` | File (JSON) | ∞ | Structured knowledge |
| **Long-term** | `LongTermMemory` | File (JSON) | ∞ | Compressed memories |
| **Episodic** | `EpisodicMemory` | File (JSON) | ∞ | Events + timeline |
| **Session** | `SessionMemory` | File (JSON) | 24 hours | Conversation context |
| **Project** | `ProjectMemory` | File (JSON) | ∞ | Project-focused data |

### 7.2 Memory Architecture Diagram


```
                   MemoryManager
                        │
        ┌───────────────┼───────────────┐
        │               │               │
   ┌────▼────┐    ┌─────▼─────┐    ┌────▼────┐
   │  Redis  │    │File System │    │ Qdrant  │
   │ Working │    │ Knowledge  │    │(planned)│
   │ Conv.   │    │ Long-term  │    │         │
   │         │    │ Episodic   │    │         │
   └─────────┘    │ Session    │    └─────────┘
                  │ Project    │
                  └────────────┘
```

### 7.3 Memory Consolidation


When a memory layer exceeds threshold (default: 50 entries), the `MemoryManager.compress_memory()` method:
> Terjemahan Indonesia: When sebuah memory layer exceeds threshold (default: 50 entries), MemoryManager.compress_memory() method:

1. Collects entries from the source layer
2. Generates a summary via LLM (`model_router.complete()`)
3. Creates a `ConsolidatedBlock` with source IDs
4. Stores the compressed block in long-term memory
5. Deletes the original entries

```python
async def compress_memory(self, layer: str, threshold: int = 50):
    keys = await self._layers[layer].list_keys()
    if len(keys) > threshold:
        block = await self.consolidate(layer, "", max_entries=threshold)
        if block:
            await self.store("longterm", block.block_id, block.consolidated_content)
            for k in block.source_ids:
                await self._layers[layer].delete(k)
```

---

## 8. Cognitive Pipeline

### 8.1 Pipeline Services


Each cognitive service implements:
> Terjemahan Indonesia: Each kognitif layanan implements:

```python
class CognitiveService(ABC):
    @abstractmethod
    async def process(self, context: dict[str, Any]) -> dict[str, Any]:
        """Process and return enriched context."""
```

### 8.2 Service Input/Output Contracts


| Service | Input (from context) | Output (added to context) |
|---|---|---|
| `perception` | `input`, `project_id` | `memories`, `world_entities` |
| `memory` | `perception` | `relevant_memories`, `working_memory` |
| `reasoning` | `perception` | `hypotheses[]`, `chain`, `decision` |
| `planning` | `perception` | `roadmap` |
| `decision` | `options[]`, `perception` | `selected_option_id`, `confidence`, `reasoning` |
| `action` | `decision` | `action`, `parameters` |
| `reflection` | `perception`, `decision` | `review`, `score`, `passed` |
| `learning` | `reflection` | `learned`, `quality_score`, `suggestions` |

### 8.3 Pipeline Complexity Levels


| Complexity | Criteria | Pipeline Length | Estimated Duration |
|---|---|---|---|
| **TRIVIAL** | Single fact lookup, simple Q&A | 4 services | < 2s |
| **SIMPLE** | Known pattern, low ambiguity | 5 services | 2-5s |
| **MEDIUM** | Multi-step, moderate analysis | 7 services | 5-15s |
| **COMPLEX** | Novel problem, high stakes | 10 services | 15-60s |
| **VERY COMPLEX** | Strategic, cross-domain, high uncertainty | 10 services | 30-120s |

---

## 9. Capability Pack Architecture


### 9.1 Pack Structure

```
apps/
├── __init__.py           # Dynamic loader — discovers and registers packs
├── base.py               # BaseApp abstract class
├── network_engineer/     # Network configuration analysis & generation
│   ├── __init__.py
│   ├── analyzer.py       # Configuration analysis
│   ├── compliance.py     # Compliance checking
│   ├── generator.py      # Configuration generation
│   ├── topology.py       # Network topology
│   ├── verification_engine.py  # Post-change verification
│   ├── ... (15 modules)
│   ├── mikrotik/         # Vendor-specific parser
│   └── nic/              # Network Intelligence Center
├── code_engineer/        # Code analysis & generation
│   ├── __init__.py
│   ├── analyzer.py
│   ├── architecture_reader.py
│   ├── refactoring_engine.py
│   └── ... (9 modules)
├── research_assistant/   # Research & analysis
├── devops_assistant/     # DevOps automation
├── trading_analyst/      # Trading analysis
└── self_development/     # Self-improvement
```

### 9.2 Pack Contract

Each pack must provide:
> Terjemahan Indonesia: Each pack must menyediakan:

```python
# 1. Class inheriting from BaseApp
class NetworkEngineerApp(BaseApp):
    @property
    def capabilities(self) -> list[str]: [...]

# 2. Factory function
def get_app() -> BaseApp:
    return NetworkEngineerApp()
```

### 9.3 Skill Registration


Packs register their capabilities in `agents/skills.yaml`. The `SkillRegistry` loads these at runtime to enable capability discovery.
> Terjemahan Indonesia: Packs register their kapabilitas dalam agen/skills.yaml. SkillRegistry loads these at runtime untuk memungkinkan kapabilitas discovery.

---

## 10. Quality Gates

See `docs/quality/QUALITY_GATES.md` for complete policy.
> Terjemahan Indonesia: See docs/kualitas/QUALITY_GATES.MD untuk complete policy.

**Summary:**

| Gate | Requirement | Severity |
|---|---|---|
| MyPy | 0 errors | 🔴 BLOCKER |
| Tests | ≥95% pass (baseline: 426) | 🔴 BLOCKER |
| API Contract | Backward compatible | 🔴 BLOCKER |
| ADR | Required for architecture changes | 🔴 BLOCKER |
| Ruff Lint | No blockers | 🟡 WARNING |
| Ruff Format | 0 files reformatted | 🟡 WARNING |
| Python 3.11 Compat | No f-string backslash escapes in production | 🔴 BLOCKER |

---

## 11. Testing Strategy

### 11.1 Test Layers

| Layer | Location | Count | Framework |
|---|---|---|---|
| Unit tests | `tests/test_*.py` | 426 | pytest + pytest-asyncio |
| Integration | `backend/tests/` | Via unit tests | pytest |
| Benchmark | `benchmarks/` | 10+ | Custom benchmark runner |
| Real cases | `real_cases/` | 20+ | Dataset-driven validation |

### 11.2 Test Coverage Areas


| Area | Tests | Status |
|---|---|---|
| AI Planner | `test_ai_planner.py` | ✅ |
| Browser Agent | `test_browser_agent.py` | ✅ |
| Capability Execution | `test_capability_execution_engine.py` | ✅ |
| Capability Pipeline | `test_capability_pipeline.py` | ✅ |
| Intent Resolver | `test_intent_resolver.py` | ✅ |
| Memory Layer | `test_memory_layer.py` | ✅ |
| Multi-Agent | `test_multi_agent.py`, `test_multi_agent_coordination.py` | ✅ |
| Observability | `test_observability_tracing.py` | ✅ |
| Plugin | `test_plugin_marketplace.py` | ✅ |
| Reasoning Engine | `test_reasoning_engine.py` | ✅ |
| Reflection | `test_reflection_agent.py` | ✅ |
| Security | `test_security_audit.py` | ✅ |
| Unified Orchestrator | `test_unified_orchestrator.py` | ✅ |
| Voice/Vision | `test_voice_vision_agent.py` | ✅ |

### 11.3 Test Command

```bash
# Run all tests
pytest -v

# Run with coverage
pytest --cov=backend/app --cov=apps

# Run specific test
pytest tests/test_memory_layer.py -v
```

---

## 12. Coding Standards

### 12.1 Python Standards


| Rule | Standard |
|---|---|
| Python version | 3.11+ |
| Type hints | Required on all public functions |
| Line length | 100 characters |
| Imports | Grouped: stdlib → third-party → internal |
| Async | Use `async def` for I/O-bound operations |
| Singletons | Lazy initialization to avoid circular imports |
| Dataclasses | Use `@dataclass` for data containers |
| Enums | Use `StrEnum` or `Enum` for constants |

### 12.2 Naming Conventions


| Element | Convention | Example |
|---|---|---|
| Files | `snake_case.py` | `memory_layer.py` |
| Classes | `PascalCase` | `MemoryManager` |
| Functions | `snake_case` | `get_unified_orchestrator()` |
| Variables | `snake_case` | `memory_manager` |
| Constants | `UPPER_CASE` | `PIPELINE_PRESETS` |
| Private | `_prefix` | `_teams` |
| Type vars | `T` | `T = TypeVar('T')` |

### 12.3 MyPy Configuration


```toml
[tool.mypy]
python_version = "3.11"
strict = false
ignore_missing_imports = true
explicit_package_bases = true
namespace_packages = true
```

### 12.4 Ruff Configuration


```toml
[tool.ruff]
line-length = 100
target-version = "py311"
select = ["E", "F", "I", "N", "W", "UP"]
```

---

## Document Version History


| Version | Date | Changes |
|---|---|---|
| 1.0.0 | 2024 | Initial AES document post-engineering baseline |

---

*End of AES Architecture Specification*
