# Spesifikasi Capability Pack Full Stack Engineer

**Versi:** 1.0.0
**Status:** Production Ready (RFC-0019)
**Target Kualitas:** A- (≥85)

---

## 1. Tujuan

Full Stack Engineer adalah **otoritas rekayasa perangkat lunak** untuk ECP — Capability Pack yang menyediakan analisis rekayasa full-stack komprehensif: architecture review, code review, refactoring planning, test engineering, performance analysis, dan release engineering.

Capability Pack ini menganalisis repositori, source code, dan changes untuk menghasilkan laporan rekayasa yang actionable — **tanpa memodifikasi Core**.

---

## 2. Ruang Lingkup

### Dalam Ruang Lingkup
- **F1 Architecture Review** — Membaca repositori dan memeriksa layer violations, dependency density, modularity, tech debt
- **F2 Code Review** — Menganalisis AST dan teks kode untuk masalah security, concurrency, reliability, maintainability
- **F3 Refactoring Planner** — Merencanakan refactoring tanpa penerapan otomatis (Problem → Cause → Proposal → Benefit → Risk → Steps)
- **F4 Test Engineer** — Menganalisis direktori source dan test, memperkirakan coverage, menghasilkan test plans
- **F5 Performance Engineer** — Mendeteksi N+1 queries, blocking I/O, masalah memori, algoritma tidak efisien
- **F6 Release Engineer** — Memvalidasi changelog, semantic versioning, migrasi, rollback plan, deployment checklist
- **Experience Memory** — Merekam hasil ke riwayat

### Di Luar Cakupan
- Perbaikan kode otomatis tanpa persetujuan
- Eksekusi deployment cloud-native
- Analisis bundle frontend dari aset terkompilasi
- Manajemen proyek
- Modifikasi kontrak Core

---

## 3. Kontrak

### Input: FullStackRequest

```json
{
  "request_id": "uuid",
  "operation": "architecture_review | code_review | refactoring_plan | test_engineering | performance_analysis | release_review | full_stack_review",
  "inputs": {
    "repo_path": "string — path to repository",
    "source_code": "string — source code content",
    "filename": "string — source file name",
    "source_path": "string — path to source directory",
    "module_path": "string — module path for test engineering",
    "changes": [{"type": "string", "content": "string", "filename": "string"}]
  },
  "context": {
    "project_id": "string",
    "language": "python|javascript|typescript",
    "framework": "django|fastapi|react|vue|etc"
  },
  "quality_attributes": {
    "architecture_target": "clean_architecture|ddd|microservices|modular_monolith",
    "coverage_target": 0.85,
    "performance_target": {"latency_p95_ms": 100, "throughput_rps": 1000}
  },
  "output_format": "json | markdown"
}
```

### Output: Laporan Rekayasa Full Stack

```json
{
  "request_id": "uuid",
  "operation": "string",
  "architecture_review": {
    "architecture_score": 0.85,
    "layering_grade": "A|B+|B|C|D|F",
    "dependency_grade": "A|B+|B|C|D|F",
    "modularity_grade": "A|B+|B|C|D|F",
    "tech_debt_grade": "A|B+|B|C|D|F",
    "issues": [
      {
        "id": "string",
        "severity": "low|medium|high|critical",
        "category": "string",
        "description": "string",
        "location": "string",
        "recommendation": "string"
      }
    ]
  },
  "code_review": {
    "findings": [
      {
        "severity": "string",
        "category": "security|concurrency|reliability|maintainability",
        "title": "string",
        "description": "string",
        "recommendation": "string",
        "evidence": "string",
        "line_number": 0,
        "confidence": 0.95,
        "cwe": "CWE-xxx"
      }
    ],
    "summary": {
      "total_findings": 0,
      "by_severity": {"critical": 0, "high": 0, "medium": 0, "low": 0, "info": 0},
      "by_category": {}
    }
  },
  "refactoring_plan": {
    "plans": [
      {
        "id": "string",
        "problem": "string",
        "cause": "string",
        "proposal": "string",
        "expected_benefit": "string",
        "risk": "low|medium|high",
        "migration_steps": ["string"],
        "estimated_effort": "string"
      }
    ]
  },
  "test_engineering": {
    "coverage_adequate": true,
    "estimated_coverage": 0.85,
    "missing_tests": ["string"],
    "plans": [
      {
        "test_type": "unit|integration|contract|performance|regression",
        "description": "string",
        "suggested_tests": ["string"],
        "priority": "low|medium|high|critical",
        "estimated_coverage": 0.85
      }
    ]
  },
  "performance_analysis": {
    "issues": [
      {
        "id": "string",
        "severity": "low|medium|high|critical",
        "category": "n_plus_1|blocking_io|memory|algorithm|database",
        "description": "string",
        "location": "string",
        "recommendation": "string",
        "estimated_improvement": "string"
      }
    ],
    "summary": {
      "total_issues": 0,
      "critical_issues": 0,
      "estimated_speedup": "string"
    }
  },
  "release_review": {
    "ready": true,
    "checks": [
      {
        "check": "string",
        "passed": true,
        "details": "string",
        "severity": "low|medium|high|critical"
      }
    ],
    "blockers": ["string"],
    "summary": {
      "total_checks": 0,
      "passed_checks": 0,
      "failed_checks": 0,
      "release_readiness": "ready|not_ready|conditional"
    }
  },
  "quality_score": 0.85,
  "explanation": "string — human-readable review summary"
}
```

