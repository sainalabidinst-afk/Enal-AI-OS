# Business Analyst — Spesifikasi Capability

**Versi:** 1.0.0
**Status:** Production Ready (RFC-0013)
**Target Kualitas:** A- (≥85)

---

## 1. Tujuan

Business Analyst adalah **otoritas analisis bisnis** untuk ECP — Capability Pack yang menerjemahkan kebutuhan bisnis menjadi spesifikasi teknis yang jelas, terstruktur, dan dapat dieksekusi oleh Capability Pack lain.

Capability Pack ini mengumpulkan requirement, memodelkan proses bisnis, menghasilkan user story, use case, BRD, functional specification, gap analysis, ROI analysis, dan rekomendasi optimasi proses — **tanpa memodifikasi Core**.

---

## 2. Ruang Lingkup

### Dalam Ruang Lingkup
- **Requirement Gathering** — Pengumpulan, penataan, dan validasi requirement
- **Business Process Modeling** — Pemodelan alur kerja dengan notasi seperti BPMN
- **User Story Generation** — Menghasilkan user story yang memenuhi kriteria INVEST
- **Use Case Modeling** — Menghasilkan detail use case dari spesifikasi
- **BRD Generation** — Menghasilkan Business Requirements Document
- **Functional Specification** — Spesifikasi fungsional untuk Capability Pack hilir
- **Gap Analysis** — Identifikasi kesenjangan antara kebutuhan bisnis dan kemampuan teknis
- **ROI Analysis** — Analisis laba atas investasi (NPV, payback period)
- **Process Optimization** — Mengidentifikasi dan merekomendasikan perbaikan proses
- **Experience Memory** — Merekam hasil ke riwayat

### Di Luar Cakupan
- Fasilitasi pertemuan stakeholder
- Manajemen proyek atau alokasi sumber daya
- Definisi strategi bisnis
- Perencanaan keuangan di luar ROI
- Implementasi manajemen perubahan
- Eksekusi atau monitoring proses secara langsung
- Modifikasi kontrak Core

---

## 3. Kontrak

### Input: BusinessAnalysisRequest
```json
{
  "request_id": "uuid",
  "operation": "requirement_gathering | process_modeling | user_story | use_case | brd_generation | functional_spec | gap_analysis | roi_analysis | process_optimization",
  "business_context": {
    "domain": "e-commerce | fintech | healthcare",
    "project_name": "string",
    "description": "string — project overview"
  },
  "inputs": {
    "natural_language_requirements": ["string"],
    "stakeholder_notes": ["string"],
    "interview_transcripts": ["string"],
    "current_state_documentation": "string",
    "technical_constraints": ["string"]
  },
  "personas": [
    {
      "name": "string",
      "role": "string",
      "goals": ["string"],
      "pain_points": ["string"]
    }
  ],
  "quality_attributes": {
    "availability_target": "99.9%",
    "performance_target": "< 200ms",
    "security_target": "OWASP Top 10"
  },
  "output_format": "json | markdown | bpmn | jira | confluence"
}
```

### Output: Laporan Analisis Bisnis
```json
{
  "request_id": "uuid",
  "operation": "string",
  "requirements": [
    {
      "id": "REQ-abc123",
      "title": "string",
      "description": "string",
      "type": "functional | non_functional",
      "priority": "must_have | should_have | could_have | wont_have",
      "clarity_score": 0.85,
      "ambiguity_flags": ["string"],
      "source": "string",
      "acceptance_criteria": ["string"],
      "dependencies": ["string"]
    }
  ],
  "user_stories": [
    {
      "id": "US-abc123",
      "title": "As a Customer I want to browse products so that I can find items to purchase",
      "acceptance_criteria": ["string"],
      "story_points": "M",
      "priority": "must_have",
      "dependencies": ["string"]
    }
  ],
  "use_cases": [
    {
      "id": "UC-abc123",
      "name": "string",
      "primary_actor": "Customer",
      "preconditions": ["string"],
      "postconditions": ["string"],
      "main_scenario": ["string"],
      "alternative_scenarios": ["string"],
      "exceptions": ["string"]
    }
  ],
  "process_model": {
    "name": "string",
    "activities": [
      {"id": "act_1", "type": "task", "name": "string", "actor": "string"}
    ]
  },
  "gaps": [
    {
      "id": "GAP-abc",
      "business_need": "string",
      "current_capability": "string",
      "required_capability": "string",
      "gap_description": "string",
      "priority": "should_have",
      "estimated_effort": "string",
      "impact_if_unaddressed": "string"
    }
  ],
  "roi_result": {
    "npv": 50000.0,
    "payback_period_months": 12,
    "roi_percentage": 150.0,
    "cost_estimate": 100000.0,
    "benefit_estimate": 250000.0,
    "assumptions": ["string"]
  },
  "optimizations": [
    {
      "process_name": "string",
      "inefficiency": "string",
      "recommendation": "string",
      "estimated_savings": "40%"
    }
  ],
  "quality_score": 0.93,
  "explanation": "string — human-readable analysis summary"
}
```

