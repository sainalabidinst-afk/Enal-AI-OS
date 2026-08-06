# Self Development — Spesifikasi Capability

**Versi:** 2.0.0
**Status:** Bersertifikat
**Target Kualitas:** A+ (≥95) — Level 4 — Pakar Domain

---

## 1. Tujuan

Self Development adalah **otoritas pembelajaran dan perbaikan proyek** untuk ECP — Capability Pack yang menganalisis struktur proyek, mendeteksi kemacetan, mengusulkan perbaikan, dan menghasilkan patch dengan alur kerja persetujuan.

Capability Pack ini mengintegrasikan 7 modul inti (Project Scanner, Smell Taxonomy, Pattern Learner, Impact Predictor, Risk Modeler, Suggestion Generator, Approval Manager) melalui pipeline pembelajaran terstruktur — **tanpa memodifikasi Core**.

---

## 2. Ruang Lingkup

### Dalam Ruang Lingkup
- **Project Analysis** — Analisis struktur proyek dan hotspots
- **Code Smell Detection** — Deteksi long method, god class, duplicate code, dll
- **Bottleneck Detection** — Deteksi kemacetan arsitektur dan performa
- **Dead Code Detection** — Identifikasi kode mati dan unreachable code
- **Refactoring Proposal** — Usulan perbaikan dengan estimasi dampak
- **Patch Generation** — Pembuatan patch dengan rollback plan
- **Test Generation** — Pembuatan laporan tes untuk patch
- **Approval Workflow** — Alur kerja persetujuan untuk perubahan
- **Cross-Project Learning** — Pembelajaran pola lintas proyek
- **Impact Prediction** — Prediksi blast radius perubahan
- **Risk Modeling** — Kuantifikasi risiko perubahan
- **Forecasting** — Prediksi tren kemacetan

### Di Luar Cakupan
- Eksekusi kode otonom tanpa persetujuan
- Modifikasi langsung kontrak Core
- Penggunaan ulang engine Capability Pack lain melalui import langsung
- Deployment produksi tanpa persetujuan eksplisit pengguna

---

## 3. Kontrak

### Input: SelfDevelopmentRequest
```json
{
  "task": "analyze | identify_problems | propose_solution | generate_patch | generate_tests | learn_patterns | forecast_trends | assess_risk",
  "project_path": "string",
  "target_file": "string (optional)",
  "change_description": "string (optional)",
  "options": {
    "include_dead_code": true,
    "include_complexity": true,
    "max_suggestions": 10,
    "approval_required": true
  }
}
```

### Output: SelfDevelopmentReport
```json
{
  "task": "string",
  "project_path": "string",
  "analysis": {
    "total_files": 50,
    "total_lines": 10000,
    "issues_found": 10,
    "categories": ["long_method", "duplicate_code", "god_class"],
    "complexity_metrics": {
      "cyclomatic_complexity_avg": 8.5,
      "max_cyclomatic_complexity": 25
    }
  },
  "problems": [
    {
      "id": "uuid",
      "type": "string",
      "severity": "critical | high | medium | low",
      "location": "string",
      "description": "string",
      "impact": "string",
      "confidence": 0.9,
      "evidence": ["string"]
    }
  ],
  "solutions": [
    {
      "problem_id": "uuid",
      "solution_type": "refactor | restructure | optimize | security_hardening | testing | documentation",
      "description": "string",
      "estimated_effort": "low | medium | high",
      "risk": "low | medium | high",
      "confidence": 0.85
    }
  ],
  "patch": {
    "patch_id": "uuid",
    "diff": "unified diff",
    "is_valid": true,
    "rollback_plan": "string"
  },
  "approval": {
    "state": "pending | approved | rejected",
    "required_approvers": ["tech_lead"],
    "auto_approve_eligible": false
  }
}
```

---

## 4. Operasi

| Operasi | Deskripsi | Input | Output |
|-----------|-------------|--------|---------|
| `analyze` | Analisis lengkap proyek | project_path, options | ProjectAnalysis |
| `identify_problems` | Identifikasi masalah (code smells, bottlenecks) | project_path, options | List[Problem] |
| `propose_solution` | Usulkan solusi untuk masalah | problem_id, options | Solution |
| `generate_patch` | Generate patch untuk solusi | solution_id, options | PatchBundle |
| `generate_tests` | Generate laporan tes untuk patch | patch_id, options | TestReport |
| `learn_patterns` | Belajar pola lintas proyek | projects[], focus | PatternReport |
| `forecast_trends` | Prediksi tren kemacetan | project_path, history | ForecastReport |
| `assess_risk` | Model risiko perubahan | project_path, change_description | RiskAssessment |

