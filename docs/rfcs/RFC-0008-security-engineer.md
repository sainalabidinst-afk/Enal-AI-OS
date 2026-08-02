# RFC-0008: Capability Pack Security Engineer

| Field | Nilai |
|-------|-------|
| **RFC ID** | RFC-0008 |
| **Status** | Draft |
| **Versi** | 0.1.0 |
| **Penulis** | Enal AI OS Core Team |
| **Target Rilis** | v1.2.0 (fase Capability Excellence) |
| **Capability Pack** | Security Engineer |
| **Capability ID** | `security-engineer` |
| **Kategori** | Security |
| **Target Kualitas** | A- (≥85) |
| **Target Maturity** | Level 3 — Production Ready |
| **RFC Referensi** | RFC-0008 |

---

## Motivasi

Capability Pack ECP yang ada menghasilkan kode, konfigurasi, dan deployment. Setiap pack menghasilkan output yang membawa risiko keamanan, tetapi tidak ada security reasoning layer khusus yang secara sistematis mengevaluasi, mendeteksi, dan memperbaiki kerentanan di semua artefak.

Saat ini:

1. **Pemeriksaan keamanan bersifat embedded** — Code Engineer memiliki kesadaran OWASP dasar, Network Engineer memiliki audit firewall, tetapi tidak ada kerangka keamanan yang terpadu.
2. **Threat modeling tidak ada** — Tidak ada analisis sistematis terhadap attack surface, trust boundaries, atau threat actors sebelum deployment.
3. **Deteksi secret bersifat ad hoc** — Tidak ada deteksi dan rekomendasi rotasi terpusat untuk kredensial di kode atau konfigurasi.
4. **Risiko dependensi tidak dilacak** — Kerentanan di paket pihak ketiga tidak diaudit secara sistematis atau dikorelasikan dengan ketersediaan exploit.
5. **Kepatuhan tidak dipetakan** — Temuan keamanan tidak dikaitkan dengan kerangka kepatuhan (SOC 2, ISO 27001, HIPAA, PCI-DSS).

Capability Pack Security Engineer menjadi layer keamanan khusus yang menganalisis semua artefak yang dihasilkan ECP terhadap standar industri, mendeteksi ancaman dan kerentanan, serta menyediakan panduan remediasi dengan pemetaan kepatuhan.

---

## Pernyataan Masalah

Tanpa Capability Pack Security Engineer yang khusus:

- **Tidak ada deteksi kerentanan terpadu** — temuan keamanan bersifat spesifik-pack; SQL injection diperiksa oleh Code Engineer, firewall misconfiguration oleh Network Engineer, tetapi tidak ada satu tampilan pun yang menyatukan semuanya.
- **Cakupan OWASP Top 10 tidak lengkap** — hanya sebagian masalah yang terdeteksi, dan kualitas deteksi bervariasi antar pack.
- **Threat modeling manual** — tidak ada analisis otomatis terhadap trust boundaries, data flow, atau attack surface.
- **Tidak ada pipeline deteksi secret** — kredensial di kode, konfigurasi, atau artefak tidak diidentifikasi atau ditandai secara sistematis.
- **Kerentanan dependensi tidak diaudit** — kerentanan paket pihak ketiga (CVE) tidak dilacak atau diprioritaskan.
- **Kepatuhan tidak ditegakkan** — temuan keamanan tidak dipetakan ke persyaratan kepatuhan, membuat persiapan audit manual dan rawan kesalahan.
- **False positive dan false negative tidak dilacak per domain** — tidak ada loop umpan balik untuk meningkatkan presisi deteksi.

---

## Tujuan

