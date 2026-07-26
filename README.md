# Enal Cognitive Platform (ECP)

**AI Operating System** — A stable core. Expert capabilities. One conversation.

## What ECP Provides

| Component | Purpose |
|-----------|---------|
| **ECP Kernel** | Stable contracts, cognitive runtime, and governance layer |
| **ECP Runtime** | Execution scheduler, event bus, task queue |
| **ECP SDK** | Python SDK for building Capability Packs |
| **ECP Studio** | Trace viewer, pipeline debugger, cost dashboard |
| **ECP Marketplace** | Plugin and Capability Pack distribution |
| **ECP Apps** | Official Capability Packs — expert domains ready to use |

## Architecture Status (2026-07-27)

**Platform Release Candidate: 92/100**

| Layer | Assessment |
|-------|------------|
| Cognitive | ✅ 90% - cognitive_kernel + 7 services |
| Knowledge | ✅ 65% - semantic_graph, ontology with BGP/MPLS/CAPsMAN |
| Memory | ✅ 95% - EpisodicMemory, ConversationMemory, KnowledgeMemory, LongTermMemory |
| Multi-Agent | ✅ 80% - organization.py, society/, agents/core/ |
| Tool | ✅ 85% - tool_registry + mcp_registry |
| Workflow | ✅ 85% - Enhanced with retry, checkpoint, resume |
| Collaboration | ✅ 70% - debate_engine, collective_memory |
| Learning | ✅ 75% - Continuous learning with RL, human feedback |
| Evaluation | ✅ 80% - QualityGate, automated regression |
| Security | ✅ 85% - RBAC, audit logging, tenant isolation |
| Governance | ✅ 85% - ApprovalRequest, ApprovalStatus workflow |

## Quick Start

```bash
# Clone and setup
git clone https://github.com/sainalabidinst-afk/Enal-AI-OS.git
cd Enal-AI-OS

# Install dependencies
pip install -e .

# Install SDK
pip install -e sdk/

# Use in your code
from enal_ai import Agent, EnalAI

class MyAgent(Agent):
    name = "my-agent"
    capabilities = ["custom"]

    async def execute(self, task: str) -> str:
        return f"Processed: {task}"

agent = MyAgent()
result = await agent.run("Hello World")
```

## Current Focus: Sprint A - Engineering Hardening

**Goal:** Clean all Severity 8+ Pylance/MyPy issues

| Metric | Status |
|--------|--------|
| **Runtime Tests** | 368 passing |
| **Static Analysis** | 12/12 high-severity issues fixed |
| **Type Safety** | 91% (Pylance contract fixes applied) |

### Completed (Phase 3 - Core Cognitive Services Integration)

- ✅ Memory Engine Enhancement - SessionMemory, ProjectMemory, ranking, compression
- ✅ Orchestrator Unification - AIOrchestrator with perception → planner → memory pipeline
- ✅ Planner Upgrade - estimate_cost(), assess_risk() integrated
- ✅ Executor Enhancement - Checkpoint, Resume, Retry support
- ✅ Perception Engine - Text/Image/JSON processing with entity/intent extraction
- ✅ Learning Enhancement - RLAction, HumanFeedback, policy gradient
- ✅ Evaluation Enhancement - QualityGate with gate history
- ✅ Enterprise Governance - ApprovalRequest, tenant isolation

## Official Capability Packs

| Capability Pack | Status | Grade |
|-----------------|--------|-------|
| **Network Engineer** | ✅ Production Ready | A (≥90) |
| **Code Engineer** | ✅ Production Ready | A- (≥85) |
| **Research Assistant** | ✅ Production Ready | A- (≥85) |
| **DevOps Assistant** | ✅ Production Ready | B+ (≥80) |
| **Trading Analyst** | ⚠️ Certification Pending | B+ (≥80) |
| **Self Development** | ✅ Production Ready | A (≥90) |

## Documentation

- [Getting Started](docs/getting_started.md)
- [Agent Development Guide](docs/agent_guide.md)
- [Tool Development Guide](docs/tool_guide.md)
- [API Reference](docs/api_reference.md)
- [Architecture](docs/architecture.md)
- [SDK Reference](sdk/README.md)

## Roadmap

- [x] v0.1.0 — Core architecture and cognitive runtime
- [x] Backend Baseline v1.0.0-dev — Canonical Consolidation complete
- [x] Product Intelligence v1.0.0-dev — Telemetry, Benchmark, Capability Score, CCE
- [x] Core Cognitive Services Integration - Memory, Orchestrator, Planner, Executor, Perception
- [ ] Sprint A — Engineering Hardening (Static Analysis Clean)
- [ ] Sprint B — Browser & Evidence Engine
- [ ] Sprint C — Reflection Engine
- [ ] Sprint D — Evaluation v2 (Hallucination, Evidence scoring)
- [ ] v1.0.0 — Developer Preview (6 certified Capability Packs)

## License

MIT