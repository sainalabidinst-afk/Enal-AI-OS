# RFC-0007: Decision Intelligence Capability Pack

| Field | Value |
|-------|-------|
| **RFC ID** | RFC-0007 |
| **Status** | Draft |
| **Version** | 0.1.0 |
| **Author** | Enal AI OS Core Team |
| **Target Release** | v1.2.0 (Capability Excellence phase) |
| **Capability Pack** | Decision Intelligence |
| **Capability ID** | `decision-intelligence` |
| **Category** | Reasoning |
| **Quality Target** | A (≥90) |
| **Maturity Target** | Level 3 — Production Ready |
| **Reference RFC** | RFC-0007 |

---

## Motivation

The 6 existing Capability Packs cover code, network, research, DevOps, trading, and self-development. Each produces outputs—code, configurations, research reports, trading signals—that involve decisions requiring evidence-based reasoning.

Currently, these decisions are made in an embedded, pack-specific way. There is no shared reasoning layer that applies a consistent, auditable, and explainable decision framework across domains. This leads to:

1. **Inconsistent decision quality** — each pack reinvents evidence collection, risk scoring, and confidence estimation.
2. **No cross-domain decision reuse** — Trading Analyst's risk analysis cannot inform Code Engineer's refactoring choices, even though both involve risk vs. reward trade-offs.
3. **Limited explainability** — decisions are explained through domain-specific narratives, not through a structured evidence-to-decision chain.
4. **No decision audit trail** — decisions are produced but never recorded in a structured, queryable experience memory for learning and rollback.

Decision Intelligence becomes the **reasoning layer** that sits between evidence producers (all Capability Packs) and decision consumers (all Capability Packs), providing a unified framework for evidence-based, explainable, and auditable decision-making.

---

## Problem Statement

Without a dedicated Decision Intelligence Capability Pack:

- **Evidence is siloed per pack** — no mechanism exists to collect, rank, and synthesize evidence from multiple Capability Packs before reaching a decision.
- **Alternatives are rarely explored** — most packs produce a single recommendation without generating or comparing alternatives.
- **Risk analysis is ad hoc** — risk scoring exists in some packs (Trading, Network) but with no standardized methodology across the platform.
- **Confidence is not quantified** — confidence estimates are implicit in recommendations, not explicitly modeled or communicated.
- **Decisions are not recorded** — there is no structured Decision History to support learning, rollback recommendations, or compliance audit.
- **Trade-off analysis is missing** — multi-objective optimization (accuracy vs. latency, cost vs. reliability) is handled per-pack, not through a unified framework.

The absence of Decision Intelligence means that as ECP grows to include more Capability Packs, the quality and consistency of decisions will not scale—instead, they will fragment further.

---

## Goals

1. **Evidence Collection** — Collect and structure evidence from one or more sources (Capability Pack outputs, real-case data, benchmark results).
2. **Alternative Generation** — Generate multiple viable alternatives for any decision context.
3. **Risk Analysis** — Quantify and categorize risks associated with each alternative (probability × impact).
4. **Trade-off Analysis** — Analyze multi-objective trade-offs between alternatives (accuracy vs. cost, speed vs. safety, etc.).
5. **Decision Scoring** — Score each alternative against configurable criteria and weights.
6. **Confidence Estimation** — Produce an explicit confidence score for each decision, with uncertainty quantification.
7. **Explainable Decision** — Generate a human-readable explanation chain: evidence → reasoning → simulation → alternatives → risk → decision → rationale.
8. **Decision History** — Record every decision, its evidence, alternatives considered, and outcome to Experience Memory for learning and rollback.

### Success Criteria

| Metric | Target | Grade |
|--------|--------|-------|
| Decision Accuracy | ≥90% (correct decisions when ground truth available) | A |
| Explainability | ≥95% (full evidence-to-decision chain presented) | A+ |
| Consistency | ≥90% (same input produces same decision across runs) | A |
| Confidence Calibration | ≥85% (confidence score reflects actual accuracy ±5%) | A |
| Risk Detection | ≥90% (risks identified match ground truth) | A |
| Trade-off Completeness | ≥85% (all relevant objectives considered) | A |

---

## Non-Goals