1. **OWASP Top 10 Analysis** — Mendeteksi semua 10 kategori kerentanan di kode, konfigurasi, dan artefak.
2. **Threat Modeling** — Menganalisis arsitektur sistem untuk attack surface, trust boundaries, dan threat actors.
3. **Secret Detection** — Mengidentifikasi secret hardcoded, kredensial, API key, dan token di semua output.
4. **Vulnerability Analysis** — Mendeteksi dan memprioritaskan kerentanan yang diketahui (CVE) di dependensi.
5. **Dependency Audit** — Mengaudit paket pihak ketiga untuk kerentanan yang diketahui, versi usang, dan lisensi berisiko.
6. **Security Review** — Melakukan review keamanan sistematis terhadap artefak dan konfigurasi yang dihasilkan.
7. **Configuration Hardening** — Mengidentifikasi dan memperbaiki default konfigurasi yang tidak aman.
8. **Compliance Mapping** — Memetakan temuan ke SOC 2, ISO 27001, HIPAA, PCI-DSS, dan kerangka kepatuhan lain.

### Kriteria Keberhasilan

| Metrik | Target | Grade |
|--------|--------|-------|
| Tingkat Deteksi | ≥95% (semua kerentanan yang diketahui terdeteksi) | A- |
| Tingkat False Positive | <5% | A- |
| Cakupan Threat | ≥90% (semua kategori ancaman yang didefinisikan dianalisis) | A- |
| Deteksi Secret | ≥95% (secret hardcoded ditemukan) | A- |
| Cakupan CVE Dependensi | ≥90% (CVE yang diketahui di dependensi teridentifikasi) | A- |
| Pemetaan Kepatuhan | ≥95% (temuan dipetakan ke kontrol yang relevan) | A- |
| Explainability | ≥90% (temuan dijelaskan dengan panduan remediasi) | A- |
| Konsistensi | ≥90% (input yang sama menghasilkan temuan yang sama di setiap run) | A- |

---

## Non-Tujuan

1. **Penetration testing aktif terhadap sistem langsung** — Security Engineer menganalisis output; ia tidak melakukan eksploitasi langsung.
2. **Eksekusi incident response** — Security Engineer mengidentifikasi dan merekomendasikan; incident response memerlukan eksekusi manusia.
3. **Menggantikan alat keamanan khusus** — Alat SAST/DAST tetap menjadi sumber kebenaran; Security Engineer menyediakan orkestrasi dan korelasi.
4. **Pengungkapan kerentanan** — Security Engineer tidak mengungkapkan kerentanan secara eksternal.
5. **Modifikasi Core** — Semua implementasi berada di dalam Capability Pack Security Engineer.

---

## Scope Kapabilitas

### Kapabilitas Inti

| Kapabilitas | Deskripsi | Input | Output |
|-----------|-------------|--------|---------|
| OWASP Top 10 Analysis | Mendeteksi injection, XSS, SSRF, CSRF, broken auth, dll. di kode dan konfigurasi | Source code, API spec, file konfigurasi | Daftar temuan dengan severity, kategori OWASP, remediasi |
| Threat Modeling | Menganalisis arsitektur untuk attack surface, trust boundaries, data flows | Diagram arsitektur, deskripsi data flow | Model ancaman dengan analisis STRIDE |
| Secret Detection | Mengidentifikasi secret hardcoded, kredensial, API key, token | Kode, konfigurasi, file lingkungan, pipeline CI/CD | Temuan secret dengan tipe, severity, panduan rotasi |
| Vulnerability Analysis | Mendeteksi kerentanan yang diketahui di kode aplikasi | Source code, manifest dependensi | Laporan kerentanan dengan referensi CVE |
| Dependency Audit | Mengaudit paket pihak ketiga untuk CVE, versi usang, risiko lisensi | manifest dependensi (requirements.txt, package-lock.json, dll.) | Laporan dependensi dengan CVE, jalur upgrade, lisensi |
| Security Review | Review sistematis artefak untuk postur keamanan | Artefak yang dihasilkan, konfigurasi, kode | Laporan review keamanan dengan temuan terprioritas |
| Configuration Hardening | Mengidentifikasi default tidak aman dan merekomendasikan hardening | File konfigurasi, baseline keamanan | Rekomendasi hardening yang dipetakan ke benchmark |
| Compliance Mapping | Memetakan temuan ke kerangka kepatuhan | Temuan keamanan, persyaratan kepatuhan | Laporan pemetaan kepatuhan |

