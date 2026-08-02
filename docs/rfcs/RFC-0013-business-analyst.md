# RFC-0013: Capability Pack Business Analyst

| Field | Nilai |
|-------|-------|
| **RFC ID** | RFC-0013 |
| **Status** | Draft |
| **Versi** | 0.1.0 |
| **Penulis** | Enal AI OS Core Team |
| **Target Rilis** | v1.3.0 (fase Enterprise) |
| **Capability Pack** | Business Analyst |
| **Capability ID** | `business-analyst` |
| **Kategori** | Business Analysis |
| **Target Kualitas** | A (≥90) |
| **Target Maturity** | Level 3 — Production Ready |
| **RFC Referensi** | RFC-0013 |

---

## Motivasi

Capability Pack ECP yang ada membangun sistem, tetapi tidak ada layer business analysis khusus yang menerjemahkan kebutuhan bisnis menjadi spesifikasi teknis yang dapat dieksekusi oleh pack lain.

Saat ini:

1. **Kebutuhan dikumpulkan secara manual** — kebutuhan bisnis disampaikan sebagai bahasa alami, sering kali dengan ambiguitas, kesenjangan, dan prioritas stakeholder yang bertentangan.
2. **Tidak ada pemodelan proses bisnis** — alur kerja dan proses tidak dimodelkan secara formal sebelum diterjemahkan ke implementasi teknis.
3. **User story dan kriteria penerimaan tidak terstandarisasi** — pack yang berbeda menginterpretasikan kebutuhan secara berbeda.
4. **Tidak ada gap analysis** — perbedaan antara kebutuhan bisnis dan kapabilitas teknis tidak diidentifikasi secara sistematis.
5. **Tidak ada analisis ROI** — keputusan investasi kekurangan analisis return-on-investment yang terkuantifikasi.
6. **BRD dan spesifikasi fungsional dihasilkan secara ad hoc** — tidak ada generasi sistematis Business Requirement Documents atau functional specs.
7. **Tidak ada scoring kualitas kebutuhan** — kebutuhan yang ambigu, tidak lengkap, atau bertentangan tidak ditandai sebelum menyebabkan pengerjaan ulang downstream.

Capability Pack Business Analyst menjadi layer penerjemahan kebutuhan, mengonversi kebutuhan bisnis menjadi spesifikasi yang jelas, tidak ambigu, dan dapat dieksekusi yang dapat dikonsumsi oleh Code Engineer, System Architect, dan semua pack lain.

---

## Pernyataan Masalah

Tanpa Capability Pack Business Analyst yang khusus:

- **Kebutuhan ambigu mencapai pengembangan** — kebutuhan yang tidak jelas, samar, atau bertentangan menyebabkan pengerjaan ulang downstream.
- **Tidak ada pemodelan proses bisnis** — alur kerja kompleks tidak divisualisasikan atau dianalisis sebelum implementasi.
- **User story kekurangan kriteria penerimaan** — story dihasilkan tanpa kondisi penerimaan yang jelas dan dapat diuji.
- **Tidak ada gap analysis** — kebutuhan bisnis vs kapabilitas teknis tidak dibandingkan secara sistematis.
- **ROI tidak dikuantifikasi** — keputusan investasi kekurangan perhitungan return berbasis data.
- **BRD dan spesifikasi fungsional tidak ada** — dokumentasi formal tidak dihasilkan secara sistematis.
- **Konflik stakeholder tidak diselesaikan** — kebutuhan yang bertentangan tidak distrukturkan atau dimediasi.
- **Tidak ada optimasi proses** — proses bisnis tidak dianalisis untuk inefisiensi sebelum implementasi.

Tidak adanya Business Analyst berarti bahwa kebutuhan yang baik — fondasi semua perangkat lunak yang baik — tidak dijamin secara sistematis, menyebabkan pengerjaan ulang yang mahal dan hasil yang buruk.

---

## Tujuan

