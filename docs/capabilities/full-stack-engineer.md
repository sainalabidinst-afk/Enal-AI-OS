<!-- BILINGUAL_DOCS_START -->
## Bahasa Indonesia / English

### Ringkasan / Summary
Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.
> Terjemahan Indonesia: Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.

- Bahasa Indonesia: konten utama tetap dipertahankan dalam dokumen asli, dan bagian ini memberi konteks ringkas dalam bahasa Indonesia.
- English: the main content remains in the original document, and this section provides a concise bilingual context for international readers.

### Informasi Dokumen / Document Info
- File: `docs/capabilities/full-stack-engineer.md`
- Judul: Full Stack Engineer
- Status: bilingual header added

<!-- BILINGUAL_DOCS_END -->

# Full Stack Engineer Capability Specification

<!-- DOCUMENT_METADATA_START -->
**Owner:** Documentation Team
**Canonical Owner:** Documentation Governance Lead
**Last Verified:** 2026-08-02
**Version:** 1.0.0
**Status:** Active
**SSOT:** Capability Pack specification for full-stack-engineer
<!-- DOCUMENT_METADATA_END -->

## Version: 1.0.0
## Status: Draft (v1.0 ready for implementation)

---

## 1. Purpose

Deliver full-stack engineering intelligence for:
> Terjemahan Indonesia: Deliver full-stack rekayasa intelligence untuk:
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

### F1 â€” Architecture Review
- Reads repository using ArchitectureReader
- Checks layering violations, dependency density, modularity, technical debt
- Produces graded scores (Aâ€“F) and Architecture Score (0â€“100)

### F2 â€” Code Review
- Parses AST and scans raw text for security, concurrency, resource, maintainability, and API surface issues
- Each finding includes evidence, line number, CWE, confidence, and priority
- Categories: Security, Concurrency, Reliability, Maintainability

### F3 â€” Refactoring Planner
- Does NOT modify code
- Produces structured plan: Problem â†’ Cause â†’ Proposal â†’ Expected Benefit â†’ Risk â†’ Migration Steps
- Detects mutable defaults, long functions, high import density

### F4 â€” Test Engineer
- Analyzes source and test directories
- Estimates coverage
- Generates test plans for unit, integration, contract, performance, and regression testing

### F5 â€” Performance Engineer
- Detects N+1 queries, nested loops, blocking I/O, memory issues
- Focus areas: database, algorithm, memory, I/O

### F6 â€” Release Engineer
- Validates changelog, semantic version, migration, rollback plan, deployment checklist, post-deployment verification
- Produces boolean `ready` and detailed check results

---

## 5. Benchmark Requirements

| Metric | Target | Pass Criteria |
|--------|--------|---------------|
| Architecture Review Accuracy | â‰¥90% | Correct layering/debt detection |
| Code Review Precision | â‰¥95% | False positive â‰¤5% |
| Refactoring Plan Usefulness | â‰¥85% | Actionable plans with steps |
| Test Coverage Estimate Accuracy | Â±10% | Within 10% of actual coverage |
| Performance Detection Recall | â‰¥90% | True positive â‰¥90% |
| Release Readiness Precision | â‰¥95% | Correct ready/fail assessment |

---

## 6. Integration

- Registered as `full-stack-engineer` in `apps/__init__.py`
- Worker: `FullStackWorker` in `apps/society/workers/full_stack_worker.py`
- Capability graph entries in `apps/organization/capability_graph.py` under `full-stack` domain
- Subtask templates defined for each F1â€“F6 capability
- Reuses `apps.code_engineer` primitives (ArchitectureReader, DependencyGraphBuilder, ImpactAnalyzer, RefactoringEngine, PatchGenerator, RegressionAnalyzer, TestGenerator)

---

## 7. Roadmap

| Capability | Status |
|------------|--------|
| F1 â€” Architecture Review | âœ… Implemented |
| F2 â€” Code Review | âœ… Implemented |
| F3 â€” Refactoring Planner | âœ… Implemented |
| F4 â€” Test Engineer | âœ… Implemented |
| F5 â€” Performance Engineer | âœ… Implemented |
| F6 â€” Release Engineer | âœ… Implemented |

---

## 8. Future Enhancements

- JS/TS AST parsing via `tree-sitter` or `esprima`
- Bundle analysis via webpack/rollup stats
- Database query plan analysis via EXPLAIN
- Diff-aware review for PR/MR changes
- Integration with CI/CD for automated release checks
