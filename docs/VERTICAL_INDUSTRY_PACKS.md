# Vertical Industry Packs — Production Guide

**Document Status:** Active
**Target Release:** v3.0.0
**Owner:** Vertical Solutions Team

---

## Overview

Vertical Industry Packs (VIP) are specialized Capability Packs designed for
regulated industry domains. Unlike general-purpose packs, VIPs require
**jurisdiction-specific compliance**, **sector-specific data handling**, and
**domain-qualified review** before production deployment.

This document consolidates the four VIPs in ECP v3.0.0:

| Pack | RFC | Industry | Compliance Frameworks |
|------|-----|----------|-----------------------|
| Finance Analyst | RFC-0030 | Financial Services | SOX, Basel III, MiFID II |
| Legal Advisor | RFC-0031 | Legal Services | GDPR, eDiscovery, Bar Rules |
| HSE Specialist | RFC-0032 | Health/Safety/Environment | ISO 45001, OSHA, EPA |
| Supply Chain Analyst | RFC-0036 | Logistics & Supply Chain | ISO 28000, C-TPAT, GDPR |

---

## 1. Finance Analyst (RFC-0030)

**Category:** Vertical Industry — Financial Services
**Target Grade:** A (90.5%)
**Real Cases:** 10 in `real_cases/finance_analyst/`

### Regulatory Context
- **Investment Advice Disclaimer**: This pack does NOT provide personalized investment advice.
  All outputs are analytical and for informational purposes only.
- **SOX Compliance**: Financial calculations must be traceable and auditable.
  The pack enforces explicit input requirements (currency, units) to prevent ambiguity.
- **Data Handling**: Uses sandbox execution for any financial modeling. No direct
  access to trading systems or broker APIs without explicit user authorization.

### Core Capabilities
1. **Financial Summary** — rasio keuangan (gross margin, current ratio)
2. **Cash Flow Runway** — Estimasi runway dari kas dan burn rate
3. **Scenario Analysis** — Model sensitivitas untuk asumsi revenue
4. **Risk Modeling** — Bandingkan skenario downside dengan baseline
5. **Control Check** — Peta bukti kontrol ke checklist terversi

### Input Requirements
- `currency`: Kode mata uang yang jelas (USD, EUR, IDR, dll)
- `revenue`, `cost_of_goods_sold`, `current_assets`, `current_liabilities`
- `cash_balance`, `monthly_net_burn`
- `baseline_revenue`, `margin`, `revenue_changes_pct[]`

### Safety Boundaries
- **Tidak memberikan saran investasi individual** — Semua output informatif
- **Mensyaratkan unit/label mata uang** — Tolak input ambigu
- **Melaporkan denominator yang hilang** — Jangan bagi dengan nol
- **certification_claim = false** — Tidak boleh mendklaim kepatuhan dari bukti tidak cukup

### Deployment Notes
- Deploy di environment yang terisolasi dari sistem trading produksi
- Audit trail harus dipertahankan minimal 7 tahun untuk SOX
- Semua input/output harus ter-enkripsi at-rest

---

## 2. Legal Advisor (RFC-0031)

**Category:** Vertical Industry — Legal Services
**Target Grade:** A (90.3%)
**Real Cases:** 10 in `real_cases/legal_advisor/`

### Regulatory Context
- **Attorney-Client Privilege**: Semua interaksi yang memuat saran hukum harus
  dilindungi. Log tidak boleh berisi nasihat hukum spesifik.
- **GDPR eDiscovery**: Dokumen yang diproses harus mematuhi retention policy
  dan right-to-be-forgotten.
- **Bar Rules Compliance**: Output bersifat assistif, bukan pengganti kuasa hukum
  yang berlisensi.

