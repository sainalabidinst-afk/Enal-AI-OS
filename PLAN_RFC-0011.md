<!-- BILINGUAL_DOCS_START -->
## Bahasa Indonesia / English

### Ringkasan / Summary
Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.
> Terjemahan Indonesia: Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.

- Bahasa Indonesia: konten utama tetap dipertahankan dalam dokumen asli, dan bagian ini memberi konteks ringkas dalam bahasa Indonesia.
- English: the main content remains in the original document, and this section provides a concise bilingual context for international readers.

### Informasi Dokumen / Document Info
- File: `PLAN_RFC-0011.md`
- Judul: Plan Rfc 0011
- Status: bilingual header added

<!-- BILINGUAL_DOCS_END -->

# Plan: Implementasi RFC-0011 (System Architect)

<!-- DOCUMENT_METADATA_START -->
**Owner:** Documentation Team
**Canonical Owner:** Documentation Governance Lead
**Last Verified:** 2026-08-02
**Version:** 1.0.0
**Status:** Active
**SSOT:** Documentation for PLAN_RFC-0011
<!-- DOCUMENT_METADATA_END -->

## Informasi yang Dikumpulkan

RFC-0011 mendefinisikan **System Architect Capability Pack** â€” arsitek arsitektur untuk ECP.
Menjadi otoritas arsitektur yang me-review, memvalidasi, dan memandu desain sistem secara keseluruhan.
Ini adalah Capability Pack ke-8 ECP. **Zero Core changes.**
> Terjemahan Indonesia: RFC-0011 mendefinisikan sistem Architect kapabilitas Pack â€” arsitek arsitektur untuk ECP. Menjadi otoritas arsitektur yang me-review, memvalidasi, dan memandu desain sistem secara keseluruhan. Ini adalah kapabilitas Pack ke-8 ECP. Zero Core changes.

### Core Capabilities (8 sub-modul)
1. **Clean Architecture Review** â€” Evaluasi layers, dependency rule, boundaries
2. **DDD Analysis** â€” Evaluasi bounded contexts, aggregates, domain events
3. **Event-Driven Design** â€” Evaluasi event schemas, event flow, saga patterns
4. **CQRS Evaluation** â€” Evaluasi command/query separation appropriateness
5. **Microservices/Monolith Review** â€” Evaluasi service decomposition strategies
6. **Architecture Governance** â€” Enforce architectural rules, dependency constraints
7. **ADR Generation** â€” Generate dan track Architecture Decision Records
8. **Package Boundary Enforcement** â€” Deteksi dependency violations dan layer inversions

### Target Quality: A (â‰¥90)
- Architecture Review Completeness â‰¥95%
- Dependency Violation Detection â‰¥95%
- Package Boundary Enforcement â‰¥90%
- ADR Coverage â‰¥90%
- Design Pattern Application â‰¥85%
- Scalability Assessment â‰¥90%
- Maintainability â‰¥90%
- Explainability â‰¥95%

### Golden Test: 10 scenarios
1. Clean Architecture layer violation â†’ detection + fix suggestion
2. Dependency cycle â†’ cycle identified + breaking points
3. Package boundary violation â†’ unauthorized import detected
4. DDD bounded context misalignment â†’ boundary issues identified
5. Event-driven design anti-pattern â†’ missing event schema/saga
6. CQRS anti-pattern (write-through reads) â†’ mismatch identified
7. Monolith decomposition opportunity â†’ candidates identified
8. ADR generation â†’ ADR draft with context/decision/consequences
9. Scalability bottleneck â†’ concern identified
10. Maintainability degradation â†’ issue with remediation

### Prinsip Arsitektur
- **Zero Core changes** â€” semua di `apps/system_architect/`
- **ADR-002 compliance** â€” komunikasi via Execution Runtime, bukan direct import
- **ADR-003 compliance** â€” Worker = thin adapter
- **ADR-004 compliance** â€” Domain Engine owns business logic
- **ADR-005 compliance** â€” rekomendasi, bukan eksekusi otomatis

