# Network Engineer — Spesifikasi Capability

**Versi:** 2.1.0
**Status:** Bersertifikat (RFC-0004)
**Target Kualitas:** A+ (≥95) — Level 4 — Pakar Domain

---

## 1. Tujuan

Network Engineer adalah **otoritas jaringan vendor-agnostic** untuk ECP — Capability Pack yang menganalisis konfigurasi, mengaudit keamanan, meninjau desain, memecahkan masalah, merencanakan migrasi, dan memberikan advisori jaringan berbasis bukti.

Capability Pack ini mengintegrasikan 10 modul inti (Analyzer, Security Analyzer, Topology, Design Review, Troubleshooting, Migration Planner, Advisor, Risk Scorer, Generator, Compliance) melalui pipeline rekayasa terstruktur — **tanpa memodifikasi Core**.

---

## 2. Ruang Lingkup

### Dalam Ruang Lingkup
- **Configuration Analysis** — Parsing & validasi konfigurasi
- **Security Audit** — Audit postur keamanan
- **Design Review** — Analisis dan penilaian tingkat topologi
- **Troubleshooting** — Bukti terstruktur → hipotesis → akar penyebab
- **Migration Planning** — Rencana migrasi lintas vendor
- **Advisory** — Pertanyaan desain tingkat tinggi
- **Multi-vendor** — MikroTik RouterOS, Cisco IOS, Fortinet
- **Risk Assessment** — Analisis & rekomendasi risiko

### Di Luar Cakupan
- Push konfigurasi perangkat langsung
- Monitoring real-time
- Simulasi lalu lintas
- Terjemahan lintas vendor (peta jalan masa depan)

---

## 3. Kontrak

### Input: NetworkAnalysisRequest
```json
{
  "type": "text|topology|symptom|query",
  "content": "string (raw config, topology JSON, symptom description, or design question)",
  "vendor_hint": "mikrotik|cisco|fortinet|auto-detect",
  "analysis_type": "audit|topology|design_review|troubleshooting|migration|advisory"
}
```

### Output: NetworkAnalysisReport
```json
{
  "device": "string",
  "vendor": "string",
  "summary": "string",
  "issues": [
    {
      "severity": "critical|high|medium|low",
      "category": "string",
      "description": "string",
      "recommendation": "string",
      "confidence": 0.95
    }
  ],
  "recommendations": [
    {
      "priority": "high|medium|low",
      "problem": "string",
      "why": "string",
      "recommendation": "string"
    }
  ],
  "risk_score": 0.3,
  "design_review": {
    "network_score": 85,
    "availability_grade": "A",
    "security_grade": "B+",
    "scalability_grade": "A-",
    "performance_grade": "A",
    "issues": []
  },
  "troubleshooting": {
    "session_id": "string",
    "hypotheses": [],
    "root_cause": {}
  },
  "migration_plan": {
    "source_vendor": "string",
    "target_vendor": "string",
    "phases": [],
    "estimated_downtime_minutes": 30
  },
  "advisory": {
    "proposals": []
  }
}
```

---

## 4. Operasi

| Operasi | Deskripsi | Input | Output |
|-----------|-------------|--------|---------|
| `audit` | Full security and best-practice audit | config, vendor | NetworkAnalysisReport |
| `analyze_topology` | Infer network topology from config | config, vendor | TopologyReport |
| `review_design` | Design review on topology | topology_json | DesignReviewReport |
| `troubleshoot` | Structured troubleshooting | symptom, evidence | TroubleshootingReport |
| `plan_migration` | Cross-vendor migration plan | source_vendor, target_vendor, requirements | MigrationPlan |
| `advise` | Network design advisory | query, context | AdvisoryReport |

---

## 5. Modul Analyzer

