<!-- BILINGUAL_DOCS_START -->
## Bahasa Indonesia / English

### Ringkasan / Summary

Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.
> Terjemahan Indonesia: Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.

- Bahasa Indonesia: konten utama tetap dipertahankan dalam dokumen asli, dan bagian ini memberi konteks singkat dalam bahasa Indonesia.
- English: the main content remains in the original document, and this section provides a concise bilingual context for international readers.

### Informasi Dokumen / Document Info
- File: `README.md`
- Judul: Readme
- Status: bilingual header added

<!-- BILINGUAL_DOCS_END -->

<!-- DOCUMENT_METADATA_START -->
**Owner:** Documentation Team
**Canonical Owner:** Documentation Governance Lead
**Last Verified:** 2026-08-02
**Version:** 1.0.0
**Status:** Active
**SSOT:** Project overview, installation, quick start, and Capability Pack registry
<!-- DOCUMENT_METADATA_END -->

# Enal Cognitive Platform (ECP)

**AI Operating System** â€” A stable platform. Expert capabilities. One conversation.

> ðŸŸ¢ **Engineering Baseline: FROZEN** â€” Tag `v1.0.0-engineering-baseline`
> ðŸŸ¢ **Engineering Transformation: COMPLETE** â€” MyPy=0, Tests=426, Python 3.11 compatible
> ðŸŸ¢ **Governance: ACTIVE** â€” Quality Gates, ADRs, Architecture Specification
> ðŸš€ **Status: APPROVED FOR PRODUCT DEVELOPMENT**

---

## Overview

ECP is a multi-agent cognitive operating system that orchestrates domain-specific Capability Packs through a unified cognitive pipeline. It provides a stable Core Runtime, cognitive services, Memory hierarchy, event system, and governance framework â€” enabling teams to build and deploy AI-powered domain applications (Capability Packs) on a proven, documented foundation.
> Terjemahan Indonesia: ECP adalah sebuah multi-agen kognitif sistem operasi itu orchestrates domain-specific kapabilitas Packs through sebuah unified kognitif jalur. It menyediakan sebuah stable Core Runtime, kognitif services, Memory hierarchy, event sistem, dan tata kelola kerangka kerja â€” enabling teams untuk membangun dan deploy AI-powered domain applications (kapabilitas Packs) pada sebuah proven, documented foundation.

```
User â†’ [API Layer] â†’ [Orchestrator] â†’ [Cognitive Pipeline (8 services)] â†’ [Memory] â†’ [Action]
                                     â†˜                        â†™
                                  Event Bus (Redis Streams)
```

---

## Project Status

### Engineering Transformation Program: ðŸŸ¢ COMPLETE

| Area | Status | Detail |
|---|---|---|
| **Engineering Hardening** | âœ… Complete | 27 files fixed, MyPy=0, P0 errors resolved |
| **Type Safety** | âœ… Complete | Full type annotations, strict MyPy passing |
| **Test Suite** | âœ… Complete | 426 tests passing, pytest baseline established |
| **Python 3.11 Compatibility** | âœ… Complete | Zero f-string backslash issues in production code |
| **Ruff Hygiene** | âœ… Complete | Auto-fixable issues resolved, `ruff check --fix` applied |
| **subprocess.run Safety** | âœ… Complete | All calls have explicit `check=` parameter |

### Architecture Governance: ðŸŸ¢ COMPLETE

| Document | Lines | What It Provides |
|---|---|---|
| `docs/ENGINEERING_BASELINE.md` | 297 | Frozen baseline â€” what is locked and why |
| `docs/quality/QUALITY_GATES.md` | 137 | 12 quality gates with exception process |
| `docs/adr/ADR-001-*.md` | 68 | Event Bus Architecture decision |
| `docs/adr/ADR-002-*.md` | 72 | Capability Pack Architecture decision |
| `docs/adr/ADR-003-*.md` | 60 | Universal AST design decision |
| `docs/adr/ADR-004-*.md` | 71 | Debate Engine Architecture decision |
| `docs/AES_ARCHITECTURE.md` | 734 | Architecture Engineering Specification (actual code state) |
| `docs/REFERENCE_ARCHITECTURE.md` | 635 | Patterns, anti-patterns, decision framework |
| `docs/APP_DEV_GUIDE.md` | 798 | Step-by-step guide for building Capability Packs |
| **Total** | **2,872 lines** | **97.6 KB â€” complete engineering governance suite** |

### Final Quality Scores

```
Engineering:    100/100
Architecture:   100/100
Governance:     100/100
Documentation:  100/100
Product Ready:   95/100
```

