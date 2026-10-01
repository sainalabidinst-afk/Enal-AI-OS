# ECP v2.0+ — Additional Capabilities Analysis

**Status:** Implemented
**Date:** 2026-10-01
**ADRs referenced:** ADR-001, ADR-003, ADR-004, ADR-005, ADR-008, ADR-010, ADR-012

---

## 1. Overview

This document analyzes the three new capability packs proposed in Session 1 and
implemented as part of ECP v2.0+. All three packs follow the existing
Capability Pack pattern (ADR-003, ADR-004) and integrate with the Cognitive
Kernel pipeline (ADR-001).

---

## 2. Capability Pack Implementations

### 2.1 Scenario Simulator — What-If Engine (RFC-0023)

| Aspect | Detail |
|---|---|
| **Pack name** | `apps/scenario_simulator/` |
| **App class** | `ScenarioSimulatorApp` |
| **Engine class** | `ScenarioSimulatorEngine` |
| **Worker class** | `ScenarioSimulatorWorker` |
| **Pipeline** | `perception → memory → simulation → decision` |
| **ADR compliance** | ADR-003 (Worker is thin adapter), ADR-004 (Engine owns logic) |

**Components:**

| Component | File | Responsibility |
|---|---|---|
| `ScenarioBuilder` | `scenario_builder.py` | Parse natural language "what-if" descriptions into structured `ScenarioRequest` with variables, changes, distributions, assumptions |
| `MonteCarloRunner` | `monte_carlo_runner.py` | Run N iterations sampling from distributions (uniform, normal, triangular), producing `IterationResult` per iteration |
| `SandboxExecutor` | `sandbox_executor.py` | Execute isolated code experiments within each scenario state using `sandbox_runtime` (ADR-010) |
| `OutcomeAnalyzer` | `outcome_analyzer.py` | Compute distribution stats (mean, median, percentiles, histogram), best/worst/most-likely outcomes, key drivers |

**Integration with Core:**
- `ScenarioSimulatorEngine` is wrapped as `SimulationService` in `cognitive_kernel.py`
- Uses `backend.app.core.sandbox.SandboxRuntime` for sandboxed code execution
- Available in `TaskComplexity.COMPLEX` and `VERY_COMPLEX` pipelines per `adaptive_runtime.py`

**Existing component relationships:**
- `sandbox_runtime` (core) → `SandboxExecutor`
- `model_router` (core) → `ScenarioBuilder.parse_with_llm()`

### 2.2 Cross-Domain Knowledge Graph Generator — The Connector (RFC-0024)

| Aspect | Detail |
|---|---|
| **Pack name** | `apps/cross_domain_graph/` |
| **App class** | `CrossDomainGraphApp` |
| **Engine class** | `CrossDomainGraphEngine` |
| **Worker class** | `CrossDomainGraphWorker` |
| **Pipeline** | `perception → memory → reasoning → decision` |
| **ADR compliance** | ADR-003 (Worker is thin adapter), ADR-004 (Engine owns logic) |

**Components:**

| Component | File | Responsibility |
|---|---|---|
| `MemoryScanner` | `memory_scanner.py` | Scan all 7 memory layers (working, conversation, knowledge, longterm, episodic, session, project) for entities and concepts |
| `EntityResolver` | `entity_resolver.py` | Identify the same entity across different domains/layers and merge duplicates |
| `EdgeExtractor` | `edge_extractor.py` | Discover relationships between entities (related_to, depends_on, correlates_with, causes, etc.) |
| `GraphBuilder` | `graph_builder.py` | Build and maintain persistent cross-domain graph with persistence to disk |
| `InferenceEngine` | `engine.py` | Cross-domain Q&A using deterministic graph traversal + LLM-enhanced synthesis |

**Integration with Core:**
- Extends `backend.app.core.knowledge/graph.py` (existing `KnowledgeGraph`)
- Complements `backend.app.core.semantic_graph.py` (project-scoped semantic graph)
- Uses `memory_manager` (core) to scan all memory layers

**Existing component relationships:**
- `memory_layer.py` (7-layer memory model) → `MemoryScanner`
- `knowledge_graph.py` (core KnowledgeGraph) → `GraphBuilder` (extends, not replaces)
- `semantic_graph.py` (project graph) → `GraphBuilder` (complementary)
- `model_router` (core) → `InferenceEngine._llm_inference()`

### 2.3 Adversarial Testing Agent — Devil's Advocate (RFC-0025)

| Aspect | Detail |
|---|---|
| **Pack name** | `apps/adversarial_testing/` |
| **App class** | `AdversarialTestingApp` |
| **Engine class** | `AdversarialTestingEngine` |
| **Worker class** | `AdversarialTestingWorker` |
| **Pipeline** | `perception → memory → reasoning → simulation → decision → action` |
| **ADR compliance** | ADR-003 (Worker is thin adapter), ADR-004 (Engine owns logic), ADR-008 (anti-fragility pattern) |

**Components:**

| Component | File | Responsibility |
|---|---|---|
| `AttackVectorGenerator` | `attack_vector_generator.py` | Generate diverse adversarial attack scenarios using template-based generation across 8 attack categories |
| `AssumptionAuditor` | `assumption_auditor.py` | Identify hidden assumptions in plans, strategies, and recommendations |
| `VulnerabilityScanner` | `vulnerability_scanner.py` | Score and assess exploitability of discovered vulnerabilities against attack vectors |
| `HardeningAdvisor` | `hardening_advisor.py` | Recommend mitigations for identified vulnerabilities |
| `AdversarialGate` | `adversarial_gate.py` | Evaluate pass/fail criteria based on vulnerability severity and hardening coverage |
| `ExplanationGenerator` | `explanation_generator.py` | Generate full reasoning chain explaining why the subject passed or failed the gate |

