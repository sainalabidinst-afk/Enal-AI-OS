# RFC-0013: Business Analyst Capability Pack

| Field | Value |
|-------|-------|
| **RFC ID** | RFC-0013 |
| **Status** | Draft |
| **Version** | 0.1.0 |
| **Author** | Enal AI OS Core Team |
| **Target Release** | v1.3.0 (Enterprise phase) |
| **Capability Pack** | Business Analyst |
| **Capability ID** | `business-analyst` |
| **Category** | Business Analysis |
| **Quality Target** | A (≥90) |
| **Maturity Target** | Level 3 — Production Ready |
| **Reference RFC** | RFC-0013 |

---

## Motivation

ECP's existing Capability Packs build systems, but there is no dedicated business analysis layer that translates business needs into technical specifications that can be executed by other packs.

Currently:

1. **Requirements are gathered manually** — business needs are passed as natural language, often with ambiguity, gaps, and conflicting stakeholder priorities.
2. **No business process modeling** — workflows and processes are not formally modeled before being translated to technical implementations.
3. **User stories and acceptance criteria are not standardized** — different packs interpret requirements differently.
4. **No gap analysis** — discrepancies between business needs and technical capabilities are not systematically identified.
5. **No ROI analysis** — investment decisions lack quantified return-on-investment analysis.
6. **BRD and functional specifications are generated ad hoc** — no systematic generation of Business Requirement Documents or functional specs.
7. **No requirement quality scoring** — ambiguous, incomplete, or conflicting requirements are not flagged before they cause downstream rework.

The Business Analyst Capability Pack becomes the requirements translation layer, converting business needs into clear, unambiguous, executable specifications that Code Engineer, System Architect, and all other packs can consume.

---

## Problem Statement

Without a dedicated Business Analyst Capability Pack:

- **Ambiguous requirements reach development** — unclear, vague, or contradictory requirements cause rework downstream.
- **No business process modeling** — complex workflows are not visualized or analyzed before implementation.
- **User stories lack acceptance criteria** — stories are generated without clear, testable acceptance conditions.
- **No gap analysis** — business needs vs. technical capabilities are not systematically compared.
- **ROI is not quantified** — investment decisions lack data-driven return calculations.
- **BRD and functional specifications are missing** — formal documentation is not systematically produced.
- **Stakeholder conflicts are not resolved** — conflicting needs are not structured or mediated.
- **No process optimization** — business processes are not analyzed for inefficiencies before implementation.

The absence of Business Analyst means that good requirements—the foundation of all good software—are not systematically ensured, leading to expensive rework and poor outcomes.

---

## Goals

1. **Requirement Gathering** — Collect, structure, and validate business requirements from stakeholders.
2. **Business Process Modeling** — Model workflows and processes using BPMN-like notation.
3. **User Story Generation** — Generate well-formed user stories with acceptance criteria.
4. **Use Case Modeling** — Generate detailed use cases from requirements.
5. **BRD Generation** — Generate Business Requirement Documents from raw inputs.
6. **Functional Specification** — Generate executable functional specifications for downstream packs.
7. **Gap Analysis** — Identify and document gaps between business needs and technical capabilities.
8. **ROI Analysis** — Quantify return-on-investment for proposed features or projects.
9. **Process Optimization** — Identify inefficiencies in business processes and recommend improvements.

### Success Criteria

| Metric | Target | Grade |
|--------|--------|-------|
| Requirement Clarity | ≥90% (requirements free of ambiguity) | A |
| User Story Quality | ≥95% (stories with complete acceptance criteria) | A |
| Gap Analysis Coverage | ≥90% (all gaps identified) | A |
| ROI Accuracy | ≥85% (ROI predictions within ±10% of actual) | A |
| Process Optimization | ≥80% (inefficiencies identified and addressed) | A |
| BRD Completeness | ≥95% (all required sections present) | A |
| Stakeholder Consistency | ≥90% (conflicts identified and resolved) | A |
| Explainability | ≥95% (rationale for all recommendations) | A+ |

---

## Non-Goals

1. **Stakeholder facilitation** — Business Analyst structures requirements; it does not conduct stakeholder meetings.
2. **Business strategy definition** — Focus is on requirements translation, not business strategy.
3. **Replacing dedicated BA tools** — Tools like JIRA, Confluence, Miro remain; Business Analyst provides analysis and generation.
4. **Project management** — Does not manage project timelines, resources, or sprint planning.
5. **Core modification** — All implementation resides within the Business Analyst Capability Pack.