1. **Requirement Gathering** — Mengumpulkan, menyusun, dan memvalidasi kebutuhan bisnis dari stakeholder.
2. **Business Process Modeling** — Memodelkan alur kerja dan proses menggunakan notasi mirip BPMN.
3. **User Story Generation** — Menghasilkan user story yang terbentuk baik dengan kriteria penerimaan.
4. **Use Case Modeling** — Menghasilkan use case terperinci dari kebutuhan.
5. **BRD Generation** — Menghasilkan Business Requirement Documents dari input mentah.
6. **Functional Specification** — Menghasilkan spesifikasi fungsional yang dapat dieksekusi untuk pack downstream.
7. **Gap Analysis** — Mengidentifikasi dan mendokumentasikan kesenjangan antara kebutuhan bisnis dan kapabilitas teknis.
8. **ROI Analysis** — Mengkuantifikasi return-on-investment untuk fitur atau proyek yang diusulkan.
9. **Process Optimization** — Mengidentifikasi inefisiensi dalam proses bisnis dan merekomendasikan perbaikan.

### Kriteria Keberhasilan

| Metrik | Target | Grade |
|--------|--------|-------|
| Kejelasan Kebutuhan | ≥90% (kebutuhan bebas ambiguitas) | A |
| Kualitas User Story | ≥95% (story dengan kriteria penerimaan lengkap) | A |
| Cakupan Gap Analysis | ≥90% (semua kesenjangan teridentifikasi) | A |
| Akurasi ROI | ≥85% (prediksi ROI dalam ±10% dari aktual) | A |
| Optimasi Proses | ≥80% (inefisiensi teridentifikasi dan ditangani) | A |
| Kelengkapan BRD | ≥95% (semua bagian yang diperlukan ada) | A |
| Konsistensi Stakeholder | ≥90% (konflik teridentifikasi dan diselesaikan) | A |
| Explainability | ≥95% (alasan untuk semua rekomendasi) | A+ |

---

## Non-Tujuan

1. **Fasilitasi stakeholder** — Business Analyst menyusun kebutuhan; ia tidak melakukan pertemuan stakeholder.
2. **Definisi strategi bisnis** — Fokus pada penerjemahan kebutuhan, bukan strategi bisnis.
3. **Menggantikan alat BA khusus** — Alat seperti JIRA, Confluence, Miro tetap dipakai; Business Analyst menyediakan analisis dan generasi.
4. **Manajemen proyek** — Tidak mengelola timeline proyek, sumber daya, atau sprint planning.
5. **Modifikasi Core** — Semua implementasi berada di dalam Capability Pack Business Analyst.

---

## Scope Kapabilitas

### Kapabilitas Inti

| Kapabilitas | Deskripsi | Input | Output |
|-----------|-------------|--------|---------|
| Requirement Gathering | Mengumpulkan, menyusun, dan memvalidasi kebutuhan dari input stakeholder | Kebutuhan bahasa alami, catatan stakeholder, transkrip wawancara | Dokumen kebutuhan terstruktur dengan skor kualitas |
| Business Process Modeling | Memodelkan alur kerja menggunakan notasi mirip BPMN | Deskripsi proses, narasi alur kerja | Model proses dengan activities, gateways, data flows |
| User Story Generation | Menghasilkan user story sesuai INVEST dengan kriteria penerimaan | Kebutuhan, persona, user journeys | User story dengan kriteria penerimaan terperinci |
| Use Case Modeling | Menghasilkan use case terperinci dari kebutuhan | Kebutuhan, peran pengguna, interaksi sistem | Diagram use case dan deskripsi use case terperinci |
| BRD Generation | Menghasilkan Business Requirement Documents | Kebutuhan mentah, konteks bisnis, input stakeholder | Dokumen BRD dengan semua bagian standar |
| Functional Specification | Menghasilkan functional specs yang dapat dieksekusi untuk pack downstream | BRD, user stories, use cases | Spesifikasi fungsional dalam format terstruktur |
| Gap Analysis | Mengidentifikasi kesenjangan antara kebutuhan bisnis dan kapabilitas teknis | Kebutuhan, kondisi saat ini, batasan teknis | Laporan gap analysis dengan prioritisasi |
| ROI Analysis | Mengkuantifikasi return-on-investment untuk fitur yang diusulkan | Estimasi biaya, proyeksi manfaat, timeline | Laporan analisis ROI dengan NPV, payback period |
| Process Optimization | Mengidentifikasi dan merekomendasikan perbaikan proses | Model proses, data performa saat ini | Rekomendasi optimasi proses |

