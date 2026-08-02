# Spesifikasi Capability Pack Full Stack Engineer

<!-- DOCUMENT_METADATA_START -->
**Pemilik:** Tim Dokumentasi
**Pemilik Canonical:** Pimpinan Tata Kelola Dokumentasi
**Terakhir Diverifikasi:** 2026-08-02
**Versi:** 1.0.0
**Status:** Aktif
**SSOT:** Spesifikasi Capability Pack untuk full-stack-engineer
<!-- DOCUMENT_METADATA_END -->

## Versi: 1.0.0
## Status: Draf (v1.0 siap diterapkan)

---

## 1. Tujuan

Menyediakan rekayasa full-stack capabilities untuk:
- Architecture review dan penilaian
- Code review melampaui linting
- Perencanaan refactoring tanpa penerapan otomatis
- Rekayasa testing (unit, integration, contract, performance, regression)
- Rekayasa performance (database, frontend, algoritma)
- Rekayasa release (validasi kesiapan)

---

## 2. Ruang Lingkup

### Dalam Ruang Lingkup
- Bahasa: Python (utama), pola JS/TS (direncanakan)
- Jenis analisis: Architecture, Code Review, Refactoring, Testing, Performance, Release
- Output: Skor, Actionable Reports, Findings, Plan, Test Plans, Release Checklist

### Di Luar Ruang Lingkup
- Perbaikan kode otomatis tanpa persetujuan
- Analisis bundle frontend dari aset terkompilasi
- Eksekusi deployment cloud-native

---

## 3. Kontrak

### Input
```json
{
  "type": "repo|code|changes",
  "content": "repo path or code string",
  "filename": "string",
  "context": {}
}
```

### Output
```json
{
  "architecture_review": {
    "architecture_score": "float 0-100",
    "layering_grade": "A|B+|B|C|D|F",
    "dependency_grade": "A|B+|B|C|D|F",
    "modularity_grade": "A|B+|B|C|D|F",
    "tech_debt_grade": "A|B+|B|C|D|F",
    "issues": []
  },
  "code_review": {
    "findings": [],
    "summary": {}
  },
  "refactoring_plan": {
    "plans": []
  },
  "test_engineering": {
    "coverage_adequate": "boolean",
    "plans": []
  },
  "performance_analysis": {
    "issues": []
  },
  "release_review": {
    "ready": "boolean",
    "checks": []
  }
}
```

---

## 4. Kemampuan Detail

### F1 - Architecture Review
- Membaca repositori menggunakan ArchitectureReader
- Memeriksa layer violations, density, dependencies, modularity, tech debt
- Menghasilkan skor bertingkat (A–F) dan Architecture Score (0–100)

### F2 - Code Review
- Mem-parsing AST dan menganalisis teks code untuk masalah security, concurrency, resource, maintainability, dan API
- Setiap finding mencakup evidence, line number, CWE, confidence, dan prioritas
- Kategori: Security, Concurrency, Reliability, Maintainability

### F3 - Refactoring Planner
- TIDAK mengubah kode
- Plan disusun: Problem → Cause → Proposal → Expected Benefit → Risk → Migration Steps
- Mendeteksi mutable defaults, fungsi panjang, import density tinggi

### F4 - Test Engineer
- Menganalisis direktori source dan test
- Memperkirakan coverage
- Menghasilkan test plans untuk unit, integration, contract, performance, dan regression testing

### F5 - Performance Engineer
- Mendeteksi N+1 queries, loop penempatan, blocking I/O, masalah memori
- Area fokus: database, algoritma, memori, I/O

### F6 - Release Engineer
- Memvalidasi changelog, semantic versioning, migrasi, rollback plan, deployment checklist, post-deployment verification
- Menghasilkan boolean `ready` dan hasil pemeriksaan terperinci

---

## 5. Persyaratan Benchmark

| Metrik | Target | Kriteria Lulus |
|--------|--------|---------------|
| Architecture Review Accuracy | ≥90% | Deteksi Layering/Tech Debt yang benar |
| Code Review Precision | ≥95% | False positive ≤5% |
| Refactoring Plan Usability | ≥85% | Plan yang dapat ditindaklanjuti dengan langkah-langkah |
| Test Coverage Estimation Accuracy | ±10% | Dalam 10% dari coverage sebenarnya |
| Performance Detection Recall | ≥90% | True positive ≥90% |
| Release Readiness Precision | ≥95% | Penilaian ready/fail yang benar |

---

## 6. Integrasi

- Terdaftar sebagai `full-stack-engineer` di `apps/__init__.py`
- Worker: `FullStackWorker` di `apps/society/workers/full_stack_worker.py`
- Entri capability graph di `apps/organization/capability_graph.py` pada domain `full-stack`
- Template subtask ditentukan untuk setiap capability F1–F6
- Menggunakan kembali primitif `apps.code_engineer` (ArchitectureReader, DependencyGraphBuilder, ImpactAnalyzer, RefactoringEngine, PatchGenerator, RegressionAnalyzer, TestGenerator)

---

## 7. Peta Jalan

| Capability | Status |
|------------|--------|
| F1 - Architecture Review | ✅ Implemented |
| F2 - Code Review | ✅ Implemented |
| F3 - Refactoring Planner | ✅ Implemented |
| F4 - Test Engineer | ✅ Implemented |
| F5 - Performance Engineer | ✅ Implemented |
| F6 - Release Engineer | ✅ Implemented |

---

## 8. Peningkatan di Masa Depan

- Parsing AST JS/TS melalui `tree-sitter` atau `esprima`
- Analisis bundle melalui statistik webpack/rollup
- Analisis query plan berbasis data melalui EXPLAIN
- Review yang sadar diff untuk perubahan PR/MR
- Integrasi dengan CI/CD untuk pemeriksaan rilis otomatis

