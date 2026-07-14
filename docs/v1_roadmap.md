# ECP v1.0.0 Developer Preview

**Target Release**: Q3 2026
**Status**: In Development
**Goal**: ECP platform is complete. Next phase is Capability Excellence — making each Capability Pack genuinely expert in its domain.

## Success Criteria

ECP v1.0.0-dev is successful if and only if:

1. ✅ **6 Capability Packs** exist and are registered in Capability Graph
2. ✅ **Golden Test Suite** passes with ≥80% pass rate
3. ✅ **CI/CD Pipeline** blocks merges on any failure
4. ✅ **Documentation** covers getting started, SDK, contracts, and architecture
5. ✅ **No Framework Trap** — Core remains stable while Capability Packs evolve
6. ✅ **Architecture Governance** active: Core is frozen, Capability First Rule enforced, all changes require ADR when impacting multiple packs

## Official Capability Packs

### 1. Network Engineer
**Category**: Networking
**Capabilities**: Configuration generation, validation, deployment
**Success Criteria**:
- Configures Mikrotik routers via plugin
- Validates configurations before deployment
- Generates rollback scripts
- Uses knowledge graph for network topology
**Quality Target**: A — 100 real configs, ≥95% accuracy

### 2. Code Engineer
**Category**: Development
**Capabilities**: Full-stack code generation, testing, documentation
**Success Criteria**:
- Generates backend API from requirements
- Generates frontend UI from API spec
- Creates database schema
- Generates tests and documentation
- All components work together
**Quality Target**: B+ — 100 repositories, ≥90% code quality

### 3. Research Assistant
**Category**: Research
**Capabilities**: RAG, knowledge graphs, citation, learning
**Success Criteria**:
- Retrieves relevant documents from knowledge base
- Synthesizes information from multiple sources
- Provides citations for claims
- Learns from research sessions
**Quality Target**: B — 100 research questions, ≥85% citation accuracy

### 4. DevOps Assistant
**Category**: DevOps
**Capabilities**: CI/CD, containerization, deployment
**Success Criteria**:
- Generates Dockerfiles from application requirements
- Creates GitHub Actions workflows
- Deploys to container registry
- Verifies deployment health
**Quality Target**: B — 100 infrastructure scenarios, ≥85% correctness

### 5. Trading Analyst
**Category**: Finance
**Capabilities**: Market analysis, simulation, decision theory
**Success Criteria**:
- Analyzes market data using cognitive pipeline
- Generates trading recommendations with confidence scores
- Uses debate engine for multi-strategy comparison
- Records decisions to experience memory
**Quality Target**: Pending — 100 market scenarios, risk-adjusted returns

### 6. Self Development
**Category**: Platform
**Capabilities**: Architecture analysis, improvement proposal, patch generation, approval workflow
**Success Criteria**:
- Analyzes project structure and identifies bottlenecks
- Generates improvement proposals with risk assessment
- Produces patches and test reports
- Requires explicit user approval before applying changes
**Quality Target**: A- — 10 real projects, ≥80% improvement acceptance

## Golden Test Set

The golden test suite (`benchmarks/golden_test_set.py`) contains:
- 50 simple tasks (basic reasoning, coding, explanation)
- 50 medium tasks (API design, database schema, configuration)
- 50 complex tasks (full-stack apps, distributed systems)
- 50 domain-specific tasks (networking, trading, DevOps, research, self-development)

**Pass Threshold**: ≥80% (160/200 tests)

## CI/CD Pipeline

Every PR must pass:
1. **Lint & Format** — ruff + black
2. **Type Check** — mypy with strict mode
3. **Unit Tests** — pytest with ≥80% coverage
4. **Architecture Test** — package boundary enforcement
5. **Benchmarks** — performance and quality benchmarks
6. **SDK Compatibility** — imports and basic functionality
7. **Plugin Compatibility** — all plugins load correctly
8. **Golden Tests** — full golden test suite

**Merge Policy**: All checks must pass. No exceptions.

## Development Rules

### No Core Changes for Single Capability Improvement

> Capability First Rule: No Core change is allowed to improve a single Capability Pack.

- If one Capability Pack needs a different behavior, the change must stay inside that Capability Pack.
- If 2 or more Capability Packs need the same behavior, an ADR may be submitted with proof from both packs.
- Core changes require ADR approval and cross-capability proof.

### No New Engines Without Use Case