---

## 4. Operasi

| Operasi | Deskripsi | Input | Output |
|-----------|-------------|--------|---------|
| `requirement_gathering` | Mengumpulkan dan menata requirement | natural_language_requirements, personas | Requirements + User Stories |
| `process_modeling` | Memodelkan alur kerja bisnis | current_state_documentation | Process Model |
| `user_story` | Menghasilkan user story | requirements, personas | User Stories |
| `use_case` | Menghasilkan use case | requirements, personas | Use Cases |
| `brd_generation` | Menghasilkan dokumen BRD | requirements, user_stories | BRD |
| `functional_spec` | Menghasilkan functional specification | requirements, user_stories, use_cases | Functional Specification |
| `gap_analysis` | Mengidentifikasi kesenjangan kemampuan | inputs, technical_constraints | Gap Items |
| `roi_analysis` | Menghitung ROI | inputs, business_context | ROI Result |
| `process_optimization` | Mengoptimalkan proses bisnis | current_state_documentation | Process Optimizations |

---

## 5. Modul Analyzer

| Modul | Tanggung Jawab |
|--------|----------------|
| `requirement_collector.py` | Mengumpulkan, menata, dan memvalidasi requirement |
| `process_modeler.py` | Memodelkan alur kerja dalam notasi mirip BPMN |
| `story_generator.py` | Menghasilkan user story yang sesuai INVEST |
| `use_case_modeler.py` | Menghasilkan use case secara rinci |
| `brd_generator.py` | Menghasilkan Business Requirements Document |
| `spec_generator.py` | Menghasilkan functional specification |
| `gap_analyzer.py` | Mengidentifikasi kesenjangan bisnis-teknis |
| `roi_calculator.py` | Menghitung ROI, NPV, payback period |
| `optimizer.py` | Mengidentifikasi inefisiensi proses |

---

## 6. Dimensi Benchmark

| Dimensi | Target | Grade |
|-----------|--------|-------|
| Requirement Clarity | ≥90% | A |
| User Story Quality | ≥95% | A |
| Gap Analysis Coverage | ≥90% | A |
| ROI Analysis | ≥85% | A |
| Process Optimization | ≥80% | A |
| BRD Completeness | ≥95% | A |
| Stakeholder Consistency | ≥90% | A |
| Explainability | ≥95% | A+ |
| Consistency | ≥90% | A |

---

## 7. Dependensi

- **apps/base.py** — Definisi model dasar
- **apps/business_analyst/schemas.py** — Kontrak publik
- **apps/business_analyst/engine.py** — Domain engine
- **apps/business_analyst/worker.py** — Adaptor tipis (ADR-003)

---

## 8. Contoh Penggunaan

```python
from apps.business_analyst.engine import BusinessAnalystEngine
from apps.business_analyst.schemas import BusinessAnalysisRequest, OperationType

engine = BusinessAnalystEngine()
request = BusinessAnalysisRequest(
    operation=OperationType.requirement_gathering,
    business_context={"domain": "e-commerce", "project_name": "Online Shop"},
    inputs={"natural_language_requirements": ["Users must be able to create accounts"]},
)
report = engine.analyze(request)
print(f"Generated {len(report.requirements)} requirements")
print(f"Quality score: {report.quality_score:.0%}")
```

