# RFC-0011: System Architect Capability Pack

| Field | Value |
|-------|-------|
| **RFC ID** | RFC-0011 |
| **Status** | Draft |
| **Version** | 0.1.0 |
| **Author** | Enal AI OS Core Team |
| **Target Release** | v1.3.0 (Enterprise phase) |
| **Capability Pack** | System Architect |
| **Capability ID** | `system-architect` |
| **Category** | Architecture |
| **Quality Target** | A (≥90) |
| **Maturity Target** | Level 3 — Production Ready |
| **Reference RFC** | RFC-0011 |

---

## Motivation

ECP's existing Capability Packs generate code, design systems, and propose improvements. However, there is no dedicated architectural authority that reviews, validates, and guides the overall system design across all components.

Currently:

1. **Architecture decisions are decentralized** — each pack designs its own components without a unified architectural vision.
2. **No architecture governance** — there is no systematic enforcement of architectural principles, dependency rules, or design patterns.
3. **ADR generation is manual** — architectural decisions are not recorded in a structured, trackable format.
4. **No monolith-to-microservices analysis** — no guidance on when and how to decompose or consolidate services.
5. **Architecture reviews are ad hoc** — no systematic review of dependency violations, package boundaries, or scalability concerns.
6. **Event-driven and CQRS patterns are not evaluated** — modern architectural patterns are not systematically applied or validated.

The System Architect Capability Pack becomes the architectural authority layer, providing architecture review, Clean Architecture/DDD guidance, event-driven design, CQRS evaluation, microservices/monolith analysis, and ADR generation for all ECP projects and Capability Packs.

---

## Problem Statement

Without a dedicated System Architect Capability Pack:

- **No centralized architecture governance** — architectural violations (dependency cycles, layer violations, package boundary breaches) go undetected.
- **ADR generation is not automated** — architectural decisions are not systematically documented and tracked.
- **Design pattern evaluation is missing** — Clean Architecture, DDD, CQRS, Event-Driven patterns are not systematically applied or validated.
- **Microservices vs. monolith decisions are ad hoc** — no framework for evaluating decomposition strategies and their trade-offs.
- **Scalability and maintainability are not assessed** — no systematic analysis of architectural qualities.
- **Cross-Pack architecture consistency is not enforced** — each pack evolves independently, leading to architectural drift.
- **No architecture governance automation** — manual review processes are slow and inconsistent.

---

## Goals

1. **Clean Architecture Review** — Evaluate and enforce Clean Architecture principles (layers, dependency rule, boundaries).
2. **DDD Analysis** — Evaluate domain-driven design (bounded contexts, aggregates, domain events, anti-corruption layers).
3. **Event-Driven Design** — Evaluate event-driven architecture patterns and event schema design.
4. **CQRS Evaluation** — Evaluate Command Query Responsibility Segregation patterns and appropriateness.
5. **Microservices/Monolith Review** — Evaluate service decomposition strategies and monolith-to-microservices migration.
6. **Architecture Governance** — Enforce architectural rules, dependency constraints, and package boundaries.
7. **ADR Generation** — Generate and track Architecture Decision Records.
8. **Package Boundary Enforcement** — Detect and prevent dependency violations and layer inversions.

### Success Criteria

| Metric | Target | Grade |
|--------|--------|-------|
| Architecture Review Completeness | ≥95% (all architectural aspects reviewed) | A |
| Dependency Violation Detection | ≥95% (all violations found) | A |
| Package Boundary Enforcement | ≥90% (all violations detected) | A |
| ADR Coverage | ≥90% (decisions documented) | A |
| Design Pattern Application | ≥85% (patterns correctly evaluated) | A |
| Scalability Assessment | ≥90% (scalability concerns identified) | A |
| Maintainability Score | ≥90% (maintainability issues detected) | A |
| Explainability | ≥95% (findings explained with rationale) | A+ |

---

## Non-Goals

