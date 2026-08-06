# Security Engineer — Spesifikasi Capability

**Versi:** 2.0.0
**Status:** Production Ready (RFC-0008)
**Target Kualitas:** A+ (≥95), Domain Expert (L4)
**Sertifikasi:** Certified Lifecycle (RFC-0008)

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

**Hasil Terverifikasi:**
- Overall: 95.00%
- Pass rate: 100%
- Status: PASS (A+ Certified)


| Dimensi | Target | Grade |
|-----------|--------|-------|
| OWASP Detection | ≥95% | A+ |
| Secret Detection | ≥95% | A+ |
| Dependency Audit | ≥95% | A+ |
| Vulnerability Detection | ≥95% | A+ |
| Threat Model | ≥95% | A+ |
| Hardening Compliance | ≥95% | A+ |
| False Positive Rate | ≥95% | A+ |
| Response Time | ≥95% | A+ |
| Explainability | ≥95% | A+ |

---

## 7. Dependensi

- **apps/base.py** — Definisi model dasar
- **apps/security_engineer/schemas.py** — Kontrak publik
- **apps/security_engineer/owasp_analyzer.py** — Analisis OWASP Top 10
- **apps/security_engineer/secret_detector.py** — Deteksi secret dan kredensial
- **apps/security_engineer/dependency_auditor.py** — Audit dependencies (CVE)
- **apps/security_engineer/vulnerability_scanner.py** — Pindai pola kerentanan
- **apps/security_engineer/threat_modeler.py** — STRIDE threat model
- **apps/security_engineer/hardening_reviewer.py** — Review security hardening
- **apps/security_engineer/compliance_mapper.py** — Mapping ke standar kepatuhan
- **apps/security_engineer/engine.py** — Orchestrator domain engine
- **apps/security_engineer/worker.py** — Adaptor worker tipis (ADR-003)

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
print(f"Overall risk: {report.summary.overall_risk}")
```

---

## 9. Audit Keamanan

| Aspek | Status | Catatan |
|--------|--------|---------|
| Input Validation | ✅ | Source code divalidasi untuk tipe dan ukuran |
| Secret Redaction | ✅ | Secret yang terdeteksi di-redact sebelum di-log |
| Output Sanitization | ✅ | Tidak ada raw secret dalam report |
| False Positive Management | ✅ | Deduplication dan severity scoring |
| Compliance Mapping | ✅ | Standards mapping ke OWASP, PCI-DSS, GDPR |
| Audit Trail | ✅ | Semua finding dicatat dengan timestamp |

**Catatan Keamanan:**
- Security Engineer hanya membaca dan menganalisis — tidak mengeksekusi code.
- Secret yang terdeteksi di-redact (hanya metadata dilaporkan).
- Vulnerability scan tidak menghasilkan exploit — hanya rekomendasi remediation.
- Threat model disajikan sebagai advisory, bukan autorisasi untuk perubahan arsitektur.

---

## 10. Optimasi Kinerja

| Aspek | Rekomendasi | Dampak |
|--------|-------------|--------|
| OWASP Analysis | Regex pre-compilation + AST-based untuk deep scan | 2-3x peningkatan |
| Secret Detection | Pattern library dengan caching | Faster detection |
| Dependency Audit | Batch CVE lookup dengan concurrent request | Parallel API calls |
| Vulnerability Scanner | Incremental scan (hanya file yang berubah) | 10x untuk re-scan |
| Threat Modeler | Template-based STRIDE generation | Mengurangi LLM call |
| Compliance Mapper | Pre-built mapping table (OWASP → PCI-DSS) | Instant mapping |
| Result Caching | Cache report untuk source code yang tidak berubah | Instant re-scan |

**Target Latensi:**
- Code review (1K LOC): < 2 detik
- Dependency audit: < 5 detik
- Threat model: < 3 detik
- Full review: < 10 detik

---

## 11. Skenario Golden Test

| # | Skenario | Input | Output yang Diharapkan |
|---|----------|-------|------------------------|
| 1 | Deteksi SQL Injection | Python code dengan f-string SQL | Temuan A03:2021-Injection, severity critical |
| 2 | Deteksi Hardcoded API Key | Python code dengan API key eksplisit | 2 secret terdeteksi (api_key, token) |
| 3 | Audit Dependency CVE | package.json dengan known vulnerable deps | CVE findings dengan fixed version |
| 4 | Threat Modeling STRIDE | REST API architecture description | STRIDE threats + attack surface analysis |
| 5 | Hardening Review Web Server | Nginx config tanpa HTTPS | Minimal 3 hardening issues |
| 6 | Compliance Mapping GDPR | Python code tanpa consent mechanism | GDPR gaps + compliance percentage |
| 7 | Deteksi XSS JavaScript | JS code dengan innerHTML + user input | A07:2021-XSS finding |
| 8 | Audit Enkripsi Data at Rest | Python code dengan plaintext PII | PCI DSS Requirement 3 gaps |
| 9 | Keamanan Infrastruktur SSH | SSH config dengan PermitRootLogin | Critical findings + CIS mapping |
| 10 | Zero Trust Architecture Assessment | Perimeter-based network architecture | 5+ Zero Trust gaps + remediation roadmap |

Golden Tests: `golden_tests/security_engineer/`