### Out of Scope

- Fasilitasi stakeholder atau manajemen pertemuan
- Perencanaan proyek atau alokasi sumber daya
- Formulasi strategi bisnis
- Perencanaan keuangan di luar analisis ROI
- Implementasi change management
- Eksekusi atau monitoring proses langsung

---

## Kontrak Publik

### Input Contract: Business Analysis Request

```json
{
  "request_id": "uuid",
  "operation": "requirement_gathering | process_modeling | user_story | use_case | brd_generation | functional_spec | gap_analysis | roi_analysis | process_optimization",
  "business_context": {
    "domain": "string — e.g., e-commerce, fintech, healthcare",
    "project_name": "string",
    "description": "string — project overview"
  },
  "inputs": {
    "natural_language_requirements": ["string"],
    "stakeholder_notes": ["string"],
    "interview_transcripts": ["string"],
    "current_state_documentation": "string",
    "technical_constraints": ["string"],
    "personas": [
      {
        "name": "string",
        "role": "string",
        "goals": ["string"],
        "pain_points": ["string"]
      }
    ]
  },
  "quality_attributes": {
    "availability_target": "string",
    "performance_target": "string",
    "security_target": "string"
  },
  "output_format": "json | markdown | bpmn | jira | confluence"
}
```

### Output Contract: Business Analysis Report

```json
{
  "request_id": "uuid",
  "operation": "string",
  "requirements": [
    {
      "id": "string",
      "title": "string",
      "description": "string",
      "type": "functional | non_functional",
      "priority": "must_have | should_have | could_have | won't_have",
      "clarity_score": 0.0,
      "ambiguity_flags": ["string"],
      "source": "string — stakeholder or document source",
      "acceptance_criteria": ["string"],
      "dependencies": ["string"]
    }
  ],
  "user_stories": [
    {
      "id": "string",
      "title": "As a <role> I want <goal> so that <benefit>",
      "description": "string",
      "acceptance_criteria": ["string"],
      "story_points": 0,
      "priority": "must_have | should_have | could_have | won't_have",
      "dependencies": ["string"]
    }
  ],
  "process_models": [
    {
      "id": "string",
      "name": "string",
      "activities": ["string"],
      "gateways": ["string"],
      "data_flows": ["string"],
      "start_event": "string",
      "end_event": "string"
    }
  ],
  "gap_analysis": {
    "current_state": "string",
    "target_state": "string",
    "gaps": [
      {
        "description": "string",
        "impact": "high | medium | low",
        "priority": "critical | high | medium | low",
        "remediation": "string"
      }
    ],
    "capability_gaps": ["string"]
  },
  "roi_analysis": {
    "investment_cost": 0.0,
    "projected_benefits": 0.0,
    "time_horizon_months": 0,
    "npv": 0.0,
    "payback_period_months": 0,
    "irr": 0.0,
    "confidence_score": 0.0
  },
  "optimization_recommendations": [
    {
      "process": "string",
      "inefficiency": "string",
      "recommendation": "string",
      "expected_benefit": "string",
      "effort": "low | medium | high"
    }
  ],
  "quality_metrics": {
    "requirement_clarity": 0.0,
    "story_quality": 0.0,
    "completeness": 0.0,
    "ambiguity_resolution_rate": 0.0
  },
  "summary": {
    "total_requirements": 0,
    "user_stories_count": 0,
    "gaps_identified": 0,
    "recommendations_count": 0,
    "overall_confidence": 0.0,
    "next_steps": ["string"]
  }
}
```

