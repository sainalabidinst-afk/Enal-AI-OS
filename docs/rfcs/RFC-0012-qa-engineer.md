# RFC-0012: QA Engineer Capability Pack

| Field | Value |
|-------|-------|
| **RFC ID** | RFC-0012 |
| **Status** | Draft |
| **Version** | 0.1.0 |
| **Author** | Enal AI OS Core Team |
| **Target Release** | v1.3.0 (Enterprise phase) |
| **Capability Pack** | QA Engineer |
| **Capability ID** | `qa-engineer` |
| **Category** | Quality Assurance |
| **Quality Target** | A (≥90) |
| **Maturity Target** | Level 3 — Production Ready |
| **Reference RFC** | RFC-0012 |

---

## Motivation

ECP's existing Capability Packs generate code, configurations, and systems, but there is no dedicated quality assurance layer that systematically validates outputs, generates tests, and ensures quality across all artifacts.

Currently:

1. **Test generation is embedded in Code Engineer** — only Python unit tests are generated; no integration, regression, or mutation testing.
2. **No regression test automation** — changes are not systematically tested for regressions.
3. **No mutation testing** — test suite quality is not measured by mutation score.
4. **No flaky test detection** — intermittent test failures go undetected and undermine confidence.
5. **No golden test generator** — there is no systematic generation of golden test cases for other Capability Packs.
6. **No benchmark test generation** — no performance or load testing of generated systems.
7. **No test coverage analysis across the platform** — coverage gaps are not tracked holistically.

The QA Engineer Capability Pack becomes the quality assurance layer, providing test generation, regression testing, mutation testing, flaky test detection, golden test generation for other packs, benchmark testing, coverage analysis, and performance validation for all ECP systems.

---

## Problem Statement

Without a dedicated QA Engineer Capability Pack:

- **Test quality is not measured** — no mutation score, no coverage analysis, no flakiness detection.
- **Regression is detected late** — no systematic regression test generation or execution.
- **Golden tests are not generated** — other Capability Packs lack systematic test case generation.
- **No performance validation** — generated systems are not benchmarked for performance.
- **Flaky tests erode trust** — intermittent failures are not detected or investigated.
- **Test coverage is incomplete** — coverage gaps across all Capability Pack outputs are not tracked.
- **No benchmark test generation** — no automated performance/load test creation for generated systems.

The absence of QA Engineer means that quality assurance is reactive rather than proactive, and that test quality itself is never measured or improved.

---

## Goals

1. **Unit Test Generation** — Generate unit tests for all code outputs from Code Engineer.
2. **Integration Test Generation** — Generate integration tests covering component interactions.
3. **Regression Test Automation** — Generate and maintain regression test suites for evolving systems.
4. **Mutation Testing** — Measure test suite quality via mutation score.
5. **Golden Test Generation** — Generate golden test cases for other Capability Packs (Code, Network, Trading, DevOps).
6. **Benchmark Test Generation** — Generate performance and load tests for systems.
7. **Flaky Test Detection** — Detect, classify, and report intermittent test failures.
8. **Test Coverage Analysis** — Measure and report coverage across all Capability Pack outputs.
9. **Performance Validation** — Validate performance requirements against benchmarks.

### Success Criteria

| Metric | Target | Grade |
|--------|--------|-------|
| Test Generation Coverage | ≥95% (all code covered by generated tests) | A |
| Mutation Score | ≥80% (test suite quality) | A |
| Regression Detection | ≥95% (regressions caught before deployment) | A |
| Golden Test Generation | ≥90% (test cases for other packs generated) | A |
| Flaky Test Detection | ≥90% (flaky tests identified) | A |
| Coverage Analysis | ≥85% (coverage measured across all packs) | A |
| Performance Validation | ≥90% (benchmarks validated) | A |
| Explainability | ≥90% (test findings explained) | A |

---

## Non-Goals

