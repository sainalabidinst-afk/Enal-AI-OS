# Self Development — Spesifikasi Capability

**Versi:** 2.1.0
**Status:** Bersertifikat (RFC-0022)
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

## 11. Growth Engine (Personal Growth)

Growth Engine mengubah pack ini dari "dokumentasi aktivitas" menjadi **engine pertumbuhan
pribadi**: analitik, goal alignment, rekomendasi, habit tracking, dan integrasi lintas pack.

### 11.1 Modul

| Modul | File | Tanggung Jawab |
|-------|------|----------------|
| Learning Analytics | `apps/self_development/learning_analytics.py` | Progres belajar, skill level, bucket per minggu/bulan, grafik konsol |
| Goal Aligner | `apps/self_development/goal_aligner.py` | Mengaitkan aktivitas ke goal jangka panjang + validasi relevansi |
| Recommendation Engine | `apps/self_development/recommendation_engine.py` | Rekomendasi project/skill berikutnya dari skill ladder, goal gap, dan Knowledge |
| Habit Tracker | `apps/self_development/habit_tracker.py` | Check-in harian/mingguan, streak counter, reminder, alert |
| Cross-Pack Bridge | `apps/self_development/cross_pack_bridge.py` | Menjalankan project nyata lewat pack lain dan menghitungnya sebagai progres |
| Growth Repository | `apps/self_development/growth_repository.py` | Persisted store untuk aktivitas, goal, dan habit |

### 11.2 Kontrak Pertumbuhan

```json
POST /api/v1/self-development/activities
{
  "title": "Bangun ETL pipeline",
  "kind": "project",
  "duration_minutes": 120,
  "skills": ["python", "etl"],
  "goal_id": "gdev-xxxxxxxx"
}
```

```json
POST /api/v1/self-development/goals
{
  "title": "Sertifikasi Data Engineer",
  "kind": "certification",
  "target_skills": ["python", "sql", "etl"],
  "success_criteria": ["Lulus ujian sertifikasi"],
  "target_date": "2026-12-31"
}
```

### 11.3 Endpoint

| Method | Path | Fungsi |
|--------|------|--------|
| GET | `/api/v1/self-development/report` | Laporan gabungan: progress, goals, habits, rekomendasi |
| GET | `/api/v1/self-development/progress` | Snapshot analitik (`granularity=week\|month`) |
| GET | `/api/v1/self-development/progress/chart` | Grafik ASCII + `series` untuk chart frontend |
| POST | `/api/v1/self-development/activities` | Catat aktivitas belajar |
| GET | `/api/v1/self-development/activities` | Daftar aktivitas (filter kind/skill/goal) |
| GET/POST | `/api/v1/self-development/goals` | Goal jangka panjang + progres coverage |
| POST | `/api/v1/self-development/goals/validate` | Validasi relevansi aktivitas → goal |
| POST | `/api/v1/self-development/goals/align` | Re-align seluruh aktivitas |
| GET | `/api/v1/self-development/recommendations` | Rekomendasi project/skill berikutnya |
| GET/POST | `/api/v1/self-development/habits` | Habit + streak counter |
| POST | `/api/v1/self-development/habits/{id}/check-in` | Check-in habit |
| GET | `/api/v1/self-development/habits/reminders` | Reminder habit yang belum terpenuhi |
| POST | `/api/v1/self-development/alerts/dispatch` | Evaluasi + publish alert ke event bus |
| GET | `/api/v1/self-development/learning-projects` | Katalog project lintas pack |
| POST | `/api/v1/self-development/learning-projects/{id}/run` | Jalankan project via pack tujuan |

### 11.4 Goal Alignment

Skoring menggabungkan cakupan skill target (65%) dan overlap kata kunci dengan judul goal
plus success criteria (35%):

| Skor | Verdict | Arti |
|------|---------|------|
| ≥ 0.60 | `aligned` | Aktivitas selaras penuh dengan goal |
| ≥ 0.30 | `partial` | Relevan sebagian, perlu ditambah skill |
| < 0.30 | `unrelated` | Goal drift — memicu alert |

Goal dapat bersumber dari Growth Repository (sertifikasi, portfolio, milestone karier) atau
dicerminkan dari **Goal Management** core (`backend/app/core/goal_engine.py`) melalui
`core_goal_id`.

### 11.5 Habit & Alert Pipeline

Streak dihitung per periode (hari ISO atau minggu ISO) dan hanya menghitung periode
berurutan yang berakhir pada periode berjalan. Reminder dievaluasi dari dua aturan:

- `habit_reminder` — target periode belum terpenuhi (severity `critical` untuk harian).
- `goal_drift` — aktivitas terbaru tidak selaras dengan goal mana pun.

Alert dipublish ke stable event bus pada event type
`self_development.habit.reminder`, `self_development.habit.streak`, dan
`self_development.goal.drift`.

### 11.6 Cross-Pack Learning Projects

| Project id | Pack | Skill yang didapat |
|------------|------|--------------------|
| `trading-backtest` | trading-analyst | statistics, backtesting, risk-management |
| `architecture-review` | system-architect | clean-architecture, ddd, architecture-review |
| `knowledge-graph` | knowledge-engineer | knowledge-graph, ontology, data-modeling |
| `research-digest` | research-assistant | research, evidence-evaluation |
| `data-pipeline-etl` | data-engineer | data-engineering, etl, data-quality |

Setiap project mendelegasikan ke engine pack tujuan (import lazy, tanpa duplikasi logika),
lalu aktivitas tetap dihitung sebagai progres dan divalidasi terhadap goal.

### 11.7 Observability

Setiap pencatatan aktivitas, check-in, dan eksekusi project mempublish gauge ke RFC-0001
`MetricsCollector`: `self_development.activities`, `.projects`, `.hours`, `.skills`,
`.alignment_rate`. Panel **Learning progress** pada console observability
(`/console/observability`) menampilkan hours, projects, skill level, dan grafik
mingguan/bulanan.

### 11.8 Penyimpanan

State runtime disimpan pada `apps/self_development/growth.json` (diabaikan oleh git).
Endpoint dan API tests memakai `GrowthRepository` dengan `tmp_path`, sehingga store
produksi tidak tersentuh oleh pengujian.

---

## 12. Riwayat Perubahan

| Versi | Tanggal | Perubahan |
|-------|---------|-----------|
| 2.1.0 | 2026-10-04 | Growth Engine: learning analytics, goal alignment, recommendation, habit tracking, cross-pack learning projects, 15 endpoint baru |
| 2.0.0 | 2026-08-05 | Level 4 Domain Expert, A+ grade, 10 golden tests, security audit, performance optimization |