### Out of Scope

- Eksekusi exploit langsung
- Incident response produksi
- Pengungkapan kerentanan kepada vendor
- Orkestrasi keamanan dan respons otomatis (SOAR)
- Penetration testing jaringan terhadap infrastruktur langsung
- Operasi hardware security module

---

## Kontrak Publik

### Input Contract: Security Assessment Request

```json
{
  "assessment_id": "uuid",
  "target_type": "code | config | dependency | architecture | full_review",
  "target": {
    "source_code": "string — code content or repository path",
    "config_files": ["string — configuration file contents"],
    "dependencies": ["string — dependency manifest content"],
    "architecture": "object — architecture description"
  },
  "standards": ["OWASP-Top-10", "STRIDE", "CIS", "SOC-2", "ISO-27001", "HIPAA", "PCI-DSS", "NIST-CSF"],
  "include_remediation": true,
  "include_compliance_mapping": true,
  "check_secrets": true,
  "check_dependencies": true,
  "scan_depth": "quick | thorough"
}
```

### Output Contract: Security Assessment Report

```json
{
  "assessment_id": "uuid",
  "target_type": "string",
  "findings": [
    {
      "id": "string",
      "category": "string — OWASP category, STRIDE threat, or CIS benchmark",
      "severity": "critical | high | medium | low",
      "title": "string",
      "description": "string",
      "evidence": "object — file, line, code snippet",
      "remediation": "string",
      "owasp_mapping": "string — OWASP Top 10 category if applicable",
      "compliance_mapping": ["string — compliance frameworks"],
      "confidence": 0.0
    }
  ],
  "secrets": [
    {
      "id": "string",
      "type": "api_key | password | token | certificate | other",
      "location": "string — file path or config section",
      "severity": "critical | high | medium | low",
      "rotation_required": true,
      "confidence": 0.0
    }
  ],
  "dependency_findings": [
    {
      "package": "string",
      "version": "string",
      "severity": "critical | high | medium | low",
      "cve": "string — CVE identifier",
      "description": "string",
      "fix_version": "string",
      "confidence": 0.0
    }
  ],
  "threat_model": {
    "attack_surface": "string — description of exposed surfaces",
    "trust_boundaries": ["string"],
    "data_flows": ["string"],
    "threats": ["string — STRIDE threats identified"],
    "risk_rating": "critical | high | medium | low"
  },
  "summary": {
    "total_findings": 0,
    "critical_count": 0,
    "high_count": 0,
    "medium_count": 0,
    "low_count": 0,
    "overall_risk": "critical | high | medium | low",
    "compliance_score": 0.0,
    "recommendations_count": 0
  },
  "compliance_report": {
    "standards": ["string"],
    "mapped_findings": 0,
    "compliance_percentage": {},
    "gaps": ["string"]
  }
}
```

### Temuan Keamanan (Experience Memory)

```json
{
  "record_id": "uuid",
  "assessment_id": "uuid",
  "timestamp": "ISO 8601",
  "target_type": "string",
  "total_findings": 0,
  "critical_count": 0,
  "high_count": 0,
  "resolved": [
    {"finding_id": "string", "resolution": "string", "timestamp": "ISO 8601"}
  ],
  "false_positives": [
    {"finding_id": "string", "rationale": "string", "timestamp": "ISO 8601"}
  ],
  "fp_rate": 0.0,
  "detection_rate": 0.0
}
```

---

## Titik Integrasi (Capability Graph)