1. **Actual code architecture refactoring** — System Architect analyzes and recommends; refactoring is executed by Code Engineer.
2. **Real-time architecture monitoring** — Focus is on review and governance, not continuous monitoring.
3. **Replacing dedicated architecture tools** — tools like Structurizr, ArchUnit, or dependency checkers remain valid; System Architect provides orchestration.
4. **Infrastructure architecture** — Does not design physical infrastructure or cloud topology (DevOps Assistant handles deployment).
5. **Core modification** — All implementation resides within the System Architect Capability Pack.

---

## Capability Scope

### Core Capabilities

| Capability | Description | Inputs | Outputs |
|-----------|-------------|--------|---------|
| Clean Architecture Review | Evaluate layers, dependency rule, boundaries | Codebase, architecture diagrams | Review report with violations and recommendations |
| DDD Analysis | Evaluate bounded contexts, aggregates, domain events | Domain model, code structure | DDD assessment with improvement suggestions |
| Event-Driven Design | Evaluate event schemas, event flow, saga patterns | Event definitions, flow diagrams | Event-driven design review |
| CQRS Evaluation | Evaluate command/query separation appropriateness | Use cases, data models | CQRS suitability assessment |
| Microservices/Monolith Review | Evaluate decomposition strategy and migration path | Service boundaries, data relationships | Decomposition review with recommendations |
| Architecture Governance | Enforce architectural rules and constraints | Codebase, dependency graph | Governance report with violations |
| ADR Generation | Generate and track architectural decisions | Decision context, options considered | ADR document + tracking record |
| Package Boundary Enforcement | Detect dependency violations and layer inversions | Code structure, import graph | Violation report with fix guidance |

### Out of Scope

- Actual code refactoring or implementation
- Infrastructure/cloud architecture design
- Real-time architecture compliance monitoring
- Replacing dedicated static analysis tools
- Database schema design (Database Engineer handles this)
- Network topology design (Network Engineer handles this)

---

## Public Contracts

### Input Contract: Architecture Review Request

```json
{
  "review_id": "uuid",
  "review_type": "full_review | clean_architecture | ddd | event_driven | cqrs | microservices | package_boundary | adr_generation",
  "workspace_path": "string — path to project/workspace",
  "architecture_style": "clean_architecture | layered | hexagonal | ddd | microservices | monolith | event_driven",
  "existing_adrs": ["string — ADR IDs already in effect"],
  "constraints": ["string — architectural constraints"],
  "focus_areas": ["scalability | maintainability | testability | deployability | modifiability"],
  "include_recommendations": true
}
```

### Output Contract: Architecture Review Report

```json
{
  "review_id": "uuid",
  "review_type": "string",
  "findings": [
    {
      "id": "string",
      "category": "layer_violation | dependency_cycle | package_boundary | ddd_violation | event_design | cqrs_mismatch | monolith_anti_pattern | architecture_smell",
      "severity": "critical | high | medium | low",
      "title": "string",
      "description": "string",
      "evidence": "object — file path, line, code snippet",
      "recommendation": "string",
      "impact": "scalability | maintainability | testability | deployability | modifiability",
      "confidence": 0.0
    }
  ],
  "adr_draft": {
    "title": "string",
    "status": "proposed",
    "context": "string",
    "decision": "string",
    "consequences": ["string"]
  },
  "ddd_assessment": {
    "bounded_contexts": [
      {
        "name": "string",
        "entities": ["string"],
        "value_objects": ["string"],
        "aggregates": ["string"],
        "repositories": ["string"]
      }
    ],
    "anti_corruption_layers": ["string"],
    "domain_events": ["string"]
  },
  "architecture_metrics": {
    "dependency_cycles": 0,
    "layer_violations": 0,
    "package_boundaries_crossed": 0,
    "maintainability_score": 0.0,
    "scalability_score": 0.0,
    "testability_score": 0.0
  },
  "recommendations": [
    {
      "priority": "critical | high | medium | low",
      "problem": "string",
      "solution": "string",
      "effort": "low | medium | high",
      "impact": "string"
    }
  ],
  "summary": {
    "total_findings": 0,
    "critical_count": 0,
    "high_count": 0,
    "medium_count": 0,
    "low_count": 0,
    "overall_risk": "critical | high | medium | low",
    "confidence": 0.0
  }
}
```