### Catatan Kebutuhan (Experience Memory)

```json
{
  "record_id": "uuid",
  "request_id": "uuid",
  "timestamp": "ISO 8601",
  "requirements_count": 0,
  "user_stories_count": 0,
  "gaps_identified": 0,
  "roi_positive": true,
  "requirements_accepted": 0,
  "outcome": "accepted | partially_accepted | rejected | revised"
}
```

---

## Titik Integrasi (Capability Graph)

```
Business Stakeholder / User
    │
    │  provides natural language requirements
    ▼
Business Analyst Engine
    │
    │  ┌─────────────────────────────────────────────────────┐
    │  │ 1. Requirement Gathering                            │
    │  │ 2. Business Process Modeling                       │
    │  │ 3. User Story Generation                            │
    │  │ 4. Use Case Modeling                                │
    │  │ 5. BRD Generation                                  │
    │  │ 6. Functional Specification                         │
    │  │ 7. Gap Analysis                                     │
    │  │ 8. ROI Analysis                                     │
    │  │ 9. Process Optimization → Experience Memory         │
    │  └─────────────────────────────────────────────────────┘
    │
    │  produces structured functional specification
    ▼
Execution Runtime
    │
    │  routes to consumer Capability Packs (Code Engineer, System Architect, etc.)
    ▼
Consumer Capability Packs
    │
    │  consume functional spec for implementation
    ▼
User / Human Approval Loop
```

### Template Tugas

| Tugas | Subtugas |
|------|----------|
| Business Analysis | Input collection → Requirement gathering → Process modeling → User story generation → Use case modeling → Gap analysis → ROI analysis → Process optimization → Specification generation |

---

## Capability Pack Konsumen

| Capability Pack Konsumen | Use Case |
|--------------------------|----------|
| **Code Engineer** | Mengonsumsi functional specs untuk menghasilkan kode dan test |
| **System Architect** | Mengonsumsi functional specs untuk desain arsitektur |
| **DevOps Assistant** | Mengonsumsi kebutuhan deployment dan spesifikasi infrastruktur |
| **Decision Intelligence** | Mengevaluasi ROI dan risiko dari inisiatif bisnis yang diusulkan |
| **Self Development** | Mengidentifikasi peluang perbaikan proses bisnis |

---

## Dependensi

### Dependensi Internal (Shared Contracts)

1. **Execution Runtime** — Routing dan orkestrasi tugas (sesuai ADR-002)
2. **Experience Memory** — Persistensi catatan kebutuhan dan keputusan (sesuai ADR-011)
3. **Shared Contracts** — Definisi Task/Intent dan skema hasil (sesuai ADR-006)

### Pengetahuan Eksternal

1. **BABOK (Business Analysis Body of Knowledge)** — Praktik BA standar
2. **BPMN** — Business Process Model and Notation
3. **INVEST Criteria** — Kerangka kualitas user story
4. **ROI/NPV/IRR** — Metodologi analisis keuangan

### Tidak Ada Perubahan Core yang Diperlukan

Semua implementasi berada di dalam Capability Pack Business Analyst:

```
apps/
└── business_analyst/
    ├── engine.py              # Domain Engine (per ADR-004)
    ├── worker.py              # Thin adapter (per ADR-003)
    ├── schemas.py             # Public contracts
    ├── requirement_gatherer.py  # Requirement gathering and structuring
    ├── process_modeler.py     # Business process modeling (BPMN-like)
    ├── story_generator.py     # User story generation
    ├── use_case_modeler.py    # Use case modeling
    ├── brd_generator.py       # BRD generation
    ├── spec_generator.py      # Functional specification generation
    ├── gap_analyzer.py        # Gap analysis
    ├── roi_calculator.py      # ROI analysis
    └── optimizer.py           # Process optimization
```

