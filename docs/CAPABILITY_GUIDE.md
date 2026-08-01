# Capability Guide

This document describes each official Capability Pack, including its scope, knowledge focus, benchmark targets, and explicit out-of-scope boundaries.
Use this as the source of truth for what each Capability Pack is expected to know and not know.

---

## Capability Engineer Status (2026-07-27)
**Platform Release Candidate**

| Capability Pack | Grade | Notes |
|-----------------|-------|-------|
| Network Engineer | A (≥90) | Production Ready |
| Code Engineer | A- (≥85) | Production Ready |
| Research Assistant | A- (≥85) | Production Ready |
| DevOps Assistant | B+ (≥80) | Production Ready |
| Trading Analyst | B+ (≥80) | Certification Pending |
| Self Development | A (≥90) | Production Ready |

---

## Network Engineer

**Capability ID:** `network`
**Category:** Networking
**Quality Target:** A

### Scope

- MikroTik RouterOS v6/v7 configuration analysis
- Topology inference from configuration
- Security and performance audit
- Configuration diff and rollback planning
- Deployment verification and risk assessment
- Compliance audit and health reporting

### Knowledge Focus

- RouterOS syntax and semantics
- Firewall, NAT, routing, DHCP, DNS
- MikroTik-specific best practices
- Enterprise network design patterns
- ISP backbone and edge patterns

### Out of Scope

- Cisco IOS/NX-OS full automation
- Fortinet FortiOS full automation
- BGP/OSPF/MPLS automation
- Multi-router orchestration
- Live device API/SSH execution
- Hardware procurement or cabling

### Benchmark Target

- 100 real MikroTik configs
- ≥95% accuracy on issue detection
- ≥90% recommendation quality

---

## Code Engineer

**Capability ID:** `code`
**Category:** Development
**Quality Target:** A- (≥85) - Production Ready

### Scope

- Backend API design and implementation
- Frontend UI generation from API spec
- Database schema design and migration
- Unit, integration, and E2E test generation
- Documentation generation (API, README, runbooks)
- Code review for correctness, security, and maintainability

### Knowledge Focus

- Python, JavaScript/TypeScript, SQL
- Clean Architecture, DDD, Hexagonal, CQRS
- REST and GraphQL API design
- Database indexing, query optimization
- Testing strategies and coverage patterns
- Security: injection, auth, secrets handling

### Out of Scope

- Mobile native (Swift/Kotlin) production apps
- Kernel/driver development
- Game development
- ML model training pipelines
- Infrastructure provisioning

### Benchmark Target

- 100 real repositories
- ≥90% code quality score
- ≥85% test generation usefulness

---

## Research Assistant

**Capability ID:** `research`
**Category:** Research
**Quality Target:** A- (≥85) - Production Ready

### Scope

- Literature survey and synthesis
- Multi-source RAG retrieval
- Evidence ranking and contradiction detection
- Citation with provenance
- Structured report generation
- Experiment design advisory

### Knowledge Focus

- Scientific and technical writing patterns
- Evidence quality evaluation
- Citation formats and provenance tracking
- Statistical significance and experimental design
- Research gap identification

### Out of Scope

- Live web search without approved retrieval tools
- Medical/legal/financial advice
- Primary data collection
- Human subject research oversight
- Patent or IP legal analysis

### Benchmark Target

- 100 research questions
- ≥85% citation accuracy
- ≥80% evidence ranking quality

---

## DevOps Assistant

**Capability ID:** `devops`
**Category:** DevOps
**Quality Target:** B+ (≥80) - Production Ready

### Scope

- Dockerfile generation from requirements
- CI/CD pipeline generation
- Kubernetes manifest generation
- Monitoring and alerting configuration
- Deployment health verification
- Infrastructure diagram and documentation

### Knowledge Focus

- Docker, Kubernetes, Terraform
- GitHub Actions, GitLab CI
- Cloud patterns: AWS, Azure, GCP
- Observability: metrics, logs, traces
- Security scanning and policy-as-code

### Out of Scope

- Live cloud account provisioning
- Production incident command
- Hardware datacenter operations
- Custom cloud provider integrations outside registry
- Cost optimization auditing

### Benchmark Target

- 100 infrastructure scenarios
- ≥85% correctness on generated configs
- ≥80% deployment verification accuracy

---

## Trading Analyst

**Capability ID:** `trading`
**Category:** Finance
**Quality Target:** B+ (≥80) - Certification Pending

### Scope

- Market data analysis and trend detection
- Risk assessment and position sizing
- Portfolio exposure analysis
- Strategy backtesting
- Multi-strategy comparison via debate engine
- Decision recording and experience memory

### Knowledge Focus

- Technical indicators and statistical signals
- Market regime detection
- Risk models: VaR, drawdown, correlation
- Portfolio construction and rebalancing
- Macro event and news impact assessment
- Trading psychology and behavioral biases