---

## Capability Scope

### Core Capabilities

| Capability | Description | Inputs | Outputs |
|-----------|-------------|--------|---------|
| Requirement Gathering | Collect, structure, and validate requirements from stakeholder inputs | Natural language requirements, stakeholder notes, interview transcripts | Structured requirement documents with quality scores |
| Business Process Modeling | Model workflows using BPMN-like notation | Process descriptions, workflow narratives | Process models with activities, gateways, data flows |
| User Story Generation | Generate INVEST-compliant user stories with acceptance criteria | Requirements, personas, user journeys | User stories with detailed acceptance criteria |
| Use Case Modeling | Generate detailed use cases from requirements | Requirements, user roles, system interactions | Use case diagrams and detailed use case descriptions |
| BRD Generation | Generate Business Requirement Documents | Raw requirements, business context, stakeholder inputs | BRD document with all standard sections |
| Functional Specification | Generate executable functional specs for downstream packs | BRD, user stories, use cases | Functional specification in structured format |
| Gap Analysis | Identify gaps between business needs and technical capabilities | Requirements, current state, technical constraints | Gap analysis report with prioritization |
| ROI Analysis | Quantify return-on-investment for proposed features | Cost estimates, benefit projections, timeline | ROI analysis report with NPV, payback period |
| Process Optimization | Identify and recommend process improvements | Process models, current performance data | Process optimization recommendations |

### Out of Scope

- Stakeholder facilitation or meeting management
- Project planning or resource allocation
- Business strategy formulation
- Financial planning beyond ROI analysis
- Change management implementation
- Live process execution or monitoring

---

## Public Contracts

### Input Contract: Business Analysis Request

```json
{
  "request_id": "uuid",
  "operation": "requirement_gathering | process_modeling | user_story | use_case | brd_generation | functional_spec | gap_analysis | roi_analysis | process_optimization",
  "business_context": {
    "domain": "string — e.g., e-commerce, fintech, healthcare",
    "project_name": "string",
    "description": "string — project overview"
  },
  "inputs": {
    "natural_language_requirements": ["string"],
    "stakeholder_notes": ["string"],
    "interview_transcripts": ["string"],
    "current_state_documentation": "string",
    "technical_constraints": ["string"],
    "personas": [
      {
        "name": "string",
        "role": "string",
        "goals": ["string"],
        "pain_points": ["string"]
      }
    ]
  },
  "quality_attributes": {
    "availability_target": "string",
    "performance_target": "string",
    "security_target": "string"
  },
  "output_format": "json | markdown | bpmn | jira | confluence"
}
```

### Output Contract: Business Analysis Report

```json
{
  "request_id": "uuid",
  "operation": "string",
  "requirements": [
    {
      "id": "string",
      "title": "string",
      "description": "string",
      "type": "functional | non_functional",
      "priority": "must_have | should_have | could_have | won't_have",
      "clarity_score": 0.0,
      "ambiguity_flags": ["string"],
      "source": "string — stakeholder or document source",
      "acceptance_criteria": ["string"],
      "dependencies": ["string"]
    }
  ],
  "user_stories": [
    {
      "id": "string",
      "title": "As a <role> I want <goal> so that <benefit>",
      "description": "string",
      "acceptance_criteria": ["string"],
      "story_points": 0,
      "priority": "must_have | should_have | could_have | won't_have",
      "dependencies": ["string"]
    }
  ],
  "process_models": [
    {
      "id": "string",
      "name": "string",
      "activities": ["string"],
      "gateways": ["string"],
      "data_flows": ["string"],
      "start_event": "string",
      "end_event": "string"
    }
  ],
  "gap_analysis": {
    "current_state": "string",
    "target_state": "string",
    "gaps": [
      {
        "description": "string",
        "impact": "high | medium | low",
        "priority": "critical | high | medium | low",
        "remediation": "string"
      }
    ],
    "capability_gaps": ["string"]
  },
  "roi_analysis": {
    "investment_cost": 0.0,
    "projected_benefits": 0.0,
    "time_horizon_months": 0,
    "npv": 0.0,
    "payback_period_months": 0,
    "irr": 0.0,
    "confidence_score": 0.0
  },
  "optimization_recommendations": [
    {
      "process": "string",
      "inefficiency": "string",
      "recommendation": "string",
      "expected_benefit": "string",
      "effort": "low | medium | high"
    }
  ],
  "quality_metrics": {
    "requirement_clarity": 0.0,
    "story_quality": 0.0,
    "completeness": 0.0,
    "ambiguity_resolution_rate": 0.0
  },
  "summary": {
    "total_requirements": 0,
    "user_stories_count": 0,
    "gaps_identified": 0,
    "recommendations_count": 0,
    "overall_confidence": 0.0,
    "next_steps": ["string"]
  }
}
```

