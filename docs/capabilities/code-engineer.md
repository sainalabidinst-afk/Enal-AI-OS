# Code Engineer — Spesifikasi Capability

**Versi:** 2.0.0
**Status:** Bersertifikat (RFC-0006)
**Target Kualitas:** A+ (≥95) — Level 4 — Pakar Domain

---

## 1. Tujuan

Code Engineer adalah **otoritas rekayasa perangkat lunak** untuk ECP — Capability Pack yang menganalisis arsitektur, mereview kode, menghasilkan patch, dan menguji perangkat lunak berbasis bukti.

Capability Pack ini mengintegrasikan 12 modul inti (Parser, Analyzer, Architecture Reader, Dependency Graph, Impact Analyzer, Refactoring Engine, Patch Generator, Regression Analyzer, Test Generator, Architecture Patterns, Secure Coding, Solid Analysis) melalui pipeline rekayasa terstruktur — **tanpa memodifikasi Core**.

---

## 2. Ruang Lingkup

### Dalam Ruang Lingkup
- **Code Review** — Analisis kualitas, keamanan, dan arsitektur
- **Refactoring** — Saran perbaikan dengan estimasi dampak
- **Patch Generation** — Pembuatan patch yang aman dan reversible
- **Test Generation** — Unit test, integrasi, dan edge cases
- **Architecture Analysis** — Clean Architecture, DDD, CQRS, Event Sourcing, SOLID
- **Dependency Analysis** — Circular dependency, orphan modules, coupling
- **Security Analysis** — OWASP Top 10, hardcoded secrets, injection
- **Database Schema Design** — Normalization, indexing, relationships

### Di Luar Cakupan
- Pengembangan kernel/driver
- Pengembangan game
- Model pelatihan pipeline ML
- Penyediaan infrastruktur

---

## 3. Kontrak

### Input: CodeAnalysisRequest
```json
{
  "task": "review | refactor | generate_tests | generate_patch | analyze_architecture | analyze_dependencies | design_schema",
  "code": "string (source code to analyze)",
  "filename": "string",
  "language": "python | javascript | typescript | java | go",
  "repository_path": "string (optional)",
  "options": {
    "include_security": true,
    "include_architecture": true,
    "include_refactoring": true,
    "max_suggestions": 10
  }
}
```

### Output: CodeAnalysisReport
```json
{
  "task": "string",
  "filename": "string",
  "functions": 15,
  "classes": 5,
  "issues": [
    {
      "severity": "critical | high | medium | low | info",
      "category": "string",
      "description": "string",
      "recommendation": "string",
      "line_number": 10,
      "confidence": 0.95
    }
  ],
  "architecture_patterns": {
    "total_findings": 3,
    "findings": []
  },
  "secure_coding": {
    "total_findings": 2,
    "findings": []
  },
  "refactoring_suggestions": [],
  "test_generation": {
    "total_tests": 12,
    "edge_cases": 3,
    "coverage_estimate": 0.85
  },
  "patch": {
    "patch_id": "uuid",
    "diff": "unified diff",
    "is_valid": true
  }
}
```

---

## 4. Operasi

| Operasi | Deskripsi | Input | Output |
|-----------|-------------|--------|---------|
| `review` | Full code review (quality + security + architecture) | code, filename, language | CodeAnalysisReport |
| `refactor` | Refactoring suggestions with impact analysis | code, filename | RefactoringReport |
| `generate_tests` | Unit/integration test generation | source_path, module_path | TestFile |
| `generate_patch` | Generate rollback-ready patch | original, modified, filename | PatchBundle |
| `analyze_architecture` | Clean Architecture, DDD, CQRS analysis | repository_path | ArchitectureReport |
| `analyze_dependencies` | Dependency graph and circular deps | repository_path | DependencyGraphReport |
| `design_schema` | Database schema design | requirements | SchemaDesign |
| `analyze_regression_risk` | Regression risk assessment | repo_path, changes | RegressionReport |

---

## 5. Modul Analyzer