1. **Replacing production test infrastructure** — QA Engineer generates tests; execution happens in CI/CD.
2. **Live test execution against production systems** — Focus is on test generation and analysis, not execution.
3. **Replacing dedicated testing tools** — Tools like pytest, Jest, k6 remain; QA Engineer provides orchestration and generation.
4. **Manual test case design** — Focus is on automated test generation.
5. **Core modification** — All implementation resides within the QA Engineer Capability Pack.

---

## Capability Scope

### Core Capabilities

| Capability | Description | Inputs | Outputs |
|-----------|-------------|--------|---------|
| Unit Test Generation | Generate unit tests for source code | Source code, language spec | Unit test files with pass/fail expectation |
| Integration Test Generation | Generate tests covering component interactions | API specs, database schema, service definitions | Integration test files |
| Regression Test Automation | Generate and maintain regression test suites | Codebase, change history, test results | Regression test suite + maintenance plan |
| Mutation Testing | Measure test suite quality via mutation score | Source code, test suite | Mutation score report with killed/survived mutants |
| Golden Test Generation | Generate golden test cases for other Capability Packs | Pack output specs, expected results | Golden test cases for Code, Network, Trading, DevOps |
| Benchmark Test Generation | Generate performance/load tests | System specs, performance requirements | Benchmark test scripts + expected metrics |
| Flaky Test Detection | Detect and classify intermittent test failures | Test results history, CI/CD logs | Flaky test report with classification |
| Test Coverage Analysis | Measure coverage across all Capability Pack outputs | Source code, test suites | Coverage report with gaps identified |
| Performance Validation | Validate performance against benchmarks | Benchmark results, performance metrics | Performance validation report |

### Out of Scope

- Live test execution against production systems
- Test runner infrastructure (pytest, Jest, etc.)
- CI/CD pipeline execution
- Manual test case design
- Database test data generation (beyond fixtures)
- Security testing (Security Engineer handles this)

---

## Public Contracts

### Input Contract: QA Test Request

```json
{
  "request_id": "uuid",
  "operation": "unit_test | integration_test | regression_test | mutation_test | golden_test | benchmark_test | flaky_test | coverage | performance_validation",
  "target": {
    "source_code": "string — code content or repository path",
    "test_suite": "string — existing test suite content",
    "language": "python | javascript | typescript | go | java",
    "framework": "pytest | jest | junit | go-test"
  },
  "for_capability_pack": "string — target pack for golden test generation",
  "coverage_target": 0.0,
  "mutation_target": 0.0,
  "performance_requirements": {
    "latency_p95_ms": 0,
    "throughput_rps": 0,
    "max_memory_mb": 0
  },
  "include_uncovered_code": true
}
```

### Output Contract: QA Test Report

```json
{
  "request_id": "uuid",
  "operation": "string",
  "test_artifacts": [
    {
      "file_path": "string",
      "test_type": "unit | integration | regression | golden | benchmark",
      "test_count": 0,
      "expected_pass": 0,
      "content": "string — generated test content"
    }
  ],
  "coverage_report": {
    "line_coverage": 0.0,
    "branch_coverage": 0.0,
    "function_coverage": 0.0,
    "uncovered_lines": ["string"],
    "gaps": ["string"]
  },
  "mutation_report": {
    "mutation_score": 0.0,
    "total_mutants": 0,
    "killed": 0,
    "survived": 0,
    "timeout": 0,
    "no_coverage": 0,
    "weakest_areas": ["string"]
  },
  "regression_report": {
    "tests_added": 0,
    "tests_removed": 0,
    "risky_changes": ["string"],
    "maintenance_notes": ["string"]
  },
  "flaky_test_report": {
    "flaky_tests": [
      {
        "test_name": "string",
        "failure_rate": 0.0,
        "classification": "network | timing | shared_state | order_dependent",
        "severity": "critical | high | medium | low"
      }
    ],
    "total_flaky": 0
  },
  "performance_validation": {
    "meets_latency_requirement": true,
    "meets_throughput_requirement": true,
    "latency_p95": 0,
    "throughput": 0.0,
    "bottlenecks": ["string"]
  },
  "summary": {
    "total_tests_generated": 0,
    "tests_passing": 0,
    "coverage_improvement": 0.0,
    "mutation_score": 0.0,
    "overall_risk": "critical | high | medium | low",
    "recommendations": ["string"]
  }
}
```