```
Consumer Capability Pack (Code Engineer, Network Engineer, DevOps Assistant)
    │
    │  submits artifact for security assessment via task/intent
    ▼
Execution Runtime
    │
    │  routes to Security Engineer Domain Engine
    ▼
Security Engineer Engine
    │
    │  ┌──────────────────────────────────────────────┐
    │  │ 1. OWASP Top 10 Analysis                     │
    │  │ 2. Secret Detection                          │
    │  │ 3. Dependency Audit                          │
    │  │ 4. Threat Modeling                            │
    │  │ 5. Vulnerability Analysis                     │
    │  │ 6. Configuration Hardening                    │
    │  │ 7. Security Review                             │
    │  │ 8. Compliance Mapping → Experience Memory     │
    │  └──────────────────────────────────────────────┘
    │
    │  returns Security Assessment Report
    ▼
Consumer Capability Pack
    │
    │  receives findings + remediation + compliance mapping
    ▼
User / Human Approval Loop
```

### Template Tugas

| Tugas | Subtugas |
|------|----------|
| Security Assessment | Target analysis → OWASP scan → Secret detection → Dependency audit → Threat modeling → Vulnerability analysis → Hardening review → Compliance mapping → Report |

---

## Capability Pack Konsumen

| Capability Pack Konsumen | Use Case |
|--------------------------|----------|
| **Code Engineer** | Review keamanan kode yang dihasilkan, pemindaian OWASP, deteksi secret di source |
| **DevOps Assistant** | Audit keamanan konfigurasi yang dihasilkan, container hardening, keamanan CI/CD |
| **Network Engineer** | Review keamanan konfigurasi jaringan, analisis firewall policy, audit kepatuhan |
| **System Architect** | Threat modeling untuk proposal arsitektur, validasi security-by-design |

---

## Dependensi

### Dependensi Internal (Shared Contracts)

1. **Execution Runtime** — Routing dan orkestrasi tugas (sesuai ADR-002)
2. **Experience Memory** — Persistensi temuan keamanan (sesuai ADR-011)
3. **Shared Contracts** — Definisi Task/Intent dan skema hasil (sesuai ADR-006)

### Basis Pengetahuan Eksternal

1. **OWASP Top 10 (2021)** — Klasifikasi kerentanan
2. **CWE (Common Weakness Enumeration)** — Taksonomi kelemahan
3. **CVE Database** — Referensi kerentanan yang diketahui
4. **CIS Benchmarks** — Baseline hardening konfigurasi
5. **Kerangka kepatuhan** — SOC 2, ISO 27001, HIPAA, PCI-DSS, NIST-CSF

### Tidak Ada Perubahan Core yang Diperlukan

Semua implementasi berada di dalam Capability Pack Security Engineer:

```
apps/
└── security_engineer/
    ├── engine.py                  # Domain Engine (per ADR-004)
    ├── worker.py                  # Thin adapter (per ADR-003)
    ├── schemas.py                 # Public contracts
    ├── owasp_analyzer.py          # OWASP Top 10 analysis
    ├── threat_modeler.py          # Threat modeling (STRIDE)
    ├── secret_detector.py         # Secret detection
    ├── vulnerability_scanner.py   # Vulnerability analysis
    ├── dependency_auditor.py      # Dependency audit
    ├── hardening_reviewer.py      # Configuration hardening
    ├── compliance_mapper.py       # Compliance mapping
    └── knowledge_base.py          # Security knowledge
```

**Dampak ADR:** Tidak ada. Tidak diperlukan modifikasi Core, Runtime, Kernel, atau shared contract.

---

## Spesifikasi Benchmark

### Kerangka Benchmark