### Architecture Review Record (Experience Memory)

```json
{
  "record_id": "uuid",
  "review_id": "uuid",
  "timestamp": "ISO 8601",
  "review_type": "string",
  "total_findings": 0,
  "violations_detected": 0,
  "adr_generated": true,
  "recommendations_count": 0,
  "outcome": "accepted | partially_accepted | rejected | revised",
  "adr_status": "proposed | accepted | rejected",
  "revisions": [{"revision_id": "uuid", "changes": "string"}]
}
```

---

## Integration Points (Capability Graph)

```
Consumer Capability Pack (Code Engineer, Self Development, and all others)
    │
    │  submits project for architecture review via task/intent
    ▼
Execution Runtime
    │
    │  routes to System Architect Domain Engine
    ▼
System Architect Engine
    │
    │  ┌─────────────────────────────────────────────────┐
    │  │ 1. Clean Architecture Review                    │
    │  │ 2. DDD Analysis                                 │
    │  │ 3. Event-Driven Design                          │
    │  │ 4. CQRS Evaluation                              │
    │  │ 5. Microservices/Monolith Review                │
    │  │ 6. Package Boundary Enforcement                  │
    │  │ 7. ADR Generation                               │
    │  │ 8. Architecture Metrics → Experience Memory     │
    │  └─────────────────────────────────────────────────┘
    │
    │  returns Architecture Review Report
    ▼
Consumer Capability Pack
    │
    │  receives findings + recommendations + ADR draft
    ▼
User / Human Approval Loop
```

### Task Template

| Task | Subtasks |
|------|----------|
| Architecture Review | Project scan → Dependency graph → Layer analysis → Package boundary check → DDD evaluation → Clean architecture review → ADR generation → Metrics → Report |

---

## Consumer Capability Packs

| Consumer Capability Pack | Use Case |
|--------------------------|----------|
| **Code Engineer** | Review generated code architecture, check for violations, apply ADRs |
| **Self Development** | Architecture improvement evaluation, package boundary validation |
| **Decision Intelligence** | Architecture risk scoring for system changes |
| **QA Engineer** | Architecture-based test strategy planning |
| **DevOps Assistant** | Microservices deployment architecture review |

---

## Dependencies

### Internal Dependencies (Shared Contracts)

1. **Execution Runtime** — Task routing and orchestration (per ADR-002)
2. **Experience Memory** — Architecture review records persistence (per ADR-011)
3. **Shared Contracts** — Task/Intent definition and result schema (per ADR-006)
4. **Capability Graph** — Dependency graph from Capability Pack registrations

### External Knowledge

1. **Clean Architecture** — Robert C. Martin's principles (layers, dependency rule, boundaries)
2. **DDD** — Eric Evans' domain-driven design patterns
3. **Event-Driven Architecture** — Enterprise integration patterns, event sourcing
4. **CQRS** — Command Query Responsibility Segregation patterns
5. **Microservices Patterns** — Chris Richardson's decomposition strategies
6. **Architecture Smells** — Taxonomy of architecture quality issues

### No Core Changes Required

All implementation resides within the System Architect Capability Pack:

```
apps/
└── system_architect/
    ├── engine.py              # Domain Engine (per ADR-004)
    ├── worker.py              # Thin adapter (per ADR-003)
    ├── schemas.py             # Public contracts
    ├── dependency_graph.py    # Import/dependency graph builder
    ├── layer_analyzer.py      # Clean Architecture layer analysis
    ├── ddd_analyzer.py        # DDD pattern evaluation
    ├── event_analyzer.py      # Event-driven design review
    ├── cqrs_evaluator.py      # CQRS suitability assessment
    ├── microservices_analyzer.py # Microservices/monolith review
    ├── boundary_enforcer.py   # Package boundary enforcement
    └── adr_generator.py       # ADR document generation
```