1. **Live execution of decisions** — Decision Intelligence produces recommendations; execution requires explicit user approval per ADR-005.
2. **Replacing domain expertise** — Decision Intelligence is a reasoning layer, not a substitute for domain knowledge. It amplifies but does not replace Trading, Code, Network, etc.
3. **Real-time market trading signals** — Trading Analyst retains ownership of trading signal generation. Decision Intelligence may score trading decisions but does not generate signals.
4. **Single decision point enforcement** — Each Capability Pack may still produce its own domain-specific recommendations. Decision Intelligence provides a cross-cutting scoring and explanation layer.
5. **Core modification** — All implementation must reside within the Decision Intelligence Capability Pack, following ADR-002 and ADR-004.

---

## Capability Scope

### Core Capabilities

| Capability | Description | Inputs | Outputs |
|-----------|-------------|--------|---------|
| Evidence Collection | Collect, validate, and structure evidence from one or more sources. | Capability Pack outputs, API responses, benchmark data, real-case files | Structured evidence set with quality scores |
| Alternative Generation | Enumerate viable alternatives for a given decision context. | Decision context, evidence set, constraints | Set of alternatives with initial feasibility scores |
| Risk Analysis | Assess probability and impact of each alternative. | Alternatives, evidence, historical data | Risk profile per alternative (probability × impact) |
| Trade-off Analysis | Analyze multi-objective trade-offs between alternatives. | Alternatives, weighted criteria, constraints | Pareto frontier of trade-off scores |
| Decision Scoring | Score and rank alternatives against configurable criteria. | Alternatives, criteria weights, evidence, risk | Ranked alternatives with composite scores |
| Confidence Estimation | Quantify uncertainty and confidence in the final decision. | Evidence quality, model confidence, historical calibration | Confidence score (0–100%) with uncertainty bounds |
| Explainable Decision | Produce a traceable, human-readable explanation. | Full decision trace, evidence, reasoning chain | Explanation document (evidence → decision → rationale) |
| Decision History | Record decisions to Experience Memory for learning and rollback. | Final decision, alternatives, evidence, outcome | Decision record in Experience Memory |

### Out of Scope

- Real-time trading execution
- Live cloud resource provisioning
- Direct integration with external decision systems without mediation
- Legal, medical, or financial advisory beyond ECP's existing Scope boundaries
- Autonomous application of decisions (requires approval per ADR-005)
- Replacing the internal reasoning of other Capability Packs

---

## Public Contracts

### Input Contract: Decision Request

```json
{
  "decision_id": "uuid",
  "context": "string — natural language description of the decision to be made",
  "evidence_sources": [
    {
      "source_id": "string — capability_id or external source identifier",
      "evidence_type": "analysis | recommendation | data | benchmark | historical",
      "payload": "object — structured evidence payload",
      "quality_score": 0.0,
      "weight": 0.0
    }
  ],
  "constraints": ["string — hard constraints that eliminate alternatives"],
  "objectives": [
    {
      "name": "Accuracy",
      "weight": 0.30,
      "goal": "maximize | minimize"
    },
    {
      "name": "Risk",
      "weight": 0.25,
      "goal": "minimize"
    },
    {
      "name": "Cost",
      "weight": 0.20,
      "goal": "minimize"
    },
    {
      "name": "Latency",
      "weight": 0.25,
      "goal": "minimize"
    }
  ],
  "risk_tolerance": "low | medium | high",
  "max_alternatives": 5,
  "include_explanation": true
}
```

### Output Contract: Decision Result

```json
{
  "decision_id": "uuid",
  "recommended_decision": "string — the chosen alternative or action",
  "alternatives": [
    {
      "id": "string",
      "description": "string",
      "score": 0.0,
      "confidence": 0.0,
      "risk_profile": {
        "overall_risk": 0.0,
        "probability": 0.0,
        "impact": 0.0,
        "risk_factors": ["string"]
      },
      "trade_offs": {
        "accuracy": 0.0,
        "cost": 0.0,
        "latency": 0.0
      }
    }
  ],
  "confidence_score": 0.0,
  "confidence_explanation": "string",
  "explanation": {
    "evidence_summary": "string",
    "reasoning_chain": ["string"],
    "simulation_results": "object",
    "risk_assessment": "string",
    "final_rationale": "string"
  },
  "decision_history_ref": "string — reference to Experience Memory entry"
}
```

### Decision Record (Experience Memory)

