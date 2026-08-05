# Spesifikasi Capability Pack System Architect

<!-- DOCUMENT_METADATA_START -->
**Pemilik:** Tim Dokumentasi
**Pemilik Canonical:** Pimpinan Tata Kelola Dokumentasi
**Terakhir Diverifikasi:** 2026-08-02
**Versi:** 2.0.0
**Status:** Aktif
**SSOT:** Spesifikasi Capability Pack untuk System Architect
<!-- DOCUMENT_METADATA_END -->

## Versi: 1.0.0
## Status: Production Ready (RFC-0011)
## Quality Target: A (≥90)

---

## 1. Tujuan

System Architect adalah **otoritas arsitektur** untuk ECP — Capability Pack yang menjadi acuan untuk me-review, memvalidasi, dan memandu desain sistem secara keseluruhan.

Capability Pack ini menganalisis struktur proyek, mengevaluasi Clean Architecture, pola DDD, desain event-driven, kesesuaian CQRS, dekomposisi microservices/monolith, batasan package, dan menghasilkan Architecture Decision Record (ADR) — **tanpa memodifikasi Core**.

---

## 2. Ruang Lingkup

### Dalam Ruang Lingkup
- **Architecture Review (Clean Architecture)** — Evaluasi layer, aturan dependensi, batasan
- **Analisis DDD** — Evaluasi bounded context, aggregate, domain event, anti-corruption layer
- **Desain Event-Driven** — Evaluasi skema event, alur event, pola saga
- **Evaluasi CQRS** — Evaluasi kesesuaian command/query separation
- **Review Microservices/Monolith** — Evaluasi strategi dekomposisi layanan
- **Governance Arsitektur** — Menegakkan aturan arsitektur, batasan dependensi, dan core change guard
- **Generasi ADR** — Menghasilkan dan melacak Architecture Decision Record
- **Package Boundary Enforcement** — Deteksi pelanggaran dependensi dan inversi layer

### Di Luar Ruang Lingkup
- Eksekusi refactoring otomatis (hanya rekomendasi — memenuhi ADR-005)
- Modifikasi kontrak Core
- Impor langsung dari Capability Pack lain (kepatuhan ADR-002)

---

## 3. Kontrak

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
    ↓
DependencyGraph (import graph, circular deps, layer classification)
    ↓
LayerAnalysis (Clean Architecture violations)
    ↓
DDDAnalysis (bounded contexts, aggregates, anti-corruption)
    ↓
EventAnalysis (event schema, saga patterns)
    ↓
CQRSEvaluation (command/query separation)
    ↓
MicroservicesReview (decomposition, migration)
    ↓
BoundaryEnforcement (package boundary violations)
    ↓
Governance (Core change guard, Capability First Rule)
    ↓
ADRGeneration (structured ADR drafts)
    ↓
ArchitectureReviewReport
```

---

## 5. Hasil Benchmark (RFC-0011)

**Hasil Terverifikasi:**
- Overall: 97.50%
- Pass rate: 100%
- Status: PASS


| Dimensi | Target |
|-----------|--------|
| Architecture Review Completeness | ≥95% |
| Dependency Violation Detection | ≥95% |
| Package Boundary Enforcement | ≥90% |
| ADR Coverage | ≥90% |
| Design Pattern Application | ≥85% |
| Scalability Assessment | ≥90% |
| Maintainability | ≥90% |
| Explainability | ≥95% |

Benchmark: `benchmarks/system_architect_benchmark.py`

---

## 6. Skenario Golden Test

| # | Skenario | Deteksi |
|---|----------|-----------|
| 1 | Pelanggaran layer Clean Architecture | Pelanggaran layer + saran perbaikan |
| 2 | Dependency cycle | Siklus teridentifikasi + titik puncaknya |
| 3 | Pelanggaran package boundary | Impor tidak sah terdeteksi |
| 4 | Ketidakselarasan bounded context DDD | Masalah batas teridentifikasi |
| 5 | Anti-pola desain event-driven | Skema/saga event tidak ada |
| 6 | Anti-pola CQRS (read-write) | Ketidakcocokan teridentifikasi |
| 7 | Peluang dekomposisi monolith | Kandidat teridentifikasi |
| 8 | Generasi ADR | Draft ADR dengan context/decision/consequences |
| 9 | Scalability bottleneck | Kekhawatiran teridentifikasi |
| 10 | Degradasi maintainability | Masalah dengan remediasi |

---

## 7. Integrasi Konsumen

System Architect menjadi **otoritas arsitektur** untuk:
- **Code Engineer** — review arsitektur pada repositori yang dihasilkan
- **Self Development** — analisis arsitektur dan rekomendasi refactoring
- **Decision Intelligence** — sumber bukti untuk keputusan arsitektur
- **Semua Capability Pack** — validasi kepatuhan ADR-001/002/003/004/005

`SystemArchitectWorker` adalah adaptor tipis (ADR-003) yang merutekan tugas yang ditentukan ke `SystemArchitectEngine.review()`.

---

## 8. Kepatuhan Arsitektur

| Prinsip | Kepatuhan |
|-----------|------------|
| ADR-001 Core Pipeline Freeze | ✅ Zero Core Change |
| ADR-002 Capability Pack Independence | ✅ Tidak ada impor langsung |
| ADR-003 Worker = Hanya Adaptor | ✅ Worker mendelegasikan ke Engine |
| ADR-004 Domain Engine Memiliki Business Logic | ✅ Engine memiliki pipeline |
| ADR-005 Persetujuan Manusia Diperlukan | ✅ Rekomendasi saja, tanpa eksekusi otomatis |
| Kernel Stability | ✅ Tidak di Core |

---

## 9. File

| File | Tujuan |
|------|---------|
| `apps/system_architect/schemas.py` | Model Pydantic |
| `apps/system_architect/dependency_graph.py` | Pembangun import graph + klasifikasi layer |
| `apps/system_architect/layer_analyzer.py` | Analisis layer Clean Architecture |
| `apps/system_architect/ddd_analyzer.py` | Analisis bounded context DDD |
| `apps/system_architect/event_analyzer.py` | Analisis desain event-driven |
| `apps/system_architect/cqrs_evaluator.py` | Evaluasi kesesuaian CQRS |
| `apps/system_architect/microservices_analyzer.py` | Analisis microservices/monolith |
| `apps/system_architect/adr_generator.py` | Generasi ADR |
| `apps/system_architect/boundary_enforcer.py` | Package boundary enforcement |
| `apps/system_architect/governance.py` | Aturan governance arsitektur |
| `apps/system_architect/scalability_analyzer.py` | Analisis skala sistem (scalability bottlenecks) |
| `apps/system_architect/security_architect.py` | Review arsitektur untuk keamanan (auth, encryption, threat surface) |
| `apps/system_architect/cost_optimizer.py` | Analisis optimasi biaya arsitektur |
| `apps/system_architect/refactoring_strategy.py` | Rekomendasi strategi refactoring berbasis temuan |
| `apps/system_architect/engine.py` | Orchestrator domain engine |
| `apps/system_architect/worker.py` | Adaptor worker tipis |
| `benchmarks/system_architect_benchmark.py` | Benchmark (8 dimensi) |