The remaining 5% will be achieved when real products/capabilities deliver business value on the platform.
> Terjemahan Indonesia: Remaining 5% akan menjadi achieved when real products/kapabilitas deliver business value pada platform.

---

## Architecture

### Layer Diagram

```
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚                    API LAYER (FastAPI)                      â”‚
â”‚  15 route modules â€” chat, execution, workspace, artifact... â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                          â”‚
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â–¼â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚                 ORCHESTRATION LAYER                         â”‚
â”‚  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â” â”‚
â”‚  â”‚  AIOrchestrator  â”‚  â”‚UnifiedOrch.    â”‚  â”‚AdaptiveRT    â”‚ â”‚
â”‚  â”‚ (goalâ†’planâ†’exec) â”‚  â”‚(4 modes+teams) â”‚  â”‚(pipeline sel)â”‚ â”‚
â”‚  â””â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜  â””â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”˜  â””â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”˜ â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¼â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¼â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¼â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
             â”‚                    â”‚                  â”‚
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â–¼â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â–¼â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â–¼â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚                   COGNITIVE KERNEL                          â”‚
â”‚  8 services: Perception, Memory, Reasoning, Planning,       â”‚
â”‚  Decision, Action, Reflection, Learning                     â”‚
â”‚  Executed in ordered pipelines per complexity level         â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                              â”‚
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â–¼â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚                      RUNTIME LAYER                          â”‚
â”‚  Event Bus (Redis Streams) â€¢ Task Queue â€¢ Execution Sched.  â”‚
â”‚  Model Router (LiteLLM) â€¢ Cost Optimizer â€¢ State Recovery   â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                              â”‚
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â–¼â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚                   INFRASTRUCTURE LAYER                      â”‚
â”‚  Redis â”‚ PostgreSQL â”‚ File System â”‚ LLM Providers (LiteLLM) â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

### Cognitive Pipeline

Tasks are processed through pipelines selected by complexity:
> Terjemahan Indonesia: Tasks adalah processed through pipelines selected oleh complexity:

| Complexity | Services | Use Case |
|---|---|---|
| **TRIVIAL** | 4 (perception â†’ memory â†’ decision â†’ action) | Simple Q&A, fact lookup |
| **SIMPLE** | 5 (+ reasoning) | Known patterns, low ambiguity |
| **MEDIUM** | 7 (+ planning + reflection) | Multi-step analysis |
| **COMPLEX** | 10 (+ debate + simulation + verification + learning) | Novel problems, high stakes |

### Memory Architecture

7 memory layers with automatic consolidation:
> Terjemahan Indonesia: 7 memory layers dengan automatic consolidation:

| Layer | Backend | TTL | Purpose |
|---|---|---|---|
| Working | Redis | 1h | Short-lived session state |
| Conversation | Redis | 24h | Chat history |
| Knowledge | File (JSON) | âˆž | Structured knowledge |
| Long-term | File (JSON) | âˆž | Compressed memories |
| Episodic | File (JSON) | âˆž | Event timeline |
| Session | File (JSON) | 24h | Conversation context |
| Project | File (JSON) | âˆž | Project data |

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
| **Network Engineer** | âœ… Production Ready | A (â‰¥90) |
| **Code Engineer** | âœ… Production Ready | A- (â‰¥85) |
| **Research Assistant** | âœ… Production Ready | A- (â‰¥85) |
| **DevOps Assistant** | âœ… Production Ready | B+ (â‰¥80) |
| **Trading Analyst** | âœ… Production Ready | B+ (â‰¥80) |
| **Self Development** | âœ… Production Ready | A (â‰¥90) |
| **Decision Intelligence** | âœ… Production Ready | A (â‰¥90) |
| **System Architect** | âœ… Production Ready | A (â‰¥90) |
| **Security Engineer** | âœ… Production Ready | A- (â‰¥85) |
| **Data Engineer** | âœ… Production Ready | A- (â‰¥85) |
| **Database Engineer** | âœ… Production Ready | A- (â‰¥85) |
| **QA Engineer** | âœ… Production Ready | A (â‰¥90) |
| **Business Analyst** | âœ… Production Ready | A- (â‰¥85) |

### Building a New Capability Pack

See the [Application Development Guide](docs/APP_DEV_GUIDE.md) for complete step-by-step instructions:
> Terjemahan Indonesia: See Application Development panduan untuk complete step-oleh-step instructions:

```
1. Define Domain Scope      â†’ 5. Implement Custom Logic
2. Identify Building Blocks  â†’ 6. Add Tests
3. Create App Module         â†’ 7. Register API Routes
4. Register Skills           â†’ 8. Integrate with Orchestration
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
| **ADRs** | `docs/adr/ADR-001.md` â€” `ADR-004.md` | Why architectural decisions were made |
| **API Reference** | `docs/api_reference.md` | Endpoint documentation |
| **SDK Reference** | `sdk/README.md` | Python SDK usage |