**ADR Impact:** None. No Core, Runtime, Kernel, or shared contract modification required.

---

## Benchmark Specification

### Benchmark Framework

| Dimension | Definition | Measurement | Target |
|-----------|------------|-------------|--------|
| **Architecture Review Completeness** | % of architectural aspects reviewed | % of expected analysis performed | ≥95% |
| **Dependency Violation Detection** | % of violations correctly identified | % of ground truth violations found | ≥95% |
| **Package Boundary Enforcement** | % of boundary violations detected | % of boundary issues found | ≥90% |
| **ADR Coverage** | % of decisions documented as ADRs | ADRs generated / decisions made | ≥90% |
| **Design Pattern Application** | % of patterns correctly evaluated | % of patterns correctly assessed | ≥85% |
| **Scalability Assessment** | % of scalability concerns identified | % of scalability issues found | ≥90% |
| **Maintainability** | % of maintainability issues detected | % of issues found in expert review | ≥90% |
| **Explainability** | Clarity of findings and recommendations | Human evaluation score | ≥95% |
| **Consistency** | Same input produces same output | Variance across 10 runs < 5% | ≥90% |

### Benchmark Dataset

- **100 architecture projects** covering:
  - Python monoliths
  - Node.js microservices
  - Java/Spring layered applications
  - Go hexagonal architectures
  - TypeScript frontend/backend applications
  - Mixed technology stacks

### Benchmark Dimensions Detail

| Scenario Type | Description | Ground Truth |
|---------------|-------------|-------------|
| Architecture Review | Full project structure analyzed for violations | Expert review |
| Dependency Violation | Cyclic dependencies, layer inversions | Manual static analysis |
| Package Boundary | Unauthorized cross-package imports | Import graph analysis |
| Scalability | Performance and scaling design issues | Architectural review |
| Maintainability | Code organization and testability concerns | Expert maintainability assessment |

---

## Golden Test Specification

| # | Scenario | Expected Outcome | Acceptance Criteria |
|---|----------|-----------------|---------------------|
| 1 | Clean Architecture layer violation | Violation detected with fix suggestion | ≥95% detection |
| 2 | Dependency cycle in Python project | Cycle identified with breaking points | ≥95% detection |
| 3 | Package boundary violation | Unauthorized import detected | ≥90% detection |
| 4 | DDD bounded context misalignment | Context boundary issues identified | ≥85% detection |
| 5 | Event-driven design anti-pattern | Missing event schema or saga detected | ≥85% detection |
| 6 | CQRS anti-pattern (write-through reads) | CQRS mismatch identified | ≥85% detection |
| 7 | Monolith decomposition opportunity | Decomposition candidates identified | ≥90% completeness |
| 8 | ADR generation for architectural decision | ADR draft produced with context/decision/consequences | ≥90% completeness |
| 9 | Scalability bottleneck in service design | Scalability concern identified | ≥90% detection |
| 10 | Maintainability degradation | Maintainability issue with remediation | ≥90% detection |

### Golden Test Acceptance Criteria

- All 10 golden test scenarios pass at ≥90% of acceptance criteria (100% pass)
- Overall System Architect golden test pass rate ≥90%
- All architecture violations include remediation guidance
- ADR drafts conform to standard template

---

## Real Case Requirements

### Real Case Directory

`real_cases/system_architect/` must contain:

| Requirement | Minimum Count |
|-------------|---------------|
| Real architecture reviews from actual usage | 20 |
| Cases with dependency violations | 10 |
| Cases with package boundary violations | 10 |
| Cases with ADR generation | 10 |
| Cases with expert review/validation | 15 |

### Real Case Structure