### Core Capabilities
1. **Clause Extraction** — Ekstrak klausal dari dokumen dengan lokasi sumber
2. **Clause Deviation Check** — Bandingkan dengan playbook yang disetujui
3. **Obligation Registration** — Ekstrak pihak, aksi, trigger, deadline
4. **Conflict Detection** — Identifikasi ketidakkonsistenan antar sumber
5. **Source Summarization** — Ringkasan dokumen hukum dengan referensi sumber

### Input Requirements
- `document_id`, `text`, `page`
- `playbook_id`, `playbook_rule`
- `source_document`, `source_id`, `jurisdiction`, `effective_date`
- `approved_sources[]`: Daftar sumber yang dipercaya

### Safety Boundaries
- **Tidak mengeluarkan nasiah hukum** — Output assistif, bukan pengganti kuasa hukum
- **Hanya mengandalkan sumber yang disetujui** — Tolak sumber di luar registry
- **Mensyurfatkan abstain** — Jika tidak ada sumber yang mendukung, jangan ambil kesimpulan
- **Meminta yurisdi** — Untuk analisis bergantung yurisdi, minta input sebelum memproses

### Deployment Notes
- Hanya sumber hukum yang disetujui yang dapat diproses
- Semua dokumen harus melalui pipeline consent management
- Retention policy: semua dokumen hukum wajib disimpan 10 tahun
- Integrasi dengan Document Processing pack untuk parsing DOCX/PDF

---

## 3. HSE Specialist (RFC-0032)

**Category:** Vertical Industry — Health/Safety/Environment
**Target Grade:** A (90.8%)
**Real Cases:** 10 in `real_cases/hse_specialist/`

### Regulatory Context
- **OSHA Compliance**: Hazard identification harus mengikuti
  OSHA 29 CFR 1910 standar.
- **ISO 45001**: Risk scoring menggunakan hierarki kontrol (elimination,
  substitution, engineering, administrative, PPE).
- **EPA Environmental**: Environmental impact harus dilaporkan
  terpisah dari occupational safety.

### Core Capabilities
1. **Hazard Identification** — Identifikasi bahaya dari deskripsi tugas dan lokasi
2. **Risk Scoring** — Skor risiko dengan matriks likelihood × severity (1-5)
3. **Control Review** — Evaluasi efektivitas kontrol yang ada
4. **Incident Analysis** — Organisir narratif insiden ke timeline dan faktor
5. **Compliance Checking** — Periksa kesenjangan kepatuhan (ISO 45001, OSHA)

### Input Requirements
- `task`: Deskripsi tugas kerja yang akan dianalisis
- `site_context`: Konteks lokasi kerja
- `hazard`, `likelihood` (1-5), `severity` (1-5)
- `existing_controls[]`: Daftar kontrol yang sudah ada
- `standard`: Standar kepatuhan (ISO 45001, OSHA-1910, dll)

### Safety Boundaries
- **Tidak mengeluarkan perintah operasional** — Tidak kontrol peralatan secara autonom
- **Tidak mengganti penilaian profesional HSE** — Semua output assistif, membutuhkan review
- **Mensyaratkan likelihood dan severity** — Jangan hitung risiko jika data tidak lengkap
- **Eskalasi bahaya mendadak** — Ikuti prosedur situs untuk bahaya kritis

### Deployment Notes
- Integrasi dengan Safety Instrumented System (SIS) membutuhkan approval manual
- Semua risk assessment harus ditandatangani oleh HSE professional terlisensi
- Site-specific konfigurasi diperlukan (regional OSHA standards, lokal regulations)

---

## 4. Supply Chain Analyst (RFC-0036)

**Category:** Vertical Industry — Logistics & Supply Chain
**Target Grade:** A (91.0%)
**Real Cases:** 10 in `real_cases/supply-chain-analyst/`

### Regulatory Context
- **ISO 28000**: Sistem manajemen keamanan rantai pasok
- **C-TPAT**: Customs-Trusted Trader program untuk keamanan supply chain
- **GDPR**: Data pelanggan dan rantai pasok harus dilindungi
- **Import/Export Compliance**: ECCN, ITAR, dan tariff compliance

