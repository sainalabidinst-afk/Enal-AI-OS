# RFC-0011: System Architect Capability Pack

| Field | Value |
|-------|-------|
| **RFC ID** | RFC-0011 |
| **Status** | Draft |
| **Version** | 0.1.0 |
| **Author** | Enal AI OS Core Team |
| **Target Release** | v1.3.0 (Enterprise phase, Phase 3) |
| **Capability Pack** | System Architect |
| **Capability ID** | `system-architect` |
| **Category** | Architecture |
| **Quality Target** | A (≥90) |
| **Maturity Target** | Level 3 — Production Ready |
| **Reference RFC** | RFC-0011 |

---

## Motivation

Code Engineer generates code with good architecture patterns (Clean Architecture, DDD, SOLID, CQRS — per RFC-0006). Self Development analyzes project structure and proposes improvements. However, no Capability Pack provides **enterprise-level system architecture** capabilities:

- Cross-system architecture governance
- Event-driven and microservices design at scale
- Architecture decision record (ADR) generation
- Architecture violation detection (package boundaries, dependency rules)
- Architecture quality assessment (scalability, maintainability, modularity)

The System Architect Capability Pack becomes the **architecture governance layer** — ensuring that systems designed and built by Code Engineer, DevOps Assistant, and Self Development adhere to enterprise architecture principles and best practices.

Key motivations:

1. **Architecture quality degrades at scale** — as more services are generated, architectural drift and violations go undetected.
2. **ADR generation is manual** — architecture decisions are not systematically documented.
3. **Cross-system dependencies are not analyzed** — microservices and event-driven architectures lack dependency and impact analysis.
4. **Architecture governance is absent** — no centralized enforcement of architecture rules (package boundaries, layering, dependency direction).
5. **Scalability and maintainability are not quantified** — architecture quality is assessed qualitatively, not through structured metrics.

---

## Problem Statement

Without a dedicated System Architect Capability Pack:

- **Architecture violations go undetected** — Code Engineer detects patterns but does not enforce package boundaries or dependency direction across services.
- **ADR generation is ad hoc** — architecture decisions are not systematically captured, versioned, or linked to impact analysis.
- **Cross-system dependency analysis is missing** — when one service changes, the impact on dependent services is not assessed.
- **Event-driven architecture design is partial** — event flow, event schemas, and consumer patterns are not systematically designed.
- **Microservices decomposition is not evaluated** — the granularity and boundaries of microservices are not assessed for maintainability and scalability.
- **Monolith decomposition is not guided** — monolith-to-microservices migration lacks structured architecture review.
- **Architecture governance is decentralized** — each pack applies its own architecture rules with no central policy enforcement.

The absence of System Architect means architectural debt accumulates across the platform without detection, remediation, or governance.

---

## Goals

1. **Clean Architecture Analysis** — Assess and recommend clean architecture layers, boundaries, and dependency rules.
2. **DDD Implementation** — Analyze bounded contexts, aggregates, domain events, and anti-corruption layers.
3. **Event-Driven Design** — Design event flows, event schemas, and consumer patterns.
4. **Microservices Architecture** — Evaluate microservices boundaries, decomposition, and communication patterns.
5. **Monolith Review** — Assess monolith health and provide decomposition recommendations.
6. **Architecture Governance** — Enforce architecture rules (package boundaries, dependency direction, layering).
7. **ADR Generation** — Automatically generate and manage Architecture Decision Records.
8. **Architecture Quality Metrics** — Quantify scalability, maintainability, modularity, and coupling.

### Success Criteria

| Metric | Target | Grade |
|--------|--------|-------|
| Architecture Violation Detection | ≥95% (violations correctly identified) | A |
| ADR Generation Quality | ≥90% (ADRs contain all required sections with traceability) | A |
| Dependency Analysis Accuracy | ≥90% (cross-system dependencies correctly mapped) | A |
| Architecture Quality Assessment | ≥85% (scalability/maintainability scores match expert review) | A- |
| ADR Compliance | ≥95% (all significant decisions have ADRs) | A |
| Event Flow Completeness | ≥90% (all event flows have documented schemas) | A |
| Package Boundary Enforcement | ≥95% (all package boundaries enforced) | A |
| Consistency | ≥90% (same architecture produces same analysis across runs) | A |

---

## Non-Goals

