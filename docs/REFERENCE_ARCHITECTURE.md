# Reference Architecture — Enal Cognitive Platform (ECP)

**Version:** 1.0.0  
**Based on:** `docs/AES_ARCHITECTURE.md`  
**Status:** 🟢 Active  

---

## Table of Contents

1. [Purpose](#1-purpose)
2. [What is a Reference Architecture](#2-what-is-a-reference-architecture)
3. [Architecture Building Blocks](#3-architecture-building-blocks)
4. [Application Types on ECP](#4-application-types-on-ecp)
5. [Building an Application on ECP](#5-building-an-application-on-ecp)
6. [Architecture Decision Framework](#6-architecture-decision-framework)
7. [Patterns Catalog](#7-patterns-catalog)
8. [Anti-Patterns](#8-anti-patterns)
9. [Quality Attributes](#9-quality-attributes)
10. [Architecture Evolution](#10-architecture-evolution)
11. [Related Documents](#11-related-documents)

---

## 1. Purpose

This Reference Architecture extends the AES (Architecture Engineering Specification) by providing:

- **Reusable patterns** for building applications on ECP
- **Decision framework** for architects building new capability packs or applications
- **Quality attribute tradeoffs** and how to evaluate them
- **Evolution guidance** for growing the platform without breaking the baseline

**Audience:** Solution architects, senior engineers, and platform teams building on ECP.

---

## 2. What is a Reference Architecture

A Reference Architecture is a **template architecture** that:

1. Identifies the key **architectural building blocks**
2. Defines **how blocks interact** (contracts, protocols, data flow)
3. Documents **proven patterns** and known **anti-patterns**
4. Provides **decision criteria** for choosing approaches

It is NOT a rigid blueprint. It is a **starting point** that application teams adapt to their specific domain requirements while maintaining platform compatibility.

### Relationship to Other Documents

```
Engineering Baseline (what is frozen)
        │
        ▼
AES Architecture (how the platform is built)
        │
        ▼
Reference Architecture (how to build ON the platform) ← ANDA DISINI
        │
        ▼
Application Development Guide (step-by-step for app teams)
```

---

## 3. Architecture Building Blocks

ECP provides these reusable building blocks for any application:

### 3.1 Core Blocks (Provided by Platform)

| Block | Component | How to Use |
|---|---|---|
| **Perception** | `CognitiveKernel.perception` | Feed user input, get structured entities/intents |
| **Memory** | `MemoryManager` (7 layers) | Store/retrieve/search across memory hierarchies |
| **Reasoning** | `ReasoningEngine` | Generate hypotheses, chain reasoning steps |
| **Planning** | `StrategicPlanner` / `AIPlanner` | Decompose goals into actionable plans |
| **Decision** | `DecisionEngine` | Evaluate options, select with confidence |
| **Reflection** | `ReflectionService` | Self-review outputs for quality |
| **Learning** | `ContinuousLearning` | Extract learning signals from outcomes |
| **Debate** | `DebateEngine` | Multi-perspective output verification |
| **Simulation** | `SimulationEngine` | What-if analysis before execution |
| **Verification** | `SelfVerification` | Post-execution correctness checking |

### 3.2 Infrastructure Blocks (Provided by Platform)

| Block | Component | Abstraction |
|---|---|---|
| **Event Bus** | `EventBus` | Redis Streams — pub/sub + persistent |
| **Task Queue** | `TaskQueue` | In-memory async queue |
| **Execution** | `ExecutionIntegration` | Session + scheduler + progress |
| **Model Router** | `ModelRouter` | LiteLLM — multi-provider LLM access |
| **State Recovery** | `StateRecovery` | Checkpoint/restore for long tasks |
| **Governance** | `Governance` | Approval workflows, tenant isolation |
| **Security** | `SecurityModel` | RBAC, audit logging |

### 3.3 Extension Points (For Application Teams)

| Extension Point | What to Implement | Example |
|---|---|---|
| **Capability Pack** | `BaseApp` subclass + `get_app()` factory | `NetworkEngineerApp` |
| **Vendor Parser** | Parse config → Universal AST models | `mikrotik.py` → `UniversalFirewallRule` |
| **Custom Worker** | Task handler for society runtime | `network_worker.py` |
| **Plugin** | Plugin manifest + handler | MikroTik plugin |
| **API Route** | FastAPI router module | `api/chat.py` |
| **Event Handler** | Subscribe to event type | `task.completed` → notify |

---

## 4. Application Types on ECP

Based on the existing capability packs, ECP supports these application archetypes:

### 4.1 Analysis Applications

**Description:** Analyze input data, produce insights and recommendations.

**Examples:** Network Engineer (config analysis), Code Engineer (code review)

**Common Pipeline:**
```
Perception → Memory → Reasoning → Decision → Reflection
```

**Key Blocks:** Perception, Memory, Reasoning, Knowledge Graph

### 4.2 Generation Applications

**Description:** Generate artifacts (configs, code, documents) from specifications.

**Examples:** Network Engineer (config generation), Code Engineer (patch generation)

**Common Pipeline:**
```
Perception → Planning → Reasoning → Decision → Action → Reflection
```

**Key Blocks:** Planning, Action, Verification, Debate

### 4.3 Assistant Applications

**Description:** Interactive chat-based assistant with memory and context.

**Examples:** Research Assistant, DevOps Assistant, Self-Development

**Common Pipeline:**
```
Perception → Memory → Reasoning → Decision → Reflection → Learning
```

**Key Blocks:** Memory (conversation + session), Continuous Learning

### 4.4 Automation Applications

**Description:** Execute multi-step workflows with monitoring and recovery.

**Examples:** DevOps (CI/CD orchestration), Trading (strategy execution)

**Common Pipeline:**
```
Perception → Planning → Execution → Verification → Reflection
```

**Key Blocks:** Execution Integration, State Recovery, Governance

---

## 5. Building an Application on ECP

### 5.1 Step-by-Step Process

```
Step 1: Define Domain Scope
        │
        ▼
Step 2: Identify Required Building Blocks
        │
        ▼
Step 3: Implement Capability Pack
        │
        ▼
Step 4: Register Skills
        │
        ▼
Step 5: Implement Custom Logic
        │
        ▼
Step 6: Add Tests
        │
        ▼
Step 7: Register API Routes (if needed)
        │
        ▼
Step 8: Integrate with Orchestration
```

### 5.2 Step Details

#### Step 1: Define Domain Scope

```markdown
Domain: Network Engineering
Scope: Configuration analysis, generation, compliance checking
Boundary: Starts from config text, ends at validated configuration
Exclusions: Real-time network monitoring, traffic analysis
```

#### Step 2: Identify Required Building Blocks

```python
required_blocks = [
    "perception",    # Parse config text
    "memory",        # Recall vendor knowledge
    "reasoning",     # Analyze config patterns
    "decision",      # Select fixes
    "reflection",    # Verify output quality
]
```

#### Step 3: Implement Capability Pack

```python
# apps/my_app/__init__.py
from apps.base import BaseApp

class MyApp(BaseApp):
    @property
    def capabilities(self) -> list[str]:
        return ["my-domain:analyze", "my-domain:generate"]

    @property
    def pipeline(self) -> list[str]:
        return ["perception", "memory", "reasoning", "decision"]

def get_app() -> BaseApp:
    return MyApp()
```

#### Step 4: Register Skills

```yaml
# agents/skills.yaml
skills:
  - id: "my-domain:analyze"
    name: "My Domain Analysis"
    pack: "my_app"
    description: "Analyze domain-specific input"
    pipeline: ["perception", "memory", "reasoning", "decision"]
```

#### Step 5: Implement Custom Logic

Place domain-specific logic in the app module. Keep core cognitive services generic.

```
apps/my_app/
├── __init__.py           # App class + factory
├── analyzer.py           # Domain analysis logic
├── generator.py          # Output generation
└── models.py             # Domain data models
```

#### Step 6: Add Tests

```python
# tests/test_my_app.py
import pytest
from apps.my_app import get_app

@pytest.mark.asyncio
async def test_my_app_analyze():
    app = get_app()
    result = await app.analyze("test input")
    assert result["status"] == "success"
```

#### Step 7: Register API Routes

```python
# backend/app/api/my_app.py
from fastapi import APIRouter
from apps.my_app import get_app

router = APIRouter(prefix="/my-app")

@router.post("/analyze")
async def analyze(input: str):
    app = get_app()
    return await app.analyze(input)
```

#### Step 8: Integrate with Orchestration

```python
# Register in unified_orchestrator._extract_skills()
if "my-keyword" in task_lower:
    skills.append("my-domain")
```

---

## 6. Architecture Decision Framework

### 6.1 Decision Categories

| Category | When to Use | Requires ADR |
|---|---|---|
| **Core Platform Change** | Modifying Event Bus, Memory Manager, Cognitive Kernel | ✅ Yes |
| **New Capability Pack** | Adding a new domain application | ❌ No (unless it breaks existing contracts) |
| **New Infrastructure** | Adding PostgreSQL, new LLM provider, new queue | ✅ Yes (if it changes data flow) |
| **API Contract Change** | Modifying public endpoint signatures | ✅ Yes (backward compatibility required) |
| **Internal Refactor** | Restructuring within a module | ❌ No |
| **New Pattern** | First use of a new architectural pattern | ✅ Yes |

### 6.2 Decision Flowchart

```
Do you need to change ECP?
        │
        ├── Modify core (Event Bus, Kernel, Memory)?
        │   └── ✅ ADR required + Baseline freeze review
        │
        ├── Add new capability pack?
        │   └── ❌ No ADR needed. Follow Reference Architecture
        │
        ├── Change public API?
        │   ├── Backward compatible? → ❌ No ADR
        │   └── Breaking change? → ✅ ADR + deprecation period
        │
        └── Change infrastructure?
            ├── Additive (new feature)? → ❌ No ADR
            └── Replacing (swap component)? → ✅ ADR required
```

### 6.3 Tradeoff Evaluation Template

```markdown
## Decision: [Title]

### Options Considered
1. Option A: [description]
2. Option B: [description]

### Evaluation Criteria
| Criterion | Weight | Option A | Option B |
|---|---|---|---|
| Development effort | 30% | 8/10 | 5/10 |
| Runtime performance | 25% | 7/10 | 9/10 |
| Maintainability | 25% | 9/10 | 6/10 |
| Platform alignment | 20% | 8/10 | 7/10 |

### Recommendation
Option A: [rationale]

### Consequences
- Positive: [benefits]
- Negative: [tradeoffs]
- Mitigation: [how to address negative]
```

---

## 7. Patterns Catalog

### Pattern 1: Lazy Singleton

**Context:** Avoid circular imports at module load time.

**Solution:**

```python
# Instead of module-level instantiation:
event_bus = EventBus()  # ❌ May cause circular imports

# Use lazy initialization:
_event_bus = None

def get_event_bus() -> EventBus:
    global _event_bus
    if _event_bus is None:
        _event_bus = EventBus()
    return _event_bus
```

**Used in:** `unified_orchestrator.py`, `event_bus.py`

---

### Pattern 2: Pipeline Execution

**Context:** Execute a sequence of cognitive services where each service enriches a shared context.

**Solution:**

```python
async def execute_pipeline(pipeline: list[str], context: dict) -> dict:
    result = context
    for service_name in pipeline:
        service = services[service_name]
        result = await service.process(result)
        result[f"{service_name}_result"] = result
    return result
```

**Used in:** `cognitive_kernel.py`, `adaptive_runtime.py`

---

### Pattern 3: Universal AST

**Context:** Support multiple vendor formats without N×M complexity.

**Solution:**

```
vendor_config → [Vendor Parser] → UniversalAST → [Analysis/Gemeration]
                                      │
                                      ├── UniversalFirewallRule
                                      ├── UniversalNATRule
                                      ├── UniversalBGP
                                      └── UniversalInterface
```

**Used in:** `apps/network_engineer/`, `attachments/parsers/network/`

---

### Pattern 4: Event-Driven Decoupling

**Context:** Modules must communicate without direct coupling.

**Solution:**

```python
# Publisher: No knowledge of subscribers
await event_bus.publish(Event(
    event_type="task.completed",
    payload={"task_id": task.id, "result": result},
    source="execution_scheduler",
))

# Subscriber: No knowledge of publishers
event_bus.subscribe("task.completed", handle_task_completed)
```

**Used in:** `event_bus.py` — cross-module communication

---

### Pattern 5: Memory Consolidation

**Context:** Prevent unbounded memory growth while retaining important information.

**Solution:**

```
threshold exceeded → collect entries → LLM summary → consolidate → store in long-term → delete originals
```

**Trigger:** Automatic when any memory layer exceeds 50 entries.

**Used in:** `memory_layer.py`

---

### Pattern 6: Cognitive Pipeline Selection

**Context:** Different task complexities require different cognitive processing depth.

**Solution:**

```python
complexity = cognitive_budget.estimate(task)
pipeline = PIPELINE_PRESETS[complexity]
# TRIVIAL → 4 services (fast, cheap)
# COMPLEX → 10 services (thorough, expensive)
```

**Used in:** `adaptive_runtime.py`

---

## 8. Anti-Patterns

### Anti-Pattern 1: Direct Cross-Module Call

```python
# ❌ ANTI-PATTERN: Direct import between capability packs
from apps.code_engineer import CodeEngineerApp
network_app = NetworkEngineerApp()
network_app._code_engineer = CodeEngineerApp()  # Tight coupling!

# ✅ CORRECT: Use Event Bus
await event_bus.publish(Event(
    event_type="code:analyze",
    payload={"code": config_script},
    source="network_engineer",
    target="code_engineer",
))
```

### Anti-Pattern 2: Core Importing Apps

```python
# ❌ ANTI-PATTERN: Core module imports app
from apps.network_engineer import NetworkEngineerApp
# This creates a circular dependency: apps → core → apps

# ✅ CORRECT: Apps import core, not the other way
from backend.app.core.adaptive_runtime import adaptive_runtime
```

### Anti-Pattern 3: Direct Infrastructure Access from Apps

```python
# ❌ ANTI-PATTERN: App accesses infrastructure directly
import redis.asyncio as aioredis
redis = aioredis.from_url("redis://localhost")

# ✅ CORRECT: Use platform abstractions
from backend.app.core.memory_layer import memory_manager
await memory_manager.store("working", key, value)
```

### Anti-Pattern 4: Bypassing Pipeline

```python
# ❌ ANTI-PATTERN: Direct service call bypassing pipeline
from backend.app.core.decision_engine import decision_engine
result = await decision_engine.decide(options, context)
# Bypasses perception, memory, reasoning, planning

# ✅ CORRECT: Use pipeline
from backend.app.core.cognitive_kernel import cognitive_kernel
result = await cognitive_kernel.execute_pipeline(
    ["perception", "memory", "reasoning", "decision"],
    {"input": task}
)
```

### Anti-Pattern 5: Unbounded Memory Growth

```python
# ❌ ANTI-PATTERN: Store without consolidation plan
await memory_manager.store("episodic", key, value)
# Never called: await memory_manager.compress_memory("episodic")

# ✅ CORRECT: Automatic consolidation via threshold
# MemoryManager enforces compression at threshold=50
```

---

## 9. Quality Attributes

### 9.1 Quality Attribute Tradeoffs

| Attribute | How ECP Addresses | Tradeoff |
|---|---|---|
| **Performance** | Pipeline selection minimizes unnecessary services | Less thorough for complex tasks when misclassified |
| **Scalability** | Event Bus enables horizontal scaling; memory consolidation bounds growth | Redis dependency adds operational complexity |
| **Reliability** | State Recovery for long tasks; Event Bus persistence | Additional storage for checkpoint data |
| **Security** | RBAC via SecurityModel; tenant isolation via Governance | Additional latency on auth checks |
| **Maintainability** | Loose coupling via Event Bus; clear dependency rules | Event flow is implicit — requires documentation |
| **Testability** | 368 unit tests; memory layers are mockable | Integration tests require Redis/PostgreSQL |
| **Extensibility** | Capability Pack pattern; plugin system | New packs must implement BaseApp contract |
| **Observability** | Telemetry events across all operations | Additional event bus traffic |

### 9.2 Measuring Quality Attributes

| Attribute | Metric | Target | Measurement |
|---|---|---|---|
| Performance | P95 response time | < 30s for MEDIUM pipeline | Benchmark runner |
| Reliability | Task success rate | > 99% | Execution session logs |
| Code Quality | MyPy errors | 0 | `mypy apps/ backend/` |
| Test Quality | Test pass rate | > 95% | `pytest` |
| Coverage | Line coverage | > 80% | `pytest --cov` |
| Memory | Memory layer size | < 50 entries before consolidation | `memory_manager.count()` |

---

## 10. Architecture Evolution

### 10.1 Evolution Principles

1. **Preserve the baseline:** Never break frozen contracts without ADR
2. **Add, don't replace:** New functionality should be additive, not replacement
3. **Abstract, don't concretize:** Keep generic patterns in core; domain specifics in apps
4. **Document first:** ADR before implementation for architectural changes

### 10.2 Expected Evolution Paths

| Evolution | Trigger | Approach |
|---|---|---|
| **New LLM provider** | Better model available | Add to `ModelRouter`, no architecture change |
| **New memory backend** | Qdrant/vector search for knowledge | Add new `MemoryLayer` subclass, register in `MemoryManager` |
| **Multi-region deployment** | Production scaling | Event Bus → Kafka/RabbitMQ compatible |
| **New capability pack** | New domain application | Follow Reference Architecture, no core change |
| **Plugin ecosystem** | Third-party extensions | Extend `PluginManifest`, add marketplace |
| **Real-time collaboration** | Multi-user requirement | Add WebSocket to Event Bus, conflict resolution |

### 10.3 Deprecation Policy

1. Mark as deprecated in CHANGELOG.md + doc comment
2. Maintain backward compatibility for 2 minor versions
3. Remove in next major version
4. Provide migration guide

---

## 11. Related Documents

| Document | Location | Purpose |
|---|---|---|
| Engineering Baseline | `docs/ENGINEERING_BASELINE.md` | What is frozen |
| AES Architecture | `docs/AES_ARCHITECTURE.md` | How platform is built |
| Quality Gate Policy | `docs/quality/QUALITY_GATES.md` | Merge rules |
| Architecture Decisions | `docs/adr/ADR-*.md` | Why decisions were made |
| Application Dev Guide | `docs/APP_DEV_GUIDE.md` | Step-by-step for app teams |
| Sprint Hardening Summary | `SPRINT_HARDENING_SUMMARY.md` | What was fixed |
| API Reference | `docs/api_reference.md` | API endpoint documentation |

---

## Document Version History

| Version | Date | Changes |
|---|---|---|
| 1.0.0 | 2024 | Initial Reference Architecture document |

---

*End of Reference Architecture*