| Dimensi | Definisi | Pengukuran | Target |
|-----------|------------|-------------|--------|
| **Detection Rate** | % kerentanan yang diketahui terdeteksi | % kerentanan ground truth ditemukan | ≥95% |
| **False Positive Rate** | % temuan yang merupakan alarm palsu | False positive / total temuan | <5% |
| **Completeness** | Cakupan semua pemeriksaan keamanan | % pemeriksaan OWASP/STRIDE/CIS yang diterapkan | ≥90% |
| **Explainability** | Kejelasan temuan dan remediasi | Skor evaluasi manusia | ≥90% |
| **Safety** | Tidak ada jaminan keamanan palsu | % temuan yang aman | ≥95% |
| **Efficiency** | Waktu respons dan penggunaan sumber daya | Latency P95 < 3000ms | dalam anggaran |
| **Consistency** | Input yang sama menghasilkan output yang sama | Varian di 10 run < 5% | ≥90% |
| **Compliance Mapping** | % temuan yang dipetakan ke standar | Temuan dipetakan / total temuan | ≥95% |

### Dataset Benchmark

- **100 penilaian keamanan** yang mencakup:
  - Kode: aplikasi Python, JavaScript/TypeScript, SQL, Go, Java
  - Konfigurasi: Docker, Kubernetes, cloud IaC (Terraform), konfigurasi jaringan
  - Dependensi: Python/pip, Node/npm, Go modules, Java/Maven
  - Arsitektur: microservices, monolith, serverless, hybrid

### Detail Dimensi Benchmark

| Tipe Skenario | Deskripsi | Sumber Ground Truth |
|---------------|-------------|---------------------|
| SQL Injection | Pola SQLi klasik dan blind | OWASP Benchmark, DVWA |
| Cross-Site Scripting (XSS) | XSS reflected, stored, DOM-based | OWASP Benchmark |
| Server-Side Request Forgery (SSRF) | SSRF ke endpoint internal/eksternal | SSRF test suites |
| Cross-Site Request Forgery (CSRF) | Token CSRF hilang, masalah same-origin | OWASP Testing Guide |
| Command Injection | Pola injection perintah OS | Injection test suites |
| Secret Exposure | Kredensial hardcoded, token, kunci | Gitleaks, TruffleHog test data |
| Dependency CVE | CVE yang diketahui di paket pihak ketiga | NVD, Snyk, GitHub Advisory |
| Configuration Hardening | Default tidak aman, enkripsi hilang | CIS Benchmarks |

---

## Spesifikasi Golden Test

| # | Skenario | Hasil yang Diharapkan | Kriteria Penerimaan |
|---|----------|-----------------|---------------------|
| 1 | SQL Injection di kode Python | SQLi terdeteksi dengan remediasi | ≥95% deteksi, <5% FP |
| 2 | XSS reflected di JavaScript | XSS terdeteksi dengan remediasi | ≥95% deteksi, <5% FP |
| 3 | SSRF di endpoint API | SSRF terdeteksi dengan remediasi | ≥95% deteksi, <5% FP |
| 4 | CSRF pada endpoint pengubah state | CSRF terdeteksi dengan remediasi | ≥95% deteksi, <5% FP |
| 5 | Command injection di panggilan shell | Injection command terdeteksi | ≥95% deteksi, <5% FP |
| 6 | API key hardcoded di konfigurasi | Secret terdeteksi dengan saran rotasi | ≥95% deteksi, <5% FP |
| 7 | Dependensi dengan CVE yang diketahui | CVE teridentifikasi dengan versi perbaikan | ≥90% deteksi, <5% FP |
| 8 | Konfigurasi Docker tidak aman | Rekomendasi hardening disediakan | ≥90% cakupan, <5% FP |
| 9 | Threat modeling pada arsitektur microservice | Attack surface dan ancaman teridentifikasi | ≥90% cakupan threat |
| 10 | Pemetaan kepatuhan untuk SOC 2 | Temuan dipetakan ke kontrol SOC 2 | ≥95% akurasi pemetaan |

### Kriteria Penerimaan Golden Test