### Core Capabilities
1. **Demand Forecasting** — Prediksi permintaan dengan model statistik
2. **Inventory Optimization** — Optimasi stok dengan metode EOQ dan safety stock
3. **Risk Assessment** — Identifikasi risiko supplier, geografi, dan bahan baku
4. **Route Optimization** — Optimasi rute pengiriman dengan biaya dan lead time

### Input Requirements
- `analysis_type`: demand_forecast | inventory_optimization | risk_assessment | route_optimization
- `historical_data`: Data permintaan historis
- `suppliers[]`: Daftar supplier dengan lokasi, rating, lead time
- `products[]`: Daftar produk dengan permintaan, lead time, biaya
- `constraints`: Kapasitas gudang, budget, service level

### Safety Boundaries
- **Tidak mengganti sistem SCM** — Output assistif, integrasi manual
- **Data supplier harus terverifikasi** — Tolak sumber yang tidak diverifikasi
- **Lead time dan ketersediaan harus eksplisit** — Jangan asumsi nilai default
- **Environmental impact** harus dipertimbangkan dalam risk assessment

### Deployment Notes
- Integrasi dengan ERP/SCM sistem membutuhkan API gateway dan rate limiting
- Data supplier harus melalui vetting keamanan sebelum pemrosesan
- Semua perhitungan harus reproducible dan teraudit

---

## Cross-Pack Integration Patterns

### Finance Analyst ↔ Supply Chain Analyst
- Supply Chain cost data feeds ke Finance Analyst untuk working capital analysis
- Finance Analyst risk scenarios memicu Supply Chain contingency planning
- Shared reference data: currency, units, time periods

### Legal Advisor ↔ Compliance Officer
- Legal Advisor clause extraction feeds Compliance Officer control mapping
- Compliance Officer framework requirements drive Legal Advisor playbook rules
- Shared registry: approved legal sources, contract templates

### HSE Specialist ↔ Infrastructure Engineer
- HSE site hazard data informs Infrastructure design reviews
- Infrastructure Engineer safety controls feed HSE control effectiveness scoring
- Shared reference: facility layouts, equipment specifications

### Cross-Capability Dependencies
| VIP | Consumes From | Provides To |
|-----|---------------|-------------|
| Finance Analyst | Infrastructure Engineer, System Architect | Product Manager, Compliance Officer |
| Legal Advisor | Compliance Officer, Knowledge Engineer | Compliance Officer, Data Engineer |
| HSE Specialist | Compliance Officer, Infrastructure Engineer | Infrastructure Engineer, DevOps Assistant |
| Supply Chain Analyst | Data Engineer, Infrastructure Engineer | Finance Analyst, Product Manager |

---

## Governance Requirements

Sebelum mengaktifkan Vertical Industry Pack di production:

1. **Domain Owner Approval** — Setiap VIP membutuhkan persetujuan dari professional
   yang berlisensi di bidangnya (CFO, General Counsel, HSE Director, Supply Chain VP)
2. **Data Residency** — Pastikan data industri vertikal sesuai regional regulations
3. **Audit Trail** — Semua interaksi harus ter-log dan dapat di-audit
4. **Review Cycle** — Paling sedikit bulanan review oleh domain owner
5. **Incident Escalation** — Prosedur eskalasi untuk VIP-specific risks harus didokumentasikan

---

## Production Readiness Checklist — VIP

- [ ] Domain owner identified dan terlibat
- [ ] Regulatory compliance framework teridentifikasi
- [ ] Data handling & retention policy didokumentasikan
- [ ] Safety boundaries diverifikasi oleh security team
- [ ] Integration test dengan pack konsumen selesai
- [ ] Audit trail dikonfigurasi ke ELK/Loki
- [ ] Alerting dikonfigurasi untuk VIP-specific failure modes
- [ ] Training dokumen tersedia untuk end users
- [ ] Incident escalation path didokumentasikan
