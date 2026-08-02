<!-- BILINGUAL_DOCS_START -->
## Bahasa Indonesia / English

### Ringkasan / Summary

Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.
> Terjemahan Indonesia: Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.

- Bahasa Indonesia: konten utama tetap dipertahankan dalam dokumen asli, dan bagian ini memberi konteks ringkas dalam bahasa Indonesia.
- English: the main content remains in the original document, and this section provides a concise bilingual context for international readers.

### Informasi Dokumen / Document Info
- File: `docs/CAPABILITY_STRATEGY.md`
- Judul: Capability Strategy
- Status: bilingual header added

<!-- BILINGUAL_DOCS_END -->

<!-- DOCUMENT_METADATA_START -->
**Owner:** Documentation Team
**Canonical Owner:** Documentation Governance Lead
**Last Verified:** 2026-08-02
**Version:** 1.0.0
**Status:** Active
**SSOT:** Capability Pack maturity model, profiles, and lifecycle strategy
<!-- DOCUMENT_METADATA_END -->

# ECP Capability Strategy

**Version:** 1.0.0
**Effective:** 2026-08-02
**Parent:** `GOVERNANCE_CHARTER.md`
**Purpose:** Defines the strategy for Capability Pack evolution, maturity, quality grading, lifecycle, and knowledge expansion.

---

## 1. Strategy Philosophy

> **Core is the stable platform. Capability Packs are the place where innovation happens.**

All knowledge expansion, feature growth, and domain evolution happens **inside Capability Packs**. Core remains unchanged.
> Terjemahan Indonesia: All knowledge expansion, feature growth, dan domain evolution happens inside kapabilitas Packs. Core remains unchanged.

The development cycle is:
> Terjemahan Indonesia: Development cycle adalah:

```
Real Usage → Measurement → Capability Improvement → Benchmark → Release
```

- Real-world cases are the **primary source** of Capability Pack improvement.
- Synthetic benchmarks **validate** improvements; real-world cases **drive** them.
- Each Capability Pack independently evolves at its own pace.

---

## 2. Capability Maturity Model

Maturity describes the **lifecycle stage** of a Capability Pack — not its quality grade. A pack must progress through these levels to reach production readiness.
> Terjemahan Indonesia: Maturity describes lifecycle stage dari sebuah kapabilitas Pack — not its kualitas grade. sebuah pack must progress through these levels untuk reach production readiness.

| Level | Label | Description | Requirements |
|-------|-------|-------------|--------------|
| 1 | **Experimental** | Concept prototype, exploratory | RFC, basic implementation |
| 2 | **Functional** | Works for basic scenarios | Golden tests, documented scope, known limitations |
| 3 | **Production Ready** | Stable, qualified for release | Benchmark ≥80%, ≥50 real cases, documentation, no P0/P1 security issues |
| 4 | **Domain Expert** | Deep domain knowledge, multi-vendor/multi-domain | Benchmark ≥90%, ≥200 real cases, multi-vendor coverage |
| 5 | **Certified** | Audited, benchmarked, reference-quality | Independent audit, public benchmark dashboard, ≥500 real cases |
| 6 | **Reference Capability** | Industry benchmark for the domain | Cross-project validation, published methodology, community adoption |

**Current Status (2026-08-02):**

| Capability Pack | Maturity Level | Target Level |
|-----------------|----------------|--------------|
| Network Engineer | 3 — Production Ready | 4 — Domain Expert |
| Code Engineer | 3 — Production Ready | 4 — Domain Expert |
| Research Assistant | 3 — Production Ready | 4 — Domain Expert |
| DevOps Assistant | 3 — Production Ready | 4 — Domain Expert |
| Trading Analyst | 2 — Functional | 3 — Production Ready |
| Self Development | 3 — Production Ready | 4 — Domain Expert |
| Decision Intelligence | 3 — Production Ready | 4 — Domain Expert |
| System Architect | 3 — Production Ready | 4 — Domain Expert |
| Security Engineer | 3 — Production Ready | 4 — Domain Expert |
| Data Engineer | 3 — Production Ready | 4 — Domain Expert |
| Database Engineer | 3 — Production Ready | 4 — Domain Expert |
| QA Engineer | 3 — Production Ready | 4 — Domain Expert |
| Business Analyst | 3 — Production Ready | 4 — Domain Expert |

