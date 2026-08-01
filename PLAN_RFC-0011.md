# Plan: Implementasi RFC-0011 (System Architect)

## Informasi yang Dikumpulkan

RFC-0011 mendefinisikan **System Architect Capability Pack** — arsitek arsitektur untuk ECP.
Menjadi otoritas arsitektur yang me-review, memvalidasi, dan memandu desain sistem secara keseluruhan.
Ini adalah Capability Pack ke-8 ECP. **Zero Core changes.**

### Core Capabilities (8 sub-modul)
1. **Clean Architecture Review** — Evaluasi layers, dependency rule, boundaries
2. **DDD Analysis** — Evaluasi bounded contexts, aggregates, domain events
3. **Event-Driven Design** — Evaluasi event schemas, event flow, saga patterns
4. **CQRS Evaluation** — Evaluasi command/query separation appropriateness
5. **Microservices/Monolith Review** — Evaluasi service decomposition strategies
6. **Architecture Governance** — Enforce architectural rules, dependency constraints
7. **ADR Generation** — Generate dan track Architecture Decision Records
8. **Package Boundary Enforcement** — Deteksi dependency violations dan layer inversions

### Target Quality: A (≥90)
- Architecture Review Completeness ≥95%
- Dependency Violation Detection ≥95%
- Package Boundary Enforcement ≥90%
- ADR Coverage ≥90%
- Design Pattern Application ≥85%
- Scalability Assessment ≥90%
- Maintainability ≥90%
- Explainability ≥95%

### Golden Test: 10 scenarios
1. Clean Architecture layer violation → detection + fix suggestion
2. Dependency cycle → cycle identified + breaking points
3. Package boundary violation → unauthorized import detected
4. DDD bounded context misalignment → boundary issues identified
5. Event-driven design anti-pattern → missing event schema/saga
6. CQRS anti-pattern (write-through reads) → mismatch identified
7. Monolith decomposition opportunity → candidates identified
8. ADR generation → ADR draft with context/decision/consequences
9. Scalability bottleneck → concern identified
10. Maintainability degradation → issue with remediation

### Prinsip Arsitektur
- **Zero Core changes** — semua di `apps/system_architect/`
- **ADR-002 compliance** — komunikasi via Execution Runtime, bukan direct import
- **ADR-003 compliance** — Worker = thin adapter
- **ADR-004 compliance** — Domain Engine owns business logic
- **ADR-005 compliance** — rekomendasi, bukan eksekusi otomatis

### Leverage Existing
- Code Engineer sudah punya `dependency_graph.py` — bisa dijadikan foundation untuk:
  - `dependency_graph.py` di System Architect (import graph builder spesifik untuk arsitektur)
  - Layer analyzer bisa menggunakan AST parser dari `apps.code_engineer.parser`
- Pattern Decision Intelligence (engine + worker + schemas) bisa diikuti

## Plan Implementasi

### Step 1: Buat package structure + schemas
- `apps/system_architect/__init__.py` — ekspor publik
- `apps/system_architect/schemas.py` — ArchitectureReviewRequest, ArchitectureReviewReport, Finding, DDDContext, ArchitectureMetrics, ADRDraft, Recommendation (Pydantic models)

### Step 2: Implementasi Dependency Graph Builder
- `apps/system_architect/dependency_graph.py` — Import graph analysis, circular dep detection, layer classification
- Extend dari pattern Code Engineer tapi dengan fokus layer detection arsitektur
- Layer detection: entities, use_cases, interface_adapters, frameworks, infrastructure

### Step 3: Implementasi Layer Analyzer (Clean Architecture)
- `apps/system_architect/layer_analyzer.py` — Clean Architecture layer violation detection
- Dependency rule enforcement (inner layers → outer layers OK, outer → inner VIOLATION)
- Package boundary checking

### Step 4: Implementasi DDD Analyzer
- `apps/system_architect/ddd_analyzer.py` — DDD pattern evaluation
- Bounded context detection, aggregate identification, anti-corruption layer analysis

### Step 5: Implementasi Event Analyzer
- `apps/system_architect/event_analyzer.py` — Event-driven design review
- Event schema analysis, saga pattern detection, event flow validation

### Step 6: Implementasi CQRS Evaluator
- `apps/system_architect/cqrs_evaluator.py` — CQRS suitability assessment
- Command/query separation analysis, read/write model detection

### Step 7: Implementasi Microservices Analyzer
- `apps/system_architect/microservices_analyzer.py` — Microservices/monolith review
- Service decomposition analysis, migration path evaluation

### Step 8: Implementasi ADR Generator
- `apps/system_architect/adr_generator.py` — ADR document generation
- Template-based with context-aware content

### Step 9: Implementasi Architecture Governance + Boundary Enforcer
- `apps/system_architect/boundary_enforcer.py` — Package boundary enforcement
- `apps/system_architect/governance.py` — Architecture rule checking

### Step 10: Implementasi Engine + Worker + Benchmark
- `apps/system_architect/engine.py` — SystemArchitectEngine orchestrator
- `apps/system_architect/worker.py` — Thin adapter (per ADR-003)
- `benchmarks/system_architect_benchmark.py` — 100 architecture projects
- Metrics: review completeness, violation detection, boundary enforcement, ADR coverage, design pattern, scalability, maintainability, explainability, consistency

### Step 11: Dokumentasi + TODO.md
- `docs/capabilities/system-architect.md` — profile Capability Pack resmi
- Update `docs/CAPABILITY_STRATEGY.md` — System Architect sebagai official pack ke-8
- Update `docs/RELEASE_CRITERIA.md` — Developer Preview quality targets + DoD
- Update `docs/v1_roadmap.md` — Capability Packs overview
- Update `TODO.md` — track progress

## Dependent Files
- `apps/system_architect/` — seluruh package baru (12+ file)
- `benchmarks/system_architect_benchmark.py` — benchmark baru
- `docs/capabilities/system-architect.md` — profile pack
- `docs/CAPABILITY_STRATEGY.md` — update profil pack
- `docs/RELEASE_CRITERIA.md` — update DoD
- `docs/v1_roadmap.md` — update overview
- `TODO.md` — track progress

## Follow-up Steps
- Import verification + smoke test pipeline
- Benchmark run (100 scenarios)
- Validasi integration points dengan Code Engineer (first consumer)
- Update TODO.md

## Total Estimasi: 11 steps
