<!-- BILINGUAL_DOCS_START -->
## Bahasa Indonesia / English

### Ringkasan / Summary
Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.
> Terjemahan Indonesia: Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.

- Bahasa Indonesia: konten utama tetap dipertahankan dalam dokumen asli, dan bagian ini memberi konteks ringkas dalam bahasa Indonesia.
- English: the main content remains in the original document, and this section provides a concise bilingual context for international readers.

### Informasi Dokumen / Document Info
- File: `docs/capabilities/system-architect.md`
- Judul: System Architect
- Status: bilingual header added

<!-- BILINGUAL_DOCS_END -->

# System Architect Capability Specification

<!-- DOCUMENT_METADATA_START -->
**Owner:** Documentation Team
**Canonical Owner:** Documentation Governance Lead
**Last Verified:** 2026-08-02
**Version:** 1.0.0
**Status:** Active
**SSOT:** Capability Pack specification for system-architect
<!-- DOCUMENT_METADATA_END -->

## Version: 1.0.0
## Status: Production Ready (RFC-0011)
## Quality Target: A (â‰¥90)

---

## 1. Purpose

System Architect adalah **arsitek arsitektur** untuk ECP â€” Capability Pack yang
menjadi otoritas arsitektur untuk me-review, memvalidasi, dan memandu desain
sistem secara keseluruhan.
> Terjemahan Indonesia: Sistem Architect adalah arsitek arsitektur untuk ECP â€” kapabilitas Pack yang menjadi otoritas arsitektur untuk me-review, memvalidasi, dan memandu desain sistem secara keseluruhan.

Capability Pack ini menganalisis struktur proyek, Clean Architecture compliance,
DDD patterns, event-driven design, CQRS suitability, microservices/monolith
decomposition, package boundaries, dan menghasilkan Architecture Decision Records
(ADR) â€” **tanpa memodifikasi Core**.
> Terjemahan Indonesia: Kapabilitas Pack ini menganalisis struktur proyek, Clean arsitektur compliance, DDD patterns, event-driven design, CQRS suitability, microservices/monolith decomposition, package boundaries, dan menghasilkan arsitektur Decision Records (ADR) â€” tanpa memodifikasi Core.

---

## 2. Scope

### In Scope
- **Clean Architecture Review** â€” Evaluasi layers, dependency rule, boundaries
- **DDD Analysis** â€” Evaluasi bounded contexts, aggregates, domain events, anti-corruption
- **Event-Driven Design** â€” Evaluasi event schemas, event flow, saga patterns
- **CQRS Evaluation** â€” Evaluasi command/query separation appropriateness
- **Microservices/Monolith Review** â€” Evaluasi service decomposition strategies
- **Architecture Governance** â€” Enforce architectural rules, dependency constraints, Core change guard
- **ADR Generation** â€” Generate dan track Architecture Decision Records
- **Package Boundary Enforcement** â€” Deteksi dependency violations dan layer inversions

### Out of Scope
- Eksekusi refactoring otomatis (rekomendasi saja â€” ADR-005 compliance)
- Modifikasi Core contracts
- Direct import dari Capability Pack lain (ADR-002 compliance)

---

## 3. Contract

### Input: ArchitectureReviewRequest
```json
{
  "review_id": "uuid",
  "review_type": "full_review|clean_architecture|ddd|event_driven|cqrs|microservices|package_boundary|adr_generation",
  "workspace_path": "path-to-project",
  "architecture_style": "clean_architecture|layered|hexagonal|ddd|microservices|monolith|event_driven",
  "existing_adrs": ["ADR-001", "ADR-002"],
  "constraints": ["no core changes", "use shared contracts"],
  "focus_areas": ["scalability", "maintainability", "testability", "deployability", "modifiability"],
  "include_recommendations": true
}
```

### Output: ArchitectureReviewReport
```json
{
  "review_id": "uuid",
  "review_type": "full_review",
  "findings": [
    {
      "category": "layer_violation|dependency_cycle|package_boundary|ddd_violation|event_design|cqrs_mismatch|monolith_anti_pattern|architecture_smell",
      "severity": "critical|high|medium|low",
      "title": "string",
      "description": "string",
      "evidence": {"source_file": "...", "line_number": 0},
      "recommendation": "string",
      "impact": "scalability|maintainability|testability|deployability|modifiability",
      "confidence": 0.0-1.0
    }
  ],
  "adr_draft": {
    "title": "ADR-N: Title",
    "status": "proposed",
    "context": "string",
    "decision": "string",
    "consequences": ["string"]
  },
  "ddd_assessment": {
    "bounded_contexts": [{"name": "string", "entities": [], "aggregates": []}],
    "anti_corruption_layers": [],
    "domain_events": []
  },
  "architecture_metrics": {
    "dependency_cycles": 0,
    "layer_violations": 0,
    "package_boundaries_crossed": 0,
    "maintainability_score": 0.0,
    "scalability_score": 0.0,
    "testability_score": 0.0
  },
  "recommendations": [{"priority": "high", "problem": "string", "solution": "string"}],
  "summary": {
    "total_findings": 0,
    "critical_count": 0,
    "high_count": 0,
    "medium_count": 0,
    "low_count": 0,
    "overall_risk": "medium",
    "confidence": 0.0
  }
}
```