### Requirement Record (Experience Memory)

```json
{
  "record_id": "uuid",
  "request_id": "uuid",
  "timestamp": "ISO 8601",
  "requirements_count": 0,
  "user_stories_count": 0,
  "gaps_identified": 0,
  "roi_positive": true,
  "requirements_accepted": 0,
  "outcome": "accepted | partially_accepted | rejected | revised"
}
```

---

## Integration Points (Capability Graph)

```
Business Stakeholder / User
    │
    │  provides natural language requirements
    ▼
Business Analyst Engine
    │
    │  ┌─────────────────────────────────────────────────────┐
    │  │ 1. Requirement Gathering                            │
    │  │ 2. Business Process Modeling                       │
    │  │ 3. User Story Generation                            │
    │  │ 4. Use Case Modeling                                │
    │  │ 5. BRD Generation                                  │
    │  │ 6. Functional Specification                         │
    │  │ 7. Gap Analysis                                     │
    │  │ 8. ROI Analysis                                     │
    │  │ 9. Process Optimization → Experience Memory         │
    │  └─────────────────────────────────────────────────────┘
    │
    │  produces structured functional specification
    ▼
Execution Runtime
    │
    │  routes to consumer Capability Packs (Code Engineer, System Architect, etc.)
    ▼
Consumer Capability Packs
    │
    │  consume functional spec for implementation
    ▼
User / Human Approval Loop
```

### Task Template

| Task | Subtasks |
|------|----------|
| Business Analysis | Input collection → Requirement gathering → Process modeling → User story generation → Use case modeling → Gap analysis → ROI analysis → Process optimization → Specification generation |

---

## Consumer Capability Packs

| Consumer Capability Pack | Use Case |
|--------------------------|----------|
| **Code Engineer** | Consume functional specs to generate code and tests |
| **System Architect** | Consume functional specs for architecture design |
| **DevOps Assistant** | Consume deployment requirements and infrastructure specs |
| **Decision Intelligence** | Evaluate ROI and risk of proposed business initiatives |
| **Self Development** | Identify business process improvement opportunities |

---

## Dependencies

### Internal Dependencies (Shared Contracts)

1. **Execution Runtime** — Task routing and orchestration (per ADR-002)
2. **Experience Memory** — Requirement and decision records persistence (per ADR-011)
3. **Shared Contracts** — Task/Intent definition and result schema (per ADR-006)

### External Knowledge

1. **BABOK (Business Analysis Body of Knowledge)** — Standard BA practices
2. **BPMN** — Business Process Model and Notation
3. **INVEST Criteria** — User story quality framework
4. **ROI/NPV/IRR** — Financial analysis methodologies

### No Core Changes Required

All implementation resides within the Business Analyst Capability Pack:

```
apps/
└── business_analyst/
    ├── engine.py              # Domain Engine (per ADR-004)
    ├── worker.py              # Thin adapter (per ADR-003)
    ├── schemas.py             # Public contracts
    ├── requirement_gatherer.py  # Requirement gathering and structuring
    ├── process_modeler.py     # Business process modeling (BPMN-like)
    ├── story_generator.py     # User story generation
    ├── use_case_modeler.py    # Use case modeling
    ├── brd_generator.py       # BRD generation
    ├── spec_generator.py      # Functional specification generation
    ├── gap_analyzer.py        # Gap analysis
    ├── roi_calculator.py      # ROI analysis
    └── optimizer.py           # Process optimization
```

**ADR Impact:** None. No Core, Runtime, Kernel, or shared contract modification required.

---

## Benchmark Specification

### Benchmark Framework