---

## 5. Modul Analyzer

| Modul | File | Tanggung Jawab |
|-------|------|----------------|
| `project_scanner.py` | ProjectScanner | Scan struktur proyek, deteksi hotspots |
| `smell_taxonomy.py` | SmellTaxonomy | Kategorisasi masalah (code smells, bottlenecks) |
| `pattern_learner.py` | PatternLearner | Belajar pola lintas proyek |
| `impact_predictor.py` | ImpactPredictor | Prediksi blast radius perubahan |
| `risk_modeler.py` | RiskModeler | Model risiko kuantitatif |
| `suggestion_generator.py` | SuggestionGenerator | Saran perbaikan berprioritas |
| `approval_manager.py` | ApprovalManager | Alur kerja persetujuan |
| `schemas.py` | Schemas | Kontrak typed (Problem, Solution, Patch, dll) |

---

## 6. Dimensi Benchmark

| Dimensi | Target | Grade |
|-----------|--------|-------|
| Problem Detection Accuracy | ≥95% | A+ |
| Solution Relevance | ≥95% | A+ |
| Patch Validity | ≥95% | A+ |
| Test Coverage Estimate | ≥90% | A |
| Approval Workflow Compliance | ≥95% | A+ |
| Pattern Learning Quality | ≥90% | A |
| Risk Model Accuracy | ≥90% | A |
| Consistency | ≥95% | A+ |

---

## 7. Dependensi

- **apps/base.py** — Definisi model dasar
- **apps/self_development/schemas.py** — Kontrak publik
- **apps/self_development/engine.py** — Domain engine
- **apps/self_development/worker.py** — Adaptor tipis (ADR-003)

---

## 8. Contoh Penggunaan

```python
from apps.self_development.engine import SelfDevelopmentEngine

engine = SelfDevelopmentEngine()
analysis = await engine.analyze_project("/path/to/project")
problems = await engine.identify_problems("/path/to/project")
solution = await engine.propose_solution(problems[0].id)
patch = await engine.generate_patch(solution.id)
tests = await engine.generate_tests(patch.id)
```

---

## 9. Audit Keamanan

### OWASP Top 10
- A03: Injection: Patch generation dengan command injection
- A05: Security Misconfiguration: Approval bypass, weak access control
- A08: Data Integrity Failures: Patch yang tidak diverifikasi
- A09: Logging Failures: Missing audit trail untuk perubahan

### Deteksi Rahasia
- Hardcoded secrets dalam patch yang dihasilkan
- Credentials dalam diff output
- API keys dalam generated code

### Pencegahan Injeksi
- Command injection dalam patch application
- Path traversal dalam file operations
- Template injection dalam code generation

### Validasi Input
- Validasi project_path (tidak ada path traversal)
- Validasi patch content (tidak ada malicious code)
- Validasi change_description

### Default Aman
- Semua perubahan memerlukan approval
- Rollback plan dihasilkan untuk setiap patch
- Audit trail untuk semua operasi
- Fail-closed untuk approval workflow

---

## 10. Optimasi Kinerja

### Strategi Caching
- Project structure cache (hash-based)
- Smell detection cache untuk file yang tidak berubah
- Pattern learning cache untuk proyek yang sudah dianalisis

### Peluang Paralelisme
- Parallel scanning untuk banyak file/proyek
- Independent analyzers (complexity, duplication, architecture) paralel
- Test generation untuk module yang berbeda paralel

### Optimasi Memori
- Streaming scan untuk proyek besar
- Lazy loading untuk smell taxonomy
- Disk-based cache untuk large dependency graphs

### Efisiensi Token
- Context compression untuk large codebases
- Incremental analysis untuk perubahan kecil
- Selective analysis berdasarkan scope

---

## 11. Riwayat Perubahan

| Versi | Tanggal | Perubahan |
|-------|---------|-----------|
| 2.0.0 | 2026-08-05 | Level 4 Domain Expert, A+ grade, 10 golden tests, security audit, performance optimization |