### Out of Scope

- Live trade execution
- Brokerage account integration
- Regulatory compliance for specific jurisdictions
- Tax optimization
- Personal financial advisory

### Benchmark Target

- 100 market scenarios
- Risk-adjusted return quality
- Consistency across repeated analysis

---

## Self Development

**Capability ID:** `self-development`
**Category:** Platform
**Quality Target:** A (≥90) - Production Ready

### Scope

- Project structure analysis
- Bottleneck and dead-code detection
- Refactoring proposal generation
- Patch and test report generation
- Approval workflow orchestration
- Cross-project pattern learning

### Knowledge Focus

- Software architecture patterns
- Code smell taxonomy
- Testing and coverage strategies
- Documentation quality standards
- Change impact and risk assessment

### Out of Scope

- Autonomous code execution without approval
- Direct modification of Core contracts
- Cross-Capability Pack engine reuse by direct import
- Production deployment without explicit user approval

### Benchmark Target

- 10 real projects
- ≥80% improvement acceptance rate
- ≥90% approval workflow compliance

---

## Task Templates

Each Capability Pack defines standard task templates.
Templates represent common execution paths and are used by Execution Runtime to plan and parallelize work.

### Network Engineer

| Task | Subtasks |
|------|----------|
| Audit | Parse → Topology → Security → Compliance → Recommendation → Documentation |
| Optimization | Performance review → Bottleneck identification → Configuration tuning → Validation |
| Migration | Version assessment → Change impact → Rollback plan → Execution → Verification |
| Design | Requirements → Topology design → Security design → Documentation → Implementation plan |
| Automation | Diff generation → Risk scoring → Backup → Verification → Deployment |

### Code Engineer

| Task | Subtasks |
|------|----------|
| Review | Parse → Architecture → Security → Dead code → Recommendations |
| Refactor | Analysis → Proposal → Patch → Tests → Validation |
| Generate | Requirements → Architecture → Backend → Frontend → Database → Tests → Documentation |
| Architecture | Requirements → Domain modeling → Layer design → Interface definition → Documentation |
| Modernization | Assessment → Dependency analysis → Migration plan → Execution → Validation |

### Trading Analyst

| Task | Subtasks |
|------|----------|
| Analysis | Market data → Indicators → Structure → Bias → Levels |
| Strategy | Idea → Rules → Backtest → Risk → Validation |
| Portfolio | Holdings → Correlation → Exposure → Rebalancing → Risk |
| Risk | Position sizing → Stop loss → Drawdown → Scenario → Mitigation |
| Execution Planning | Entry → Exit → Position size → Risk check → Alternatives → Decision |

### Research Assistant

| Task | Subtasks |
|------|----------|
| Retrieval | Question → Source search → Filtering → Ranking → Citations |
| Evidence | Sources → Quality check → Contradiction detection → Confidence → Synthesis |
| Synthesis | Sources → Themes → Integration → Gaps → Summary → Citations |
| Experiment | Hypothesis → Design → Variables → Method → Validation |
| Peer Review | Submission → Criteria check → Gap analysis → Feedback → Score |

### DevOps Assistant

| Task | Subtasks |
|------|----------|
| Generate | Requirements → Container config → CI/CD → IaC → Documentation |
| Verify | Configuration review → Security scan → Health check → Validation |
| Multi-cloud | Requirements → Provider selection → Service mapping → Cost estimate → Implementation |
| Platform | Requirements → Observability design → Policy definition → GitOps setup → Documentation |
| Resilience | Requirements → Failure modes → Chaos plan → Monitoring → Runbooks |

### Self Development

| Task | Subtasks |
|------|----------|
| Analyze | Project scan → Structure analysis → Bottleneck detection → Dependency analysis |
| Propose | Issues → Impact assessment → Solution design → Risk evaluation → Proposal |
| Patch | Proposal → Diff generation → Test creation → Validation → Rollback plan |
| Learn | Patterns → Cross-project analysis → Knowledge update → Recommendation |
| Predict | Change → Impact model → Risk forecast → Mitigation → Confidence |

---

## Knowledge Expansion Roadmap

This section documents planned knowledge expansions for each Capability Pack during the Capability Excellence phase. All additions happen inside Capability Packs. Core remains unchanged.

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

---

### Code Engineer

**Planned additions:**
- Clean Architecture: layers, dependency rule, boundaries
- DDD: bounded contexts, aggregates, domain events, anti-corruption
- SOLID: all 5 principles with Python/TypeScript examples
- CQRS: command/query separation, write/read models
- Event Sourcing: event store, replay, projection
- Secure Coding: OWASP Top 10, injection, auth, secrets

**Reference RFC:** RFC-0006

---

### Research Assistant

**Planned additions:**
- Evidence ranking: source quality, recency, methodology
- Contradiction detection: identify conflicting claims
- Citation quality: completeness, format, provenance
- Confidence estimation: uncertainty quantification
- Synthesis patterns: multi-paper integration