### Test Quality Record (Experience Memory)

```json
{
  "record_id": "uuid",
  "request_id": "uuid",
  "timestamp": "ISO 8601",
  "target_capability_pack": "string",
  "tests_generated": 0,
  "mutation_score": 0.0,
  "coverage_before": 0.0,
  "coverage_after": 0.0,
  "flaky_tests_found": 0,
  "performance_validated": true,
  "outcome": "passed | partial | failed | revised"
}
```

---

## Integration Points (Capability Graph)

```
Consumer Capability Pack (Code Engineer, System Architect, QA-dependent apps)
    │
    │  submits code/test suite for QA analysis via task/intent
    ▼
Execution Runtime
    │
    │  routes to QA Engineer Domain Engine
    ▼
QA Engineer Engine
    │
    │  ┌─────────────────────────────────────────────────────┐
    │  │ 1. Unit Test Generation                             │
    │  │ 2. Integration Test Generation                      │
    │  │ 3. Regression Test Automation                       │
    │  │ 4. Mutation Testing                                 │
    │  │ 5. Golden Test Generation                           │
    │  │ 6. Benchmark Test Generation                        │
    │  │ 7. Flaky Test Detection                             │
    │  │ 8. Coverage Analysis → Experience Memory            │
    │  │ 9. Performance Validation                           │
    │  └─────────────────────────────────────────────────────┘
    │
    │  returns QA Test Report
    ▼
Consumer Capability Pack
    │
    │  receives generated tests + quality metrics
    ▼
User / Human Approval Loop (tests added to CI/CD by user)
```

### Task Template

| Task | Subtasks |
|------|----------|
| Test Suite Generation | Project scan → Test plan → Unit tests → Integration tests → Coverage analysis → Mutation test → Flaky detection → Performance validation → Report |

---

## Consumer Capability Packs

| Consumer Capability Pack | Use Case |
|--------------------------|----------|
| **Code Engineer** | Generate and analyze tests for generated code |
| **System Architect** | Architecture-based test strategy, coverage analysis |
| **DevOps Assistant** | CI/CD test pipeline design, flaky test detection |
| **Self Development** | Test coverage for improvement proposals |

---

## Dependencies

### Internal Dependencies (Shared Contracts)

1. **Execution Runtime** — Task routing and orchestration (per ADR-002)
2. **Experience Memory** — Test quality records persistence (per ADR-011)
3. **Shared Contracts** — Task/Intent definition and result schema (per ADR-006)

### External Testing Tools (for golden test validation reference)

1. **pytest** — Python test framework (reference for generated test patterns)
2. **Jest** — JavaScript/TypeScript testing
3. **JUnit** — Java testing
4. **mut.py / mutmut** — Mutation testing tools
5. **coverage.py** — Coverage analysis
6. **k6 / locust** — Load and performance testing

### No Core Changes Required

All implementation resides within the QA Engineer Capability Pack:

```
apps/
└── qa_engineer/
    ├── engine.py              # Domain Engine (per ADR-004)
    ├── worker.py              # Thin adapter (per ADR-003)
    ├── schemas.py             # Public contracts
    ├── test_generator.py      # Unit/integration test generation
    ├── regression_tester.py   # Regression test automation
    ├── mutation_tester.py     # Mutation testing
    ├── golden_test_gen.py     # Golden test case generation
    ├── benchmark_gen.py       # Benchmark test generation
    ├── flaky_detector.py      # Flaky test detection
    ├── coverage_analyzer.py   # Coverage analysis
    └── performance_validator.py # Performance validation
```

**ADR Impact:** None. No Core, Runtime, Kernel, or shared contract modification required.