### Leverage Existing
- Code Engineer sudah punya `dependency_graph.py` â€” bisa dijadikan foundation untuk:
  - `dependency_graph.py` di System Architect (import graph builder spesifik untuk arsitektur)
  - Layer analyzer bisa menggunakan AST parser dari `apps.code_engineer.parser`
> Terjemahan Indonesia: Dependency_graph.py di sistem Architect (import graph builder spesifik untuk arsitektur) Layer analyzer bisa menggunakan AST parser dari apps.code_engineer.parser
- Pattern Decision Intelligence (engine + worker + schemas) bisa diikuti

## Plan Implementasi

### Step 1: Buat package structure + schemas
- `apps/system_architect/__init__.py` â€” ekspor publik
- `apps/system_architect/schemas.py` â€” ArchitectureReviewRequest, ArchitectureReviewReport, Finding, DDDContext, ArchitectureMetrics, ADRDraft, Recommendation (Pydantic models)

### Step 2: Implementasi Dependency Graph Builder
- `apps/system_architect/dependency_graph.py` â€” Import graph analysis, circular dep detection, layer classification
- Extend dari pattern Code Engineer tapi dengan fokus layer detection arsitektur
- Layer detection: entities, use_cases, interface_adapters, frameworks, infrastructure

### Step 3: Implementasi Layer Analyzer (Clean Architecture)
- `apps/system_architect/layer_analyzer.py` â€” Clean Architecture layer violation detection
- Dependency rule enforcement (inner layers â†’ outer layers OK, outer â†’ inner VIOLATION)
- Package boundary checking

### Step 4: Implementasi DDD Analyzer
- `apps/system_architect/ddd_analyzer.py` â€” DDD pattern evaluation
- Bounded context detection, aggregate identification, anti-corruption layer analysis

### Step 5: Implementasi Event Analyzer
- `apps/system_architect/event_analyzer.py` â€” Event-driven design review
- Event schema analysis, saga pattern detection, event flow validation

### Step 6: Implementasi CQRS Evaluator
- `apps/system_architect/cqrs_evaluator.py` â€” CQRS suitability assessment
- Command/query separation analysis, read/write model detection

### Step 7: Implementasi Microservices Analyzer
- `apps/system_architect/microservices_analyzer.py` â€” Microservices/monolith review
- Service decomposition analysis, migration path evaluation

### Step 8: Implementasi ADR Generator
- `apps/system_architect/adr_generator.py` â€” ADR document generation
- Template-based with context-aware content

### Step 9: Implementasi Architecture Governance + Boundary Enforcer
- `apps/system_architect/boundary_enforcer.py` â€” Package boundary enforcement
- `apps/system_architect/governance.py` â€” Architecture rule checking

### Step 10: Implementasi Engine + Worker + Benchmark
- `apps/system_architect/engine.py` â€” SystemArchitectEngine orchestrator
- `apps/system_architect/worker.py` â€” Thin adapter (per ADR-003)
- `benchmarks/system_architect_benchmark.py` â€” 100 architecture projects
- Metrics: review completeness, violation detection, boundary enforcement, ADR coverage, design pattern, scalability, maintainability, explainability, consistency

### Step 11: Dokumentasi + TODO.md
- `docs/capabilities/system-architect.md` â€” profile Capability Pack resmi
- Update `docs/CAPABILITY_STRATEGY.md` â€” System Architect sebagai official pack ke-8
- Update `docs/RELEASE_CRITERIA.md` â€” Developer Preview quality targets + DoD
- Update `docs/v1_roadmap.md` â€” Capability Packs overview
- Update `TODO.md` â€” track progress

## Dependent Files
- `apps/system_architect/` â€” seluruh package baru (12+ file)
- `benchmarks/system_architect_benchmark.py` â€” benchmark baru
- `docs/capabilities/system-architect.md` â€” profile pack
- `docs/CAPABILITY_STRATEGY.md` â€” update profil pack
- `docs/RELEASE_CRITERIA.md` â€” update DoD
- `docs/v1_roadmap.md` â€” update overview
- `TODO.md` â€” track progress

## Follow-up Steps
- Import verification + smoke test pipeline
- Benchmark run (100 scenarios)
- Validasi integration points dengan Code Engineer (first consumer)
- Update TODO.md

## Total Estimasi: 11 steps