- Semua 10 skenario golden test lulus pada ≥90% dari kriteria penerimaan individu (100% pass)
- Tingkat kelulusan golden test Security Engineer keseluruhan ≥90%
- Tingkat false positive <5% di semua skenario
- Panduan remediasi lengkap dihasilkan untuk setiap temuan

---

## Persyaratan Real Case

### Direktori Real Case

`real_cases/security_engineer/` harus berisi:

| Persyaratan | Jumlah Minimum |
|-------------|---------------|
| Penilaian keamanan nyata dari penggunaan aktual | 20 |
| Kasus dengan temuan secret exposure | 5 |
| Kasus dengan temuan CVE dependensi | 5 |
| Kasus dengan pemetaan kepatuhan (SOC 2/ISO 27001) | 10 |
| Kasus dengan threat modeling | 10 |
| Kasus dengan review/validasi ahli | 15 |

### Struktur Real Case

```
real_cases/security_engineer/<case_id>/
├── input/
│   ├── target_type.md
│   ├── source/                 # Source code, configs, or manifests
│   └── standards.txt           # Applicable security standards
├── output/
│   ├── assessment_report.json  # Full Security Assessment Report
│   └── findings_explanation.md
└── evaluation.md               # Ground truth, expert review, lessons learned
```

### Target Real Case

| Metrik | Target |
|--------|--------|
| Kasus nyata yang dicatat | ≥20 (Level 3) → ≥100 (Level 4) |
| Skor kualitas kasus nyata (review ahli) | ≥90% |
| Temuan divalidasi oleh reviewer manusia | ≥80% |

---

## Definition of Done

```text
Definition of Done — Security Engineer Capability Pack

Functional
- [ ] OWASP Top 10 Analysis detects all 10 categories in code and configs
- [ ] Threat Modeling produces STRIDE analysis with trust boundaries and data flows
- [ ] Secret Detection identifies hardcoded credentials, API keys, tokens
- [ ] Vulnerability Analysis detects known CVEs in application code
- [ ] Dependency Audit covers pip, npm, Go, and Maven dependencies
- [ ] Security Review produces prioritized findings with remediation
- [ ] Configuration Hardening provides CIS-aligned recommendations
- [ ] Compliance Mapping maps findings to SOC 2, ISO 27001, HIPAA, PCI-DSS

Benchmark
- [ ] Detection Rate ≥ 95% (grade A-)
- [ ] False Positive Rate < 5%
- [ ] Threat Coverage ≥ 90%
- [ ] Secret Detection ≥ 95%
- [ ] Dependency CVE Coverage ≥ 90%
- [ ] Compliance Mapping ≥ 95%
- [ ] Explainability ≥ 90%
- [ ] Consistency ≥ 90%

Golden Tests
- [ ] All 10 pack golden test scenarios pass at ≥90% of acceptance criteria (100% pass)

Real Cases
- [ ] ≥ 20 real cases logged in real_cases/security_engineer/
- [ ] Evaluation notes recorded for each case
- [ ] ≥ 5 cases with secret exposure findings
- [ ] ≥ 5 cases with dependency CVE findings
- [ ] ≥ 10 cases with compliance mapping
- [ ] ≥ 10 cases with threat modeling

Documentation
- [ ] Capability Guide updated (CAPABILITY_GUIDE.md — Security Engineer section)
- [ ] API reference / contract updated (this RFC + schemas.py)
- [ ] Real case evaluation summary published

SDK
- [ ] Pack accessible via SDK without Core changes
- [ ] Security Engineer callable via Execution Runtime task routing

Performance
- [ ] Latency P95 < 3000ms for standard assessments
- [ ] Latency P95 < 8000ms for full architecture review

Security
- [ ] No known P0/P1 security issues in the pack itself
- [ ] Security assessments do not execute payloads or exploit vulnerabilities

Regression
- [ ] No regression in existing Capability Pack benchmark dimensions
- [ ] Benchmark reproducible (documented command + persisted result)

Release Notes
- [ ] Capability Changelog updated
```