**Dampak ADR:** Tidak ada. Tidak diperlukan modifikasi Core, Runtime, Kernel, atau shared contract.

---

## Spesifikasi Benchmark

### Kerangka Benchmark

| Dimensi | Definisi | Pengukuran | Target |
|-----------|------------|-------------|--------|
| **Requirement Clarity** | % kebutuhan bebas ambiguitas | Review ahli terhadap kualitas kebutuhan | ≥90% |
| **User Story Quality** | % story dengan kriteria penerimaan lengkap | Kriteria penerimaan ada / story | ≥95% |
| **Gap Analysis Coverage** | % kesenjangan bisnis-teknis teridentifikasi | Kesenjangan ditemukan / ground truth kesenjangan | ≥90% |
| **ROI Accuracy** | Prediksi ROI sesuai hasil aktual | ROI diprediksi vs aktual dalam ±10% | ≥85% |
| **Process Optimization** | % inefisiensi teridentifikasi dan ditangani | Perbaikan ditemukan / total inefisiensi | ≥80% |
| **BRD Completeness** | % bagian BRD yang diperlukan ada | Bagian ada / total yang diharapkan | ≥95% |
| **Stakeholder Consistency** | % konflik teridentifikasi dan diselesaikan | Konflik diselesaikan / total konflik | ≥90% |
| **Explainability** | Kejelasan alasan untuk rekomendasi | Skor evaluasi manusia | ≥95% |
| **Consistency** | Input yang sama menghasilkan spec yang sama | Varian di 10 run < 5% | ≥90% |

### Dataset Benchmark

- **100 kasus bisnis** yang mencakup:
  - E-commerce (inventory, checkout, recommendation)
  - Fintech (platform trading, penilaian risiko, kepatuhan)
  - Healthcare (manajemen pasien, penjadwalan janji temu)
  - SaaS (platform multi-tenant, billing, analitik)
  - Enterprise (otomasi alur kerja, reporting, integrasi)

### Detail Dimensi Benchmark

| Tipe Skenario | Deskripsi | Ground Truth |
|---------------|-------------|-------------|
| Ambiguous Requirements | Kebutuhan dengan bahasa tidak jelas | Disambiguasi ahli |
| Conflicting Stakeholder Needs | Stakeholder dengan prioritas berlawanan | Catatan resolusi konflik |
| Missing Acceptance Criteria | Story tanpa kondisi yang dapat diuji | Kriteria yang dilengkapi ahli |
| Process Optimization | Proses bisnis tidak efisien | Catatan perbaikan proses |

---

## Spesifikasi Golden Test

| # | Skenario | Hasil yang Diharapkan | Kriteria Penerimaan |
|---|----------|-----------------|---------------------|
| 1 | Kebutuhan ambigu ("sistem cepat") | Kebutuhan diklarifikasi dengan kriteria terukur | ≥90% peningkatan kejelasan |
| 2 | Kebutuhan stakeholder bertentangan (keamanan vs kegunaan) | Konflik teridentifikasi dan dimediasi | ≥90% resolusi |
| 3 | Kriteria penerimaan hilang di user story | Kriteria dihasilkan dengan kondisi yang dapat diuji | ≥95% kelengkapan |
| 4 | Proses dengan inefisiensi (langkah persetujuan manual) | Bottleneck teridentifikasi dengan saran otomasi | ≥85% deteksi |
| 5 | Analisis ROI dengan data biaya/manfaat | NPV, payback, IRR dihitung | ≥85% akurasi vs aktual |
| 6 | Gap analysis (kondisi saat ini vs target) | Kesenjangan teridentifikasi dengan prioritas | ≥90% cakupan |
| 7 | BRD generation dari catatan mentah | BRD lengkap dengan semua bagian | ≥95% kelengkapan |
| 8 | Use case modeling dari kebutuhan | Use case terperinci dengan aktor dan alur | ≥90% kelengkapan |
| 9 | Functional specification untuk Code Engineer | Spec terstruktur yang dapat dikonsumsi Code Engineer | ≥90% kegunaan |
| 10 | Model proses bisnis dari deskripsi alur kerja | Model mirip BPMN dengan activities dan gateways | ≥90% akurasi |