| Modul | File | Tanggung Jawab |
|-------|------|----------------|
| `analyzer.py` | NetworkAnalyzer | Configuration parsing and analysis |
| `analyzer_security.py` | SecurityAnalyzer | Security posture analysis |
| `analyzer_network.py` | NetworkAnalyzer | Network-specific analysis |
| `analyzer_vendor.py` | VendorAnalyzer | Vendor-specific parsing |
| `analyzer_ip_routing.py` | IPRoutingAnalyzer | IP routing analysis |
| `topology.py` | TopologyAnalyzer | Topology inference |
| `design_review.py` | DesignReviewEngine | Design review and scoring |
| `troubleshooting.py` | TroubleshootingEngine | Structured troubleshooting |
| `migration_planner.py` | MigrationPlanner | Cross-vendor migration planning |
| `advisor.py` | NetworkAdvisor | Network design advisory |
| `risk_scorer.py` | RiskScorer | Risk scoring |
| `compliance.py` | ComplianceChecker | Compliance checking |
| `generator.py` | ConfigGenerator | Configuration generation |
| `simulator.py` | ConfigSimulator | Configuration simulation |
| `diff_engine.py` | DiffEngine | Configuration diff |
| `verification_engine.py` | VerificationEngine | Deployment verification |
| `docs_generator.py` | DocsGenerator | Documentation generation |

---

## 6. Dimensi Benchmark

| Dimensi | Target | Grade |
|-----------|--------|-------|
| Accuracy | ≥95% | A+ |
| Precision | ≥95% | A+ |
| Recall | ≥95% | A+ |
| Security Detection | ≥95% | A+ |
| Design Review Quality | ≥95% | A+ |
| Troubleshooting Accuracy | ≥90% | A |
| Migration Plan Quality | ≥90% | A |
| Latency | < 2 detik | A |
| Coverage | ≥90% | A |

---

## 7. Vendor yang Didukung

|Vendor|Format|Status Parser|Status Analyzer|Real Cases|
|--------|--------|---------------|----------------|-----------|
|MikroTik|.rsc, .conf|✅|✅|35|
|Cisco IOS|.conf, .txt|✅|✅|33|
|Fortinet|.conf|✅|✅|33|

---

## 8. Audit Keamanan

### OWASP Top 10
- A01:2021 – Broken Access Control: Unrestricted firewall policies, weak authentication
- A02:2021 – Cryptographic Failures: Weak SNMP community strings, plaintext credentials
- A03:2021 – Injection: Command injection via management interfaces
- A04:2021 – Insecure Design: Single points of failure, lack of redundancy
- A05:2021 – Security Misconfiguration: Default credentials, unnecessary services exposed
- A06:2021 – Vulnerable Components: Outdated firmware, unpatched vulnerabilities
- A07:2021 – Authentication Failures: Weak or absent authentication
- A08:2021 – Data Integrity Failures: Lack of configuration integrity checks
- A09:2021 – Logging Failures: Insufficient audit logging
- A10:2021 – SSRF: Management interface exposure

### Deteksi Rahasia
- SNMP community strings dalam konfigurasi
- Plaintext passwords dalam konfigurasi
- API keys dan tokens
- Private keys dalam konfigurasi

### Pencegahan Injeksi
- Command injection melalui management interfaces
- Configuration injection
- SNMP injection

### Validasi Input
- Validasi sintaks konfigurasi
- Validasi vendor compatibility
- Validasi nilai parameter

### Default Aman
- Firewall default deny
- SSH dengan key-based authentication only
- SNMP dengan v3 dan autentikasi
- Management interface terbatas ke management VLAN

---

## 9. Optimasi Kinerja

### Strategi Caching
- Configuration parse cache (hash-based)
- Analysis result cache untuk konfigurasi yang tidak berubah
- Vendor rule cache untuk analisis berulang

### Peluang Paralelisme
- Parallel analysis untuk banyak konfigurasi
- Independent checks (security, best practice, compliance) paralel
- Multi-vendor analysis paralel

### Optimasi Memori
- Streaming parser untuk konfigurasi besar (>10MB)
- Lazy loading untuk vendor rules
- Disk-based cache untuk large topology graphs

### Efisiensi
- Vendor auto-detection dengan signature matching
- Incremental analysis untuk perubahan kecil
- Rule pre-filtering untuk menghindari false positives

---

## 10. Riwayat Perubahan

| Versi | Tanggal | Perubahan |
|-------|---------|-----------|
| 2.1.0 | 2026-08-05 | Level 4 Domain Expert, A+ grade, 10 golden tests, security audit, performance optimization |
| 2.0.0 | 2026-08-04 | Initial release, 101 real cases, 100% benchmark score |
