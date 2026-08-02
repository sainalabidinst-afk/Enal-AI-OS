<!-- BILINGUAL_DOCS_START -->
## Bahasa Indonesia / English

### Ringkasan / Summary
Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.
> Terjemahan Indonesia: Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.

- Bahasa Indonesia: isi utama dokumen disajikan dalam versi Indonesia di bawah konten asli.
- English: the main prose content is presented in an Indonesian bilingual section below the original content.

### Informasi Dokumen / Document Info
- File: `docs/capabilities/business-analyst.md`
- Judul: Business Analyst
- Status: bilingual content applied

<!-- BILINGUAL_DOCS_END -->

# Business Analyst Capability Specification

## Version: 1.0.0
## Status: Production Ready (RFC-0013)
## Quality Target: A- (≥85)

---

## 1. Purpose

Business Analyst adalah **otoritas analisis bisnis** untuk ECP — Capability Pack yang
menerjemahkan kebutuhan bisnis menjadi spesifikasi teknis yang jelas, terstruktur,
dan dapat dieksekusi oleh pack lain.
> Terjemahan Indonesia: Business Analyst adalah otoritas analisis bisnis untuk ECP — kapabilitas Pack yang menerjemahkan kebutuhan bisnis menjadi spesifikasi teknis yang jelas, terstruktur, dan dapat dieksekusi oleh pack lain.

Capability Pack ini mengumpulkan requirements, memodelkan proses bisnis, menghasilkan
user story, use case, BRD, functional spec, gap analysis, ROI analysis, dan
rekomendasi optimasi proses — **tanpa memodifikasi Core**.
> Terjemahan Indonesia: Kapabilitas Pack ini mengumpulkan requirements, memodelkan proses bisnis, menghasilkan user story, use case, BRD, functional spec, gap analysis, ROI analysis, dan rekomendasi optimasi proses — tanpa memodifikasi Core.

---

## 2. Scope

### In Scope
- **Requirement Gathering** — Kumpulkan, struktur, dan validasi requirements
- **Business Process Modeling** — Model workflow dengan notasi BPMN-like
- **User Story Generation** — Generate user story INVEST-compliant dengan acceptance criteria
- **Use Case Modeling** — Generate use case detail dari requirements
- **BRD Generation** — Generate Business Requirement Documents
- **Functional Specification** — Generate functional spec untuk downstream packs
- **Gap Analysis** — Identifikasi gap antara kebutuhan bisnis dan kemampuan teknis
- **ROI Analysis** — Analisis return-on-investment (NPV, payback period)
- **Process Optimization** — Identifikasi dan rekomendasikan perbaikan proses
- **Experience Memory** — Perekaman hasil ke history

### Out of Scope
- Fasilitasi stakeholder meeting
- Manajemen proyek atau alokasi sumber daya
- Definisi strategi bisnis
- Perencanaan finansial di luar ROI analysis
- Implementasi change management
- Eksekusi atau monitoring proses live
- Modifikasi Core contracts

---

## 3. Contract

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

### Output: BusinessAnalysisReport
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

## 4. Operations

| Operation | Description | Inputs | Outputs |
|-----------|-------------|--------|---------|
| requirement_gathering | Collect and structure requirements | natural_language_requirements, personas | Requirements + UserStories |
| process_modeling | Model business workflows | current_state_documentation | ProcessModel |
| user_story | Generate user stories | requirements, personas | UserStories |
| use_case | Generate use cases | requirements, personas | UseCases |
| brd_generation | Generate BRD document | requirements, user_stories | Markdown BRD |
| functional_spec | Generate functional specification | requirements, user_stories, use_cases | FunctionalSpec |
| gap_analysis | Identify capability gaps | inputs, technical_constraints | GapItems |
| roi_analysis | Calculate ROI | inputs, business_context | ROIResult |
| process_optimization | Optimize business processes | current_state_documentation | ProcessOptimizations |

---

## 5. Analyzer Modules

| Module | Responsibility |
|--------|----------------|
| requirement_gatherer.py | Collect, structure, validate requirements |
| process_modeler.py | Model workflows in BPMN-like notation |
| story_generator.py | Generate INVEST-compliant user stories |
| use_case_modeler.py | Generate detailed use cases |
| brd_generator.py | Generate Business Requirement Documents |
| spec_generator.py | Generate functional specifications |
| gap_analyzer.py | Identify business-technical gaps |
| roi_calculator.py | Calculate ROI, NPV, payback period |
| optimizer.py | Identify process inefficiencies |

---

## 6. Benchmark Dimensions

| Dimension | Target | Grade |
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

## 7. Dependencies

- **apps/base.py** — Base model definitions
- **apps/business_analyst/schemas.py** — Public contracts
- **apps/business_analyst/engine.py** — Domain Engine
- **apps/business_analyst/worker.py** — Thin adapter (ADR-003)

---

## 8. Usage Example

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