---

## Risiko

| Risiko | Dampak | Kemungkinan | Mitigasi |
|------|--------|------------|------------|
| Tingkat false positive tinggi merusak kepercayaan | Tinggi — pengguna mengabaikan temuan | Sedang | Kalibrasi berkelanjutan pada 100 penilaian; loop umpan balik FP |
| False negative (kerentanan terlewat) menciptakan rasa aman palsu | Kritis — pelanggaran produksi | Sedang | Pemindaian multi-sumber; confidence scoring; validasi human-in-loop |
| Ketergantungan pada database CVE eksternal (ketersediaan) | Sedang — data kerentanan basi | Rendah | Cache lokal dengan TTL; fallback ke data CVE terakhir yang diketahui |
| Threat modeling terlalu berfokus pada pola yang diketahui | Sedang — melewatkan serangan baru | Sedang | Analisis berbasis pola + heuristik; pembaruan model rutin |
| Pemetaan kepatuhan tertinggal dari pembaruan kerangka | Rendah — data kepatuhan basi | Tinggi | Sinkronisasi kerangka kepatuhan triwulanan; pelacakan versi |
| Latensi pemindaian pada codebase besar | Sedang — memblokir alur kerja developer | Tinggi | Pemindaian inkremental; analisis paralel; caching |
| Deteksi secret menghasilkan false positive pada data test | Sedang — menurunkan kualitas sinyal | Tinggi | Deteksi sadar konteks (jalur test vs prod); dukungan allowlist |

---

## Dampak ADR

**Apakah ini memerlukan perubahan Core?** Tidak.

Security Engineer adalah **Capability Pack baru** yang mengikuti pola yang sudah ada:

- **ADR-001 (Core Pipeline Freeze):** Tidak ada perubahan Core. Semua logika di `apps/security_engineer/`.
- **ADR-002 (Capability Pack Independence):** Security Engineer berkomunikasi dengan pack lain melalui tugas Execution Runtime dan shared contract saja. Tanpa import langsung.
- **ADR-003 (Worker = Adapter Only):** Worker tipis merutekan tugas ke Domain Engine.
- **ADR-004 (Domain Engine Owns Business Logic):** Semua logika analisis keamanan berada di `apps/security_engineer/engine.py`.
- **ADR-005 (Human Approval Required):** Penilaian adalah rekomendasi; remediasi memerlukan persetujuan eksplisit pengguna.
- **ADR-006 (Capability Contract v1 Frozen):** Menggunakan Capability Contract yang ada untuk pendaftaran node dan subtask template. Tidak ada perubahan kontrak.
- **ADR-007 (Conversation Boundary):** Security Engineer dipanggil melalui Execution Runtime, bukan langsung oleh Conversation Manager.
- **ADR-008 (Core Change Requires Cross-Capability Proof):** Tidak berlaku — tidak ada perubahan Core.

**ADR yang Diperlukan:** Tidak ada. Ini adalah Capability Pack baru, bukan modifikasi Core.

---

## Rencana Rollout

### Fase 1: Prototipe (RFC → Experimental)

**Durasi:** 5 minggu

- [ ] Membuat struktur paket `apps/security_engineer/`
- [ ] Mengimplementasikan analyzer OWASP Top 10 (pola SQLi, XSS)
- [ ] Mengimplementasikan deteksi secret dasar
- [ ] Mendefinisikan kontrak publik (Assessment Request, Report)
- [ ] Mengimplementasikan adapter Worker tipis
- [ ] Membuat 10 skenario golden test (tipe serangan inti)
- [ ] Integrasi: Code Engineer → Security Engineer (code scan)
- [ ] Integrasi: Network Engineer → Security Engineer (config audit)
- **Gate:** 10 golden test lulus pada ≥80%

### Fase 2: Kapabilitas Lengkap (Experimental → Stable)

