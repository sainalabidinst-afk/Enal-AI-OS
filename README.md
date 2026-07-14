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

## Quick Start

```bash
# Clone and setup
git clone https://github.com/sainalabidinst-afk/Enal-AI-OS.git
cd Enal-AI-OS

# Start infrastructure
docker-compose up -d

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

## Current Focus: Product Intelligence v1.0.0-dev

Milestone: Backend Baseline + Frontend MVP + Telemetry + Benchmark + Capability Scoring + Quality Intelligence.

### Quality Gate

| Metric | Status |
|--------|--------|
| **Telemetry** | Active — JSONL event collection + KPI aggregation |
| **Benchmark** | Active — Async runner with concurrency control |
| **Capability Score** | Active — 5-dimension scoring per vendor |
| **CCE** | Active — Regression detection, trend analysis, confidence calibration |
| **Quality Gate** | Active — CI fails on regression ≥5 points |

![CCE](https://img.shields.io/badge/CCE-Pending-blue)
![License](https://img.shields.io/badge/License-MIT-green)

> **Note:** The CCE badge shows the latest average capability score. It is updated automatically by GitHub Actions after each push to `main`. First run requires backend to be accessible in CI environment.

### Official Capability Packs

| Capability Pack | Current Expertise | Target |
|-----------------|-------------------|--------|
| **Network Engineer** | MikroTik RouterOS analysis | A (≥90) |
| **Code Engineer** | Full-stack generation, review | A- (≥85) |
| **Research Assistant** | RAG-powered research | A- (≥85) |
| **DevOps Assistant** | CI/CD automation | B+ (≥80) |
| **Trading Analyst** | Market analysis (Certification Gate) | B+ (≥80) |
| **Self Development** | Project improvement | A (≥90) |

### Network Engineer MVP

The first reference app demonstrating ECP's capabilities:

- **Upload** RouterOS config (.rsc)
- **Parse** and understand topology
- **Analyze** for security and performance issues
- **Generate** configurations from requirements
- **Simulate** before deployment
- **Document** automatically

**Why Network Engineer?**
- Unique differentiation from generic AI coding assistants
- Demonstrates full ECP stack: SDK, Runtime, Contracts, Marketplace, Studio
- Real-world production use case
- First of 6 Official Capability Packs

## Documentation

- [Getting Started](docs/getting_started.md)
- [Agent Development Guide](docs/agent_guide.md)
- [Tool Development Guide](docs/tool_guide.md)
- [API Reference](docs/api_reference.md)
- [Architecture](docs/architecture.md)
- [SDK Reference](sdk/README.md)
- [v1 Roadmap](docs/v1_roadmap.md)

## Roadmap

- [x] v0.1.0 — Core architecture and cognitive runtime
- [x] Backend Baseline v1.0.0-dev — Canonical Consolidation complete
- [x] Frontend MVP v1.0.0-dev — Next.js interface complete
- [x] Product Intelligence v1.0.0-dev — Telemetry, Benchmark, Capability Score, CCE
- [ ] Capability Baseline v1.0.0-dev — Each capability meets target KPI
- [ ] v1.0.0 — Developer Preview (6 certified Capability Packs, dogfooding complete)
- [ ] v1.1.0 — Capability Excellence (all packs raised one grade)
- [ ] v1.2.0 — Community Ecosystem (Marketplace, community packs)
- [ ] v1.3.0 — Enterprise (multi-tenant, SLA, governance)

## Capability Quality Targets

| Capability Pack | Target | Score Source |
|-----------------|--------|--------------|
| Network Engineer | ≥95 | benchmarks/cce.py |
| Cisco | ≥90 | benchmarks/cce.py |
| Fortinet | ≥90 | benchmarks/cce.py |
| Linux | ≥90 | benchmarks/cce.py |
| Windows | ≥90 | benchmarks/cce.py |
| VMware | ≥85 | benchmarks/cce.py |
| Dell | ≥85 | benchmarks/cce.py |
| Aruba | ≥85 | benchmarks/cce.py |
| UniFi | ≥90 | benchmarks/cce.py |
| Code Engineer | A- (≥85) | benchmarks/capability_benchmark.py |
| Research Assistant | A- (≥85) | benchmarks/capability_benchmark.py |
| DevOps Assistant | B+ (≥80) | benchmarks/capability_benchmark.py |
| Trading Analyst | B+ (≥80, lulus Certification) | benchmarks/capability_benchmark.py |
| Self Development | A (≥90) | benchmarks/capability_benchmark.py |

> **Source of truth:** Capability scores are computed by `benchmarks/cce.py` via `GET /api/v1/benchmark/capability-scores`. Every capability must pass benchmark + telemetry + real cases before being considered complete.

## License

MIT