```json
{
  "record_id": "uuid",
  "decision_id": "uuid",
  "timestamp": "ISO 8601",
  "context": "string",
  "chosen_alternative": "string",
  "alternatives_count": 0,
  "confidence_score": 0.0,
  "evidence_count": 0,
  "risk_score": 0.0,
  "explanation": "string",
  "outcome": "pending | accepted | rejected | revised",
  "user_feedback": "string — optional",
  "revision_history": [{"revision_id": "uuid", "changes": "string"}]
}
```

---

## Integration Points (Capability Graph)

The Decision Intelligence Capability Pack integrates with all existing and future Capability Packs through the **Execution Runtime** and **shared contracts only** (per ADR-002). It does not import other Capability Pack engines directly.

### Integration Pipeline

```
Consumer Capability Pack
    │
    │  submits evidence via task/intent
    ▼
Execution Runtime
    │
    │  routes to Decision Intelligence Domain Engine
    ▼
Decision Intelligence Engine
    │
    │  ┌──────────────────────────────────────────┐
    │  │ 1. Evidence Collection                   │
    │  │ 2. Alternative Generation                │
    │  │ 3. Risk Analysis                         │
    │  │ 4. Trade-off Analysis                    │
    │  │ 5. Decision Scoring                      │
    │  │ 6. Confidence Estimation                 │
    │  │ 7. Explainable Decision                  │
    │  │ 8. Decision History → Experience Memory  │
    │  └──────────────────────────────────────────┘
    │
    │  returns Decision Result
    ▼
Consumer Capability Pack
    │
    │  receives scored recommendation + explanation
    ▼
User / Human Approval Loop
```

### Task Template

| Task | Subtasks |
|------|----------|
| Score Decision | Evidence Collection → Alternative Generation → Risk Analysis → Trade-off Analysis → Decision Scoring → Confidence Estimation → Explanation → Decision History |

---

## Consumer Capability Packs

Decision Intelligence serves all existing Capability Packs as a cross-cutting reasoning layer:

| Consumer Capability Pack | Use Case |
|--------------------------|----------|
| **Trading Analyst** | Score trading alternatives, quantify risk-adjusted confidence, explain rationale for trade recommendations |
| **Code Engineer** | Score refactoring alternatives, analyze trade-offs (complexity vs. performance), estimate risk of changes |
| **Network Engineer** | Compare configuration alternatives, analyze failure risk, recommend rollback-safe changes |
| **DevOps Assistant** | Evaluate deployment strategies, trade-off cost vs. reliability, recommend optimal rollout |
| **Research Assistant** | Score evidence quality, quantify confidence in synthesized conclusions, explain reasoning |
| **Self Development** | Evaluate architecture improvement proposals, score risk vs. benefit, produce explainable plans |
| **Decision Intelligence** (self) | Use its own reasoning layer for meta-decisions about evidence weighting and confidence calibration |

---

## Dependencies

### Internal Dependencies (Shared Contracts)

1. **Execution Runtime** — Task routing and orchestration (per ADR-002)
2. **Experience Memory** — Decision record persistence (per ADR-011)
3. **Shared Contracts** — Task/Intent definition and result schema (per ADR-006)

### No Core Changes Required

All implementation resides within the Decision Intelligence Capability Pack:

```
apps/
└── decision_intelligence/
    ├── engine.py                # Domain Engine (owner of business logic per ADR-004)
    ├── worker.py                # Thin adapter (per ADR-003)
    ├── schemas.py               # Public contracts (Decision Request, Decision Result)
    ├── evidence_collector.py    # Evidence collection submodule
    ├── alternative_generator.py # Alternative generation submodule
    ├── risk_analyzer.py         # Risk analysis submodule
    ├── tradeoff_analyzer.py     # Trade-off analysis submodule
    ├── scoring_engine.py        # Decision scoring submodule
    ├── confidence_estimator.py  # Confidence estimation submodule
    └── explanation_generator.py # Explainable decision submodule
```

**ADR Impact:** None. No Core, Runtime, Kernel, or shared contract modification required (ADR-001, ADR-006 remain unchanged).

---

## Benchmark Specification

### Benchmark Framework