---

## 3. Quality Grades

Quality Grades describe the **current benchmark result** of a Capability Pack. They are outcomes of evaluation, not maturity levels.
> Terjemahan Indonesia: Kualitas Grades describe current benchmark result dari sebuah kapabilitas Pack. They adalah outcomes dari evaluation, not maturity levels.

| Grade | Meaning | Benchmark Score |
|-------|---------|-----------------|
| C | **Functional** — works for basic scenarios | ≥65% |
| B | **Production-ready** — stable and reliable | ≥75% |
| B+ | **Production-ready** — above-average reliability | ≥80% |
| A- | **Domain expert** — deep knowledge in primary domain | ≥85% |
| A | **Expert** — comprehensive domain mastery | ≥90% |
| A+ | **Reference implementation** — industry benchmark | ≥95% |

**Current Quality Grades (2026-08-02):**

| Capability Pack | Grade | Score | Status |
|-----------------|-------|-------|--------|
| Network Engineer | A | ≥90 | Production Ready |
| Code Engineer | A- | ≥85 | Production Ready |
| Research Assistant | A- | ≥85 | Production Ready |
| DevOps Assistant | B+ | ≥80 | Production Ready |
| Trading Analyst | B+ | ≥80 | Certification Pending |
| Self Development | A | ≥90 | Production Ready |
| Decision Intelligence | A | 91.25% | Production Ready (RFC-0007) |
| System Architect | A | 97.50% | Production Ready (RFC-0011) |
| Security Engineer | A- | ≥85 | Production Ready (RFC-0008) |
| Data Engineer | A- | ≥85 | Production Ready (RFC-0009) |
| Database Engineer | A- | ≥85 | Production Ready (RFC-0010) |
| QA Engineer | A | ≥90 | Production Ready (RFC-0012) |
| Business Analyst | A- | ≥85 | Production Ready (RFC-0013) |

### Quality Grade vs Maturity Level

These two concepts are independent:
> Terjemahan Indonesia: These two concepts adalah independent:

- **Maturity Level** = Where the pack is in its lifecycle (e.g., Production Ready)
- **Quality Grade** = How well the pack performs in benchmarks (e.g., A)

A pack at Level 3 (Production Ready) may be working toward A+ grade. A pack at Level 4 (Domain Expert) may have a lower grade if its domain scope has expanded faster than benchmark scores.
> Terjemahan Indonesia: Sebuah pack at Level 3 (Production Ready) may menjadi working toward sebuah+ grade. sebuah pack at Level 4 (Domain Expert) may memiliki sebuah lower grade if its domain scope memiliki expanded faster than benchmark scores.

---

## 4. Capability Lifecycle

Each Capability Pack follows a defined lifecycle from proposal to deprecation:
> Terjemahan Indonesia: Each kapabilitas Pack follows sebuah defined lifecycle dari proposal untuk deprecation:

```
Proposal
    ↓
  RFC
    ↓
Prototype
    ↓
Experimental
    ↓
Stable
    ↓
Certified
    ↓
Maintenance
    ↓
Deprecated
```

### Phase Descriptions

| Phase | Gate | Activities |
|-------|------|------------|
| **Proposal** | Idea document | Define scope, target domain, use cases |
| **RFC** | RFC approved | Community review, architecture alignment |
| **Prototype** | Prototype demo | Core logic implemented, basic tests |
| **Experimental** | Golden tests pass | Known limitations documented, benchmark v1 |
| **Stable** | Benchmark ≥80%, ≥50 real cases | Full documentation, security review, SDK access |
| **Certified** | Independent audit | Public benchmark dashboard, reference documentation |
| **Maintenance** | No active development | Bug fixes only, no new features |
| **Deprecated** | Replacement identified | Notice period, migration guide, archive |