---

## 4. Operasi

| Operasi | Deskripsi | Input | Output |
|-----------|-------------|--------|---------|
| `architecture_review` | Meninjau arsitektur repositori | repo_path | ArchitectureReport |
| `code_review` | Meninjau kode untuk masalah | source_code, filename | CodeReviewReport |
| `refactoring_plan` | Merencanakan refactoring | source_code, filename | RefactoringPlan |
| `test_engineering` | Rekayasa testing | source_path, module_path | TestEngineerReport |
| `performance_analysis` | Analisis kinerja kode | source_code, filename | PerformanceAnalysisReport |
| `release_review` | Validasi kesiapan rilis | changes, context | ReleaseReadinessReport |
| `full_stack_review` | Review full stack terpadu | repo_path | FullStackReport |

---

## 5. Modul Analyzer

| Modul | Tanggung Jawab |
|--------|----------------|
| `architecture_review.py` | F1: Architecture review dengan skor bertingkat |
| `architecture_review_engine.py` | Mesin review arsitektur |
| `code_review.py` | F2: Code review dengan AST analysis |
| `refactoring_planner.py` | F3: Refactoring planning tanpa eksekusi |
| `test_engineer.py` | F4: Test engineering dan coverage estimation |
| `performance_engineer.py` | F5: Performance analysis (N+1, blocking I/O, memory) |
| `release_engineer.py` | F6: Release readiness validation |
| `repo_engine.py` | Repository scanning dan intelligence |

---

## 6. Dimensi Benchmark

| Dimensi | Target | Grade |
|-----------|--------|-------|
| Architecture Review Accuracy | ≥90% | A |
| Code Review Precision | ≥95% | A |
| Refactoring Plan Usability | ≥85% | A- |
| Test Coverage Estimation Accuracy | ±10% | A |
| Performance Detection Recall | ≥90% | A |
| Release Readiness Precision | ≥95% | A |
| Explainability | ≥90% | A |
| Consistency | ≥85% | A- |

---

## 7. Dependensi

- **apps/base.py** — Definisi model dasar
- **apps/full_stack_engineer/schemas.py** — Kontrak publik
- **apps/full_stack_engineer/engine.py** — Domain engine
- **apps/full_stack_engineer/worker.py** — Adaptor tipis (ADR-003)
- **apps.code_engineer** — Primitif arsitektur (ArchitectureReader, DependencyGraphBuilder, dll.)

---

## 8. Contoh Penggunaan

```python
from apps.full_stack_engineer.engine import FullStackEngineerEngine
from apps.full_stack_engineer.schemas import FullStackRequest, OperationType

engine = FullStackEngineerEngine()
request = FullStackRequest(
    operation=OperationType.architecture_review,
    inputs={"repo_path": "/path/to/repo"},
    context={"project_id": "my-project", "language": "python"},
)
report = engine.review(request)
print(f"Architecture score: {report.architecture_review.architecture_score:.0%}")
print(f"Findings: {len(report.code_review.findings)} code issues")
print(f"Refactoring plans: {len(report.refactoring_plan.plans)}")
```