1. **Architecture implementation** — System Architect analyzes and recommends; it does not implement architectural changes.
2. **Replacing Code Engineer's pattern detection** — Code Engineer detects patterns in code; System Architect evaluates architecture at the system level.
3. **Real-time architecture monitoring** — Continuous runtime architecture analysis is out of scope (observability is DevOps' domain).
4. **Replacing enterprise architecture frameworks** — TOGAF, Zachman, etc. are frameworks, not replacements for System Architect's automated analysis.
5. **Core modification** — All implementation resides within the System Architect Capability Pack.

---

## Capability Scope

### Core Capabilities

| Capability | Description | Inputs | Outputs |
|-----------|-------------|--------|---------|
| Clean Architecture Analysis | Assess architecture layers, boundaries, dependency rules. | Codebase, dependency graph, module structure | Architecture assessment with violation list |
| DDD Implementation | Analyze bounded contexts, aggregates, domain events. | Domain models, codebase, event logs | DDD compliance report, boundary recommendations |
| Event-Driven Design | Design event flows, schemas, and consumer patterns. | Event logs, system interactions, message queues | Event architecture document, schema definitions |
| Microservices Architecture | Evaluate service boundaries, decomposition, communication. | Service definitions, API specs, dependency graph | Decomposition analysis, communication patterns |
| Monolith Review | Assess monolith health and suggest decomposition. | Monolith codebase, module structure | Health score, decomposition roadmap |
| Architecture Governance | Enforce architecture rules across all systems. | Codebase, package structure, dependency graph | Rule violation report, governance dashboard |
| ADR Generation | Generate and manage Architecture Decision Records. | Architecture decisions, context, constraints | ADR documents with traceability matrix |
| Architecture Quality Metrics | Quantify scalability, maintainability, modularity. | Architecture assessment, code metrics, benchmarks | Quality scores with dimension breakdown |

### Out of Scope

- Runtime architecture monitoring and alerting
- Architecture framework consulting (TOGAF, Zachman)
- Enterprise business architecture (strategy-level)
- Physical infrastructure architecture (data center design)
- Real-time service mesh configuration

---

## Public Contracts

### Input Contract: Architecture Review Request

```json
{
  "review_id": "uuid",
  "intent": "architecture_review | adr_generation | governance_check | quality_assessment | monolith_review | event_design | microservices_analysis",
  "system": {
    "name": "string — system name",
    "type": "monolith | microservices | event_driven | hybrid",
    "description": "string",
    "version": "string"
  },
  "artifacts": [
    {
      "type": "source_code | architecture_diagram | api_spec | dependency_graph | event_log | adr",
      "location": "string — path or repository reference",
      "content": "string — optional inline content"
    }
  ],
  "architecture_rules": [
    {
      "rule_id": "string",
      "name": "string",
      "description": "string",
      "violation_severity": "critical | high | medium | low"
    }
  ],
  "quality_attributes": ["scalability", "maintainability", "modularity", "observability", "testability"],
  "context": {
    "business_capabilities": ["string"],
    "data_domains": ["string"],
    "integration_points": ["string"]
  }
}
```

### Output Contract: Architecture Review Result

```json
{
  "review_id": "uuid",
  "status": "success | partial | failed",
  "architecture_violations": [
    {
      "rule_id": "string",
      "rule_name": "string",
      "severity": "critical | high | medium | low",
      "description": "string",
      "location": "string — file or module",
      "evidence": "string — import statement, dependency, or metric",
      "remediation": "string"
    }
  ],
  "ddd_compliance": {
    "bounded_contexts": [{"name": "string", "modules": ["string"], "status": "compliant | partial"}],
    "aggregates": [{"name": "string", "root": "string", "entities": ["string"]}],
    "domain_events": [{"name": "string", "aggregate": "string", "schema": "string"}],
    "anti_corruption_layers": [{"context_a": "string", "context_b": "string", "acl_pattern": "string"}]
  },
  "event_architecture": {
    "event_flows": [{"name": "string", "producer": "string", "consumers": ["string"], "schema": "string"}],
    "event_schemas": [{"name": "string", "fields": [{"name": "string", "type": "string"}]}],
    "eventual_consistency_guarantees": ["string"]
  },
  "microservices_analysis": {
    "service_boundaries": [{"name": "string", "responsibilities": ["string"]}],
    "communication_patterns": [{"service": "string", "pattern": "sync | async | streaming"}],
    "decomposition_quality": 0.0,
    "boundaries_violations": ["string"]
  },
  "monolith_review": {
    "health_score": 0.0,
    "decomposition_readiness": 0.0,
    "module_coupling": {"tight": ["string"], "loose": ["string"]},
    "breaking_changes_needed": ["string"]
  },
  "adr_generated": [
    {
      "adr_id": "string",
      "title": "string",
      "status": "proposed | accepted | deprecated",
      "decision": "string",
      "consequences": "string",
      "alternatives_considered": ["string"],
      "related_violations": ["string"]
    }
  ],
  "quality_metrics": {
    "scalability": 0.0,
    "maintainability": 0.0,
    "modularity": 0.0,
    "coupling": 0.0,
    "complexity": 0.0
  },
  "recommendations": [
    {
      "type": "refactor | rearchitect | extract_service | add_boundary | change_communication",
      "priority": "critical | high | medium | low",
      "description": "string",
      "affected_systems": ["string"],
      "estimated_effort": "string"
    }
  ],
  "confidence_score": 0.0,
  "confidence_explanation": "string"
}
```

### Architecture Decision Record (Experience Memory)

```json
{
  "record_id": "uuid",
  "review_id": "uuid",
  "timestamp": "ISO 8601",
  "adr_id": "string",
  "title": "string",
  "decision": "string",
  "status": "proposed | accepted | deprecated | superseded",
  "related_violations": ["string"],
  "affected_packs": ["string"]
}
```

---

## Integration Points (Capability Graph)

System Architect integrates with Code Engineer, DevOps Assistant, Self Development, Data Engineer, and Security Engineer through Execution Runtime and shared contracts only (per ADR-002).

### Integration Pipeline

```
Consumer Capability Pack
    │
    │  submits system description + artifacts via task/intent
    ▼
Execution Runtime
    │
    │  routes to System Architect Domain Engine
    ▼
System Architect Engine
    │
    │  ┌──────────────────────────────────────────────┐
    │  │ 1. Input Analysis (artifacts, codebase)      │
    │  │ 2. Clean Architecture Analysis                 │
    │  │ 3. DDD Implementation Review                   │
    │  │ 4. Event-Driven Design                       │
    │  │ 5. Microservices Analysis                    │
    │  │ 6. Monolith Review                           │
    │  │ 7. Architecture Governance (rules check)   │
    │  │ 8. ADR Generation → Experience Memory        │
    │  └──────────────────────────────────────────────┘
    │
    │  returns Architecture Review Result
    ▼
Consumer Capability Pack
    │
    │  receives violations + recommendations + ADRs
    ▼
User / Human Approval Loop
```

### Task Template

| Task | Subtasks |
|------|----------|
| Architecture Review | Input Analysis → Clean Architecture Analysis → DDD Review → Event-Driven Design → Microservices Analysis → Monolith Review → Governance Check → ADR Generation → Experience Memory |

---

## Consumer Capability Packs

| Consumer Capability Pack | Use Case |
|--------------------------|----------|
| **Code Engineer** | Architecture governance check on generated code, ADR generation for design decisions |
| **DevOps Assistant** | Architecture review of deployment topology, microservices communication patterns |
| **Self Development** | Architecture quality assessment for improvement proposals, ADR generation for changes |
| **Data Engineer** | Data architecture review, event flow design for data pipelines |
| **Decision Intelligence** | Architecture risk as an objective in decision scoring |
| **Security Engineer** | Trust boundary analysis, architecture-level security controls |

---

## Dependencies

### Internal Dependencies (Shared Contracts)

1. **Execution Runtime** — Task routing (per ADR-002)
2. **Experience Memory** — ADR and finding record persistence (per ADR-011)
3. **Shared Contracts** — Task/Intent definition and result schema (per ADR-006)

### Package Structure

```
apps/
└── system_architect/
    ├── engine.py                  # Domain Engine (owner of business logic per ADR-004)
    ├── worker.py                  # Thin adapter (per ADR-003)
    ├── schemas.py                 # Public contracts (Review Request, Result)
    ├── architecture_analyzer.py   # Clean architecture + DDD analysis
    ├── event_designer.py          # Event-driven design submodule
    ├── microservices_analyzer.py # Microservices boundary analysis
    ├── monolith_reviewer.py       # Monolith health and decomposition
    ├── governance_checker.py      # Architecture rule enforcement
    ├── adr_generator.py           # ADR generation and management
    └── quality_assessor.py        # Architecture quality metrics (scalability, maintainability)
```

**ADR Impact:** None. No Core, Runtime, Kernel, or shared contract modification required (ADR-001, ADR-006 remain unchanged).

---

## Benchmark Specification

### Benchmark Framework

| Dimension | Definition | Measurement | Target |
|-----------|------------|-------------|--------|
| **Violation Detection** | Correct identification of architecture violations | % of violations correctly identified | ≥95% |
| **ADR Quality** | Completeness and traceability of generated ADRs | % of ADRs with decision, consequences, alternatives | ≥90% |
| **Dependency Accuracy** | Correct cross-system dependency mapping | % of dependencies correctly identified | ≥90% |
| **Quality Assessment** | Accuracy of scalability/maintainability scores | Correlation with expert review ≥0.85 | ≥85% |
| **Governance Compliance** | Architecture rules enforced across all systems | % of rule violations detected | ≥95% |
| **Event Completeness** | All event flows have documented schemas | % of event flows with complete schemas | ≥90% |
| **Package Boundary Enforcement** | All package boundaries correctly enforced | % of boundary violations detected | ≥95% |
| **Consistency** | Same architecture produces same analysis | Variance across 5 repeated runs < 3% | ≥90% |

### Benchmark Dataset

- **100 architecture review scenarios** covering:
  - Monolith projects (40) — Python, Java, Node.js, Go
  - Microservices projects (35) — service mesh, API gateway, event-driven
  - Hybrid architectures (15) — monolith + microservices
  - Event-driven systems (10) — Kafka, RabbitMQ, event sourcing
  - Architecture violations (25 of the above) — circular deps, layer violations, boundary breaches

### Golden Test Scenarios

| Category | Test Cases |
|----------|-----------|
| Architecture Violation | Circular dependency, layer violation, package boundary breach, dependency rule violation |
| ADR Generation | Decision documentation, consequence analysis, alternative comparison |
| Dependency Analysis | Cross-service dependency mapping, impact analysis |
| Quality Metrics | Scalability score, maintainability score, modularity assessment |
| Event Design | Event flow, schema completeness, consumer patterns |
| Package Boundaries | Module isolation, import restrictions, boundary enforcement |

---

## Golden Test Specification

The golden test suite must include System Architect scenarios:

| # | Scenario | Expected Outcome | Acceptance Criteria |
|---|----------|-----------------|---------------------|
| 1 | Circular dependency in monolith | Detected as critical violation | ≥95% detection |
| 2 | Layer violation (domain importing infrastructure) | Detected with remediation | ≥95% detection |
| 3 | Package boundary breach (service importing internal modules) | Detected with severity | ≥95% detection |
| 4 | ADR for cross-service data consistency decision | ADR with decision, consequences, alternatives | ≥90% completeness |
| 5 | Microservices with shared database | Violation detected, decomposition recommended | ≥90% correctness |
| 6 | Event flow without schema documentation | Missing schema flagged | ≥90% detection |
| 7 | Monolith health assessment | Health score + decomposition roadmap | ≥85% accuracy |
| 8 | Scalability assessment of microservices | Scalability score + bottleneck identification | ≥85% accuracy |
| 9 | Dependency impact analysis (service A changes) | All dependents identified | ≥90% accuracy |
| 10 | Architecture governance compliance check | All rules evaluated, violations reported | ≥95% compliance |

### Golden Test Acceptance Criteria

- All 10 golden test scenarios pass at ≥90% of acceptance criteria (100% pass)
- Architecture violations detected with ≥95% accuracy and ≤5% false positives
- ADRs generated with ≥90% completeness (decision, consequences, alternatives)
- Package boundary enforcement at ≥95%
- Confidence scores calibrated within ±5%

---

## Real Case Requirements

### Real Case Directory

`real_cases/system_architect/` must contain:

| Requirement | Minimum Count |
|-------------|---------------|
| Real architecture reviews from actual projects | 20 |
| Cases with ADR generation | 15 |
| Cases with microservices analysis | 15 |
| Cases with monolith review | 10 |
| Cases with architecture governance check | 15 |

### Real Case Structure

```
real_cases/system_architect/<case_id>/
├── input/
│   ├── artifacts/                  # Source code, diagrams, specs
│   ├── architecture_request.json  # Full Architecture Review Request
│   └── rules.json                  # Architecture rules to check
├── output/
│   ├── review_result.json         # Full Architecture Review Result
│   ├── adr_*.md                   # Generated ADR documents
│   └── finding_records.json       # Experience Memory entries
└── evaluation.md                  # Expert review, violation verification, lessons learned
```

### Real Case Targets

| Metric | Target |
|--------|--------|
| Real cases logged | ≥20 (Level 3) → ≥100 (Level 4) |
| ADR quality (expert review) | ≥90% completeness |
| Architecture violation accuracy | ≥95% verified by experts |

---

## Definition of Done

```text
Definition of Done — System Architect Capability Pack

Functional
- [ ] Clean Architecture Analysis covers layers, boundaries, dependency rules
- [ ] DDD Implementation analyzes bounded contexts, aggregates, domain events, ACLs
- [ ] Event-Driven Design produces event flows and schemas with ≥3 consumer patterns
- [ ] Microservices Analysis evaluates service boundaries and communication patterns
- [ ] Monolith Review produces health score + decomposition roadmap
- [ ] Architecture Governance checks package boundaries and dependency rules
- [ ] ADR Generation produces ADRs with decision, consequences, and alternatives

Benchmark
- [ ] Benchmark score ≥ 90 (grade A) across all dimensions
- [ ] Violation detection ≥ 95%
- [ ] ADR quality ≥ 90%
- [ ] Package boundary enforcement ≥ 95%
- [ ] Governance compliance ≥ 95%
- [ ] Consistency ≥ 90%

Golden Tests
- [ ] All 10 golden test scenarios pass at ≥90% (100% pass)

Real Cases
- [ ] ≥ 20 real cases logged in real_cases/system_architect/
- [ ] Evaluation notes recorded for each case
- [ ] ≥ 15 cases with ADR generation
- [ ] ≥ 15 cases with architecture governance check

Documentation
- [ ] Capability Guide updated (CAPABILITY_GUIDE.md — System Architect section)
- [ ] API reference / contract updated (this RFC + schemas.py)
- [ ] Architecture review methodology documented

SDK
- [ ] Pack accessible via SDK without Core changes
- [ ] System Architect callable via Execution Runtime task routing

Performance
- [ ] Latency P95 < 5000ms for standard architecture reviews
- [ ] Latency P95 < 15000ms for full system reviews

Security
- [ ] No known P0/P1 security issues
- [ ] Architecture analysis does not expose sensitive code content

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
| False positive architecture violations | Medium — developer frustration | Medium | Conservative severity; explainable findings; user override |
| ADR generation is too generic | Medium — low value | Medium | Context-aware ADR templates; domain-specific decision factors |
| Microservices analysis over-recommends decomposition | High — unnecessary complexity | Low | Cost-benefit analysis; team size guidance; complexity scoring |
| Event design lacks domain context | Medium — poor schemas | Medium | Require system context; template-based event design |
| Governance rules are too strict | Medium — blocks legitimate changes | Low | Configurable rule severity; exception handling via ADR process |
| Quality metrics are inaccurate | Medium — wrong decisions | Medium | Multi-method assessment; expert calibration; confidence bounds |

---

## ADR Impact

**Does this require Core changes?** No.

System Architect is a **new Capability Pack** that follows established patterns:

- **ADR-001 (Core Pipeline Freeze):** No Core changes. All logic in `apps/system_architect/`.
- **ADR-002 (Capability Pack Independence):** Communicates with other packs via Execution Runtime tasks and shared contracts only.
- **ADR-003 (Worker = Adapter Only):** Thin Worker routes architecture tasks to the Domain Engine.
- **ADR-004 (Domain Engine Owns Business Logic):** All architecture logic in `apps/system_architect/engine.py`.
- **ADR-005 (Human Approval Required):** Architecture changes and ADR adoption require explicit user approval.
- **ADR-006 (Capability Contract v1 Frozen):** Uses existing Capability Contract for registration.
- **ADR-007 (Conversation Boundary):** Invoked through Execution Runtime.
- **ADR-008 (Core Change Requires Cross-Capability Proof):** Not applicable — no Core changes.
- **ADR-009 (Single Conversation Interface):** Users say "Review my system architecture" — internal analysis engine selection is transparent.
- **ADR-010 (Workspace Isolation):** Architecture findings and ADRs scoped per Workspace.
- **ADR-011 (Artifact Persistence):** Architecture review reports and ADRs persisted as versioned Artifacts.
- **ADR-012 (Progress Transparency):** Progress shown as "Analyzing dependencies...", "Checking architecture rules...", "Generating ADR..."
- **ADR-013 (Outcome First Rule):** Users request outcomes ("Should we split this monolith?"), not mechanisms.
- **ADR-014 (Operational Product Layer):** Uses Artifact Service for versioned ADR storage.

**ADR Required:** None. This is a new Capability Pack, not a Core modification.

---

## Rollout Plan

### Phase 1: Core Analysis (RFC → Experimental)

**Duration:** 4 weeks

- [ ] Create `apps/system_architect/` package structure
- [ ] Implement Clean Architecture Analysis (layers, boundaries, dependency rules)
- [ ] Implement Package Boundary Enforcement
- [ ] Implement ADR Generation (basic templates)
- [ ] Define public contracts (Review Request, Result)
- [ ] Implement thin Worker adapter
- [ ] Create 10 golden test scenarios
- [ ] Integration: Code Engineer → System Architect (governance check)
- [ ] Integration: Self Development → System Architect (architecture quality)
- **Gate:** 10 golden tests pass at ≥85%

### Phase 2: Full Lifecycle (Experimental → Stable)

**Duration:** 6 weeks

- [ ] Implement DDD Implementation analysis (bounded contexts, aggregates, events, ACLs)
- [ ] Implement Event-Driven Design (event flows, schemas)
- [ ] Implement Microservices Analysis (boundaries, communication patterns)
- [ ] Implement Monolith Review (health, decomposition roadmap)
- [ ] Implement Architecture Quality Metrics (scalability, maintainability, modularity)
- [ ] Expand golden tests to 10 full scenarios
- [ ] Log ≥20 real cases
- [ ] **Benchmark:** 100 projects, violation detection ≥95%, ADR quality ≥90%
- [ ] **Integration:** DevOps Assistant, Data Engineer, Security Engineer
- **Gate:** All 10 golden tests pass at ≥90%; benchmark ≥90%

### Phase 3: Certified (Stable → Certified)

**Duration:** 6 weeks

- [ ] All 6+ Capability Packs integrated with System Architect
- [ ] ADR generation validated on ≥50 real architecture decisions
- [ ] Microservices analysis validated on ≥30 real projects
- [ ] Independent audit of architecture quality metrics methodology
- [ ] Public benchmark dashboard
- [ ] **Benchmark:** ≥95% sustained across all dimensions
- [ ] **Real Cases:** ≥100 cases with ≥95% violation detection accuracy
- **Gate:** Independent audit passed; benchmark ≥95% sustained

---

## Future Enhancements

### Phase 2 (Post-v1.0.0 Release)

1. **Architecture Decision Impact Simulation** — Predict the cross-system impact of architectural decisions
2. **Real-Time Architecture Guardrails** — CI/CD integration for architecture violation detection
3. **Architecture Evolution Tracking** — Track architecture quality trends over time
4. **Cross-Project Pattern Library** — Shared architecture patterns discovered across Workspaces

### Enterprise Phase 3

1. **Architecture Compliance Dashboard** — Real-time architecture governance across all systems
2. **Automated Refactoring Recommendation** — Generate code changes to fix architecture violations
3. **Multi-Tenant Architecture Isolation** — Architecture boundary enforcement in multi-tenant environments
4. **Architecture Decision Marketplace** — Industry-standard ADR templates and decision patterns

### Long-term

1. **System Architect Marketplace** — Third-party architecture rule packs and quality assessment models
2. **Generative Architecture Design** — AI-generated architecture designs from requirements
3. **Architecture Debt Management** — Track, prioritize, and remediate architectural debt over time
4. **Enterprise Architecture Integration** — Sync with TOGAF, Zachman, and custom EA frameworks

---

## Real Case Requirements

*(See [Real Case Requirements](#real-case-requirements) section above for full specification)*

System Architect real cases are sourced from:

1. **Code Engineer** — Generated codebase architecture reviews and ADR generation
2. **DevOps Assistant** — Deployment topology and microservices communication analysis
3. **Self Development** — Architecture improvement proposal quality assessment
4. **Data Engineer** — Data pipeline architecture and event flow design
5. **Security Engineer** — Trust boundary analysis and security architecture review

---

## Definition of Done

*(See [Definition of Done](#definition-of-done) section above for full checklist)*