### Current Lifecycle Status

| Capability Pack | Lifecycle Phase | Notes |
|-----------------|-----------------|-------|
| Network Engineer | Stable | Progressing toward Certified |
| Code Engineer | Stable | Progressing toward Certified |
| Research Assistant | Stable | Progressing toward Certified |
| DevOps Assistant | Stable | Progressing toward Certified |
| Trading Analyst | Experimental → Stable | Certification in progress |
| Self Development | Stable | Progressing toward Certified |
| Decision Intelligence | Stable | Shared reasoning layer (RFC-0007) |
| System Architect | Stable | Architecture authority (RFC-0011) |
| Security Engineer | Stable | Production Ready (RFC-0008) |
| Data Engineer | Stable | Production Ready (RFC-0009) |
| Database Engineer | Stable | Production Ready (RFC-0010) |
| QA Engineer | Stable | Production Ready (RFC-0012) |
| Business Analyst | Stable | Production Ready (RFC-0013) |

---

## 5. Official Capability Packs

### 5.1 Network Engineer

**Category:** Networking
**Capabilities:** Configuration generation, validation, deployment
**Success Criteria:**
- Configures MikroTik routers via Plugin
- Validates configurations before deployment
- Generates rollback scripts
- Uses Knowledge Graph for network topology
**Quality Target:** A — 100 real configs, ≥95% accuracy
**Maturity Target:** Level 4 — Domain Expert

### 5.2 Code Engineer

**Category:** Development
**Capabilities:** Full-stack code generation, testing, documentation
**Success Criteria:**
- Generates backend API from requirements
- Generates frontend UI from API spec
- Creates database schema
- Generates tests and documentation
- All components work together
**Quality Target:** A- (≥85) — 100 repositories, ≥90% code quality
**Maturity Target:** Level 4 — Domain Expert

### 5.3 Research Assistant

**Category:** Research
**Capabilities:** RAG, Knowledge Graphs, citation, learning
**Success Criteria:**
- Retrieves relevant documents from knowledge base
- Synthesizes information from multiple sources
- Provides citations for claims
- Learns from research sessions
**Quality Target:** A- (≥85) — 100 research questions, ≥85% citation accuracy
**Maturity Target:** Level 4 — Domain Expert

### 5.4 DevOps Assistant

**Category:** DevOps
**Capabilities:** CI/CD, containerization, deployment
**Success Criteria:**
- Generates Dockerfiles from application requirements
- Creates GitHub Actions workflows
- Deploys to container registry
- Verifies deployment health
**Quality Target:** B+ (≥80) — 100 infrastructure scenarios, ≥85% correctness
**Maturity Target:** Level 4 — Domain Expert

### 5.5 Trading Analyst

**Category:** Finance
**Capabilities:** Market analysis, simulation, decision theory
**Success Criteria:**
- Analyzes market data using cognitive pipeline
- Generates trading recommendations with confidence scores
- Uses debate engine for multi-strategy comparison
- Records decisions to experience memory
**Quality Target:** B+ (≥80) — 100 market scenarios, risk-adjusted returns
**Maturity Target:** Level 3 — Production Ready (Certification Pending)

### 5.6 Self Development

**Category:** Platform
**Capabilities:** Architecture analysis, improvement proposal, patch generation, approval workflow
**Success Criteria:**
- Analyzes project structure and identifies bottlenecks
- Generates improvement proposals with risk assessment
- Produces patches and test reports
- Requires explicit user approval before applying changes
**Quality Target:** A (≥90) — 10 real projects, ≥80% improvement acceptance
**Maturity Target:** Level 4 — Domain Expert

### 5.7 Decision Intelligence