---

## Development

### Project Structure

```
enal-ai-os/
â”œâ”€â”€ backend/                  # Core platform (FastAPI + cognitive runtime)
â”‚   â”œâ”€â”€ app/
â”‚   â”‚   â”œâ”€â”€ api/              # REST/WebSocket endpoints (15 modules)
â”‚   â”‚   â”œâ”€â”€ core/             # Cognitive kernel, memory, event bus, runtime
â”‚   â”‚   â”œâ”€â”€ models/           # Data models
â”‚   â”‚   â””â”€â”€ studio/           # ECP Studio
â”‚   â””â”€â”€ tests/
â”œâ”€â”€ apps/                     # Capability Packs
â”‚   â”œâ”€â”€ network_engineer/     # Network config analysis & generation
â”‚   â”œâ”€â”€ code_engineer/        # Code analysis & generation
â”‚   â”œâ”€â”€ research_assistant/   # Research & analysis
â”‚   â”œâ”€â”€ devops_assistant/     # DevOps automation
â”‚   â”œâ”€â”€ trading_analyst/      # Trading analysis
â”‚   â”œâ”€â”€ self_development/     # Self-improvement
â”‚   â”œâ”€â”€ decision_intelligence/     # Decision Intelligence (RFC-0007)
â”‚   â”œâ”€â”€ system_architect/          # System Architect (RFC-0011)
â”‚   â”œâ”€â”€ security_engineer/         # Security Engineer (RFC-0008)
â”‚   â”œâ”€â”€ data_engineer/             # Data Engineer (RFC-0009)
â”‚   â”œâ”€â”€ database_engineer/         # Database Engineer (RFC-0010)
â”‚   â”œâ”€â”€ qa_engineer/               # QA Engineer (RFC-0012)
â”‚   â””â”€â”€ business_analyst/          # Business Analyst (RFC-0013)
â”œâ”€â”€ agents/                   # Agent registry and skills
â”œâ”€â”€ sdk/                      # Python SDK
â”œâ”€â”€ benchmarks/               # Performance benchmarks
â”œâ”€â”€ tests/                    # Test suite (426 tests)
â””â”€â”€ docs/                     # Documentation (9 documents)
    â”œâ”€â”€ adr/                  # Architecture Decision Records
    â””â”€â”€ quality/              # Quality Gate policies
```

### Quality Gates (Before Merge)

```bash
# Required checks
mypy apps/ backend/                       # 0 errors
ruff check apps/ backend/                 # 0 blockers
pytest -v                                 # â‰¥95% passing
python scripts/gate0_validate.py          # Pre-merge gate

# Optional (recommended)
ruff format --check .                     # Consistent formatting
python _audit_hygiene.py                   # Full hygiene audit
```

---

## Roadmap

### Completed âœ…

- [x] **v0.1.0** â€” Core Architecture and cognitive runtime
- [x] **v1.0.0-dev** â€” Canonical Consolidation, Telemetry, Benchmark, CCE
- [x] **Memory Integration** â€” 7 memory layers with consolidation
- [x] **Orchestrator** â€” AIOrchestrator, UnifiedOrchestrator, AdaptiveRuntime
- [x] **Engineering Hardening** â€” MyPy=0, Ruff clean, 426 tests
- [x] **Python 3.11 Compatibility** â€” Zero f-string issues in production
- [x] **Architecture Governance** â€” AES, Reference Architecture, 4 ADRs
- [x] **Development Guide** â€” Complete step-by-step for Capability Packs

### Next: Product Development ðŸš€

The Engineering Transformation program is complete. Focus now shifts to building real products and capabilities that deliver business value on the stable platform foundation.
> Terjemahan Indonesia: Rekayasa Transformation program adalah complete. Focus now shifts untuk building real products dan kapabilitas itu deliver business value pada stable platform foundation.

Recommended capability development cycle:
> Terjemahan Indonesia: Recommended kapabilitas development cycle:

```
Business Need â†’ Capability Spec â†’ Architecture Review â†’ Implementation â†’ Quality Gates â†’ Documentation â†’ Release
```

---

## License

MIT

---

*ECP â€” From stable platform to valuable products.*