---

## Benchmark Specification

### Benchmark Framework

| Dimension | Definition | Measurement | Target |
|-----------|------------|-------------|--------|
| **Test Generation Coverage** | % of code covered by generated tests | Coverage analysis on generated tests | ≥95% |
| **Mutation Score** | Quality of generated test suite | Mutants killed / total mutants | ≥80% |
| **Regression Detection** | % of regressions caught by generated tests | Regressions caught in test runs | ≥95% |
| **Golden Test Generation** | % of golden test cases generated for other packs | Golden tests generated / expected | ≥90% |
| **Flaky Test Detection** | % of flaky tests identified | Flaky detected / ground truth flaky | ≥90% |
| **Coverage Analysis Accuracy** | Correctness of coverage reports | Expert-validated coverage | ≥85% |
| **Performance Validation** | % of performance requirements validated | Benchmarks validated | ≥90% |
| **Explainability** | Clarity of test findings and gaps | Human evaluation score | ≥90% |
| **Consistency** | Same input produces same tests | Variance across 10 runs < 5% | ≥90% |

### Benchmark Dataset

- **100 repository audits** covering:
  - Python repositories (APIs, data pipelines, web apps)
  - JavaScript/TypeScript projects (frontend, backend, full-stack)
  - Go services (microservices, CLI tools)
  - Java applications (Spring Boot, enterprise)
  - Mixed technology stacks

### Benchmark Dimensions Detail

| Scenario Type | Description | Ground Truth |
|---------------|-------------|-------------|
| Regression | Test suite fails on known regression | Inject known bugs, verify detection |
| Mutation | Mutants killed by generated tests | Mutant analysis tool output |
| Flaky Tests | Intermittent test failures detected | Flaky test database |
| Coverage | Coverage gaps identified | Coverage tool output |
| Benchmark | Performance benchmarks generated and validated | Performance test execution |

---

## Golden Test Specification

| # | Scenario | Expected Outcome | Acceptance Criteria |
|---|----------|-----------------|---------------------|
| 1 | Unit test for Python function | Tests generated, covering all branches | ≥95% coverage |
| 2 | Integration test for REST API | Tests generated for all endpoints | ≥90% endpoint coverage |
| 3 | Regression test for known bug | Test catches regression | ≥95% detection |
| 4 | Mutation testing on code | Mutations killed | ≥80% mutation score |
| 5 | Flaky test detection | Flaky test identified and classified | ≥90% detection |
| 6 | Coverage gap identification | Uncovered code identified | ≥85% accuracy |
| 7 | Golden test for Code Engineer | Golden test case generated | ≥90% completeness |
| 8 | Golden test for Network Engineer | Golden test case generated | ≥90% completeness |
| 9 | Benchmark test generation | Load test script generated with metrics | ≥90% completeness |
| 10 | Performance validation | Latency/throughput validated against targets | ≥90% pass rate |

### Golden Test Acceptance Criteria

- All 10 golden test scenarios pass at ≥90% of acceptance criteria (100% pass)
- Overall QA Engineer golden test pass rate ≥90%
- All generated tests are syntactically valid for their target framework
- Mutation score ≥80% on all benchmark projects

---

## Real Case Requirements

### Real Case Directory

`real_cases/qa_engineer/` must contain:

| Requirement | Minimum Count |
|-------------|---------------|
| Real repository audits from actual usage | 20 |
| Cases with mutation testing | 10 |
| Cases with flaky test detection | 5 |
| Cases with coverage analysis | 15 |
| Cases with golden test generation for other packs | 10 |
| Cases with expert review/validation | 15 |

### Real Case Structure

```
real_cases/qa_engineer/<case_id>/
├── input/
│   ├── source_code/         # Repository or code snapshot
│   ├── existing_tests/      # Existing test suite (if any)
│   └── test_request.json
├── output/
│   ├── generated_tests/     # Generated test files
│   ├── qa_report.json       # Full QA Test Report
│   └── recommendations.md   # Improvement suggestions
└── evaluation.md            # Ground truth, expert review, lessons learned
```