**Category:** Platform — Shared Reasoning
**Capabilities:** Evidence collection, alternative generation, risk analysis, trade-off analysis, scoring, confidence estimation, explainable decision, decision history
**Success Criteria (RFC-0007):**
- Evidence-based decision-making from multiple Capability Pack sources
- Generates explainable recommendations with confidence scores
- Analyzes risk (probability × impact) and trade-offs across alternatives
- Records decisions to Experience Memory / Decision History
- Full explainability chain: evidence → reasoning → alternatives → risk → decision → rationale
**Quality Target:** A (≥90) — benchmark overall 91.25%
**Benchmark:** `benchmarks/decision_intelligence_benchmark.py` (8 dimensions)
**Maturity Target:** Level 3 — Production Ready

### 5.8 System Architect

**Category:** Platform — Architecture Authority
**Capabilities:** Architecture review, Clean Architecture validation, DDD analysis, event-driven design, CQRS evaluation, microservices/monolith analysis, package boundary enforcement, governance, ADR generation
**Success Criteria (RFC-0011):**
- Reviews repository structure against Clean Architecture, DDD, event-driven, CQRS, and microservices patterns
- Detects dependency cycles, layer violations, and package boundary violations
- Enforces Architecture Governance: Core change guard, Capability First Rule, pack independence
- Generates structured ADR drafts from review findings
- Full explainability chain: findings → metrics → recommendation → ADR
**Quality Target:** A (≥90) — benchmark overall 97.50%
**Benchmark:** `benchmarks/system_architect_benchmark.py` (8 dimensions)
**Maturity Target:** Level 4 — Domain Expert

### 5.9 Security Engineer

**Category:** Security
**Capabilities:** OWASP Top 10 analysis, security audit, penetration test, threat modeling, secret detection, vulnerability analysis, dependency audit, configuration hardening, compliance mapping
**Success Criteria (RFC-0008):**
- Enterprise security capabilities across OWASP Top 10
- Threat modeling and secret detection
- Vulnerability analysis and dependency audit
- Configuration hardening and compliance mapping
**Quality Target:** A- (≥85)
**Benchmark:** `benchmarks/security_engineer_benchmark.py` (9 dimensions)
**Maturity Target:** Level 3 — Production Ready

### 5.10 Data Engineer

**Category:** Data
**Capabilities:** ETL/ELT pipeline, data cleaning, dataset validation, schema evolution, feature engineering, time-series handling, data quality assurance
**Success Criteria (RFC-0009):**
- Full data lifecycle management: ETL/ELT, data cleaning, dataset validation
- Schema evolution and feature engineering
- Time-series handling and data quality assurance
**Quality Target:** A- (≥85)
**Benchmark:** `benchmarks/data_engineer_benchmark.py` (8 dimensions)
**Maturity Target:** Level 3 — Production Ready

### 5.11 Database Engineer

**Category:** Database
**Capabilities:** Schema design, query optimization, migration management, replication planning, backup/recovery, index recommendation, performance analysis
**Success Criteria (RFC-0010):**
- Enterprise database capabilities: schema design, query optimization
- Migration management, replication planning, backup/recovery
- Index recommendation and performance analysis
**Quality Target:** A- (≥85)
**Benchmark:** `benchmarks/database_engineer_benchmark.py` (8 dimensions)
**Maturity Target:** Level 3 — Production Ready

### 5.12 QA Engineer

**Category:** Quality Assurance
**Capabilities:** Unit/integration test generation, regression test automation, mutation testing, Golden Test generation for other packs, benchmark test generation, flaky test detection, coverage analysis, performance validation
**Success Criteria (RFC-0012):**
- Automated quality assurance: unit/integration test generation
- Regression test automation and mutation testing
- Golden Test generation for other packs
- Benchmark test generation and coverage analysis
**Quality Target:** A (≥90)
**Benchmark:** `benchmarks/qa_engineer_benchmark.py` (9 dimensions)
**Maturity Target:** Level 3 — Production Ready

### 5.13 Business Analyst

