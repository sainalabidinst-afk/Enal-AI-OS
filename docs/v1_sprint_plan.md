<!-- BILINGUAL_DOCS_START -->
## Bahasa Indonesia / English

### Ringkasan / Summary
Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.
> Terjemahan Indonesia: Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.

- Bahasa Indonesia: konten utama tetap dipertahankan dalam dokumen asli, dan bagian ini memberi konteks ringkas dalam bahasa Indonesia.
- English: the main content remains in the original document, and this section provides a concise bilingual context for international readers.

### Informasi Dokumen / Document Info
- File: `docs/v1_sprint_plan.md`
- Judul: V1 Sprint Plan
- Status: bilingual header added

<!-- BILINGUAL_DOCS_END -->

# ECP v1.0-dev Milestone Plan

<!-- DOCUMENT_METADATA_START -->
**Owner:** Documentation Team
**Canonical Owner:** Documentation Governance Lead
**Last Verified:** 2026-08-02
**Version:** 1.0.0
**Status:** Active
**SSOT:** Documentation for v1_sprint_plan
<!-- DOCUMENT_METADATA_END -->

**Methodology:** Product milestone-based, not feature-based.
**Definition of Done:** Milestone meets all delivery criteria and gates are satisfied.

---

## Milestone 1 â€” Network Engineer MVP

**Status:** âœ… Accepted
**Baseline:** `v1.0.0-dev+network-sprint2`

**Goal:** Prove ECP can analyze, generate, simulate, and document network configurations.

**Duration:** 2â€“3 weeks

**Definition of Done:**
- [x] Upload `.rsc` file
- [x] Parse RouterOS configuration
- [x] Build internal topology
- [x] Detect configuration problems
- [x] Generate recommendations
- [x] Generate improved configuration
- [x] Produce deployment documentation
- [x] Pass all Golden Tests for networking domain (31/31 scenarios)

**Deliverables:**
- RouterOS parser (v6/v7)
- Network graph builder
- 45 analysis rules
- Recommendation engine (P0â€“P3)
- Documentation generator (Markdown)

---

## Milestone 1.5 â€” Hardening

**Status:** âœ… Accepted

**Goal:** Strengthen Milestone 1 with regression suite, benchmarks, and coverage tracking.

**Duration:** 3â€“5 days

**Definition of Done:**
- [x] 31 golden test scenarios (7 original + 24 new)
- [x] Regression dataset (broken, invalid, partial, v6, v7)
- [x] Rule coverage tracker (hit count, precision, recall, F1)
- [x] Performance benchmarks (500/5k/50k lines)
- [x] Confidence calibration from evidence
- [x] All tests passing

---

## Milestone 2 â€” Controlled Deployment

**Status:** âœ… Accepted

**Goal:** Build deployment pipeline with safety, audit, and human approval.

**Duration:** 2â€“3 weeks

**Definition of Done:**
- [x] Semantic Configuration Diff Engine
- [x] Backup Manager (export â†’ hash â†’ timestamp â†’ artifact store)
- [x] Risk Scoring Engine (config/rollback/security/downtime)
- [x] Verification Engine (interface, gateway, DNS, DHCP, routes)
- [x] Audit Trail (all steps recorded as artifacts)
- [x] Controlled Deployment Orchestrator
- [x] Deployment Runbook UX (Changes/Risk/Pre-Deployment/Deployment/Post-Deployment/Recovery)
- [x] Deployment Timeline (visual step progress)
- [x] Explain Before Deploy (process-oriented language)
- [x] Rollback Status: Pending / Ready / Unavailable / Completed
- [x] Human approval required in v1.0-dev
- [x] All Milestone 2 tests pass (7/7)

---

## Milestone 3 â€” Network Operations

**Status:** ðŸ“‹ Planned

**Goal:** Operational workflows that network engineers use every day.

**Duration:** 2â€“3 weeks