| Dimension | Definition | Measurement | Target |
|-----------|------------|-------------|--------|
| **Requirement Clarity** | % of requirements free of ambiguity | Expert review of requirement quality | ≥90% |
| **User Story Quality** | % of stories with complete acceptance criteria | Acceptance criteria present / stories | ≥95% |
| **Gap Analysis Coverage** | % of business-technical gaps identified | Gaps found / ground truth gaps | ≥90% |
| **ROI Accuracy** | ROI predictions match actual outcomes | ROI predicted vs. actual within ±10% | ≥85% |
| **Process Optimization** | % of inefficiencies identified and addressed | Improvements found / total inefficiencies | ≥80% |
| **BRD Completeness** | % of required BRD sections present | Sections present / total expected | ≥95% |
| **Stakeholder Consistency** | % of conflicts identified and resolved | Conflicts resolved / total conflicts | ≥90% |
| **Explainability** | Clarity of rationale for recommendations | Human evaluation score | ≥95% |
| **Consistency** | Same input produces same spec | Variance across 10 runs < 5% | ≥90% |

### Benchmark Dataset

- **100 business cases** covering:
  - E-commerce (inventory, checkout, recommendation)
  - Fintech (trading platform, risk assessment, compliance)
  - Healthcare (patient management, appointment scheduling)
  - SaaS (multi-tenant platform, billing, analytics)
  - Enterprise (workflow automation, reporting, integration)

### Benchmark Dimensions Detail

| Scenario Type | Description | Ground Truth |
|---------------|-------------|-------------|
| Ambiguous Requirements | Requirements with unclear language | Expert disambiguation |
| Conflicting Stakeholder Needs | Stakeholders with opposing priorities | Conflict resolution records |
| Missing Acceptance Criteria | Stories without testable conditions | Expert-completed criteria |
| Process Optimization | Inefficient business processes | Process improvement records |

---

## Golden Test Specification

| # | Scenario | Expected Outcome | Acceptance Criteria |
|---|----------|-----------------|---------------------|
| 1 | Ambiguous requirement ("fast system") | Requirement clarified with measurable criteria | ≥90% clarity improvement |
| 2 | Conflicting stakeholder needs (security vs. usability) | Conflict identified and mediated | ≥90% resolution |
| 3 | Missing acceptance criteria in user story | Criteria generated with testable conditions | ≥95% completeness |
| 4 | Process with inefficiency (manual approval step) | Bottleneck identified with automation suggestion | ≥85% detection |
| 5 | ROI analysis with cost/benefit data | NPV, payback, IRR calculated | ≥85% accuracy vs. actual |
| 6 | Gap analysis (current vs. target state) | Gaps identified with priorities | ≥90% coverage |
| 7 | BRD generation from raw notes | Complete BRD with all sections | ≥95% completeness |
| 8 | Use case modeling from requirement | Detailed use cases with actors and flows | ≥90% completeness |
| 9 | Functional specification for Code Engineer | Structured spec consumable by Code Engineer | ≥90% usability |
| 10 | Business process model from workflow description | BPMN-like model with activities and gateways | ≥90% accuracy |

### Golden Test Acceptance Criteria

- All 10 golden test scenarios pass at ≥90% of acceptance criteria (100% pass)
- Overall Business Analyst golden test pass rate ≥90%
- All generated user stories have complete acceptance criteria
- ROI calculations validated against financial standards

---

## Real Case Requirements

### Real Case Directory

`real_cases/business_analyst/` must contain:

| Requirement | Minimum Count |
|-------------|---------------|
| Real business analysis cases from actual usage | 20 |
| Cases with ambiguous requirements | 5 |
| Cases with conflicting stakeholder needs | 5 |
| Cases with missing acceptance criteria | 5 |
| Cases with ROI analysis | 10 |
| Cases with process optimization | 5 |
| Cases with expert review/validation | 15 |

### Real Case Structure

```
real_cases/business_analyst/<case_id>/
├── input/
│   ├── raw_requirements/       # Natural language requirements, stakeholder notes
│   ├── business_context.md      # Domain and project description
│   └── constraints.md           # Technical and business constraints
├── output/
│   ├── analysis_report.json    # Full Business Analysis Report
│   ├── functional_spec.md      # Generated functional specification
│   ├── user_stories.jsonl      # Generated user stories
│   └── roi_analysis.md         # ROI calculation details
└── evaluation.md               # Ground truth, expert review, lessons learned
```

