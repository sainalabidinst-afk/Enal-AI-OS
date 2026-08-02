<!-- BILINGUAL_DOCS_START -->
## Bahasa Indonesia / English

### Ringkasan / Summary
Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.
> Terjemahan Indonesia: Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.

- Bahasa Indonesia: isi utama dokumen disajikan dalam versi Indonesia di bawah konten asli.
- English: the main prose content is presented in an Indonesian bilingual section below the original content.

### Informasi Dokumen / Document Info
- File: `docs/capabilities/qa-engineer.md`
- Judul: Qa Engineer
- Status: bilingual content applied

<!-- BILINGUAL_DOCS_END -->

# QA Engineer Capability Specification

## Version: 1.0.0
## Status: Production Ready (RFC-0012)
## Quality Target: A (≥90)

---

## 1. Purpose

QA Engineer adalah **otoritas kualitas perangkat lunak** untuk ECP — Capability Pack yang
menjamin kualitas kode melalui generasi test, mutation testing, coverage analysis,
flaky detection, dan validasi performa.
> Terjemahan Indonesia: QA Engineer adalah otoritas kualitas perangkat lunak untuk ECP — kapabilitas Pack yang menjamin kualitas kode melalui generasi test, mutation testing, coverage analysis, flaky detection, dan validasi performa.

Capability Pack ini menganalisis kode sumber, menghasilkan unit test, integration test,
regression test, golden test, dan laporan kualitas — **tanpa memodifikasi Core**.
> Terjemahan Indonesia: Kapabilitas Pack ini menganalisis kode sumber, menghasilkan unit test, integrasi test, regression test, golden test, dan laporan kualitas — tanpa memodifikasi Core.

---

## 2. Scope

### In Scope
- **Unit Test Generation** — Generasi test unit otomatis dari kode sumber
- **Integration Test Generation** — Generasi test integrasi untuk endpoints dan interaksi
- **Regression Test Automation** — Generasi suite regresi dengan risk assessment
- **Mutation Testing** — Analisis kekuatan test dengan mutation score
- **Golden Test Generation** — Test golden untuk Capability Pack lain
- **Benchmark Test Generation** — Test performa dan beban
- **Flaky Test Detection** — Deteksi test yang tidak stabil
- **Coverage Analysis** — Analisis line, branch, dan function coverage
- **Performance Validation** — Validasi latency dan throughput
- **Experience Memory** — Perekaman hasil kualitas ke history

### Out of Scope
- Eksekusi test langsung ke environment produksi
- Modifikasi Core contracts
- Direct import dari Capability Pack lain (ADR-002 compliance)

---

## 3. Contract

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

### Output: QATestReport
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

## 4. Operations

| Operation | Description | Inputs | Outputs |
|-----------|-------------|--------|---------|
| unit_test | Generate unit tests from source code | source_code, language, framework | TestArtifacts + CoverageReport |
| integration_test | Generate integration tests | source_code, language, framework | TestArtifacts + CoverageReport |
| regression_test | Generate regression test suite | source_code, language, framework | TestArtifacts + RegressionInfo |
| mutation_test | Run mutation testing analysis | source_code, language, test_artifacts | MutationReport |
| golden_test | Generate golden tests for a pack | target_pack, source_code | TestArtifacts |
| benchmark_test | Generate benchmark tests | source_code, language | TestArtifacts |
| flaky_test | Detect flaky tests | test_results | FlakyTestFindings |
| coverage | Analyze test coverage | source_code, test_suite | CoverageReport |
| performance_validation | Validate performance requirements | source_code, perf_reqs | PerformanceValidation |

---

## 5. Analyzer Modules

| Module | Responsibility |
|--------|----------------|
| test_generator.py | Generate unit, integration, regression, benchmark tests |
| mutation_tester.py | Generate and evaluate mutation operators |
| flaky_detector.py | Detect flaky tests from execution history |
| coverage_analyzer.py | Analyze line, branch, function coverage |
| performance_validator.py | Validate latency and throughput requirements |
| golden_test_gen.py | Generate golden tests for Capability Packs |

---

## 6. Benchmark Dimensions

| Dimension | Target | Grade |
|-----------|--------|-------|
| Test Generation Coverage | ≥95% | A |
| Mutation Score | ≥80% | A |
| Regression Detection | ≥95% | A |
| Golden Test Gen | ≥90% | A |
| Flaky Test Detection | ≥90% | A |
| Coverage Accuracy | ≥85% | A |
| Performance Validation | ≥90% | A |
| Explainability | ≥90% | A |
| Consistency | ≥90% | A |

---

## 7. Dependencies

- **apps/base.py** — Base model definitions
- **apps/qa_engineer/schemas.py** — Public contracts
- **apps/qa_engineer/engine.py** — Domain Engine
- **apps/qa_engineer/worker.py** — Thin adapter (ADR-003)

---

## 8. Usage Example

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