**Definition of Done:**
- [ ] Configuration Compare (backup-to-backup semantic diff + impact)
- [ ] Compliance Audit (policy-based Pass/Fail)
- [ ] Health Report (health/security/performance/maintainability scores)
- [ ] Change Impact Analysis (predict impact before deployment)
- [ ] Explain Like Engineer (plain-language explanations for onboarding)
- [ ] All Milestone 3 tests pass (â‰¥95%)
- [ ] Dogfooding feedback incorporated

**Deliverables:**
- `apps/network_engineer/compare.py`
- `apps/network_engineer/compliance.py`
- `apps/network_engineer/health.py`
- `apps/network_engineer/impact_analyzer.py`
- `apps/network_engineer/explainer.py`

**What We Will NOT Build:**
- BGP automation
- MPLS automation
- CAPsMAN automation
- WireGuard automation
- Multi-router orchestration

---

## Dogfooding Phase

**Status:** ðŸ§ª In Progress (1â€“2 weeks)

**Goal:** Use Network Engineer on real configs before building new features.

**Activities:**
- Audit real MikroTik configs (Sun Clint, lab, production)
- Compare ECP findings with expert judgment
- Log false positives, false negatives, UX issues
- Collect Time Saved data

**Output:**
- `dogfooding/feedback_YYYY-MM-DD.md`
- Updated golden test scenarios
- Top 5 priorities for Milestone 3

**See:** `docs/dogfooding_guide.md`

---

## Milestone 4 â€” Reasoning Excellence

**Status:** ðŸŽ¯ Target: v1.0-dev Release

**Goal:** Improve reasoning quality across all Capability Packs without changing Core.

**Duration:** Ongoing

**Focus areas:**
- Deeper domain reasoning in Capability Packs
- Better explanation generation
- Improved risk and impact analysis
- Context-aware recommendations

**Success Criteria:**
- Network: detects not just open ports, but likely purpose and associated firewall gaps
- Trading: explains BUY/SELL with alternatives, risk, and failure scenarios
- Research: identifies contradictions between sources with confidence estimates
- Code: recommends architecture patterns with rationale
- All Capability Packs maintain Consistency score â‰¥85%

---

## Milestone 5 â€” Developer Preview

**Status:** ðŸŽ¯ Target: v1.0.0 Release

**Goal:** Product-ready release with all certification, documentation, and tooling complete.

**Definition of Done:**
- [ ] All Capability Packs meet quality targets
- [ ] Trading Analyst Certification passed
- [ ] Artifact Store v1 implemented
- [ ] Developer website launched
- [ ] SDK documentation complete
- [ ] Tutorial and Quick Start video published
- [ ] Marketplace functional
- [ ] Capability Discovery API public
- [ ] Capability Benchmark Dashboard operational
- [ ] Studio trace viewer functional

**Release Checklist:**
- [ ] Release notes drafted
- [ ] Migration guide for capability pack authors
- [ ] SDK examples published
- [ ] Quick Start video/tutorial prepared
- [ ] Public Developer Preview announcement

---

## Weekly Development Rhythm

| Day | Focus |
|-----|-------|
| Monday | Knowledge expansion |
| Tuesday | Benchmark improvement |
| Wednesday | Reasoning improvement |
| Thursday | Explainability improvement |
| Friday | Benchmark score increase |

All work happens inside Capability Packs. Core remains untouched.
> Terjemahan Indonesia: All work happens inside kapabilitas Packs. Core remains untouched.

---

## Do Not List

The following are no longer acceptable as regular development activities:
> Terjemahan Indonesia: Following adalah no longer acceptable as regular development activities:

- âŒ Add new Runtime
- âŒ Add new Planner
- âŒ Add new Kernel
- âŒ Add new Layer
- âŒ Modify Core for a single Capability Pack

Any exception requires an approved ADR with cross-capability proof.
> Terjemahan Indonesia: Any exception requires sebuah approved ADR dengan cross-kapabilitas proof.

---

## Target Capability Quality â€” v1.0 Developer Preview

