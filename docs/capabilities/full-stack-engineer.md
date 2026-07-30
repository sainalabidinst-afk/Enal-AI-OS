# Full Stack Engineer Capability Specification

## Version: 1.0.0
## Status: Draft (v1.0 ready for implementation)

---

## 1. Purpose

Deliver full-stack engineering intelligence for:
- Architecture review and scoring
- Code review beyond linting
- Refactoring planning without auto-apply
- Test engineering (unit, integration, contract, performance, regression)
- Performance engineering (database, frontend, algorithm)
- Release engineering (readiness validation)

---

## 2. Scope

### In Scope
- Language: Python (primary), JS/TS patterns (planned)
- Analysis types: Architecture, Code Review, Refactoring, Testing, Performance, Release
- Output: Scores, Graded Reports, Findings, Plans, Test Plans, Release Readiness

### Out of Scope
- Auto-fixing code without approval
- Frontend bundle analysis from compiled assets
- Cloud-native deployment execution

---

## 3. Contract

### Input
```json
{
  "type": "repo|code|changes",
  "content": "repo path or code string",
  "filename": "string",
  "context": {}
}
```

### Output
```json
{
  "architecture_review": {
    "architecture_score": "float 0-100",
    "layering_grade": "A|B+|B|C|D|F",
    "dependency_grade": "A|B+|B|C|D|F",
    "modularity_grade": "A|B+|B|C|D|F",
    "tech_debt_grade": "A|B+|B|C|D|F",
    "issues": []
  },
  "code_review": {
    "findings": [],
    "summary": {}
  },
  "refactoring_plan": {
    "plans": []
  },
  "test_engineering": {
    "coverage_adequate": "boolean",
    "plans": []
  },
  "performance_analysis": {
    "issues": []
  },
  "release_review": {
    "ready": "boolean",
    "checks": []
  }
}
```

---

## 4. Capability Details

### F1 — Architecture Review
- Reads repository using ArchitectureReader
- Checks layering violations, dependency density, modularity, technical debt
- Produces graded scores (A–F) and Architecture Score (0–100)

### F2 — Code Review
- Parses AST and scans raw text for security, concurrency, resource, maintainability, and API surface issues
- Each finding includes evidence, line number, CWE, confidence, and priority
- Categories: Security, Concurrency, Reliability, Maintainability

### F3 — Refactoring Planner
- Does NOT modify code
- Produces structured plan: Problem → Cause → Proposal → Expected Benefit → Risk → Migration Steps
- Detects mutable defaults, long functions, high import density

### F4 — Test Engineer
- Analyzes source and test directories
- Estimates coverage
- Generates test plans for unit, integration, contract, performance, and regression testing

### F5 — Performance Engineer
- Detects N+1 queries, nested loops, blocking I/O, memory issues
- Focus areas: database, algorithm, memory, I/O

### F6 — Release Engineer
- Validates changelog, semantic version, migration, rollback plan, deployment checklist, post-deployment verification
- Produces boolean `ready` and detailed check results

---

## 5. Benchmark Requirements

| Metric | Target | Pass Criteria |
|--------|--------|---------------|
| Architecture Review Accuracy | ≥90% | Correct layering/debt detection |
| Code Review Precision | ≥95% | False positive ≤5% |
| Refactoring Plan Usefulness | ≥85% | Actionable plans with steps |
| Test Coverage Estimate Accuracy | ±10% | Within 10% of actual coverage |
| Performance Detection Recall | ≥90% | True positive ≥90% |
| Release Readiness Precision | ≥95% | Correct ready/fail assessment |

---

## 6. Integration

- Registered as `full-stack-engineer` in `apps/__init__.py`
- Worker: `FullStackWorker` in `apps/society/workers/full_stack_worker.py`
- Capability graph entries in `apps/organization/capability_graph.py` under `full-stack` domain
- Subtask templates defined for each F1–F6 capability
- Reuses `apps.code_engineer` primitives (ArchitectureReader, DependencyGraphBuilder, ImpactAnalyzer, RefactoringEngine, PatchGenerator, RegressionAnalyzer, TestGenerator)

---

## 7. Roadmap

| Capability | Status |
|------------|--------|
| F1 — Architecture Review | ✅ Implemented |
| F2 — Code Review | ✅ Implemented |
| F3 — Refactoring Planner | ✅ Implemented |
| F4 — Test Engineer | ✅ Implemented |
| F5 — Performance Engineer | ✅ Implemented |
| F6 — Release Engineer | ✅ Implemented |

---

## 8. Future Enhancements

- JS/TS AST parsing via `tree-sitter` or `esprima`
- Bundle analysis via webpack/rollup stats
- Database query plan analysis via EXPLAIN
- Diff-aware review for PR/MR changes
- Integration with CI/CD for automated release checks
