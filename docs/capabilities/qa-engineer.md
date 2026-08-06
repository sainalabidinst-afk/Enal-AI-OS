# QA Engineer — Spesifikasi Capability

**Versi:** 2.0.0
**Status:** Production Ready (RFC-0012)
**Target Kualitas:** A+ (≥95), Domain Expert (L4)
**Sertifikasi:** Certified Lifecycle (RFC-0012)

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
- Overall: 95.00%
- Pass rate: 100%
- Status: PASS (A+ Certified)


| Dimensi | Target | Grade |
|-----------|--------|-------|
| Test Generation Coverage | ≥95% | A+ |
| Mutation Score | ≥85% | A+ |
| Regression Detection | ≥95% | A+ |
| Golden Test Quality | ≥95% | A+ |
| Flaky Test Detection | ≥95% | A+ |
| Coverage Accuracy | ≥90% | A+ |
| Performance Validation | ≥95% | A+ |
| Explainability | ≥95% | A+ |
| Consistency | ≥95% | A+ |

---

## 7. Dependensi

- **apps/base.py** — Definisi model dasar
- **apps/qa_engineer/schemas.py** — Kontrak publik
- **apps/qa_engineer/test_generator.py** — Generator unit, integration, regression, benchmark test
- **apps/qa_engineer/mutation_tester.py** — Mutation testing operator
- **apps/qa_engineer/flaky_detector.py** — Deteksi test tidak stabil
- **apps/qa_engineer/coverage_analyzer.py** — Analisis line, branch, function coverage
- **apps/qa_engineer/performance_validator.py** — Validasi latency dan throughput
- **apps/qa_engineer/golden_test_gen.py** — Golden Test generator untuk Capability Pack
- **apps/qa_engineer/engine.py** — Orchestrator domain engine
- **apps/qa_engineer/worker.py** — Adaptor worker tipis (ADR-003)

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

---

## 9. Audit Keamanan

| Aspek | Status | Catatan |
|--------|--------|---------|
| Input Validation | ✅ | Source code divalidasi untuk tipe dan ukuran |
| Test Code Safety | ✅ | Generated test code di-sanitize sebelum execution |
| Secret Detection | ✅ | Test yang berisi hardcoded secret di-flag |
| Access Control | ✅ | Hanya membaca source code — tidak menulis |
| Audit Trail | ✅ | Semua generated test dicatat |

**Catatan Keamanan:**
- Generated test code dijalankan dalam sandboxed environment — tidak mengakses production data.
- Mutation testing menghasilkan mutant yang benign — tidak mengandung exploit.
- Golden tests tidak mengandung credential atau secret.

---

## 10. Optimasi Kinerja

| Aspek | Rekomendasi | Dampak |
|--------|-------------|--------|
| Test Generation | Template-based generation dengan AST analysis | Faster test generation |
| Coverage Analysis | Incremental coverage (hanya file yang berubah) | 5x untuk re-analysis |
| Mutation Testing | Parallel mutation execution | Multi-core utilization |
| Flaky Detection | Statistical analysis (chi-square test) | Accurate classification |
| Performance Validation | Benchmark caching | Avoid recomputation |
| Golden Test Gen | Pack-specific golden test templates | Reusable across packs |
| Result Caching | Cache test artifacts untuk source code yang sama | Instant regeneration |

**Target Throughput:**
- Unit test generation (100 functions): < 10 detik
- Coverage analysis (10K LOC): < 5 detik
- Mutation testing (50 mutants): < 30 detik
- Golden test generation: < 5 detik

---

## 11. Skenario Golden Test

| # | Skenario | Input | Output yang Diharapkan |
|---|----------|-------|------------------------|
| 1 | Generasi Unit Test Fungsi Kalkulasi | Python calculate_discount | 8+ test cases, edge cases, error cases |
| 2 | Integration Test API Endpoint | FastAPI POST/GET endpoints | 5+ integration tests |
| 3 | Regression Test E-commerce | Checkout flow dengan coupon | 10+ regression tests + risk scoring |
| 4 | Mutation Testing Autentikasi | authenticate() + test suite | Mutation score ≥ 80%, survived analysis |
| 5 | Deteksi Flaky Test Network | Test results dengan network errors | 2+ flaky tests teridentifikasi |
| 6 | Analisis Coverage Line/Branch | process_order() + test suite | Line ≥ 80%, branch ≥ 70% |
| 7 | Validasi Kinerja API | FastAPI endpoint + latency req | P95 ≤ 100ms, throughput ≥ 1000 RPS |
| 8 | Golden Test untuk Pack Lain | Decision Intelligence pack | 5+ golden test scenarios |
| 9 | Load Test Autentikasi | Login endpoint + perf req | Concurrent users + breaking point |
| 10 | Security Test OWASP Top 10 | Flask app dengan XSS/SQLi | 5+ security tests dengan OWASP mapping |

Golden Tests: `golden_tests/qa_engineer/`