### Kriteria Penerimaan Golden Test

- Semua 10 skenario golden test lulus pada ≥90% dari kriteria penerimaan individu (100% pass)
- Tingkat kelulusan golden test Business Analyst keseluruhan ≥90%
- Semua user story yang dihasilkan memiliki kriteria penerimaan lengkap
- Perhitungan ROI divalidasi terhadap standar keuangan

---

## Persyaratan Real Case

### Direktori Real Case

`real_cases/business_analyst/` harus berisi:

| Persyaratan | Jumlah Minimum |
|-------------|---------------|
| Kasus business analysis nyata dari penggunaan aktual | 20 |
| Kasus dengan kebutuhan ambigu | 5 |
| Kasus dengan kebutuhan stakeholder bertentangan | 5 |
| Kasus dengan kriteria penerimaan hilang | 5 |
| Kasus dengan analisis ROI | 10 |
| Kasus dengan optimasi proses | 5 |
| Kasus dengan review/validasi ahli | 15 |

### Struktur Real Case

```
real_cases/business_analyst/<case_id>/
├── input/
│   ├── raw_requirements/       # Natural language requirements, stakeholder notes
│   ├── business_context.md      # Domain and project description
│   └── constraints.md           # Technical and business constraints
├── output/
│   ├── analysis_report.json    # Full Business Analysis Report
│   ├── functional_spec.md      # Generated functional specification
│   ├── user_stories.jsonl      # Generated user stories
│   └── roi_analysis.md         # ROI calculation details
└── evaluation.md               # Ground truth, expert review, lessons learned
```

### Target Real Case

| Metrik | Target |
|--------|--------|
| Kasus nyata yang dicatat | ≥20 (Level 3) → ≥100 (Level 4) |
| Skor kualitas kasus nyata (review ahli) | ≥90% |
| Kebutuhan diterima downstream | ≥85% spec yang dihasilkan digunakan tanpa revisi besar |

---

## Definition of Done