| Dimension | Definition | Measurement | Target |
|-----------|------------|-------------|--------|
| **Accuracy** | Correctness of final decision | % of decisions matching ground truth or expert consensus | ≥90% |
| **Completeness** | Coverage of evidence, alternatives, and objectives | % of required elements considered in decision | ≥90% |
| **Explainability** | Clarity and traceability of the decision chain | Human evaluation: full evidence→decision chain presented | ≥95% |
| **Safety** | No harmful or unsafe recommendations | % of decisions passing safety constraints | ≥95% |
| **Efficiency** | Response time and resource usage | Latency P95 < 2000ms, token usage optimal | within budget |
| **Consistency** | Same input produces same output across runs | Variance across 10 repeated runs < 5% | ≥90% |
| **Confidence Calibration** | Confidence score reflects actual accuracy | Calibration curve: confidence within ±5% of actual accuracy | ≥85% |
| **Risk Detection** | Risks identified match ground truth | % of known risks detected before decision | ≥90% |

### Benchmark Dataset

- **100 decision scenarios** covering the domains of:
  - Trading (risk-adjusted trade selection, position sizing)
  - Code (refactoring vs. rewrite, library selection)
  - Network (configuration migration, firewall policy changes)
  - DevOps (deployment strategy, rollback planning)
  - Research (evidence synthesis, conclusion confidence)
  - Self-Development (architecture improvement scoring)
  - Cross-domain (multi-pack trade-off decisions)

### Benchmark Dimensions Detail

| Scenario Type | Description | Ground Truth Source |
|---------------|-------------|---------------------|
| Conflicting Evidence | Evidence sources disagree | Expert consensus |
| Incomplete Evidence | Some evidence missing | Expert consensus |
| Multi-objective Optimization | Multiple competing objectives | Pareto optimality |
| High Risk | Decision with significant downside | Expert review |
| Low Confidence | High uncertainty in evidence | Confidence calibration |
| Decision Revision | Revisiting prior decisions with new evidence | Decision history |
| Rollback Recommendation | Identifying when to revert a decision | Historical outcomes |

---

## Golden Test Specification

The golden test suite (`benchmarks/golden_test_set.py`) must include Decision Intelligence scenarios:

| # | Scenario | Expected Outcome | Acceptance Criteria |
|---|----------|-----------------|---------------------|
| 1 | Simple binary decision (Go/No-Go) | Correct choice with explanation | ≥90% accuracy |
| 2 | Conflicting evidence from 3 sources | Weighted evidence synthesis | ≥85% resolution accuracy |
| 3 | Incomplete evidence (2 of 4 sources missing) | Proceed with confidence downgrade | Confidence < 70%, explicit warning |
| 4 | Multi-objective optimization (3 objectives) | Pareto-optimal alternative selected | ≥90% correctness |
| 5 | High-risk decision | Risk flagged and explained | ≥95% risk detection |
| 6 | Low confidence scenario | Confidence score ≤ 30%, recommendation deferred | Confidence calibration within ±5% |
| 7 | Decision revision with new evidence | Revised decision with comparison to prior | Revision trace logged |
| 8 | Rollback recommendation | Rollback advised when risk exceeds threshold | ≥90% trigger accuracy |
| 9 | Trade-off analysis (speed vs. accuracy) | Clear trade-off visualization | All objectives scored |
| 10 | Explainability chain completeness | Full evidence→decision chain presented | ≥95% completeness |

### Golden Test Acceptance Criteria

- All 10 golden test scenarios pass at ≥90% of individual acceptance criteria
- Overall Decision Intelligence golden test pass rate ≥90%
- Full explanation chain generated for every scenario
- Confidence scores calibrated within ±5% of actual accuracy

---

## Real Case Requirements

### Real Case Directory

`real_cases/decision_intelligence/` must contain:

| Requirement | Minimum Count |
|-------------|---------------|
| Real decision cases from actual usage | 20 |
| Cases with decision revision history | 5 |
| Cases with rollback recommendations | 5 |
| Cases involving multiple Capability Packs | 10 |
| Cases with expert review/validation | 15 |

### Real Case Structure

Each real case must include:

```
real_cases/decision_intelligence/<case_id>/
├── input/
│   ├── context.md           # Decision context and goals
│   ├── evidence/            # Evidence from source Capability Packs
│   │   └── <source_id>.json
│   └── constraints.md       # Hard constraints
├── output/
│   ├── decision_result.json # Full Decision Result contract output
│   ├── explanation.md       # Human-readable explanation
│   └── experience_memory_entry.json
└── evaluation.md            # Ground truth, expert review, lessons learned
```

