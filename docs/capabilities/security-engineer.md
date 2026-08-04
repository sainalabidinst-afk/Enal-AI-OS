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

### Input: SecurityAssessmentRequest
```json
{
  "assessment_id": "uuid",
  "target_type": "code | config | dependency | architecture | full_review",
  "target": {
    "source_code": "string",
    "language": "python | javascript | go | java",
    "manifest_content": "string",
    "config_content": "string",
    "architecture_description": "string",
    "components": ["web", "api", "database"],
    "data_flows": [{"from": "web", "to": "api"}]
  },
  "standards": ["owasp_top10", "cis", "pci_dss", "gdpr", "hipaa", "iso27001", "soc2", "nist_csf"],
  "include_remediation": true,
  "include_compliance_mapping": true,
  "check_secrets": true,
  "check_dependencies": true,
  "scan_depth": "quick | thorough"
}
```

### Output: SecurityAssessmentReport
```json
{
  "assessment_id": "uuid",
  "target_type": "string",
  "findings": [
    {
      "id": "uuid",
      "category": "A03:2021-Injection | vulnerability_detection | ...",
      "severity": "critical | high | medium | low",
      "title": "SQL injection via f-string in execute()",
      "description": "SQL query constructed using f-string interpolation.",
      "evidence": {"file": "app.py", "line": 10, "pattern": "..."},
      "remediation": "Use parameterized queries with placeholders.",
      "owasp_mapping": "A03:2021-Injection",
      "compliance_mapping": ["pci_dss", "owasp_top10"],
      "confidence": 0.95
    }
  ],
  "secrets": [
    {
      "id": "uuid",
      "type": "api_key | password | token | certificate | private_key",
      "location": "config.py:14",
      "severity": "critical | high | medium | low",
      "remediation": "Rotate the API key and store in a secrets manager.",
      "confidence": 0.9,
      "evidence": {"type": "api_key", "redacted_value": "sk-...abcd", "line": 14}
    }
  ],
  "summary": {
    "total_findings": 15,
    "critical_count": 2,
    "high_count": 5,
    "medium_count": 6,
    "low_count": 2,
    "overall_risk": "critical | high | medium | low",
    "compliance_score": 0.85,
    "recommendations_count": 3
  },
  "compliance_report": {
    "standards": ["owasp_top10", "pci_dss"],
    "mapped_findings": 10,
    "compliance_percentage": {"owasp_top10": 0.7, "pci_dss": 0.65},
    "gaps": ["Missing WAF", "No rate limiting"]
  }
}
```

---

## 4. Operasi

| Operasi | Deskripsi | Input | Output |
|-----------|-------------|--------|---------|
| `full_review` | Full security assessment (OWASP + secrets + vulns + threat model + hardening + compliance) | target, standards, options | SecurityAssessmentReport |
| `code` | OWASP analysis + secret detection + vulnerability scan on source code | source_code, language | Security Findings |
| `config` | Hardening review on configuration files | config_content, config_type | Security Findings |
| `dependency` | Dependency audit against CVE databases | manifest_content, manifest_type | Dependency Findings |
| `architecture` | Threat modeling (STRIDE) for architecture description | architecture_description, components, data_flows | Threat Model |

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
from apps.security_engineer.schemas import SecurityAssessmentRequest, AssessmentType

engine = SecurityEngineerEngine()
request = SecurityAssessmentRequest(
    target_type=AssessmentType.full_review,
    target={
        "source_code": "query = f\"SELECT * FROM users WHERE id = {user_id}\"",
        "language": "python",
    },
    standards=["owasp_top10", "cis"],
    check_secrets=True,
    include_remediation=True,
)
report = engine.review(request)
print(f"Found {len(report.findings)} security issues")
```