```
real_cases/system_architect/<case_id>/
├── input/
│   ├── project/             # Project source or structure description
│   └── review_request.json
├── output/
│   ├── report.json          # Full Architecture Review Report
│   ├── adr_draft.md         # Generated ADR
│   └── recommendations.md
└── evaluation.md            # Ground truth, expert review, lessons learned
```

### Real Case Targets

| Metric | Target |
|--------|--------|
| Real cases logged | ≥20 (Level 3) → ≥100 (Level 4) |
| Real case quality score (expert review) | ≥90% |
| ADR adoption rate | ≥80% of generated ADRs accepted by consumer packs |

---

## Definition of Done

```text
Definition of Done — System Architect Capability Pack

Functional
- [ ] Clean Architecture Review detects layer violations and dependency rule breaches
- [ ] DDD Analysis evaluates bounded contexts, aggregates, and anti-corruption layers
- [ ] Event-Driven Design reviews event schemas and saga patterns
- [ ] CQRS Evaluation assesses command/query separation appropriateness
- [ ] Microservices/Monolith Review evaluates decomposition strategies
- [ ] Architecture Governance enforces architectural rules and constraints
- [ ] ADR Generation produces structured ADR drafts for architectural decisions
- [ ] Package Boundary Enforcement detects unauthorized cross-package imports

Benchmark
- [ ] Architecture Review Completeness ≥ 95% (grade A)
- [ ] Dependency Violation Detection ≥ 95%
- [ ] Package Boundary Enforcement ≥ 90%
- [ ] ADR Coverage ≥ 90%
- [ ] Design Pattern Application ≥ 85%
- [ ] Scalability Assessment ≥ 90%
- [ ] Maintainability ≥ 90%
- [ ] Explainability ≥ 95%
- [ ] Consistency ≥ 90%

Golden Tests
- [ ] All 10 pack golden test scenarios pass at ≥90% of acceptance criteria (100% pass)

Real Cases
- [ ] ≥ 20 real cases logged in real_cases/system_architect/
- [ ] Evaluation notes recorded for each case
- [ ] ≥ 10 cases with dependency violations
- [ ] ≥ 10 cases with package boundary violations
- [ ] ≥ 10 cases with ADR generation

Documentation
- [ ] Capability Guide updated (CAPABILITY_GUIDE.md — System Architect section)
- [ ] API reference / contract updated (this RFC + schemas.py)
- [ ] Real case evaluation summary published

SDK
- [ ] Pack accessible via SDK without Core changes
- [ ] System Architect callable via Execution Runtime task routing

Performance
- [ ] Latency P95 < 3000ms for single project review
- [ ] Latency P95 < 8000ms for multi-module monorepo

Security
- [ ] No known P0/P1 security issues
- [ ] Generated ADRs do not expose sensitive implementation details

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
| Over-flagging leads to analysis paralysis | High — too many findings to address | Medium | Severity-based filtering; prioritize critical findings |
| Architecture metrics are noisy or inconsistent | Medium — unreliable assessment | High | Standardized metric definitions; calibration across projects |
| ADR generation produces boilerplate content | Medium — low value ADRs | Medium | Template-based with context-aware content; quality threshold |
| Package boundary analysis misses complex imports | Medium — undetected violations | Low | AST-based analysis with import resolution; multi-language support |
| DDD analysis misclassifies domain boundaries | Medium — incorrect recommendations | Low | Pattern-based with expert validation; confidence scoring |
| Recommendations conflict with existing architecture decisions | Medium — confusion and rework | Medium | ADR cross-reference; existing decision awareness |
| Performance cost of deep analysis on large codebases | Low — slow review process | High | Incremental analysis; parallel processing; progress reporting |

---

## ADR Impact

**Does this require Core changes?** No.

System Architect is a **new Capability Pack** that follows the established patterns:

- **ADR-001 (Core Pipeline Freeze):** No Core changes. All logic in `apps/system_architect/`.
- **ADR-002 (Capability Pack Independence):** System Architect communicates with other packs via Execution Runtime tasks and shared contracts only. No direct imports.
- **ADR-003 (Worker = Adapter Only):** A thin Worker routes tasks to the Domain Engine.
- **ADR-004 (Domain Engine Owns Business Logic):** All architecture analysis logic resides in `apps/system_architect/engine.py`.
- **ADR-005 (Human Approval Required):** All architectural recommendations and ADRs require human approval; no automated refactoring.
- **ADR-006 (Capability Contract v1 Frozen):** Uses the existing Capability Contract for node and subtask template registration. No contract changes.
- **ADR-007 (Conversation Boundary):** System Architect is invoked through Execution Runtime, not directly by Conversation Manager.
- **ADR-008 (Core Change Requires Cross-Capability Proof):** Not applicable — no Core changes.

**ADR Required:** None. This is a new Capability Pack, not a Core modification.

---

## Rollout Plan

### Phase 1: Prototype (RFC → Experimental)

**Duration:** 5 weeks

- [ ] Create `apps/system_architect/` package structure
- [ ] Implement dependency graph builder (Python import analysis)
- [ ] Implement basic layer analysis and package boundary detection
- [ ] Implement Clean Architecture violation detection
- [ ] Define public contracts (Review Request, Review Report)
- [ ] Implement thin Worker adapter
- [ ] Create 10 golden test scenarios
- [ ] Integration: Code Engineer → System Architect (architecture review)
- [ ] Integration: Self Development → System Architect (boundary enforcement)
- **Gate:** 10 golden tests pass at ≥80%

### Phase 2: Full Capabilities (Experimental → Stable)

**Duration:** 8 weeks

- [ ] Implement DDD analysis (bounded contexts, aggregates)
- [ ] Implement event-driven design review
- [ ] Implement CQRS evaluation
- [ ] Implement microservices/monolith review
- [ ] Implement ADR generation with standard template
- [ ] Add JavaScript/TypeScript and Java support
- [ ] Expand golden tests to 10 full scenarios
- [ ] Log ≥20 real cases from Code Engineer and Self Development usage
- [ ] **Benchmark:** 100 projects, ≥95% review completeness, ≥95% violation detection
- [ ] **Integration:** QA Engineer starts using System Architect for architecture-based test planning
- **Gate:** All 10 golden tests pass at ≥90%; benchmark ≥95%

### Phase 3: Ecosystem (Stable → Certified)

**Duration:** 6 weeks

- [ ] All 5+ consumer packs integrated
- [ ] ADR generation validated by expert review
- [ ] Multi-language support (Python, JS/TS, Java, Go)
- [ ] Independent audit of violation detection accuracy
- [ ] Public benchmark dashboard available
- [ ] **Benchmark:** ≥95% across all dimensions sustained
- [ ] **Real Cases:** ≥100 cases with ≥80% expert validation
- **Gate:** Independent audit passed; benchmark ≥95% sustained

---

## Future Enhancements

### Fase 2 (Post-v1.0.0 Release)

1. **Architecture Decision Impact Analysis** — Evaluate consequences of architectural decisions before they are made
2. **Architecture Fitness Function** — Continuously validate architectural rules through automated tests
3. **Multi-Repository Architecture Review** — Review architecture across multiple services/repositories
4. **Architecture Debt Tracking** — Track and prioritize architectural debt accumulation

### Fase 3 (Enterprise)

1. **Enterprise Architecture Governance** — Central policy management and compliance reporting across all projects
2. **Architecture Intelligence Dashboard** — Portfolio-level architecture metrics and trend analysis
3. **Cross-Project Architecture Reuse** — Identify and promote architectural patterns across projects
4. **Architecture Migration Planning** — Plan and execute large-scale architectural transformations

### Long-term

1. **AI-Driven Architecture Synthesis** — Generate optimal architectures from requirements
2. **Architecture Evolution Forecasting** — Predict architectural drift and recommend interventions
3. **Architecture Compliance as Code** — Express architectural rules as executable specifications
4. **Self-Healing Architecture** — Automatically detect and resolve architectural violations