| Capability | Target Score | Measurement |
|------------|--------------|-------------|
| Network | A (â‰¥90) | benchmarks/capability_benchmark.py |
| Code | A- (â‰¥85) | benchmarks/capability_benchmark.py |
| Research | A- (â‰¥85) | benchmarks/capability_benchmark.py |
| DevOps | B+ (â‰¥80) | benchmarks/capability_benchmark.py |
| Trading | B+ (â‰¥80, lulus Certification) | benchmarks/capability_benchmark.py |
| Self Development | A (â‰¥90) | benchmarks/capability_benchmark.py |

Scores must come from the 6-dimension benchmark, not subjective assessment.
> Terjemahan Indonesia: Scores must come dari 6-dimension benchmark, not subjective assessment.

---

## Post Developer Preview Roadmap

### v1.1 â€” Capability Excellence
- Network A+
- Trading B+
- Research A-
- Code A
- All packs improve one grade through knowledge and benchmark work

### v1.2 â€” Community Ecosystem
- Marketplace launch
- Community Capability Packs supported
- Capability Pack SDK templates
- Third-party pack certification process

### v1.3 â€” Enterprise
- Enterprise Capability Roadmap
- Advanced governance and audit features
- Multi-tenant support
- SLA and compliance tooling

---

## Capability-Specific Roadmaps

### Network Capability Roadmap

| Phase | Focus | Grade Target |
|-------|-------|--------------|
| Audit | Configuration analysis, security, compliance | A |
| Optimization | Performance tuning, best practices | A |
| Migration | Version upgrades, vendor migration | A |
| Design | Greenfield network design | A+ |
| Automation | Controlled deployment, rollback | A+ |

### Code Capability Roadmap

| Phase | Focus | Grade Target |
|-------|-------|--------------|
| Review | Code quality, security, maintainability | A- |
| Refactor | Improve structure without changing behavior | A- |
| Generate | Full-stack from requirements | A |
| Architecture | Clean Architecture, DDD, Hexagonal, CQRS | A |
| Modernization | Legacy migration, tech debt reduction | A |

### Trading Capability Roadmap

| Phase | Focus | Grade Target |
|-------|-------|--------------|
| Analysis | Market data, trends, indicators | B+ |
| Strategy | Strategy design and backtesting | A- |
| Portfolio | Portfolio construction and rebalancing | A- |
| Risk | Risk models, VaR, drawdown, correlation | A |
| Execution Planning | Trade planning with risk and alternatives | A |

### Research Capability Roadmap

| Phase | Focus | Grade Target |
|-------|-------|--------------|
| Retrieval | Multi-source RAG with citations | B |
| Evidence | Evidence ranking, contradiction detection | A- |
| Synthesis | Multi-paper synthesis with confidence | A- |
| Experiment | Experiment design advisory | A |
| Peer Review | Simulated peer review quality check | A |

### DevOps Capability Roadmap

| Phase | Focus | Grade Target |
|-------|-------|--------------|
| Generate | Dockerfiles, CI/CD, Kubernetes manifests | B+ |
| Verify | Deployment health, configuration correctness | A- |
| Multi-cloud | AWS, Azure, GCP patterns | A |
| Platform | Observability, GitOps, policy-as-code | A |
| Resilience | Chaos engineering, incident prep | A |

### Self Development Capability Roadmap

| Phase | Focus | Grade Target |
|-------|-------|--------------|
| Analyze | Project structure, bottleneck detection | A- |
| Propose | Refactoring, improvement proposals | A |
| Patch | Patch generation with test coverage | A |
| Learn | Cross-project pattern learning | A |
| Predict | Impact prediction before changes | A+ |

---

## Roadmap Summary