**Attack categories (8):** external_shock, dependency_failure, resource_exhaustion, competitive_response, regulatory_change, data_corruption, information_warfare, operational_disruption

**Integration with Core:**
- `AdversarialTestingEngine.test()` is wrapped as `AdversarialTestingService` in `cognitive_kernel.py`
- Available in `TaskComplexity.COMPLEX` and `VERY_COMPLEX` pipelines
- Integrates with Decision Intelligence's SimulationEngine and StrategicPlanner

**Existing component relationships:**
- `AdaptiveRuntime` (pipeline orchestration) → `AdversarialTestingService`
- `DecisionResult` from Decision Intelligence → subject for adversarial testing
- `Reflection` framework → similar self-critique pattern as `self_reflection.review()`

---

## 3. ADR Compliance Summary

| ADR | Requirement | How Satisfied |
|---|---|---|
| ADR-001 | Small, stable Core Pipeline | New services added to CognitiveKernel follow same ABC + lazy-import pattern; no Core logic changed |
| ADR-003 | Worker = thin adapter | All three packs: Worker only parses task → delegates to Engine → returns dict |
| ADR-004 | Domain Engine owns logic | All business logic in `engine.py` + sub-components; Worker has zero business logic |
| ADR-008 | Core changes require ≥2 consumers | `SimulationService` and `AdversarialTestingService` justified by: 1) Decision Intelligence SimulationEngine, 2) Scenario Simulator, 3) Adversarial Testing, 4) AdaptiveRuntime pipeline presets already referencing these |

---

## 4. Cognitive Services Added

| Service | File | Pipeline positions |
|---|---|---|
| `SimulationService` | `cognitive_kernel.py` | `simulation` (COMPLEX and VERY_COMPLEX) |
| `AdversarialTestingService` | `cognitive_kernel.py` | `adversarial_testing` (COMPLEX and VERY_COMPLEX) |

**Note:** The pipeline presets in `adaptive_runtime.py` already referenced `"simulation"` and `"adversarial_testing"` in the COMPLEX and VERY_COMPLEX pipelines (lines 46-67), but these services were not registered in the CognitiveKernel. This implementation completes that integration — no new pipeline slots were added to Core.

---

## 5. File Inventory

### New Files Created

```
apps/scenario_simulator/
├── __init__.py              # ScenarioSimulatorApp, get_app(), exports
├── schemas.py               # ScenarioRequest, VariableChange, SimulationResult, DistributionStats
├── scenario_builder.py      # ScenarioBuilder - NLP → structured scenario
├── monte_carlo_runner.py    # MonteCarloRunner, IterationResult
├── sandbox_executor.py      # SandboxExecutor - isolated code execution
├── outcome_analyzer.py      # OutcomeAnalyzer - stats + best/worst/most-likely
├── engine.py                # ScenarioSimulatorEngine - orchestrator
└── worker.py                # ScenarioSimulatorWorker - thin adapter

apps/cross_domain_graph/
├── __init__.py              # CrossDomainGraphApp, get_app(), exports
├── schemas.py               # GraphQueryRequest, GraphNode, GraphEdge, GraphQueryResult
├── memory_scanner.py        # MemoryScanner - scan 7 memory layers
├── entity_resolver.py       # EntityResolver - cross-domain entity resolution
├── edge_extractor.py        # EdgeExtractor - relationship discovery
├── graph_builder.py         # GraphBuilder - persistent graph management
├── engine.py                # CrossDomainGraphEngine - orchestrator
└── worker.py                # CrossDomainGraphWorker - thin adapter

apps/adversarial_testing/
├── __init__.py              # AdversarialTestingApp, get_app(), exports
├── schemas.py               # AdversarialTestRequest, AttackVector, Vulnerability, etc.
├── attack_vector_generator.py  # AttackVectorGenerator - 8 attack categories
├── assumption_auditor.py    # AssumptionAuditor - hidden assumption detection
├── vulnerability_scanner.py # VulnerabilityScanner - severity scoring
├── hardening_advisor.py     # HardeningAdvisor - mitigation recommendations
├── adversarial_gate.py      # AdversarialGate - pass/fail evaluation
├── explanation_generator.py # ExplanationGenerator - reasoning chain
├── engine.py                # AdversarialTestingEngine - orchestrator
└── worker.py                # AdversarialTestingWorker - thin adapter

tests/golden/
├── test_scenario_simulator.py       # 25 tests
├── test_cross_domain_graph.py      # 22 tests
└── test_adversarial_testing.py     # 25 tests

docs/capabilities/
└── v2-additional-capabilities-analysis.md  # This document

real_cases/
├── scenario_simulator/evaluation.md
├── cross_domain_graph/evaluation.md
└── adversarial_testing/evaluation.md

docs/rfcs/
├── RFC-0023-scenario-simulator.md
├── RFC-0024-cross-domain-graph.md
└── RFC-0025-adversarial-testing.md
```

**Modifications to existing files:**
- `backend/app/core/cognitive_kernel.py` — added `SimulationService` and `AdversarialTestingService`
- `backend/app/core/adaptive_runtime.py` — added `adversarial_testing` to COMPLEX and VERY_COMPLEX pipelines
- `agents/skills.yaml` — added `simulation`, `knowledge-graph`, `adversarial-testing` skill entries
- `docs/rfcs/README.md` — updated RFC index with RFC-0023/0024/0025

---

## 6. Test Plan

Each pack has 10+ golden tests covering:
- Schema validation
- Builder/engine component unit tests
- End-to-end integration through Engine
- Worker adapter tests
- Serialization (to_dict) tests
- Reproducibility with seeds

Tests are in `tests/golden/` and follow the existing test patterns from
`test_decision_intelligence.py` and `test_capability_pipeline.py`.