**Category:** Business Analysis
**Capabilities:** Requirement gathering, business process modeling, user story generation, use case modeling, BRD generation, functional specification, gap analysis, ROI analysis, process optimization
**Success Criteria (RFC-0013):**
- Business-to-technical translation: requirement gathering
- Business process modeling and user story generation
- Use case modeling, BRD generation, functional specification
- Gap analysis, ROI analysis, and process optimization
**Quality Target:** A- (≥85)
**Benchmark:** `benchmarks/business_analyst_benchmark.py` (9 dimensions)
**Maturity Target:** Level 3 — Production Ready

---

## 6. Benchmark Requirements

### 6.1 Capability Benchmark

Each Capability Pack must define and maintain a benchmark:
> Terjemahan Indonesia: Each kapabilitas Pack must define dan maintain sebuah benchmark:

- Minimum **100 scenarios** for A/B grade targets
- Minimum **10 projects** for A-/B+ grade targets
- Benchmark must cover 6 dimensions: **Accuracy, Completeness, Explainability, Safety, Efficiency, Consistency**
- Results must be **reproducible** and persisted in `benchmarks/`

### 6.2 Real-world Benchmark

Each Capability Pack must maintain a `real_cases/<capability_id>/` directory containing:
> Terjemahan Indonesia: Each kapabilitas Pack must maintain sebuah real_cases// directory containing:

- Real input/output pairs from actual usage
- Evaluation notes for each case
- Links to synthetic benchmark updates driven by real findings

### 6.3 Benchmark Dimensions

| Dimension | Definition | Measurement |
|-----------|------------|-------------|
| Accuracy | Correctness of outputs | % of correct findings/recommendations |
| Completeness | Coverage of all relevant aspects | % of required elements covered |
| Explainability | Clarity and reasoning quality | Human evaluation score |
| Safety | No harmful or insecure outputs | % of outputs passing safety checks |
| Efficiency | Response time and resource usage | Latency P95, token usage |
| Consistency | Same output for same input | Variance across repeated runs |

---

## 7. Knowledge Expansion

All planned knowledge additions are tracked via RFCs and implemented inside Capability Packs only. Core remains unchanged.
> Terjemahan Indonesia: All planned knowledge additions adalah tracked via RFCs dan implemented inside kapabilitas Packs only. Core remains unchanged.

### 7.1 Network Engineer

**Reference RFC:** RFC-0004

**Planned additions:**
- Cisco Design Guide: campus, data center, SD-WAN, HA
- MikroTik Best Practice: ISP edge, hotspot, IPv6, FastTrack
- Fortinet Hardening: FortiOS, policy, VPN, threat protection
- BGP: path selection, filtering, communities, monitoring
- MPLS: forwarding, LDP, VRF, traffic engineering basics
- IPv6: dual-stack, SLAAC, DHCPv6, transition mechanisms
- Zero Trust: principles, micro-segmentation, ZTNA

### 7.2 Code Engineer

**Reference RFC:** RFC-0006

**Planned additions:**
- Clean Architecture: layers, dependency rule, boundaries
- DDD: bounded contexts, aggregates, domain events, anti-corruption
- SOLID: all 5 principles with Python/TypeScript examples
- CQRS: command/query separation, write/read models
- Event Sourcing: event store, replay, projection
- Secure Coding: OWASP Top 10, injection, auth, secrets

### 7.3 Research Assistant

**Planned additions:**
- Evidence ranking: source quality, recency, methodology
- Contradiction detection: identify conflicting claims
- Citation quality: completeness, format, provenance
- Confidence estimation: uncertainty quantification
- Synthesis patterns: multi-paper integration

### 7.4 DevOps Assistant

**Planned additions:**
- Multi-cloud: AWS, Azure, GCP service patterns
- GitOps: ArgoCD, Flux, declarative deployment
- Platform engineering: IDP, developer portals
- Policy-as-code: OPA, Sentinel, Kyverno
- Chaos engineering principles

### 7.5 Trading Analyst

**Reference RFC:** RFC-0005

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

### 7.6 Self Development

**Planned additions:**
- Cross-project pattern learning
- Impact prediction before changes
- Architecture smell taxonomy
- Change risk modeling
- Automated improvement suggestions

