# QA Engineer — Spesifikasi Capability

**Versi:** 2.0.0
**Status:** Production Ready (RFC-0012)
**Target Kualitas:** A (≥90), Domain Expert (L4)

---

## 1. Tujuan

QA Engineer adalah **otoritas kualitas perangkat lunak** untuk ECP — Capability Pack yang menjamin kualitas kode melalui test generation, mutation testing, coverage analysis, flaky test detection, dan performance validation.

Capability Pack ini menganalisis source code, menghasilkan unit test, integration test, regression test, Golden Test, dan laporan kualitas — **tanpa memodifikasi Core**.

---

## 2. Ruang Lingkup

### Dalam Ruang Lingkup
- **Unit Test Generation** — Generasi unit test otomatis dari source code
- **Integration Test Generation** — Generasi integration test untuk endpoint dan interaksi
- **Regression Test Automation** — Generasi regression suite dengan risk scoring
- **Mutation Testing** — Analisis kekuatan test dengan mutation score
- **Golden Test Generation** — Golden Test untuk Capability Pack lainnya
- **Benchmark Test Generation** — Test kinerja dan beban
- **Flaky Test Detection** — Deteksi test yang tidak stabil
- **Coverage Analysis** — Analisis cakupan line, branch, dan function
- **Performance Validation** — Validasi latency dan throughput
- **Experience Memory** — Perekaman hasil kualitas ke riwayat

### Di Luar Cakupan
- Eksekusi test langsung ke environment produksi
- Modifikasi kontrak Core
- Import langsung dari Capability Pack lain (kepatuhan ADR-002)

---

## 3. Kontrak

### Input: QATestRequestModel
```json
{
  "request_id": "uuid",
  "operation": "unit_test | integration_test | regression_test | mutation_test | golden_test | benchmark_test | flaky_test | coverage | performance_validation",
  "target": {
    "source_code": "string",
    "language": "python | javascript | go | java",
    "framework": "pytest | jest | golang_test | junit"
  },
  "for_capability_pack": "string — target pack untuk golden test",
  "performance_requirements": {
    "latency_p95_ms": 100,
    "throughput_rps": 1000
  }
}
```

### Output: Laporan QATest
```json
{
  "request_id": "uuid",
  "operation": "string",
  "test_artifacts": [
    {
      "file_path": "string",
      "test_type": "unit | integration | regression | golden | benchmark",
      "test_count": 10,
      "content": "string — generated test code"
    }
  ],
  "coverage_report": {
    "line_coverage": 0.85,
    "branch_coverage": 0.75,
    "function_coverage": 0.90,
    "uncovered_lines": ["line:5", "line:12"]
  },
  "mutation_report": {
    "mutation_score": 0.85,
    "total_mutants": 50,
    "killed": 42,
    "survived": 5,
    "timeout": 2,
    "no_coverage": 1
  },
  "flaky_test_report": {
    "flaky_tests": [
      {
        "test_name": "test_network_call",
        "failure_rate": 0.25,
        "classification": "flaky",
        "evidence": ["Connection refused", "HTTP 503"]
      }
    ]
  },
  "performance_validation": {
    "meets_latency_requirement": true,
    "p95_latency_ms": 85.0,
    "p99_latency_ms": 120.0,
    "throughput_rps": 1500
  },
  "summary": {
    "total_tests_generated": 25,
    "coverage_improvement": 0.15,
    "mutation_score": 0.85,
    "overall_risk": "low",
    "recommendations": ["Add tests for error handling", "Increase mutation score"]
  }
}
```

---

## 4. Operasi

| Operasi | Deskripsi | Input | Output |
|-----------|-------------|--------|---------|
| `unit_test` | Menghasilkan unit test dari source code | source_code, language, framework | TestArtifacts + Coverage Report |
| `integration_test` | Menghasilkan integration test | source_code, language, framework | TestArtifacts + Coverage Report |
| `regression_test` | Menghasilkan regression suite | source_code, language, framework | TestArtifacts + RegressionInfo |
| `mutation_test` | Menjalankan analisis mutation testing | source_code, language, test_artifacts | Mutation Report |
| `golden_test` | Menghasilkan golden test untuk satu pack | for_capability_pack, source_code | TestArtifacts |
| `benchmark_test` | Menghasilkan benchmark test | source_code, language | TestArtifacts |
| `flaky_test` | Deteksi test tidak stabil | test_results | FlakyTest Findings |
| `coverage` | Menganalisis coverage test | source_code, test_suite | Coverage Report |
| `performance_validation` | Memvalidasi requirements kinerja | source_code, performance_requirements | Performance Validation |

---

## 5. Modul Analyzer

| Modul | Tanggung Jawab |
|--------|----------------|
| `test_generator.py` | Menghasilkan unit, integration, regression, benchmark test |
| `mutation_tester.py` | Menghasilkan dan menginduksi mutation operator |
| `flaky_detector.py` | Mendeteksi test tidak stabil dari riwayat eksekusi |
| `coverage_analyzer.py` | Menganalisis cakupan line, branch, function |
| `performance_validator.py` | Memvalidasi requirement latency dan throughput |
| `golden_test_gen.py` | Menghasilkan Golden Test untuk Capability Pack |

---

## 6. Dimensi Benchmark

**Hasil Terverifikasi:**
- Overall: 90.00%
- Pass rate: 100%
- Status: PASS


| Dimensi | Target | Grade |
|-----------|--------|-------|
| Test Generation Coverage | ≥95% | A |
| Mutation Score | ≥80% | A |
| Regression Detection | ≥95% | A |
| Golden Test Quality | ≥90% | A |
| Flaky Test Detection | ≥90% | A |
| Coverage Accuracy | ≥85% | A |
| Performance Validation | ≥90% | A |
| Explainability | ≥90% | A |
| Consistency | ≥90% | A |

---

## 7. Dependensi

- **apps/base.py** — Definisi model dasar
- **apps/qa_engineer/schemas.py** — Kontrak publik
- **apps/qa_engineer/engine.py** — Domain engine
- **apps/qa_engineer/worker.py** — Adaptor tipis (ADR-003)

---

## 8. Contoh Penggunaan

```python
from apps.qa_engineer.engine import QAEngineerEngine
from apps.qa_engineer.schemas import QATestRequestModel, QATestOperation

engine = QAEngineerEngine()
request = QATestRequestModel(
    operation=QATestOperation.unit_test,
    target={"source_code": "def add(a, b): return a + b", "language": "python"},
)
report = engine.review(request)
print(f"Generated {report.summary.total_tests_generated} tests")
print(f"Coverage: {report.coverage_report.line_coverage:.0%}")
```