**Durasi:** 8 minggu

- [ ] Mengimplementasikan Threat Modeling (analisis STRIDE)
- [ ] Mengimplementasikan Dependency Audit (pip, npm, Go, Maven)
- [ ] Mengimplementasikan Vulnerability Analysis (korelasi CVE)
- [ ] Mengimplementasikan Configuration Hardening (baseline CIS)
- [ ] Mengimplementasikan Compliance Mapping (SOC 2, ISO 27001)
- [ ] Memperluas golden test menjadi 10 skenario penuh
- [ ] Mencatat ≥20 kasus nyata dari penggunaan Code Engineer dan Network Engineer
- [ ] **Benchmark:** 100 penilaian, ≥95% deteksi, <5% FP
- [ ] **Integrasi:** DevOps Assistant mulai menggunakan Security Engineer untuk keamanan CI/CD
- **Gate:** Semua 10 golden test lulus pada ≥90%; benchmark ≥95% deteksi

### Fase 3: Ekosistem (Stable → Certified)

**Durasi:** 6 minggu

- [ ] Ketiga pack konsumen terintegrasi penuh
- [ ] Pemetaan kepatuhan divalidasi oleh review ahli
- [ ] Dependency audit terintegrasi dengan database CVE nyata
- [ ] Audit independen terhadap akurasi deteksi dan tingkat FP
- [ ] Dashboard benchmark publik tersedia
- [ ] **Benchmark:** ≥95% deteksi, <5% FP berkelanjutan
- [ ] **Real Cases:** ≥100 kasus dengan ≥80% validasi ahli
- **Gate:** Audit independen lulus; benchmark ≥95% berkelanjutan

---

## Peningkatan di Masa Depan

### Fase 2 (Pasca-Rilis v1.0.0)

1. **Interactive Application Security Testing (IAST)** — Analisis keamanan runtime selama testing
2. **Software Composition Analysis (SCA) Deep Integration** — Pemantauan dependensi real-time dengan scoring prediksi exploit (EPSS)
3. **Security Chokepoints** — Pemeriksaan keamanan tertanam di tahap pipeline CI/CD
4. **Threat Intelligence Feed** — Mengorelasikan temuan dengan threat intelligence real-time

### Fase 3 (Enterprise)

1. **Automated Remediation** — Auto-perbaikan temuan berisiko rendah dengan persetujuan manusia (sesuai ADR-005)
2. **Regulatory Reporting** — Menghasilkan laporan kepatuhan siap-audit untuk SOC 2, ISO 27001, HIPAA
3. **Security Scorecard** — Mengagregasi postur keamanan di semua proyek dan workspace
4. **Adversarial Simulation** — Generasi skenario gaya red-team terhadap arsitektur sendiri

### Jangka Panjang

1. **Security-by-Design Advisor** — Panduan keamanan terintegrasi ke dalam desain arsitektur dan kode sejak awal
2. **Vulnerability Prediction** — Prediksi berbasis ML terhadap hotspot keamanan sebelum kode ditulis
3. **Security Knowledge Graph** — Menautkan temuan, CVE, ancaman, dan kontrol kepatuhan dalam satu grafik terpadu
4. **Cross-Workspace Threat Intelligence** — Mengagregasi data ancaman anonim lintas workspace (dengan kontrol privasi)

---

## Persyaratan Real Case

*(Lihat bagian [Persyaratan Real Case](#persyaratan-real-case) di atas untuk spesifikasi lengkap)*

Real case Security Engineer bersumber dari:

1. **Code Engineer** — Review keamanan kode yang dihasilkan dengan validasi pasca-perbaikan
2. **Network Engineer** — Audit konfigurasi dengan verifikasi kepatuhan
3. **DevOps Assistant** — Pemindaian keamanan pipeline CI/CD dengan verifikasi pasca-deployment
4. **System Architect** — Threat modeling arsitektur dengan umpan balik design review