Any new engine, module, or abstraction must:
1. Be required by at least two Capability Packs
2. Have a golden test case
3. Be documented in architecture docs

### Kernel Stability

The kernel (`backend/app/core/`) must:
- Remain under 5000 lines of code
- Have zero external dependencies beyond stdlib + pydantic
- Maintain backward-compatible contracts
- Pass all tests on every commit

### Capability Pack Independence

Capability Packs must not import other Capability Pack engines directly.
All cross-pack communication flows through Execution Runtime and shared contracts only.

### Capability Benchmark Requirement

Each Capability Pack must define and maintain a benchmark:
- Minimum 100 scenarios for A/B grade targets
- Minimum 10 projects for A-/B+ grade targets
- Benchmark must cover: Accuracy, Completeness, Explainability, Safety, Efficiency, Consistency
- Results must be reproducible and persisted in `benchmarks/`

### Real-world Benchmark Requirement

Each Capability Pack must maintain a `real_cases/<capability_id>/` directory containing:
- Real input/output pairs from actual usage
- Evaluation notes for each case
- Links to synthetic benchmark updates driven by real findings

Real-world cases are the primary source of Capability Pack improvement. Synthetic benchmarks validate improvements; real-world cases drive them.
5. Not import other Capability Pack engines directly

## Timeline

| Release | Target Date | Focus |
|---------|-------------|-------|
| v1.0.0-dev | Q3 2026 | Platform complete, Architecture Governance active |
| v1.0.0 | Q4 2026 | Developer Preview: all packs certified, documentation, SDK, Studio |
| v1.1.0 | Q1 2027 | Capability Excellence: raise all packs one grade |
| v1.2.0 | Q2 2027 | Community Ecosystem: Marketplace, community packs |
| v1.3.0 | Q3 2027 | Enterprise: governance, multi-tenant, SLA |

## Metrics to Track

| Metric | Target | Measurement |
|--------|--------|-------------|
| Golden Test Pass Rate | ≥80% | benchmarks/golden_test_set.py |
| Test Coverage | ≥80% | pytest-cov |
| Type Safety | 0 errors | mypy --strict |
| Architecture Violations | 0 | benchmarks/package_boundaries.py |
| SDK Import Time | <100ms | sdk/benchmarks |
| Capability Quality Score | ≥85% | benchmarks/capability_benchmark.py |
| Improvement Velocity | >0 real cases/week per pack | real_cases/<capability_id>/ |
| Documentation Coverage | 100% | docs/ |

## Developer Preview Quality Targets

Certification requires each Capability Pack to meet or exceed the following benchmark scores:

| Capability | Target Score | Grade |
|------------|--------------|-------|
| Network | ≥90 | A |
| Code | ≥85 | A- |
| Research | ≥85 | A- |
| DevOps | ≥80 | B+ |
| Trading | ≥80 | B+ (must also pass Certification) |
| Self Development | ≥90 | A |

All scores are measured by the 6-dimension Capability Benchmark framework.

---

## Knowledge Expansion Plan

All planned knowledge additions are tracked via RFCs and implemented inside Capability Packs only. Core remains unchanged.

### Network Engineer

**Planned additions:**
- Cisco Design Guide: campus, data center, SD-WAN, HA
- MikroTik Best Practice: ISP edge, hotspot, IPv6, FastTrack
- Fortinet Hardening: FortiOS, policy, VPN, threat protection
- BGP: path selection, filtering, communities, monitoring
- MPLS: forwarding, LDP, VRF, traffic engineering basics
- IPv6: dual-stack, SLAAC, DHCPv6, transition mechanisms
- Zero Trust: principles, micro-segmentation, ZTNA

**Reference RFC:** RFC-0004

### Code Engineer

**Planned additions:**
- Clean Architecture: layers, dependency rule, boundaries
- DDD: bounded contexts, aggregates, domain events, anti-corruption
- SOLID: all 5 principles with Python/TypeScript examples
- CQRS: command/query separation, write/read models
- Event Sourcing: event store, replay, projection
- Secure Coding: OWASP Top 10, injection, auth, secrets

**Reference RFC:** RFC-0006

### Trading Analyst

**Planned additions:**
- Wyckoff: phases, composite operator, supply/demand
- ICT: market structure, FVG, order blocks, liquidity
- SMC: institutional flow, liquidity sweeps, premium/discount
- Elliott Wave: impulse/corrective patterns, Fibonacci
- Volume Profile: POC, value area, volume patterns
- Macro: indicators, Fed policy, risk-on/off
- Options: Greeks, strategies, IV, unusual activity
- Futures: contango/backwardation, basis, COT
- Psychology: biases, risk tolerance, emotional management

