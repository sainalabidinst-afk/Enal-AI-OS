# Spesifikasi Capability Pack System Architect

<!-- DOCUMENT_METADATA_START -->
**Pemilik:** Tim Dokumentasi
**Pemilik Canonical:** Pimpinan Tata Kelola Dokumentasi
**Terakhir Diverifikasi:** 2026-08-02
**Versi:** 2.0.0
**Status:** Aktif
**SSOT:** Spesifikasi Capability Pack untuk System Architect
<!-- DOCUMENT_METADATA_END -->

## Versi: 2.0.0
## Status: Production Ready (RFC-0011)
## Quality Target: A+ (≥95), Domain Expert (L4)
## Sertifikasi: Certified Lifecycle (RFC-0011)

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

## 4. Operasi

| Operasi | Deskripsi | Input | Output |
|-----------|-------------|--------|---------|
| `full_review` | Review arsitektur lengkap (all analyzers) | workspace_path, architecture_style | ArchitectureReviewReport |
| `clean_architecture` | Review khusus Clean Architecture layer violations | workspace_path | Layer violations + recommendations |
| `ddd` | Review DDD: bounded context, aggregates, ACL | workspace_path | DDD assessment + violations |
| `event_driven` | Review desain event-driven, saga patterns | workspace_path | Event design assessment |
| `cqrs` | Review CQRS: command/query separation | workspace_path | CQRS mismatch findings |
| `microservices` | Review microservices/monolith decomposition | workspace_path | Decomposition candidates |
| `package_boundary` | Review pelanggaran package boundary | workspace_path | Boundary violations |
| `adr_generation` | Generate ADR dari konteks arsitektur | context | ADR draft |

## 5. Modul Analyzer

| Modul | Tanggung Jawab |
|--------|----------------|
| `dependency_graph.py` | Membangun import graph + klasifikasi layer |
| `layer_analyzer.py` | Analisis pelanggaran layer Clean Architecture |
| `ddd_analyzer.py` | Analisis bounded context, aggregate, ACL |
| `event_analyzer.py` | Analisis desain event-driven, saga patterns |
| `cqrs_evaluator.py` | Evaluasi kesesuaian CQRS |
| `microservices_analyzer.py` | Analisis microservices/monolith |
| `adr_generator.py` | Generasi ADR |
| `boundary_enforcer.py` | Package boundary enforcement |
| `governance.py` | Aturan governance arsitektur |
| `scalability_analyzer.py` | Analisis bottleneck skalabilitas |
| `security_architect.py` | Review arsitektur untuk keamanan |
| `cost_optimizer.py` | Analisis optimasi biaya arsitektur |
| `refactoring_strategy.py` | Rekomendasi strategi refactoring |

## 6. Dimensi Benchmark

| Dimensi | Target | Grade |
|-----------|--------|-------|
| Architecture Review Completeness | ≥95% | A+ |
| Dependency Violation Detection | ≥95% | A+ |
| Package Boundary Enforcement | ≥95% | A+ |
| ADR Coverage | ≥95% | A+ |
| Design Pattern Application | ≥95% | A+ |
| Scalability Assessment | ≥95% | A+ |
| Maintainability | ≥95% | A+ |
| Explainability | ≥95% | A+ |

---

## 7. Dependensi

- **apps/base.py** — Definisi model dasar
- **apps/system_architect/schemas.py** — Kontrak publik
- **apps/system_architect/dependency_graph.py** — Pembangun import graph
- **apps/system_architect/layer_analyzer.py** — Analisis layer
- **apps/system_architect/ddd_analyzer.py** — Analisis DDD
- **apps/system_architect/event_analyzer.py** — Analisis event-driven
- **apps/system_architect/cqrs_evaluator.py** — Evaluasi CQRS
- **apps/system_architect/microservices_analyzer.py** — Analisis microservices
- **apps/system_architect/adr_generator.py** — Generasi ADR
- **apps/system_architect/boundary_enforcer.py** — Package boundary enforcement
- **apps/system_architect/governance.py** — Governance arsitektur
- **apps/system_architect/scalability_analyzer.py** — Analisis skalabilitas
- **apps/system_architect/security_architect.py** — Review arsitektur security
- **apps/system_architect/cost_optimizer.py** — Optimasi biaya arsitektur
- **apps/system_architect/refactoring_strategy.py** — Strategi refactoring
- **apps/system_architect/engine.py** — Orchestrator domain engine
- **apps/system_architect/worker.py** — Adaptor worker tipis (ADR-003)