---

## 4. Pipeline

```
ArchitectureReviewRequest
    â†“
DependencyGraph (import graph, circular deps, layer classification)
    â†“
LayerAnalysis (Clean Architecture violations)
    â†“
DDDAnalysis (bounded contexts, aggregates, anti-corruption)
    â†“
EventAnalysis (event schema, saga patterns)
    â†“
CQRSEvaluation (command/query separation)
    â†“
MicroservicesReview (decomposition, migration)
    â†“
BoundaryEnforcement (package boundary violations)
    â†“
Governance (Core change guard, Capability First Rule)
    â†“
ADRGeneration (structured ADR drafts)
    â†“
ArchitectureReviewReport
```

---

## 5. Benchmark Results (RFC-0011)

| Dimension | Target |
|-----------|--------|
| Architecture Review Completeness | â‰¥95% |
| Dependency Violation Detection | â‰¥95% |
| Package Boundary Enforcement | â‰¥90% |
| ADR Coverage | â‰¥90% |
| Design Pattern Application | â‰¥85% |
| Scalability Assessment | â‰¥90% |
| Maintainability | â‰¥90% |
| Explainability | â‰¥95% |

Benchmark: `benchmarks/system_architect_benchmark.py`
> Terjemahan Indonesia: Tolok ukur: benchmarks/system_architect_benchmark.py

---

## 6. Golden Test Scenarios

| # | Scenario | Detection |
|---|----------|-----------|
| 1 | Clean Architecture layer violation | Layer violation + fix suggestion |
| 2 | Dependency cycle | Cycle identified + breaking points |
| 3 | Package boundary violation | Unauthorized import detected |
| 4 | DDD bounded context misalignment | Boundary issues identified |
| 5 | Event-driven design anti-pattern | Missing event schema/saga |
| 6 | CQRS anti-pattern (write-through reads) | Mismatch identified |
| 7 | Monolith decomposition opportunity | Candidates identified |
| 8 | ADR generation | ADR draft with context/decision/consequences |
| 9 | Scalability bottleneck | Concern identified |
| 10 | Maintainability degradation | Issue with remediation |

---

## 7. Consumer Integration

System Architect menjadi **otoritas arsitektur** untuk:
> Terjemahan Indonesia: Sistem Architect menjadi otoritas arsitektur untuk:
- **Code Engineer** â€” review arsitektur pada repository yang dihasilkan
- **Self Development** â€” analisis arsitektur dan rekomendasi refactoring
- **Decision Intelligence** â€” evidence sumber untuk keputusan arsitektur
- **Semua Capability Pack** â€” validasi kepatuhan ADR-001/002/003/004/005

The `SystemArchitectWorker` is a thin adapter (ADR-003) that routes
task dicts to `SystemArchitectEngine.review()`.
> Terjemahan Indonesia: SystemArchitectWorker adalah sebuah thin adapter (ADR-003) itu routes task dicts untuk SystemArchitectEngine.review().

---

## 8. Architecture Compliance

| Principle | Compliance |
|-----------|------------|
| ADR-001 Core Pipeline Freeze | âœ… Zero Core changes |
| ADR-002 Capability Pack Independence | âœ… No direct imports |
| ADR-003 Worker = Adapter Only | âœ… Worker delegates to Engine |
| ADR-004 Domain Engine Owns Business Logic | âœ… Engine owns pipeline |
| ADR-005 Human Approval Required | âœ… Recommend only, no auto-execute |
| Kernel Stability | âœ… Not in Core |

---

## 9. Files

| File | Purpose |
|------|---------|
| `apps/system_architect/schemas.py` | Pydantic models |
| `apps/system_architect/dependency_graph.py` | Import graph builder + layer classification |
| `apps/system_architect/layer_analyzer.py` | Clean Architecture layer analysis |
| `apps/system_architect/ddd_analyzer.py` | DDD bounded context analysis |
| `apps/system_architect/event_analyzer.py` | Event-driven design analysis |
| `apps/system_architect/cqrs_evaluator.py` | CQRS suitability evaluation |
| `apps/system_architect/microservices_analyzer.py` | Microservices/monolith analysis |
| `apps/system_architect/adr_generator.py` | ADR generation |
| `apps/system_architect/boundary_enforcer.py` | Package boundary enforcement |
| `apps/system_architect/governance.py` | Architecture governance rules |
| `apps/system_architect/engine.py` | Domain engine orchestrator |
| `apps/system_architect/worker.py` | Thin worker adapter |
| `benchmarks/system_architect_benchmark.py` | Benchmark (8 dimensions) |