---

## 8. Future Capability Packs (Roadmap)

All Capability Packs listed below have been implemented. Future packs will only be developed after the 13 existing packs reach target grade A/A-.
> Terjemahan Indonesia: All kapabilitas Packs listed below memiliki been implemented. Future packs akan only menjadi developed after 13 existing packs reach target grade sebuah/sebuah-.

### 8.1 Security Engineer (Prioritas Tinggi — ⭐⭐⭐⭐)

**Fase:** Fase 2 — Setelah Capability Excellence
**Status:** ✅ Implemented (RFC-0008)
**Fungsi:** Keamanan aplikasi dan infrastruktur
**Kemampuan:**
- OWASP Top 10 analysis
- Security audit dan penetration test
- Threat modeling
- Secret detection dan vulnerability assessment
**Dependent Packs:** Code, DevOps, Network
**RFC Status:** RFC-0008 — Diimplementasikan
**Target Maturity:** Level 3 — Production Ready

### 8.2 Data Engineer (Prioritas Tinggi — ⭐⭐⭐⭐)

**Fase:** Fase 2 — Setelah Capability Excellence
**Status:** ✅ Implemented (RFC-0009)
**Fungsi:** Fondasi data untuk meningkatkan Trading, Research, dan analitik
**Kemampuan:**
- ETL pipeline
- Data cleaning dan quality
- Dataset versioning
- Feature engineering
- Time-series pipeline
**Dependent Packs:** Trading, Research, DevOps
**RFC Status:** RFC-0009 — Diimplementasikan
**Target Maturity:** Level 3 — Production Ready

### 8.3 Enterprise Packs (Fase 3)

| Capability Pack | Fungsi | Dependent Packs |
|-----------------|--------|-----------------|
| **Database Engineer** | SQL optimization, schema design, migration, index recommendation, performance analysis | Code, DevOps |
| **System Architect** | DDD, microservices, event driven, ADR generator, architecture review, refactoring recommendation | Code, Self Development |
| **QA Engineer** | Test generation, regression, mutation testing, Golden Test builder, benchmark generator | Code, DevOps, Self Development |
| **Business Analyst** | Requirement analysis, user story, BRD, use case, workflow | Semua pack |

### 8.4 Long-term Packs (Fase 4)

| Capability Pack | Fungsi |
|-----------------|--------|
| **Product Manager** | Roadmap, prioritization, ROI, sprint planning |
| **Documentation Engineer** | Sync documentation, OpenAPI, ADR, changelog, release notes |
| **UI/UX Designer** | Design system, wireframe, accessibility, UX audit |
| **AI Engineer** | RAG, fine-tuning, prompt engineering, agent design, evaluation |
| **Infrastructure Engineer** | Kubernetes, Docker, storage, monitoring, observability, HA cluster |

### 8.5 Yang Tidak Akan Menjadi Capability Pack

Komponen berikut akan diposisikan sebagai **Plugin**, **Service**, atau **infrastruktur platform**, bukan Capability Pack:
> Terjemahan Indonesia: Komponen berikut akan diposisikan sebagai Plugin, layanan, atau infrastruktur platform, bukan kapabilitas Pack:

- Authentication / Authorization
- PostgreSQL / Redis / MinIO / Kafka
- Plugin Marketplace
- Broker Connector / Exchange Connector
- Infrastruktur murni (load balancer, DNS, container runtime)

---

## 9. Capability Changelog Template

Each Capability Pack maintains its own changelog. The changelog records knowledge additions, benchmark improvements, and reasoning enhancements. It does not record Core changes.
> Terjemahan Indonesia: Each kapabilitas Pack maintains its own changelog. changelog records knowledge additions, benchmark improvements, dan reasoning enhancements. It does not record Core changes.

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

## 10. Approval

| Role | Status | Date |
|------|--------|------|
| Chief Product Officer | Approved | 2026-08-02 |
| Chief Architect | Approved | 2026-08-02 |