```text
Definition of Done — Business Analyst Capability Pack

Functional
- [ ] Requirement Gathering collects, structures, and validates requirements with quality scoring
- [ ] Business Process Modeling produces BPMN-like models from workflow descriptions
- [ ] User Story Generation produces INVEST-compliant stories with acceptance criteria
- [ ] Use Case Modeling generates detailed use cases with actors and flows
- [ ] BRD Generation produces complete Business Requirement Documents
- [ ] Functional Specification generates structured specs consumable by downstream packs
- [ ] Gap Analysis identifies and prioritizes business-technical gaps
- [ ] ROI Analysis calculates NPV, payback period, and IRR with confidence scoring
- [ ] Process Optimization identifies inefficiencies and recommends improvements

Benchmark
- [ ] Requirement Clarity ≥ 90% (grade A)
- [ ] User Story Quality ≥ 95%
- [ ] Gap Analysis Coverage ≥ 90%
- [ ] ROI Accuracy ≥ 85%
- [ ] Process Optimization ≥ 80%
- [ ] BRD Completeness ≥ 95%
- [ ] Stakeholder Consistency ≥ 90%
- [ ] Explainability ≥ 95%
- [ ] Consistency ≥ 90%

Golden Tests
- [ ] All 10 pack golden test scenarios pass at ≥90% of acceptance criteria (100% pass)

Real Cases
- [ ] ≥ 20 real cases logged in real_cases/business_analyst/
- [ ] Evaluation notes recorded for each case
- [ ] ≥ 5 cases with ambiguous requirements
- [ ] ≥ 5 cases with conflicting stakeholder needs
- [ ] ≥ 5 cases with missing acceptance criteria
- [ ] ≥ 10 cases with ROI analysis
- [ ] ≥ 5 cases with process optimization

Documentation
- [ ] Capability Guide updated (CAPABILITY_GUIDE.md — Business Analyst section)
- [ ] API reference / contract updated (this RFC + schemas.py)
- [ ] Real case evaluation summary published

SDK
- [ ] Pack accessible via SDK without Core changes
- [ ] Business Analyst callable via Execution Runtime task routing

Performance
- [ ] Latency P95 < 3000ms for standard business analysis
- [ ] Latency P95 < 8000ms for multi-stakeholder ROI analysis

Security
- [ ] No known P0/P1 security issues
- [ ] Generated documents do not expose confidential stakeholder information

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
| Kebutuhan ambigu salah diinterpretasikan | Tinggi — pengerjaan ulang downstream | Tinggi | Interpretasi konservatif; confidence scoring; review stakeholder diperlukan |
| Analisis ROI tidak akurat | Sedang — keputusan investasi buruk | Sedang | Analisis sensitivitas; interval confidence; kalibrasi historis |
| Rekomendasi optimasi proses tidak praktis | Sedang — usaha terbuang | Sedang | Estimasi usaha disertakan; validasi ahli pada kasus nyata |
| User story tidak sesuai ekspektasi developer | Sedang — gesekan pengembangan | Tinggi | Loop umpan balik developer; review story dengan Code Engineer |
| BRD/functional spec terlalu panjang atau terlalu ringkas | Sedang — konsumsi downstream buruk | Tinggi | Berbasis template dengan tingkat detail yang dapat dikonfigurasi; validasi downstream |
| Gap analysis melewatkan kesenjangan kritis | Tinggi — implementasi tidak lengkap | Sedang | Analisis multi-perspektif; cross-check stakeholder |
| Pemodelan proses menyederhanakan alur kerja kompleks secara berlebihan | Sedang — analisis salah | Sedang | Penyempurnaan inkremental; checkpoint validasi stakeholder |

---

## Dampak ADR

**Apakah ini memerlukan perubahan Core?** Tidak.

Business Analyst adalah **Capability Pack baru** yang mengikuti pola yang sudah ada:

- **ADR-001 (Core Pipeline Freeze):** Tidak ada perubahan Core. Semua logika di `apps/business_analyst/`.
- **ADR-002 (Capability Pack Independence):** Business Analyst berkomunikasi dengan pack lain melalui tugas Execution Runtime dan shared contract saja. Tanpa import langsung.
- **ADR-003 (Worker = Adapter Only):** Worker tipis merutekan tugas ke Domain Engine.
- **ADR-004 (Domain Engine Owns Business Logic):** Semua logika business analysis berada di `apps/business_analyst/engine.py`.
- **ADR-005 (Human Approval Required):** Semua kebutuhan dan rekomendasi memerlukan persetujuan stakeholder manusia sebelum konsumsi downstream.
- **ADR-006 (Capability Contract v1 Frozen):** Menggunakan Capability Contract yang ada untuk pendaftaran node dan subtask template. Tidak ada perubahan kontrak.
- **ADR-007 (Conversation Boundary):** Business Analyst dipanggil melalui Execution Runtime, bukan langsung oleh Conversation Manager.
- **ADR-008 (Core Change Requires Cross-Capability Proof):** Tidak berlaku — tidak ada perubahan Core.

**ADR yang Diperlukan:** Tidak ada. Ini adalah Capability Pack baru, bukan modifikasi Core.

---

## Rencana Rollout

### Fase 1: Prototipe (RFC → Experimental)

**Durasi:** 5 minggu

- [ ] Membuat struktur paket `apps/business_analyst/`
- [ ] Mengimplementasikan requirement gathering dengan quality scoring
- [ ] Mengimplementasikan user story generation dengan kriteria penerimaan
- [ ] Mengimplementasikan BRD generation (sebagian — bagian inti)
- [ ] Mendefinisikan kontrak publik (BA Request, BA Report)
- [ ] Mengimplementasikan adapter Worker tipis
- [ ] Membuat 10 skenario golden test
- [ ] Integrasi: Code Engineer ← Business Analyst (konsumsi functional spec)
- [ ] Integrasi: Self Development ← Business Analyst (optimasi proses)
- **Gate:** 10 golden test lulus pada ≥80%

### Fase 2: Kapabilitas Lengkap (Experimental → Stable)

**Durasi:** 8 minggu

- [ ] Mengimplementasikan business process modeling (mirip BPMN)
- [ ] Mengimplementasikan use case modeling
- [ ] Mengimplementasikan gap analysis
- [ ] Mengimplementasikan ROI analysis (NPV, payback, IRR)
- [ ] Mengimplementasikan process optimization
- [ ] Menyelesaikan BRD generation (semua bagian)
- [ ] Mengimplementasikan generasi functional specification
- [ ] Memperluas golden test menjadi 10 skenario penuh
- [ ] Mencatat ≥20 kasus nyata dari penggunaan Code Engineer dan perencanaan proyek
- [ ] **Benchmark:** 100 kasus bisnis, ≥90% kejelasan, ≥95% kualitas story
- [ ] **Integrasi:** System Architect mulai mengonsumsi functional specs dari Business Analyst
- [ ] **Integrasi:** DevOps Assistant mulai mengonsumsi kebutuhan infrastruktur dari Business Analyst
- **Gate:** Semua 10 golden test lulus pada ≥90%; benchmark ≥90%

### Fase 3: Ekosistem (Stable → Certified)

**Durasi:** 6 minggu

- [ ] Keempat pack konsumen terintegrasi
- [ ] Analisis ROI divalidasi terhadap standar keuangan
- [ ] Optimasi proses divalidasi pada proses bisnis nyata
- [ ] Functional specs divalidasi melalui konsumsi Code Engineer
- [ ] Audit independen terhadap kualitas kebutuhan dan gap analysis
- [ ] Dashboard benchmark publik tersedia
- [ ] **Benchmark:** ≥90% di semua dimensi berkelanjutan
- [ ] **Real Cases:** ≥100 kasus dengan ≥80% adopsi downstream
- **Gate:** Audit independen lulus; benchmark ≥90% berkelanjutan

---

## Peningkatan di Masa Depan

### Fase 2 (Pasca-Rilis v1.0.0)

1. **Stakeholder Simulation** — Memodelkan perspektif stakeholder yang berbeda dan menyelesaikan konflik secara otomatis
2. **Requirements Traceability Matrix** — Ketertelusuran end-to-end dari kebutuhan bisnis ke kode dan test
3. **Acceptance Criteria Auto-Generation untuk QA** — Memberi makan kriteria penerimaan langsung ke QA Engineer untuk generasi test
4. **Business Impact Forecasting** — Memprediksi dampak downstream dari perubahan kebutuhan pada kode, test, dan deployment

### Fase 3 (Enterprise)

1. **Multi-Project Portfolio Analysis** — Menganalisis dan memprioritaskan kebutuhan di seluruh portofolio proyek
2. **Business Architecture Integration** — Menghubungkan kapabilitas bisnis ke arsitektur teknis
3. **Regulatory Compliance Requirements** — Menghasilkan kebutuhan yang dipetakan kepatuhan (GDPR, HIPAA, SOX)
4. **Business Process Automation Discovery** — Mengidentifikasi peluang otomasi dari model proses

### Jangka Panjang

1. **AI-Powered Requirements Discovery** — Mewawancarai stakeholder dan mengekstrak kebutuhan dari percakapan
2. **Requirements Evolution Management** — Melacak perubahan kebutuhan dan dampak berjenjangnya
3. **Business Value Stream Mapping** — Analisis value stream end-to-end dari kebutuhan bisnis ke hasil pelanggan
4. **Automated Business Case Generation** — Dokumen business case lengkap dari kebutuhan dan analisis ROI