---

## 8. Contoh Penggunaan

```python
from apps.system_architect.engine import SystemArchitectEngine
from apps.system_architect.schemas import ArchitectureReviewRequest, ReviewType

engine = SystemArchitectEngine()
request = ArchitectureReviewRequest(
    review_type=ReviewType.full_review,
    workspace_path="/path/to/project",
    architecture_style="clean_architecture",
    focus_areas=["scalability", "maintainability"],
)
report = engine.review(request)
print(f"Found {len(report.findings)} architecture issues")
print(f"Maintainability score: {report.architecture_metrics.maintainability_score:.0%}")
```

---

## 9. Audit Keamanan

| Aspek | Status | Catatan |
|--------|--------|---------|
| Input Validation | ✅ | Path validation untuk workspace_path |
| Code Access Safety | ✅ | Hanya membaca file, tidak menulis |
| Sensitive Data Handling | ✅ | Tidak mengekspos credential dalam output |
| ADR Integrity | ✅ | ADR draft diawali sebagai 'proposed' — memerlukan persetujuan manusia |
| Core Protection | ✅ | ADR-001 compliance — zero Core change |

**Catatan Keamanan:**
- System Architect hanya membaca file source code — tidak mengeksekusi atau memodifikasi.
- ADR yang dihasilkan berupa 'proposed' dan memerlukan persetujuan manusia (ADR-005).
- Dependency graph construction menghindari traversal ke direktori sensitif.

---

## 10. Optimasi Kinerja

| Aspek | Rekomendasi | Dampak |
|--------|-------------|--------|
| Dependency Graph | Cache import graph antar review (invalidate on file change) | Mengurangi waktu re-analysis |
| Layer Analysis | Incremental analysis — hanya file yang berubah | 5-10x peningkatan |
| Boundary Enforcement | Pre-compile regex patterns | Faster pattern matching |
| ADR Generation | Template-based dengan slot filling | Mengurangi LLM call |
| Scalability Analysis | Sampling untuk codebase besar (>10K LOC) | Linear scaling |
| Concurrent Analysis | Jalankan analyzer secara paralel (thread pool) | Multi-core utilization |
| Result Caching | Cache report untuk workspace yang tidak berubah | Instant report untuk re-review |

**Target Latensi:**
- Full review (10K LOC): < 5 detik
- Single analyzer: < 1 detik
- ADR generation: < 500ms

---

## 11. Skenario Golden Test

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

## 12. Integrasi Konsumen

System Architect menjadi **otoritas arsitektur** untuk:
- **Code Engineer** — review arsitektur pada repositori yang dihasilkan
- **Self Development** — analisis arsitektur dan rekomendasi refactoring
- **Decision Intelligence** — sumber bukti untuk keputusan arsitektur
- **Semua Capability Pack** — validasi kepatuhan ADR-001/002/003/004/005

`SystemArchitectWorker` adalah adaptor tipis (ADR-003) yang merutekan tugas yang ditentukan ke `SystemArchitectEngine.review()`.

---

## 13. Kepatuhan Arsitektur

| Prinsip | Kepatuhan |
|-----------|------------|
| ADR-001 Core Pipeline Freeze | ✅ Zero Core Change |
| ADR-002 Capability Pack Independence | ✅ Tidak ada impor langsung |
| ADR-003 Worker = Hanya Adaptor | ✅ Worker mendelegasikan ke Engine |
| ADR-004 Domain Engine Memiliki Business Logic | ✅ Engine memiliki pipeline |
| ADR-005 Persetujuan Manusia Diperlukan | ✅ Rekomendasi saja, tanpa eksekusi otomatis |
| Kernel Stability | ✅ Tidak di Core |

---

## 14. File

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