### Real Case Targets

| Metric | Target |
|--------|--------|
| Real cases logged | ≥20 (Level 3 Production Ready) → ≥50 (Level 4 Domain Expert) |
| Real case quality score (expert review) | ≥90% |
| Post-decision outcome tracking | ≥80% of cases with tracked outcomes |

---

## Definition of Done

```text
Definition of Done — Decision Intelligence Capability Pack

Functional
- [ ] Evidence Collection accepts evidence from ≥3 source types (analysis, recommendation, data, benchmark, historical)
- [ ] Alternative Generation produces ≥2 viable alternatives for any decision context
- [ ] Risk Analysis produces probability × impact score per alternative with ≥3 risk factor categories
- [ ] Trade-off Analysis supports ≥3 simultaneous objectives with weighted scoring
- [ ] Decision Scoring ranks alternatives and produces a recommended decision
- [ ] Confidence Estimation produces 0–100% confidence with uncertainty bounds
- [ ] Explainable Decision produces full evidence→reasoning→simulation→alternatives→risk→decision→rationale chain
- [ ] Decision History records every decision to Experience Memory

Benchmark
- [ ] Benchmark score ≥ 90% (grade A) across all 6 standard dimensions + confidence calibration
- [ ] Decision accuracy ≥ 90%
- [ ] Explainability ≥ 95%
- [ ] Consistency ≥ 90%
- [ ] Confidence calibration within ±5%

Golden Tests
- [ ] All 10 pack golden test scenarios pass at ≥90% of acceptance criteria (100% pass)

Real Cases
- [ ] ≥ 20 real cases logged in real_cases/decision_intelligence/
- [ ] Evaluation notes recorded for each case
- [ ] ≥ 5 cases with decision revision history
- [ ] ≥ 5 cases with rollback recommendations

Documentation
- [ ] Capability Guide updated (CAPABILITY_GUIDE.md — Decision Intelligence section)
- [ ] API reference / contract updated (this RFC + schemas.py)
- [ ] Real case evaluation summary published

SDK
- [ ] Pack accessible via SDK without Core changes
- [ ] Decision Intelligence callable via Execution Runtime task routing

Performance
- [ ] Latency P95 < 2000ms for standard scenarios
- [ ] Latency P95 < 5000ms for multi-source evidence scenarios

Security
- [ ] No known P0/P1 security issues
- [ ] Decision explanations do not leak sensitive evidence payloads

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
| Decision Intelligence becomes a bottleneck | High — all packs depend on it | Medium | Design as non-blocking; cache evidence scoring; parallel evidence processing |
| Explanations are too verbose or too terse | Medium — affects explainability metric | High | Configurable explanation depth; default to medium; user feedback loop |
| Confidence scores are poorly calibrated | High — undermines trust | Medium | Calibrate on 100 scenarios before release; continuous learning from real cases |
| Risk analysis over-weights rare events | Medium — suboptimal decisions | Medium | Bounded risk scoring; risk tolerance parameter |
| Circular dependency: Decision Intelligence depends on packs that depend on it | High — architectural deadlock | Low | Use asynchronous evidence submission; no synchronous pack-to-pack calls |
| Multi-objective optimization finds no viable solution | Medium — decision failure | Low | Fallback to single-objective scoring; report infeasibility |
| Experience Memory grows unbounded | Low — storage cost | Medium | TTL-based pruning; summarization of old decisions |

---

## ADR Impact

**Does this require Core changes?** No.

Decision Intelligence is a **new Capability Pack** that follows the established patterns:

- **ADR-001 (Core Pipeline Freeze):** No Core changes. All logic in `apps/decision_intelligence/`.
- **ADR-002 (Capability Pack Independence):** Decision Intelligence communicates with other packs via Execution Runtime tasks and shared contracts only. No direct imports.
- **ADR-003 (Worker = Adapter Only):** A thin Worker routes tasks to the Domain Engine.
- **ADR-004 (Domain Engine Owns Business Logic):** All reasoning logic resides in `apps/decision_intelligence/engine.py`.
- **ADR-005 (Human Approval Required):** Decisions are recommendations; execution requires explicit user approval.
- **ADR-006 (Capability Contract v1 Frozen):** Uses the existing Capability Contract for node and subtask template registration. No contract changes.
- **ADR-007 (Conversation Boundary):** Decision Intelligence is invoked through Execution Runtime, not directly by Conversation Manager.
- **ADR-008 (Core Change Requires Cross-Capability Proof):** Not applicable — no Core changes.

**ADR Required:** None. This is a new Capability Pack, not a Core modification.

---

## Rollout Plan

### Phase 1: Prototype (RFC → Experimental)

**Duration:** 4 weeks

- [ ] Create `apps/decision_intelligence/` package structure
- [ ] Implement Evidence Collection and Decision Scoring (single-criteria)
- [ ] Define public contracts (Decision Request, Decision Result)
- [ ] Implement thin Worker adapter
- [ ] Create 10 golden test scenarios (simplified: binary decisions)
- [ ] Integration: Trading Analyst → Decision Intelligence (evidence submission)
- **Gate:** 10 golden tests pass at ≥80%

### Phase 2: Full Capabilities (Experimental → Stable)

**Duration:** 6 weeks

- [ ] Implement Alternative Generation
- [ ] Implement Risk Analysis (probability × impact)
- [ ] Implement Trade-off Analysis (multi-objective weighted scoring)
- [ ] Implement Confidence Estimation with calibration
- [ ] Implement Explainable Decision (full chain)
- [ ] Implement Decision History → Experience Memory
- [ ] Expand golden tests to 10 full scenarios
- [ ] Log ≥20 real cases from Trading Analyst usage
- [ ] **Benchmark:** 100 scenarios, ≥90% accuracy, ≥95% explainability
- [ ] **Integration:** Network Engineer, Code Engineer, DevOps Assistant start using Decision Intelligence for scored decisions
- **Gate:** All 10 golden tests pass at ≥90%; benchmark ≥90%

### Phase 3: Ecosystem (Stable → Certified)

**Duration:** 8 weeks

- [ ] All 6+ Capability Packs integrated with Decision Intelligence
- [ ] Confidence calibration validated on ≥50 real cases
- [ ] Decision History supports rollback recommendations
- [ ] Independent audit of decision quality and explainability
- [ ] Public benchmark dashboard available
- [ ] **Benchmark:** ≥90% across all dimensions
- [ ] **Real Cases:** ≥50 cases with ≥80% outcome tracking
- **Gate:** Independent audit passed; benchmark ≥90% sustained

---

## Future Enhancements

### Fase 2 (Post-v1.0.0 Release)

1. **Decision Simulation Engine** — Monte Carlo simulation of alternatives before scoring
2. **Multi-Model Debate** — Use multiple LLMs to debate alternatives (leveraging existing debate engine pattern from Trading Analyst)
3. **Adaptive Criteria Weighting** — Learn optimal objective weights from historical decision outcomes
4. **Decision Graph Visualization** — Interactive graph of evidence → decision → outcome chains

### Fase 3 (Enterprise)

1. **Decision Templates** — Pre-built decision frameworks for common scenarios (architecture review, deployment strategy, investment decision)
2. **Policy Engine** — Encode organizational decision policies as constraints
3. **Cross-Workspace Decision Learning** — Aggregate anonymized decision outcomes across workspaces for platform-wide confidence calibration
4. **Regulatory Compliance Layer** — Decision explainability tailored for SOC 2, ISO 27001, and other compliance frameworks

### Long-term

1. **Decision Intelligence Marketplace** — Third-party decision frameworks and custom reasoning models
2. **Causal Inference Engine** — Move from correlation-based evidence to causal reasoning for decision support
3. **Active Learning Loop** — Automatically identify and request missing evidence to reduce decision uncertainty
4. **Decision-Time Optimization** — Dynamically select reasoning depth based on decision importance and time constraints

---

## Real Case Requirements

*(See [Real Case Requirements](#real-case-requirements) section above for full specification)*

Decision Intelligence real cases are sourced from:

1. **Trading Analyst** — Trade recommendation decisions with post-market outcome
2. **Code Engineer** — Refactoring vs. rewrite decisions with code quality metrics
3. **Network Engineer** — Configuration change decisions with post-deployment verification
4. **DevOps Assistant** — Deployment strategy decisions with success/failure tracking
5. **Self Development** — Architecture improvement proposals with post-implementation review

---

## Definition of Done

*(See [Definition of Done](#definition-of-done) section above for full checklist)*
