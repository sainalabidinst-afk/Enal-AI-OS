<!-- BILINGUAL_DOCS_START -->
## Bahasa Indonesia / English

### Ringkasan / Summary
Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.
> Terjemahan Indonesia: Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.

- Bahasa Indonesia: isi utama dokumen disajikan dalam versi Indonesia di bawah konten asli.
- English: the main prose content is presented in an Indonesian bilingual section below the original content.

### Informasi Dokumen / Document Info
- File: `docs/capabilities/security-engineer.md`
- Judul: Security Engineer
- Status: bilingual content applied

<!-- BILINGUAL_DOCS_END -->

# Security Engineer Capability Specification

## Version: 1.0.0
## Status: Production Ready (RFC-0008)
## Quality Target: A- (≥85)

---

## 1. Purpose

Security Engineer adalah **otoritas keamanan siber** untuk ECP — Capability Pack yang
menganalisis kode, dependensi, dan konfigurasi untuk mendeteksi kerentanan,
membuat model ancaman, dan memastikan kepatuhan standar keamanan.
> Terjemahan Indonesia: Keamanan Engineer adalah otoritas keamanan siber untuk ECP — kapabilitas Pack yang menganalisis kode, dependensi, dan konfigurasi untuk mendeteksi kerentanan, membuat model ancaman, dan memastikan kepatuhan standar keamanan.

Capability Pack ini menganalisis kode sumber untuk OWASP Top 10, deteksi rahasia,
audit dependensi (CVE), pemindaian kerentanan, model ancaman, review hardening,
dan pemetaan kepatuhan — **tanpa memodifikasi Core**.
> Terjemahan Indonesia: Kapabilitas Pack ini menganalisis kode sumber untuk OWASP Top 10, deteksi rahasia, audit dependensi (CVE), pemindaian kerentanan, model ancaman, review hardening, dan pemetaan kepatuhan — tanpa memodifikasi Core.

---

## 2. Scope

### In Scope
- **OWASP Analysis** — Deteksi kerentanan OWASP Top 10 di kode sumber
- **Secret Detection** — Deteksi API key, token, password, dan rahasia lain
- **Dependency Audit** — Audit CVE pada dependensi
- **Vulnerability Scanning** — Pindai kerentanan umum (SQLi, XSS, CSRF, dll.)
- **Threat Modeling** — Buat model ancaman STRIDE untuk arsitektur
- **Hardening Review** — Review konfigurasi dan praktik keamanan
- **Compliance Mapping** — Pemetaan ke standar (OWASP, PCI-DSS, GDPR)
- **False Positive Reduction** — Deduplikasi dan filtering temuan
- **Experience Memory** — Perekaman hasil ke history

### Out of Scope
- Eksekusi patch atau perbaikan keamanan langsung
- Modifikasi Core contracts
- Direct import dari Capability Pack lain (ADR-002 compliance)

---

## 3. Contract

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

### Output: SecurityReviewReport
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

## 4. Operations

| Operation | Description | Inputs | Outputs |
|-----------|-------------|--------|---------|
| owasp_analysis | Analyze source for OWASP Top 10 | source_code, language | SecurityFindings |
| secret_detection | Detect exposed secrets | source_code | SecurityFindings |
| dependency_audit | Audit dependencies for CVEs | dependencies | CVEList |
| vulnerability_scan | Scan for common vulnerabilities | source_code, language | SecurityFindings |
| threat_model | Generate STRIDE threat model | architecture_context | ThreatModel |
| hardening_review | Review security configuration | source_code, language | SecurityFindings |
| compliance_mapping | Map to compliance standards | findings, standards | ComplianceReport |

---

## 5. Analyzer Modules

| Module | Responsibility |
|--------|----------------|
| owasp_analyzer.py | Detect OWASP Top 10 vulnerabilities |
| secret_detector.py | Detect exposed secrets and credentials |
| dependency_auditor.py | Audit dependencies for known CVEs |
| vulnerability_scanner.py | Scan for common vulnerability patterns |
| threat_modeler.py | Generate STRIDE threat models |
| hardening_reviewer.py | Review security hardening practices |
| compliance_mapper.py | Map findings to compliance standards |

---

## 6. Benchmark Dimensions

| Dimension | Target | Grade |
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

## 7. Dependencies

- **apps/base.py** — Base model definitions
- **apps/security_engineer/schemas.py** — Public contracts
- **apps/security_engineer/engine.py** — Domain Engine
- **apps/security_engineer/worker.py** — Thin adapter (ADR-003)

---

## 8. Usage Example

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
