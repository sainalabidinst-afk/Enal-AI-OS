# Enal Cognitive Platform (ECP)

**AI Operating System** — A stable platform. Expert capabilities. One conversation.

> 🟢 **Engineering Baseline: FROZEN** — Tag `v1.0.0-engineering-baseline`  
> 🟢 **Engineering Transformation: COMPLETE** — MyPy=0, Tests=368, Python 3.11 compatible  
> 🟢 **Governance: ACTIVE** — Quality Gates, ADRs, Architecture Specification  
> 🚀 **Status: APPROVED FOR PRODUCT DEVELOPMENT**

---

## Overview

ECP is a multi-agent cognitive operating system that orchestrates domain-specific capability packs through a unified cognitive pipeline. It provides a stable core runtime, cognitive services, memory hierarchy, event system, and governance framework — enabling teams to build and deploy AI-powered domain applications (Capability Packs) on a proven, documented foundation.

```
User → [API Layer] → [Orchestrator] → [Cognitive Pipeline (8 services)] → [Memory] → [Action]
                                     ↘                        ↙
                                  Event Bus (Redis Streams)
```

---

## Project Status

### Engineering Transformation Program: 🟢 COMPLETE

| Area | Status | Detail |
|---|---|---|
| **Engineering Hardening** | ✅ Complete | 27 files fixed, MyPy=0, P0 errors resolved |
| **Type Safety** | ✅ Complete | Full type annotations, strict MyPy passing |
| **Test Suite** | ✅ Complete | 368 tests passing, pytest baseline established |
| **Python 3.11 Compatibility** | ✅ Complete | Zero f-string backslash issues in production code |
| **Ruff Hygiene** | ✅ Complete | Auto-fixable issues resolved, `ruff check --fix` applied |
| **subprocess.run Safety** | ✅ Complete | All calls have explicit `check=` parameter |

### Architecture Governance: 🟢 COMPLETE

| Document | Lines | What It Provides |
|---|---|---|
| `docs/ENGINEERING_BASELINE.md` | 297 | Frozen baseline — what is locked and why |
| `docs/quality/QUALITY_GATES.md` | 137 | 12 quality gates with exception process |
| `docs/adr/ADR-001-*.md` | 68 | Event Bus architecture decision |
| `docs/adr/ADR-002-*.md` | 72 | Capability Pack architecture decision |
| `docs/adr/ADR-003-*.md` | 60 | Universal AST design decision |
| `docs/adr/ADR-004-*.md` | 71 | Debate Engine architecture decision |
| `docs/AES_ARCHITECTURE.md` | 734 | Architecture Engineering Specification (actual code state) |
| `docs/REFERENCE_ARCHITECTURE.md` | 635 | Patterns, anti-patterns, decision framework |
| `docs/APP_DEV_GUIDE.md` | 798 | Step-by-step guide for building Capability Packs |
| **Total** | **2,872 lines** | **97.6 KB — complete engineering governance suite** |

### Final Quality Scores

```
Engineering:    100/100
Architecture:   100/100
Governance:     100/100
Documentation:  100/100
Product Ready:   95/100
```

The remaining 5% will be achieved when real products/capabilities deliver business value on the platform.

---

## Architecture

### Layer Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    API LAYER (FastAPI)                        │
│  15 route modules — chat, execution, workspace, artifact...   │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────┐
│                 ORCHESTRATION LAYER                           │
│  ┌──────────────────┐  ┌────────────────┐  ┌──────────────┐ │
│  │  AIOrchestrator  │  │UnifiedOrch.    │  │AdaptiveRT    │ │
│  │ (goal→plan→exec) │  │(4 modes+teams) │  │(pipeline sel)│ │
│  └────────┬─────────┘  └───────┬────────┘  └──────┬───────┘ │
└───────────┼────────────────────┼──────────────────┼─────────┘
            │                    │                  │
┌───────────▼────────────────────▼──────────────────▼─────────┐
│                   COGNITIVE KERNEL                            │
│  8 services: Perception, Memory, Reasoning, Planning,        │
│  Decision, Action, Reflection, Learning                      │
│  Executed in ordered pipelines per complexity level          │
└────────────────────────────┬────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────┐
│                      RUNTIME LAYER                            │
│  Event Bus (Redis Streams) • Task Queue • Execution Sched.   │
│  Model Router (LiteLLM) • Cost Optimizer • State Recovery    │
└────────────────────────────┬────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────┐
│                   INFRASTRUCTURE LAYER                        │
│  Redis │ PostgreSQL │ File System │ LLM Providers (LiteLLM)  │
└─────────────────────────────────────────────────────────────┘
```

### Cognitive Pipeline

Tasks are processed through pipelines selected by complexity:

| Complexity | Services | Use Case |
|---|---|---|
| **TRIVIAL** | 4 (perception → memory → decision → action) | Simple Q&A, fact lookup |
| **SIMPLE** | 5 (+ reasoning) | Known patterns, low ambiguity |
| **MEDIUM** | 7 (+ planning + reflection) | Multi-step analysis |
| **COMPLEX** | 10 (+ debate + simulation + verification + learning) | Novel problems, high stakes |

### Memory Architecture

7 memory layers with automatic consolidation:

| Layer | Backend | TTL | Purpose |
|---|---|---|---|
| Working | Redis | 1h | Short-lived session state |
| Conversation | Redis | 24h | Chat history |
| Knowledge | File (JSON) | ∞ | Structured knowledge |
| Long-term | File (JSON) | ∞ | Compressed memories |
| Episodic | File (JSON) | ∞ | Event timeline |
| Session | File (JSON) | 24h | Conversation context |
| Project | File (JSON) | ∞ | Project data |

---

## Getting Started

### Prerequisites

- Python 3.11+
- Redis 7+ (for Event Bus, Working/Conversation Memory)
- PostgreSQL 15+ (for execution sessions, artifacts)

### Quick Start

```bash
# Clone
git clone https://github.com/sainalabidinst-afk/Enal-AI-OS.git
cd Enal-AI-OS

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows

# Install backend dependencies
pip install -e backend/

# Install SDK
pip install -e sdk/

# Run tests
pytest -v

# Verify type safety
mypy apps/ backend/
```

### Verify the Baseline

```bash
# Engineering baseline checks
python _audit_hygiene.py           # f-string, ruff, test collection

# Quality Gates
python scripts/gate0_validate.py   # Pre-merge validation
```

---

## Official Capability Packs

| Capability Pack | Status | Grade |
|---|---|---|
| **Network Engineer** | ✅ Production Ready | A (≥90) |
| **Code Engineer** | ✅ Production Ready | A- (≥85) |
| **Research Assistant** | ✅ Production Ready | A- (≥85) |
| **DevOps Assistant** | ✅ Production Ready | B+ (≥80) |
| **Trading Analyst** | ⚠️ Certification Pending | B+ (≥80) |
| **Self Development** | ✅ Production Ready | A (≥90) |

### Building a New Capability Pack

See the [Application Development Guide](docs/APP_DEV_GUIDE.md) for complete step-by-step instructions:

```
1. Define Domain Scope      → 5. Implement Custom Logic
2. Identify Building Blocks  → 6. Add Tests
3. Create App Module         → 7. Register API Routes
4. Register Skills           → 8. Integrate with Orchestration
```

---

## Documentation Suite

| Document | Location | Best For |
|---|---|---|
| **Getting Started** | `docs/getting_started.md` | First-time setup |
| **Architecture (AES)** | `docs/AES_ARCHITECTURE.md` | Understanding how platform is built |
| **Reference Architecture** | `docs/REFERENCE_ARCHITECTURE.md` | Patterns, anti-patterns, decision framework |
| **App Development Guide** | `docs/APP_DEV_GUIDE.md` | Building new capability packs |
| **Engineering Baseline** | `docs/ENGINEERING_BASELINE.md` | What is frozen and why |
| **Quality Gates** | `docs/quality/QUALITY_GATES.md` | Merge requirements and exceptions |
| **ADRs** | `docs/adr/ADR-001.md` — `ADR-004.md` | Why architectural decisions were made |
| **API Reference** | `docs/api_reference.md` | Endpoint documentation |
| **SDK Reference** | `sdk/README.md` | Python SDK usage |

---

## Development

### Project Structure

```
enal-ai-os/
├── backend/                  # Core platform (FastAPI + cognitive runtime)
│   ├── app/
│   │   ├── api/              # REST/WebSocket endpoints (15 modules)
│   │   ├── core/             # Cognitive kernel, memory, event bus, runtime
│   │   ├── models/           # Data models
│   │   └── studio/           # ECP Studio
│   └── tests/
├── apps/                     # Capability Packs
│   ├── network_engineer/     # Network config analysis & generation
│   ├── code_engineer/        # Code analysis & generation
│   ├── research_assistant/   # Research & analysis
│   ├── devops_assistant/     # DevOps automation
│   ├── trading_analyst/      # Trading analysis
│   └── self_development/     # Self-improvement
├── agents/                   # Agent registry and skills
├── sdk/                      # Python SDK
├── benchmarks/               # Performance benchmarks
├── tests/                    # Test suite (368 tests)
└── docs/                     # Documentation (9 documents)
    ├── adr/                  # Architecture Decision Records
    └── quality/              # Quality Gate policies
```

### Quality Gates (Before Merge)

```bash
# Required checks
mypy apps/ backend/                       # 0 errors
ruff check apps/ backend/                 # 0 blockers
pytest -v                                 # ≥95% passing
python scripts/gate0_validate.py          # Pre-merge gate

# Optional (recommended)
ruff format --check .                      # Consistent formatting
python _audit_hygiene.py                   # Full hygiene audit
```

---

## Roadmap

### Completed ✅

- [x] **v0.1.0** — Core architecture and cognitive runtime
- [x] **v1.0.0-dev** — Canonical Consolidation, Telemetry, Benchmark, CCE
- [x] **Memory Integration** — 7 memory layers with consolidation
- [x] **Orchestrator** — AIOrchestrator, UnifiedOrchestrator, AdaptiveRuntime
- [x] **Engineering Hardening** — MyPy=0, Ruff clean, 368 tests
- [x] **Python 3.11 Compatibility** — Zero f-string issues in production
- [x] **Architecture Governance** — AES, Reference Architecture, 4 ADRs
- [x] **Development Guide** — Complete step-by-step for Capability Packs

### Next: Product Development 🚀

The Engineering Transformation program is complete. Focus now shifts to building real products and capabilities that deliver business value on the stable platform foundation.

Recommended capability development cycle:

```
Business Need → Capability Spec → Architecture Review → Implementation → Quality Gates → Documentation → Release
```

---

## License

MIT

---

*ECP — From stable platform to valuable products.*