```
v1.0-dev
  â”œâ”€â”€ Milestone 1: Core Stable âœ…
  â”œâ”€â”€ Milestone 2: Conversation Ready âœ…
  â”œâ”€â”€ Milestone 3: Capability Platform âœ…
  â”œâ”€â”€ Milestone 4: Reasoning Excellence ðŸŽ¯ Target
  â”œâ”€â”€ Network Engineer Capability Pack âœ… Certified
  â”‚   â”œâ”€â”€ Milestone 3.1: Network Engineer MVP âœ… Accepted
  â”‚   â”œâ”€â”€ Milestone 3.2: Hardening âœ… Accepted
  â”‚   â”œâ”€â”€ Milestone 3.3: Controlled Deployment âœ… Accepted
  â”‚   â”œâ”€â”€ Milestone 3.4: Dogfooding ðŸ§ª In Progress
  â”‚   â””â”€â”€ Milestone 3.5: Network Operations ðŸ“‹ Planned
  â”œâ”€â”€ Milestone 5: Developer Preview ðŸŽ¯ Target
  â”‚   â”œâ”€â”€ Code Engineer Capability Pack
  â”‚   â”œâ”€â”€ Research Assistant Capability Pack
  â”‚   â”œâ”€â”€ DevOps Assistant Capability Pack
  â”‚   â””â”€â”€ Trading Analyst Capability Pack (final certification gate)
  â””â”€â”€ Post Developer Preview
      â”œâ”€â”€ v1.1: Capability Excellence
      â”œâ”€â”€ v1.2: Community Ecosystem
      â””â”€â”€ v1.3: Enterprise
```

---

## 8-Week Sprint Plan â€” First Product Release

This sprint plan assumes vibe coding discipline: AI generates, AI reviews, AI tests, AI benchmarks, humans approve.
> Terjemahan Indonesia: Ini sprint plan assumes vibe coding discipline: AI generates, AI reviews, AI tests, AI benchmarks, humans approve.

### Week 1 â€” Chat UX

**Focus:** Single conversation interface like Kimi/ChatGPT.
- Chat UI with streaming
- Markdown rendering
- File upload
- Workspace switcher
- Progress indication
- Artifact viewer

**Gate:** User can upload a MikroTik config and see streaming analysis.

---

### Week 2 â€” Workspace

**Focus:** Project isolation and memory.
- Workspace CRUD
- Conversation history per workspace
- Artifact storage and retrieval
- Memory scoping per workspace

**Gate:** User can switch between two workspaces and history is isolated.

---

### Week 3 â€” Streaming & Long Context

**Focus:** Real-time execution feedback.
- Event streaming from Execution Runtime
- Subtask progress updates
- Artifact streaming
- Error recovery messaging

**Gate:** User sees real-time progress during a 5+ step task.

---

### Week 4 â€” Capability Excellence: Network

**Focus:** Make Network Engineer genuinely expert.
- Add 20 real cases to `real_cases/network/`
- Improve analyzer depth
- Enhance explainability
- Benchmark: 92%+

**Gate:** Network benchmark score â‰¥92%.

---

### Week 5 â€” Capability Excellence: Code, Research, DevOps

**Focus:** Bring remaining packs to minimum viable quality.
- Code: Review + Patch end-to-end
- Research: Evidence ranking + citations
- DevOps: Docker + CI/CD generation

**Gate:** All three packs pass â‰¥80% benchmark.

---

### Week 6 â€” Dogfooding

**Focus:** Use ECP to build ECP.
- Audit ECP docs with Self Development
- Review ECP code with Code Capability
- Document findings in `real_cases/`

**Gate:** 50+ real cases collected, all fed back into capability packs.

---

### Week 7 â€” Benchmark & Polish

**Focus:** Measure and improve.
- Run all capability benchmarks
- Fix regressions
- Polish UX flows against USER_JOURNEYS.md
- Performance optimization

**Gate:** All 6 packs meet Developer Preview quality targets.

---

### Week 8 â€” Developer Preview

**Focus:** Product release.
- Release notes
- SDK documentation
- Quick Start
- Public announcement

**Gate:** ECP v1.0.0 released with certified capability packs.

---

## Development Rhythm

| Day | Focus |
|-----|-------|
| Monday | Knowledge expansion |
| Tuesday | Benchmark improvement |
| Wednesday | Reasoning improvement |
| Thursday | Explainability |
| Friday | Benchmark score increase |

All changes happen inside Capability Packs. Core remains untouched.
> Terjemahan Indonesia: All changes happen inside kapabilitas Packs. Core remains untouched.