**Reference RFC:** RFC-0005

---

## Post Developer Preview Releases

### v1.1.0 — Capability Excellence
- Network A+
- Trading B+
- Research A-
- Code A
- All packs improved through knowledge and benchmark work

### v1.2.0 — Community Ecosystem
- Marketplace launch
- Community Capability Pack support
- Capability Pack SDK templates
- Third-party pack certification process

### v1.3.0 — Enterprise
- Enterprise Capability Roadmap
- Advanced governance and audit features
- Multi-tenant support
- SLA and compliance tooling

---

## 12-Month Capability Roadmap

### Q1 — Trading Certification & Developer Preview
- Complete Trading Analyst Certification
- Developer Preview release
- 500 real cases across all Capability Packs

### Q2 — Capability Excellence
- Network A+
- Code A
- Trading A-
- All packs improved one grade through knowledge and real-world benchmark work

### Q3 — Community Ecosystem
- Marketplace Beta launch
- Community Capability Pack support
- Capability Pack SDK templates
- Third-party pack certification process

### Q4 — Enterprise Release
- 1,000+ real cases across all Capability Packs
- All Capability Packs have public benchmark dashboards
- Enterprise: governance, multi-tenant, SLA

---

## Capability Changelog

Each Capability Pack maintains its own changelog. The changelog records knowledge additions, benchmark improvements, and reasoning enhancements. It does not record Core changes.

### Format

```markdown
## <Capability Pack> v<version>

### Added
- <knowledge/topic>

### Improved
- <aspect>

### Fixed
- <issue>

### Benchmark
- <dimension>: <before> → <after>
```

### Example

```markdown
## Network v1.1

### Added
- BGP path selection analysis
- MPLS forwarding rules
- IPv6 dual-stack patterns

### Improved
- Firewall explanation depth
- Risk scoring accuracy: 85% → 92%

### Fixed
- VLAN false positive on trunk interfaces

### Benchmark
- Accuracy: 89% → 92%
- Explainability: B → A-
```

---

## 5-Year Free Roadmap

### Phase 0 — Architecture Complete ✅
- Core, Capability Contract, Worker, Conversation, Governance, ADR, UX Contract
- Cost: Free

### Phase 1 — Capability Excellence (0–12 months)
- Network: MikroTik → Expert Multi-Vendor
- Code: Generation → Expert Review + Architecture
- Trading: Analysis → Expert Reasoning
- Research: RAG → Expert Evidence Synthesis
- DevOps: CI/CD → Expert Multi-Cloud
- Target: 1,000 real cases, all packs A-/A/B+

### Phase 2 — Universal Workspace (6–18 months)
- Workspace becomes AI-native knowledge base
- Timeline, Knowledge, Files, Tasks, Progress, Decisions, Lessons
- Cost: Free

### Phase 3 — Local AI Stack (12–24 months)
- Ollama + Qwen/DeepSeek/Llama/Gemma
- Model Router selects best open-source model per capability
- All inference local or free-tier
- Cost: Free

### Phase 4 — Enal Models (24–36 months)
- EnalCoder: fine-tuned Qwen/DeepSeek for coding
- EnalNetwork: fine-tuned Llama on network configs
- EnalTrading: fine-tuned Qwen on trading patterns
- All via LoRA, no pretraining
- Cost: Low (single GPU or occasional cloud)

### Phase 5 — Continuous Learning (Ongoing)
- Real cases → Review → Knowledge Update → Benchmark
- Daily improvement cycle

### Phase 6 — Community (36–48 months)
- Marketplace for Capability Packs
- Community packs: SAP, AWS, Odoo, MikroTik, Fortinet, Cisco ACI
- Third-party certification

### Phase 7 — Foundation Model (48–60 months, conditional)
- Only if users >100k, revenue stable, GPUs available
- EnalLM: purpose-built for ECP execution
- Not a GPT clone, but execution-optimized model

---

## Model Strategy: Progressive Independence

**Year 1:** 100% external models (Claude, GPT, Gemini, Qwen, DeepSeek)
**Year 2:** 80% external, 20% Enal models
**Year 3:** 50% external, 50% Enal models
**Year 5:** 90% Enal models

The Model Router makes this transparent to users and Capability Packs.
All Capability Packs continue to work without changes regardless of model source.