### Real Case Targets

| Metric | Target |
|--------|--------|
| Real cases logged | ≥20 (Level 3) → ≥100 (Level 4) |
| Real case quality score (expert review) | ≥90% |
| Requirements accepted downstream | ≥85% of generated specs used without major revision |

---

## Definition of Done

```text
Definition of Done — Business Analyst Capability Pack

Functional
- [ ] Requirement Gathering collects, structures, and validates requirements with quality scoring
- [ ] Business Process Modeling produces BPMN-like models from workflow descriptions
- [ ] User Story Generation produces INVEST-compliant stories with acceptance criteria
- [ ] Use Case Modeling generates detailed use cases with actors and flows
- [ ] BRD Generation produces complete Business Requirement Documents
- [ ] Functional Specification generates structured specs consumable by downstream packs
- [ ] Gap Analysis identifies and prioritizes business-technical gaps
- [ ] ROI Analysis calculates NPV, payback period, and IRR with confidence scoring
- [ ] Process Optimization identifies inefficiencies and recommends improvements

Benchmark
- [ ] Requirement Clarity ≥ 90% (grade A)
- [ ] User Story Quality ≥ 95%
- [ ] Gap Analysis Coverage ≥ 90%
- [ ] ROI Accuracy ≥ 85%
- [ ] Process Optimization ≥ 80%
- [ ] BRD Completeness ≥ 95%
- [ ] Stakeholder Consistency ≥ 90%
- [ ] Explainability ≥ 95%
- [ ] Consistency ≥ 90%

Golden Tests
- [ ] All 10 pack golden test scenarios pass at ≥90% of acceptance criteria (100% pass)

Real Cases
- [ ] ≥ 20 real cases logged in real_cases/business_analyst/
- [ ] Evaluation notes recorded for each case
- [ ] ≥ 5 cases with ambiguous requirements
- [ ] ≥ 5 cases with conflicting stakeholder needs
- [ ] ≥ 5 cases with missing acceptance criteria
- [ ] ≥ 10 cases with ROI analysis
- [ ] ≥ 5 cases with process optimization

Documentation
- [ ] Capability Guide updated (CAPABILITY_GUIDE.md — Business Analyst section)
- [ ] API reference / contract updated (this RFC + schemas.py)
- [ ] Real case evaluation summary published

SDK
- [ ] Pack accessible via SDK without Core changes
- [ ] Business Analyst callable via Execution Runtime task routing

Performance
- [ ] Latency P95 < 3000ms for standard business analysis
- [ ] Latency P95 < 8000ms for multi-stakeholder ROI analysis

Security
- [ ] No known P0/P1 security issues
- [ ] Generated documents do not expose confidential stakeholder information

Regression
- [ ] No regression in existing Capability Pack benchmark dimensions
- [ ] Benchmark reproducible (documented command + persisted result)

Release Notes
- [ ] Capability Changelog updated
```

---

## Risks

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| Ambiguous requirements misinterpreted | High — downstream rework | High | Conservative interpretation; confidence scoring; stakeholder review required |
| ROI analysis is inaccurate | Medium — poor investment decisions | Medium | Sensitivity analysis; confidence intervals; historical calibration |
| Process optimization recommendations are impractical | Medium — wasted effort | Medium | Effort estimation included; expert validation on real cases |
| User stories don't match developer expectations | Medium — development friction | High | Developer feedback loop; story review with Code Engineer |
| BRD/functional spec too verbose or too sparse | Medium — poor downstream consumption | High | Template-based with configurable detail levels; downstream validation |
| Gap analysis misses critical gaps | High — incomplete implementation | Medium | Multi-perspective analysis; stakeholder cross-check |
| Process modeling oversimplifies complex workflows | Medium — incorrect analysis | Medium | Incremental refinement; stakeholder validation checkpoints |

---

## ADR Impact

**Does this require Core changes?** No.

Business Analyst is a **new Capability Pack** that follows the established patterns:

- **ADR-001 (Core Pipeline Freeze):** No Core changes. All logic in `apps/business_analyst/`.
- **ADR-002 (Capability Pack Independence):** Business Analyst communicates with other packs via Execution Runtime tasks and shared contracts only. No direct imports.
- **ADR-003 (Worker = Adapter Only):** A thin Worker routes tasks to the Domain Engine.
- **ADR-004 (Domain Engine Owns Business Logic):** All business analysis logic resides in `apps/business_analyst/engine.py`.
- **ADR-005 (Human Approval Required):** All requirements and recommendations require human stakeholder approval before downstream consumption.
- **ADR-006 (Capability Contract v1 Frozen):** Uses the existing Capability Contract for node and subtask template registration. No contract changes.
- **ADR-007 (Conversation Boundary):** Business Analyst is invoked through Execution Runtime, not directly by Conversation Manager.
- **ADR-008 (Core Change Requires Cross-Capability Proof):** Not applicable — no Core changes.

**ADR Required:** None. This is a new Capability Pack, not a Core modification.

---

## Rollout Plan

### Phase 1: Prototype (RFC → Experimental)

**Duration:** 5 weeks

- [ ] Create `apps/business_analyst/` package structure
- [ ] Implement requirement gathering with quality scoring
- [ ] Implement user story generation with acceptance criteria
- [ ] Implement BRD generation (partial — core sections)
- [ ] Define public contracts (BA Request, BA Report)
- [ ] Implement thin Worker adapter
- [ ] Create 10 golden test scenarios
- [ ] Integration: Code Engineer ← Business Analyst (functional spec consumption)
- [ ] Integration: Self Development ← Business Analyst (process optimization)
- **Gate:** 10 golden tests pass at ≥80%

### Phase 2: Full Capabilities (Experimental → Stable)

**Duration:** 8 weeks

- [ ] Implement business process modeling (BPMN-like)
- [ ] Implement use case modeling
- [ ] Implement gap analysis
- [ ] Implement ROI analysis (NPV, payback, IRR)
- [ ] Implement process optimization
- [ ] Complete BRD generation (all sections)
- [ ] Implement functional specification generation
- [ ] Expand golden tests to 10 full scenarios
- [ ] Log ≥20 real cases from Code Engineer and project planning usage
- [ ] **Benchmark:** 100 business cases, ≥90% clarity, ≥95% story quality
- [ ] **Integration:** System Architect starts consuming functional specs from Business Analyst
- [ ] **Integration:** DevOps Assistant starts consuming infrastructure requirements from Business Analyst
- **Gate:** All 10 golden tests pass at ≥90%; benchmark ≥90%

### Phase 3: Ecosystem (Stable → Certified)

**Duration:** 6 weeks

- [ ] All 4 consumer packs integrated
- [ ] ROI analysis validated against financial standards
- [ ] Process optimization validated on real business processes
- [ ] Functional specs validated by Code Engineer consumption
- [ ] Independent audit of requirement quality and gap analysis
- [ ] Public benchmark dashboard available
- [ ] **Benchmark:** ≥90% across all dimensions sustained
- [ ] **Real Cases:** ≥100 cases with ≥80% downstream adoption
- **Gate:** Independent audit passed; benchmark ≥90% sustained

---

## Future Enhancements

### Fase 2 (Post-v1.0.0 Release)

1. **Stakeholder Simulation** — Model different stakeholder perspectives and resolve conflicts automatically
2. **Requirements Traceability Matrix** — End-to-end traceability from business needs to code and tests
3. **Acceptance Criteria Auto-Generation for QA** — Feed acceptance criteria directly to QA Engineer for test generation
4. **Business Impact Forecasting** — Predict downstream impact of requirement changes on code, tests, and deployment

### Fase 3 (Enterprise)

1. **Multi-Project Portfolio Analysis** — Analyze and prioritize requirements across an entire project portfolio
2. **Business Architecture Integration** — Link business capabilities to technical architecture
3. **Regulatory Compliance Requirements** — Generate compliance-mapped requirements (GDPR, HIPAA, SOX)
4. **Business Process Automation Discovery** — Identify automation opportunities from process models

### Long-term

1. **AI-Powered Requirements Discovery** — Interview stakeholders and extract requirements from conversation
2. **Requirements Evolution Management** — Track requirement changes and their cascading impact
3. **Business Value Stream Mapping** — End-to-end value stream analysis from business need to customer outcome
4. **Automated Business Case Generation** — Full business case documents from requirements and ROI analysis