---

### DevOps Assistant

**Planned additions:**
- Multi-cloud: AWS, Azure, GCP service patterns
- GitOps: ArgoCD, Flux, declarative deployment
- Platform engineering: IDP, developer portals
- Policy-as-code: OPA, Sentinel, Kyverno
- Chaos engineering principles

---

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

### Self Development

**Planned additions:**
- Cross-project pattern learning
- Impact prediction before changes
- Architecture smell taxonomy
- Change risk modeling
- Automated improvement suggestions

---

## System Architect

**Reference RFC:** RFC-0011

**Capability ID:** `system-architect`
**Category:** Architecture
**Quality Target:** A (≥90)
**Maturity Target:** Level 3 — Production Ready

### Scope

- Clean Architecture layer analysis and violation detection
- DDD evaluation (bounded contexts, aggregates, anti-corruption layers)
- Event-driven design review (event schemas, saga patterns)
- CQRS evaluation
- Microservices/monolith decomposition analysis
- Architecture governance enforcement
- ADR generation for architectural decisions
- Package boundary enforcement (dependency cycles, layer inversions)

### Knowledge Focus

- Clean Architecture (Robert C. Martin)
- Domain-Driven Design (Eric Evans)
- Event-Driven Architecture (Enterprise Integration Patterns)
- CQRS patterns and anti-patterns
- Microservices decomposition strategies
- Architecture smells and governance rules

### Out of Scope

- Actual code refactoring or implementation
- Infrastructure/cloud architecture design
- Real-time architecture compliance monitoring
- Live deployment or runtime monitoring
- Database schema design (Database Engineer handles this)
- Network topology design (Network Engineer handles this)

### Benchmark Target

- 100 architecture projects (Python, JS/TS, Java, Go, TypeScript)
- ≥95% architecture review completeness
- ≥95% dependency violation detection
- ≥90% package boundary enforcement
- ≥95% explainability

### Consumers

- Code Engineer — architecture review of generated code
- Self Development — package boundary validation and improvement evaluation
- Decision Intelligence — architecture risk scoring
- QA Engineer — architecture-based test strategy planning
- DevOps Assistant — microservices deployment architecture review

---

## Future Capability Packs (Roadmap)

The following Capability Packs are planned for Fase 2 and beyond. They will be developed once all 6 existing packs reach target grade A/A-.

### Security Engineer

**Fase:** Fase 2 — Setelah Capability Excellence
**Capability ID:** `security-engineer`
**Reference RFC:** RFC-0008

**Purpose:** Enterprise security capabilities across OWASP Top 10, threat modeling, secret detection, vulnerability analysis, dependency audit, configuration hardening, and compliance mapping.

**Consumers:** Code Engineer, DevOps Assistant, Network Engineer, System Architect

### Data Engineer

**Fase:** Fase 2 — Setelah Capability Excellence
**Capability ID:** `data-engineer`
**Reference RFC:** RFC-0009

**Purpose:** Full data lifecycle management: ETL/ELT, data cleaning, dataset validation, schema evolution, feature engineering, time series handling, and data quality assurance.

**Consumers:** Trading Analyst, Research Assistant, Decision Intelligence, System Architect

### Database Engineer

**Fase:** Fase 2 — Setelah Capability Excellence
**Capability ID:** `database-engineer`
**Reference RFC:** RFC-0010

**Purpose:** Enterprise database capabilities: schema design, query optimization, migration management, replication planning, backup/recovery, index recommendation, and performance analysis.

**Consumers:** Code Engineer, Data Engineer, DevOps Assistant

### Decision Intelligence

**Fase:** Fase 2 — Setelah Capability Excellence
**Capability ID:** `decision-intelligence`
**Reference RFC:** RFC-0007

**Purpose:** Cross-domain reasoning layer for evidence-based decision-making: evidence collection, alternative generation, risk analysis, trade-off analysis, decision scoring, confidence estimation, explainable decisions, and decision history.

**Consumers:** All Capability Packs

### QA Engineer

**Fase:** Fase 3 — Enterprise
**Capability ID:** `qa-engineer`
**Reference RFC:** RFC-0012

**Purpose:** Automated quality assurance: unit/integration test generation, regression test automation, mutation testing, golden test generation for other packs, benchmark test generation, flaky test detection, coverage analysis, and performance validation.

**Consumers:** All Capability Packs

### Business Analyst

**Fase:** Fase 3 — Enterprise
**Capability ID:** `business-analyst`
**Reference RFC:** RFC-0013

**Purpose:** Business-to-technical translation: requirement gathering, business process modeling, user story generation, use case modeling, BRD generation, functional specification, gap analysis, ROI analysis, and process optimization.

**Consumers:** Code Engineer, System Architect, Self Development