| Modul | File | Tanggung Jawab |
|-------|------|----------------|
| `parser.py` | Parser | Parse Python/JS/TS code ke AST |
| `analyzer.py` | Analyzer | Code quality analysis (imports, docstrings, naming, security) |
| `architecture_reader.py` | ArchitectureReader | Baca arsitektur repositori (Clean Arch, DDD, CQRS) |
| `dependency_graph.py` | DependencyGraphBuilder | Bangun graph dependency dan deteksi circular deps |
| `impact_analyzer.py` | ImpactAnalyzer | Analisis blast radius perubahan |
| `refactoring_engine.py` | RefactoringEngine | Saran refactoring dengan estimasi dampak |
| `patch_generator.py` | PatchGenerator | Generate patch yang reversible |
| `regression_analyzer.py` | RegressionAnalyzer | Analisis risiko regresi |
| `test_generator.py` | TestGenerator | Generate unit/integration tests |
| `architecture_patterns.py` | ArchitecturePatternAnalyzer | Deteksi pola arsitektur dan pelanggaran |
| `secure_coding.py` | SecureCodingAnalyzer | OWASP Top 10, injection, hardcoded secrets |
| `solid_analysis.py` | SOLIDAnalyzer | Analisis 5 prinsip SOLID |
| `ddd_analysis.py` | DDDAnalyzer | Analisis Domain-Driven Design |
| `cqrs_analysis.py` | CQRSAnalyzer | Analisis CQRS compliance |
| `event_sourcing_analysis.py` | EventSourcingAnalyzer | Analisis Event Sourcing patterns |

---

## 6. Dimensi Benchmark

| Dimensi | Target | Grade |
|-----------|--------|-------|
| Code Review Accuracy | ≥95% | A+ |
| Security Detection (OWASP) | ≥95% | A+ |
| Refactoring Suggestions Quality | ≥95% | A+ |
| Test Generation Coverage | ≥90% | A |
| Patch Validity | ≥95% | A+ |
| Architecture Analysis | ≥95% | A+ |
| Dependency Analysis | ≥95% | A+ |
| Performance | < 5s per file | A |

---

## 7. Dependensi

- **apps/base.py** — Definisi model dasar
- **apps/code_engineer/schemas.py** — Kontrak publik (jika ada)
- **apps/code_engineer/engine.py** — Domain engine
- **apps/code_engineer/worker.py** — Adaptor tipis (ADR-003)

---

## 8. Contoh Penggunaan

```python
from apps.code_engineer.engine import CodeEngineerEngine

engine = CodeEngineerEngine()
report = engine.review(
    code="def get_user(user_id): query = f'SELECT * FROM users WHERE id = {user_id}'",
    filename="user_service.py",
    language="python"
)
print(f"Found {len(report['issues'])} issues")
for issue in report['issues']:
    print(f"  [{issue['severity']}] {issue['category']}: {issue['description']}")
```

---

## 9. Audit Keamanan

### OWASP Top 10
- A01:2021 – Broken Access Control: Review akses kontrol dalam kode
- A02:2021 – Cryptographic Failures: Deteksi hardcoded secrets, weak crypto
- A03:2021 – Injection: SQL, NoSQL, OS command, LDAP injection
- A04:2021 – Insecure Design: Missing security design patterns
- A05:2021 – Security Misconfiguration: Default credentials, verbose errors
- A06:2021 – Vulnerable Components: Dependencies dengan CVE
- A07:2021 – Authentication Failures: Weak session management
- A08:2021 – Data Integrity Failures: Insecure deserialization
- A09:2021 – Logging Failures: Missing audit logging
- A10:2021 – SSRF: Server-side request forgery

### Deteksi Rahasia
- API keys, tokens, password, certificate, private key
- Pattern matching untuk format umum (sk-, AIza, AKIA, dll)
- Redaksi otomatis dalam output

### Pencegahan Injeksi
- SQL injection: parameterized queries
- Command injection: avoid shell=True, use subprocess dengan list args
- LDAP injection: parameterized LDAP queries
- XSS: output encoding, Content-Security-Policy

### Validasi Input
- Type hints enforcement
- Input sanitization untuk boundary values
- Null/None handling

### Default Aman
- Fail-closed untuk akses kontrol
- Least privilege untuk database credentials
- Secure defaults untuk session management

---

## 10. Optimasi Kinerja

### Strategi Caching
- AST parsing cache untuk file yang tidak berubah (hash-based)
- Dependency graph cache untuk analisis berulang
- Benchmark result cache untuk skenario yang sama

### Peluang Paralelisme
- Analisis multi-file secara parallel (ProcessPoolExecutor)
- Independent analyzer modules (OWASP, DDD, SOLID) dapat dijalankan paralel
- Test generation untuk module yang berbeda secara parallel

### Optimasi Memori
- Streaming parser untuk file besar (>10MB)
- Lazy loading untuk modul analyzer
- Disk-based cache untuk graph dependency besar

### Efisiensi Token (AI-related)
- Context window management untuk large codebases
- Chunking strategy untuk analisis file besar
- Selective analysis berdasarkan scope (hanya file yang berubah)

---

## 11. Riwayat Perubahan

| Versi | Tanggal | Perubahan |
|-------|---------|-----------|
| 2.0.0 | 2026-08-05 | Level 4 Domain Expert, A+ grade, 10 golden tests, security audit, performance optimization |