### Real Case Targets

| Metric | Target |
|--------|--------|
| Real cases logged | ≥20 (Level 3) → ≥100 (Level 4) |
| Real case quality score (expert review) | ≥90% |
| Regression detection rate (post-deployment) | ≥95% |

---

## Definition of Done

```text
Definition of Done — QA Engineer Capability Pack

Functional
- [ ] Unit Test Generation for Python, JavaScript/TypeScript, Go, Java
- [ ] Integration Test Generation covering API endpoints and component interactions
- [ ] Regression Test Automation with maintenance plan
- [ ] Mutation Testing with mutation score reporting
- [ ] Golden Test Generation for Code Engineer, Network Engineer, Trading Analyst, DevOps Assistant
- [ ] Benchmark Test Generation for performance/load testing
- [ ] Flaky Test Detection with classification
- [ ] Test Coverage Analysis across all target languages
- [ ] Performance Validation against latency/throughput/budget requirements

Benchmark
- [ ] Test Generation Coverage ≥ 95% (grade A)
- [ ] Mutation Score ≥ 80%
- [ ] Regression Detection ≥ 95%
- [ ] Golden Test Generation ≥ 90%
- [ ] Flaky Test Detection ≥ 90%
- [ ] Coverage Analysis ≥ 85%
- [ ] Performance Validation ≥ 90%
- [ ] Explainability ≥ 90%
- [ ] Consistency ≥ 90%

Golden Tests
- [ ] All 10 pack golden test scenarios pass at ≥90% of acceptance criteria (100% pass)

Real Cases
- [ ] ≥ 20 real cases logged in real_cases/qa_engineer/
- [ ] Evaluation notes recorded for each case
- [ ] ≥ 10 cases with mutation testing
- [ ] ≥ 5 cases with flaky test detection
- [ ] ≥ 15 cases with coverage analysis
- [ ] ≥ 10 cases with golden test generation for other packs

Documentation
- [ ] Capability Guide updated (CAPABILITY_GUIDE.md — QA Engineer section)
- [ ] API reference / contract updated (this RFC + schemas.py)
- [ ] Real case evaluation summary published

SDK
- [ ] Pack accessible via SDK without Core changes
- [ ] QA Engineer callable via Execution Runtime task routing

Performance
- [ ] Latency P95 < 3000ms for single repository test generation
- [ ] Latency P95 < 10000ms for multi-module project with mutation testing

Security
- [ ] No known P0/P1 security issues
- [ ] Generated test content does not include vulnerabilities

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
| Generated tests are poor quality (low mutation score) | High — false confidence | Medium | Mutation-driven improvement loop; quality gates |
| Flaky test detection produces false positives | Medium — wasted debugging time | High | Historical analysis with >10 runs; confidence scoring |
| Coverage analysis misses code paths | Medium — incomplete coverage | Medium | Multi-tool coverage; path coverage where feasible |
| Golden test generation is too generic | Medium — not useful for edge cases | High | Template-based with customization hooks; feedback loop |
| Performance validation assumes wrong baselines | Medium — incorrect pass/fail | Medium | Baseline capture before testing; historical comparison |
| Mutation testing is computationally expensive | Low — slow test generation | High | Configurable mutant limit; parallel execution; sampling |
| Generated tests break on valid code changes | Medium — maintenance burden | High | Regression test maintenance plan; automated updates |

---

## ADR Impact

**Does this require Core changes?** No.

QA Engineer is a **new Capability Pack** that follows the established patterns:

- **ADR-001 (Core Pipeline Freeze):** No Core changes. All logic in `apps/qa_engineer/`.
- **ADR-002 (Capability Pack Independence):** QA Engineer communicates with other packs via Execution Runtime tasks and shared contracts only. No direct imports.
- **ADR-003 (Worker = Adapter Only):** A thin Worker routes tasks to the Domain Engine.
- **ADR-004 (Domain Engine Owns Business Logic):** All test generation and QA logic resides in `apps/qa_engineer/engine.py`.
- **ADR-005 (Human Approval Required):** Generated tests require human review before integration; no automatic CI/CD modification (per ADR-005).
- **ADR-006 (Capability Contract v1 Frozen):** Uses the existing Capability Contract for node and subtask template registration. No contract changes.
- **ADR-007 (Conversation Boundary):** QA Engineer is invoked through Execution Runtime, not directly by Conversation Manager.
- **ADR-008 (Core Change Requires Cross-Capability Proof):** Not applicable — no Core changes.

**ADR Required:** None. This is a new Capability Pack, not a Core modification.

---

## Rollout Plan

### Phase 1: Prototype (RFC → Experimental)

**Duration:** 5 weeks

- [ ] Create `apps/qa_engineer/` package structure
- [ ] Implement Python unit test generation
- [ ] Implement coverage analysis (line/branch)
- [ ] Define public contracts (QA Request, QA Report)
- [ ] Implement thin Worker adapter
- [ ] Create 10 golden test scenarios
- [ ] Integration: Code Engineer → QA Engineer (test generation for generated code)
- [ ] Integration: System Architect → QA Engineer (coverage analysis)
- **Gate:** 10 golden tests pass at ≥80%

### Phase 2: Full Capabilities (Experimental → Stable)

**Duration:** 8 weeks

- [ ] Implement integration test generation
- [ ] Implement mutation testing
- [ ] Implement flaky test detection
- [ ] Implement golden test generation for Code Engineer, Network Engineer, Trading Analyst
- [ ] Implement benchmark test generation
- [ ] Implement performance validation
- [ ] Add JavaScript/TypeScript, Go, Java support
- [ ] Expand golden tests to 10 full scenarios
- [ ] Log ≥20 real cases from Code Engineer usage
- [ ] **Benchmark:** 100 repositories, ≥95% coverage, ≥80% mutation score
- [ ] **Integration:** DevOps Assistant starts using QA Engineer for CI/CD test design
- **Gate:** All 10 golden tests pass at ≥90%; benchmark ≥95% coverage

### Phase 3: Ecosystem (Stable → Certified)

**Duration:** 6 weeks

- [ ] All 4 consumer packs integrated
- [ ] Golden test generation validated for all consumer packs
- [ ] Mutation testing calibrated on 100 repositories
- [ ] Flaky test detection validated in CI/CD pipelines
- [ ] Independent audit of test quality and coverage
- [ ] Public benchmark dashboard available
- [ ] **Benchmark:** ≥95% across all dimensions sustained
- [ ] **Real Cases:** ≥100 cases with ≥80% expert validation
- **Gate:** Independent audit passed; benchmark ≥95% sustained

---

## Future Enhancements

### Fase 2 (Post-v1.0.0 Release)

1. **AI-Powered Test Optimization** — Prioritize test execution order based on historical failure patterns
2. **Property-Based Testing Generation** — Generate property-based tests (Hypothesis, fast-check) from code contracts
3. **Test Suite Evolution** — Automatically update tests when code changes (diff-aware test repair)
4. **Cross-Project Test Intelligence** — Share test insights and flakiness patterns across projects

### Fase 3 (Enterprise)

1. **Test Environment Orchestration** — Provision and manage isolated test environments
2. **Test Data Generation** — Synthetic test data creation with privacy controls
3. **Continuous Test Quality Monitoring** — Track mutation score and coverage drift over time
4. **Test Impact Analysis** — Predict which tests need to run based on code changes

### Long-term

1. **Self-Healing Tests** — Automatically fix brittle tests when code changes
2. **Test Suite Architecture Governance** — Enforce test architecture patterns and anti-pattern detection
3. **Test Flakiness Root Cause Analysis** — Automated diagnosis and fix suggestions for flaky tests
4. **Cross-Platform Test Generation** — Generate tests for mobile, web, API, and contract testing in one workflow
