# Security Engineer — Spesifikasi Capability

**Versi:** 1.0.0
**Status:** Production Ready (RFC-0008)
**Target Kualitas:** A- (≥85)

---

## 1. Tujuan

Security Engineer adalah **otoritas keamanan siber** untuk ECP — Capability Pack yang menganalisis code, dependencies, dan configuration untuk mendeteksi kerentanan, membuat threat model, dan memastikan kepatuhan terhadap standar keamanan.

Capability Pack ini menganalisis source code untuk OWASP Top 10, secret detection, dependency audit (CVE), vulnerability scan, threat modeling, hardening review, dan compliance mapping — **tanpa memodifikasi Core**.

---

## 2. Ruang Lingkup

### Dalam Ruang Lingkup
- **OWASP Analysis** — Mendeteksi kerentanan OWASP Top 10 di source code
- **Secret Detection** — Mendeteksi API key, token, password, dan secret lainnya
- **Dependency Audit** — Audit CVE pada dependencies
- **Vulnerability Scan** — Memindai kerentanan umum (SQLi, XSS, CSRF, dll.)
- **Threat Modeling** — Membuat STRIDE threat model untuk arsitektur
- **Hardening Review** — Meninjau konfigurasi dan praktik keamanan
- **Compliance Mapping** — Memetakan kepatuhan ke standar (OWASP, PCI-DSS, GDPR)
- **False Positive Reduction** — Deduplikasi dan penyaringan findings
- **Experience Memory** — Merekam hasil ke riwayat

### Di Luar Cakupan
- Eksekusi patch atau perbaikan keamanan secara langsung
- Modifikasi kontrak Core
- Import langsung dari Capability Pack lain (kepatuhan ADR-002)

---

## 3. Kontrak

### Input: SecurityReviewRequest
```json
{
  "request_id": "uuid",
  "operation": "owasp_analysis | secret_detection | dependency_audit | vulnerability_scan | threat_model | hardening_review | compliance_mapping",
  "source_code": "string",
  "language": "python | javascript | go | java",
  "dependencies": ["package==1.0.0"],
  "architecture_context": {
    "components": ["web", "api", "database"],
    "data_flows": [{"from": "web", "to": "api"}]
  },
  "compliance_standards": ["OWASP", "PCI-DSS", "GDPR"]
}
```

### Output: Laporan Security Review
```json
{
  "request_id": "uuid",
  "operation": "string",
  "findings": [
    {
      "id": "uuid",
      "type": "owasp | secret | cve | vulnerability | threat | hardening | compliance",
      "severity": "critical | high | medium | low",
      "title": "SQL Injection in user input",
      "description": "User input is concatenated into SQL query",
      "location": "file.py:42",
      "remediation": "Use parameterized queries",
      "confidence": 0.9,
      "false_positive": false
    }
  ],
  "summary": {
    "total_findings": 15,
    "critical": 2,
    "high": 5,
    "medium": 6,
    "low": 2,
    "compliance_score": 0.85
  },
  "explanation": "string — human-readable analysis summary"
}
```

---

## 4. Operasi

| Operasi | Deskripsi | Input | Output |
|-----------|-------------|--------|---------|
| `owasp_analysis` | Menganalisis source untuk OWASP Top 10 | source_code, language | Security Findings |
| `secret_detection` | Mendeteksi secret yang ter-expose | source_code | Security Findings |
| `dependency_audit` | Audit dependencies terhadap CVE | dependencies | CVE List |
| `vulnerability_scan` | Memindai kerentanan umum | source_code, language | Security Findings |
| `threat_model` | Menghasilkan STRIDE threat model | architecture_context | Threat Model |
| `hardening_review` | Meninjau konfigurasi keamanan | source_code, language | Security Findings |
| `compliance_mapping` | Memetakan ke standar kepatuhan | findings, standards | Compliance Report |

---

## 5. Modul Analyzer

| Modul | Tanggung Jawab |
|--------|----------------|
| `owasp_analyzer.py` | Mendeteksi 10 kerentanan teratas OWASP |
| `secret_detector.py` | Mendeteksi secret dan kredensial yang ter-expose |
| `dependency_auditor.py` | Audit dependencies terhadap CVE yang diketahui |
| `vulnerability_scanner.py` | Memindai pola kerentanan umum |
| `threat_modeler.py` | Membuat STRIDE threat model |
| `hardening_reviewer.py` | Meninjau praktik security hardening |
| `compliance_mapper.py` | Memetakan findings ke standar kepatuhan |

---

## 6. Dimensi Benchmark

| Dimensi | Target | Grade |
|-----------|--------|-------|
| OWASP Detection | ≥90% | A |
| Secret Detection | ≥90% | A |
| Dependency Audit | ≥90% | A |
| Vulnerability Detection | ≥90% | A |
| Threat Model | ≥90% | A |
| Hardening Compliance | ≥90% | A |
| False Positive Rate | ≥90% | A |
| Response Time | ≥90% | A |
| Explainability | ≥90% | A |

---

## 7. Dependensi

- **apps/base.py** — Definisi model dasar
- **apps/security_engineer/schemas.py** — Kontrak publik
- **apps/security_engineer/engine.py** — Domain engine
- **apps/security_engineer/worker.py** — Adaptor tipis (ADR-003)

---

## 8. Contoh Penggunaan

```python
from apps.security_engineer.engine import SecurityEngineerEngine
from apps.security_engineer.schemas import SecurityReviewRequest

engine = SecurityEngineerEngine()
request = SecurityReviewRequest(
    operation="owasp_analysis",
    source_code="query = f\"SELECT * FROM users WHERE id = {user_id}\"",
    language="python",
)
report = engine.review(request)
print(f"Found {len(report.findings)} security issues")
```

