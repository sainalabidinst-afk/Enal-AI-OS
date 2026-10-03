# DevSecOps Capability Pack

**Version:** 3.0.0
**Target Grade:** A (≥90%)
**Status:** Implemented
**Phase:** 8
**RFC:** [RFC-0040](docs/rfcs/RFC-0040-devsecops.md)
**ADR:** [ADR-020](docs/adr/ADR-020-devsecops.md)

## Ringkasan

DevSecOps Capability Pack mengintegrasikan keamanan ke dalam pipeline CI/CD dengan security gates otomatis, dependency vulnerability scanning, runtime policy enforcement, dan compliance-as-code. Pack ini memindai supply chain dependensi, memetakan temuan ke CWE, dan mencegah deployment yang tidak aman sebelum mencapai production environment.

## Kemampuan Inti

1. **Security Gate** — Evaluasi stage-by-stage security checks dalam pipeline CI/CD. Setiap gate melaporkan checks passed/blocking serta failure reasons. Mendukung fail-closed policy.
2. **Dependency Scan** — Pindai dependency list terhadap CVE database (NVD default), klasifikasikan severity, dan rekomendasikan versi upgrade. Laporkan vulnerable dependency count dan remediation plan.
3. **Runtime Policy** — Evaluasi runtime configuration terhadap kebijakan (allowed ports, required security headers, container security). Deteksi violations berdasarkan environment (production/staging).
4. **Compliance As Code** — Pemetaan kebijakan ke standar (OWASP Top 10, SOC 2, ISO 27001, PCI-DSS). Hasilkan compliance gate evaluation dan policy violations.

## Input Schema

- `operation`: `security_gate` | `dependency_scan` | `runtime_policy` | `compliance_as_code`
- `pipeline_name` — nama pipeline CI/CD
- `dependencies[]` — daftar nama dependency
- `dependency_versions` — versi saat ini per dependency
- `policies[]` — kebijakan yang akan di-enforce
- `cve_database` — NVD (default), GitHub Advisory, dll
- `severity_threshold` — high (default), medium, low
- `scan_depth` — full (default), quick
- `environment` — production, staging, development

## Output Schema

- `security_gates[]` — PipelineSecurityGate: stage_name, checks, passed, blocking, failure_reasons
- `findings[]` — SecurityFinding: finding_id, severity, category, description, file_path, line_number, cwe_id, remediation
- `vulnerable_dependencies[]` — VulnerableDependency: name, current_version, latest_version, cve_count, severity, remediation
- `policy_violations[]` — daftar pelanggaran kebijakan
- `recommendations[]` — remediasi berprioritas

## Batasan Keamanan

- **Tidak menghentikan build otomatis** — DevSecOps hanya memberi rekomendasi; keputusan final ada pada tim keamanan
- **Tidak mengungkap detail CVE yang spesifik** — Laporkan severity dan remediation, bukan eksploit detail
- **Mensyyaratkan CVE database validation** — Tolak scan jika database tidak dapat diverifikasi

## Integration

- **Konsumsi dari**: Infrastructure Engineer (pipeline configs, IaC templates), Security Engineer (threat models), DevOps Assistant (CI/CD pipeline generation)
- **Digunakan oleh**: DevOps Assistant (security gate integration), Compliance Officer (compliance evidence), System Architect (runtime policy review)

## Benchmark

- 10 scenarios across 6 dimensions:
  1. **Security Gate** (0.93) — pipeline gate evaluation, pass/fail accuracy, blocking detection
  2. **Dependency Scan** (0.91) — CVE correlation, version upgrade recommendation, false positive rate
  3. **Runtime Policy** (0.89) — policy evaluation, environment-specific violations, remediation accuracy
  4. **Compliance As Code** (0.92) — OWASP/SOC2/ISO mapping, compliance coverage, gap identification
  5. **Safety Boundary** (0.94) — no fabricated CVE data, fail-closed on missing database, input validation
  6. **Explainability** (0.91) — finding traceability (CWE mapping), remediation justification, policy rationale

- Overall score: A (91.7%)
- Dashboard: `benchmarks/dashboards/devsecops_dashboard.html`

## Real Cases

10 real cases in `real_cases/devsecops/` covering:
- OWASP Top 10 scan for web application (SQLi, XSS, SSRF detection)
- Dependency vulnerability scan for Python project (15 packages, 3 CVEs)
- Production runtime policy check (container security, network policies, secrets)
- SOC 2 Type II compliance gate evaluation for CI/CD pipeline
- Supply chain security scan (transitive dependency depth-3 analysis)
- Container image hardening (non-root, read-only fs, drop all capabilities)
- Secret detection in Git history (hardcoded tokens, API keys, certificates)
- Pipeline security gate integration with GitHub Actions
- Dependency upgrade remediation plan (3 CVEs, 5 packages, timeline)
- Compliance-as-code drift detection (IaC policy violation recovery)

## Changelog

- **2026-10-02**: Initial implementation (RFC-0040, ADR-020)
  - `apps/devsecops/` pack with engine, schemas, worker, `security_engine.py` (DevSecOpsSecurityEngine)
  - 4 operations: security_gate, dependency_scan, runtime_policy, compliance_as_code
  - SecurityFinding with CWE mapping, VulnerableDependency with CVE correlation
  - PipelineSecurityGate with fail-closed blocking policy
  - Safety boundary check (no fabricated vulnerability data, database validation)
  - 10 benchmark scenarios across 6 dimensions, overall A (91.7%)
  - 10 real cases in `real_cases/devsecops/`
  - Benchmark dashboard: `benchmarks/dashboards/devsecops_dashboard.html`
