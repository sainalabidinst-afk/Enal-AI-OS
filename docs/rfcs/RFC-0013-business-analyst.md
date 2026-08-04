# RFC-0013: Capability Pack Business Analyst

|Bidang|Nilai|
|-------|-------|
|**ID RFC**|RFC-0013|
|**Status**|Draf|
|**Versi**|0.1.0|
|**Penulis**|Tim Inti AI OS Akhir|
|**Target Rilis**|v1.3.0 (fase Perusahaan)|
|**Capability Pack**|Business Analyst|
|**ID Kemampuan**|`business-analyst`|
|**Kategori**|Analisis Bisnis|
|**Target Kualitas**|A (≥90)|
|**Target Kematangan**|Level 3 — Siap Produksi|
|**Referensi RFC**|RFC-0013|

---

## Motivasi

Capability Pack ECP yang ada membangun sistem, tetapi tidak ada lapisan analisis bisnis khusus yang menerjemahkan kebutuhan bisnis menjadi spesifikasi teknis yang dapat dieksekusi oleh paket lain.

Saat ini:

1. **Kebutuhan dikumpulkan secara manual** — kebutuhan bisnis disampaikan sebagai bahasa alami, sering kali dengan ambiguitas, keselarasan, dan prioritas pemangku kepentingan yang berbeda.
2. **Tidak ada pemodelan proses bisnis** — alur kerja dan proses tidak dimodelkan secara formal sebelum diterjemahkan ke implementasi teknis.
3. **User story dan kriteria penerimaan tidak terstandarisasi** — paket yang berbeda menginterpretasikan kebutuhan secara berbeda.
4. **Tidak ada gap analysis** — perbedaan antara kebutuhan bisnis dan kapabilitas teknis tidak teridentifikasi secara sistematis.
5. **Tidak ada analisis ROI** — keputusan investasi kekurangan analisis return-on-investment yang terkuantifikasi.
6. **BRD dan spesifikasi fungsional dihasilkan secara ad hoc** — tidak ada generasi Dokumen Kebutuhan Bisnis yang sistematis atau spesifikasi fungsional.
7. **Tidak ada scoring kualitas kebutuhan** — kebutuhan yang ambigu, tidak lengkap, atau berbeda tidak ditandai sebelum menyebabkan pengerjaan ulang downstream.

Capability Pack Business Analyst menjadi lapisan penerjemahan kebutuhan, mengubah kebutuhan bisnis menjadi spesifikasi yang jelas, tidak ambigu, dan dapat eksekusi yang dapat dikonsumsi oleh Code Engineer, System Architect, dan semua paket lainnya.

---

## Pernyataan Masalah

Tanpa Capability Pack Business Analyst yang khusus:

- **Kebutuhan ambigu mencapai pengembangan** — kebutuhan yang tidak jelas, samar, atau berbeda menyebabkan pengerjaan ulang hilir.
- **Tidak ada pemodelan proses bisnis** — alur kerja kompleks tidak divisualisasikan atau dijelaskan sebelum diimplementasikan.
- **User story kekurangan kriteria penerimaan** — story dihasilkan tanpa kondisi penerimaan yang jelas dan dapat diuji.
- **Tidak ada gap analysis** — kebutuhan bisnis vs kapabilitas teknis tidak dibandingkan secara sistematis.
- **ROI tidak dikuantifikasi** — keputusan investasi kekurangan perhitungan return berbasis data.
- **BRD dan spesifikasi fungsional tidak ada** — dokumentasi formal tidak dihasilkan secara sistematis.
- **Konflik pemangku kepentingan tidak terselesaikan** — kebutuhan yang dipisahkan tidak distrukturkan atau dimediasi.
- **Tidak ada proses optimasi** — proses bisnis tidak dianalisis untuk inefisiensi sebelum implementasi.

Tidak adanya Business Analyst berarti bahwa kebutuhan yang baik — fondasi semua perangkat lunak yang baik — tidak dijamin secara sistematis, menyebabkan pengerjaan ulang yang mahal dan hasil yang buruk.

---

## Tujuan

1. **Requirement Gathering** — Mengumpulkan, menyusun, dan memvalidasi kebutuhan bisnis dari pemangku kepentingan.
2. **Pemodelan Proses Bisnis** — Memodelkan alur kerja dan proses menggunakan notasi mirip BPMN.
3. **User Story Generation** — Menghasilkan user story yang terbentuk baik dengan kriteria penerimaan.
4. **Use Case Modeling** — Menghasilkan use case yang terperinci dari kebutuhan.
5. **BRD Generation** — Menghasilkan Dokumen Persyaratan Bisnis dari input mentah.
6. **Spesifikasi Fungsional** — spesifikasi fungsional yang dapat dieksekusi untuk paket downstream.
7. **Gap Analysis** — Mengidentifikasi dan mendokumentasikan kesenjangan antara kebutuhan bisnis dan kapabilitas teknis.
8. **Analisis ROI** — Mengkuantifikasi laba atas investasi untuk fitur atau proyek yang diusulkan.
9. **Optimasi Proses** — Mengidentifikasi inefisiensi dalam proses bisnis dan merekomendasikan perbaikan.

### Kriteria Keberhasilan

|Metrik|Target|Nilai|
|--------|--------|-------|
|Kejelasan Kebutuhan|≥90% (kebutuhan bebas ambiguitas)|A|
|Kualitas Kisah Pengguna|≥95% (cerita dengan kriteria penerimaan lengkap)|A|
|Analisis Kesenjangan Cakupan|≥90% (semua pemandangan teridentifikasi)|A|
|Akurasi ROI|≥85% (prediksi ROI dalam ±10% dari aktual)|A|
|Proses Optimasi|≥80% (inefisiensi teridentifikasi dan ditangani)|A|
|Kelengkapan BRD|≥95% (semua bagian yang diperlukan ada)|A|
|Konsistensi Pemangku Kepentingan|≥90% (konflik teridentifikasi dan terselesaikan)|A|
|Penjelasan|≥95% (alasan untuk semua rekomendasi)|A+|

---

## Non-Tujuan

1. **Fasilitasi pemangku kepentingan** — Business Analyst menyusun kebutuhan; ia tidak melakukan pertemuan pemangku kepentingan.
2. **Definisi strategi bisnis** — Fokus pada penerjemahan kebutuhan, bukan strategi bisnis.
3. **Mengganti alat BA khusus** — Alat seperti JIRA, Confluence, Miro tetap dipakai; Business Analyst menyediakan analisis dan generasi.
4. **Manajemen proyek** — Tidak mengelola proyek timeline, sumber daya, atau perencanaan sprint.
5. **Modifikasi Core** — Semua implementasi berada di dalam Capability Pack Business Analyst.

---

## Ruang Lingkup Kapabilitas

### Kapabilitas Inti

|Kapabilitas|Deskripsi|Masukan|Keluaran|
|-----------|-------------|--------|---------|
|Pengumpulan Kebutuhan|Mengumpulkan, menyusun, dan memvalidasi kebutuhan dari input pemangku kepentingan|Kebutuhan bahasa alami, catatan pemangku kepentingan, transkrip wawancara|Dokumen kebutuhan terstruktur dengan skor kualitas|
|Pemodelan Proses Bisnis|Memodelkan alur kerja menggunakan notasi mirip BPMN|Deskripsi proses, narasi alur kerja|Modelkan proses dengan aktivitas, gateway, aliran data|
|Pembuatan Cerita Pengguna|Menghasilkan user story sesuai INVEST dengan kriteria penerimaan|Kebutuhan, persona, perjalanan pengguna|Kisah pengguna dengan kriteria penerimaan terperinci|
|Pemodelan Kasus Penggunaan|Menghasilkan use case terperinci dari kebutuhan|Kebutuhan, peran pengguna, sistem interaksi|Diagram use case dan deskripsi use case terperinci|
|Generasi BRD|Hasilkan Dokumen Persyaratan Bisnis|Kebutuhan mentah, konteks bisnis, masukan pemangku kepentingan|Dokumen BRD dengan semua bagian standar|
|Spesifikasi Fungsional|Menghasilkan spesifikasi fungsional yang dapat dieksekusi untuk paket hilir|BRD, cerita pengguna, kasus penggunaan|Spesifikasi fungsional dalam format terstruktur|
|Analisis Kesenjangan|Mengidentifikasi kesenjangan antara kebutuhan bisnis dan kapabilitas teknis|Kebutuhan, kondisi saat ini, batasan teknis|Laporan gap analysis dengan prioritisasi|
|Analisis ROI|Mengkuantifikasi laba atas investasi untuk fitur yang diusulkan|Estimasi biaya, proyeksi manfaat, timeline|Laporan analisis ROI dengan NPV, payback period|
|Optimasi Proses|Mengidentifikasi dan merekomendasikan proses perbaikan|Model proses, performa data saat ini|Rekomendasi proses optimasi|

### Di Luar Cakupan

- Fasilitasi pemangku kepentingan atau manajemen pertemuan
- Perencanaan proyek atau alokasi sumber daya
- Formulasi strategi bisnis
- Perencanaan keuangan di luar ROI
- Implementasi manajemen perubahan
- Eksekusi atau monitoring proses secara langsung

---

## Kontrak Publik

### Kontrak Masukan: Permintaan Analisis Bisnis

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

### Kontrak Keluaran: Laporan Analisis Bisnis

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

### Catatan Kebutuhan (Memori Pengalaman)

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

## Titik Integrasi (Grafik Kapabilitas)

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

### Templat Tugas

|Tugas|Subtugas|
|------|----------|
|Analisis Bisnis|Pengumpulan masukan → Pengumpulan kebutuhan → Pemodelan proses → Pembuatan cerita pengguna → Pemodelan kasus penggunaan → Analisis kesenjangan → Analisis ROI → Optimasi proses → Pembuatan spesifikasi|

---

## Capability Pack Konsumen

|Capability Pack Konsumen|Kasus Penggunaan|
|--------------------------|----------|
|**Insinyur Kode**|Mengonsumsi spesifikasi fungsional untuk menghasilkan kode dan pengujian|
|**Arsitek Sistem**|Mengonsumsi spesifikasi fungsional untuk desain arsitektur|
|**Asisten DevOps**|Mengonsumsi kebutuhan deployment dan spesifikasi infrastruktur|
|**Decision Intelligence**|Mengevaluasi ROI dan risiko dari inisiatif bisnis yang diusulkan|
|**Pengembangan Diri**|Mengidentifikasi peluang perbaikan proses bisnis|

---

## Ketergantungan

### Dependensi Internal (Kontrak Bersama)

1. **Execution Runtime** — Tugas perutean dan orkestrasi (sesuai ADR-002)
2. **Experience Memory** — Persistensi catatan kebutuhan dan keputusan (sesuai ADR-011)
3. **Kontrak Bersama** — Definisi Task/Intent dan skema hasil (sesuai ADR-006)

### Pengetahuan Eksternal

1. **BABOK (Badan Pengetahuan Analisis Bisnis)** — Praktik BA standar
2. **BPMN** — Model dan Notasi Proses Bisnis
3. **Kriteria INVESTASI** — Kerangka kualitas cerita pengguna
4. **ROI/NPV/IRR** — Metodologi analisis keuangan

### Tidak Ada Perubahan Inti yang Diperlukan

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

**Dampak ADR:** Tidak ada. Tidak diperlukan modifikasi Core, Runtime, Kernel, atau kontrak bersama.

---

## Spesifikasi Benchmark

### Kerangka Benchmark

|Dimensi|Definisi|pengukuran|Target|
|-----------|------------|-------------|--------|
|**Kejelasan Persyaratan**|% kebutuhan bebas ambiguitas|Tinjau ahli terhadap kualitas kebutuhan|≥90%|
|**Kualitas Kisah Pengguna**|% cerita dengan kriteria penerimaan lengkap|Kriteria penerimaan ada / story|≥95%|
|**Cakupan Analisis Kesenjangan**|% kekacauan bisnis-teknis teridentifikasi|Kesenjangan ditemukan / kebenaran dasar|≥90%|
|**Akurasi ROI**|Prediksi ROI sesuai hasil aktual|ROI diprediksi vs aktual dalam ±10%|≥85%|
|**Optimasi Proses**|% inefisiensi teridentifikasi dan ditangani|Perbaikan ditemukan/inefisiensi total|≥80%|
|**Kelengkapan BRD**|% bagian BRD yang diperlukan ada|Bagian ada / total yang diharapkan|≥95%|
|**Konsistensi Pemangku Kepentingan**|% konflik teridentifikasi dan terselesaikan|Konflik/konflik total terselesaikan|≥90%|
|** Penjelasan **|Kejelasan alasan untuk rekomendasi|Skor evaluasi manusia|≥95%|
|**Konsistensi**|Input yang menghasilkan spesifikasi yang sama|Varian di 10 run < 5%|≥90%|

### Kumpulan data Benchmark

- **100 kasus bisnis** yang mencakup:
  - E-commerce (inventaris, checkout, rekomendasi)
  - Fintech (perdagangan platform, penilaian risiko, presentasi)
  - Pelayanan Kesehatan (manajemen pasien, penjadwalan janji temu)
  - SaaS (platform multi-penyewa, penagihan, analitik)
  - Enterprise (otomasi alur kerja, pelaporan, integrasi)

### Detail Dimensi Benchmark

|Tipe Skenario|Deskripsi|Kebenaran Dasar|
|---------------|-------------|-------------|
|Persyaratan yang Ambigu|Kebutuhan dengan bahasa tidak jelas|Disambiguasi ahli|
|Kebutuhan Pemangku Kepentingan yang Bertentangan|Pemangku kepentingan dengan prioritas berlawanan|Catatan resolusi konflik|
|Kriteria Penerimaan Tidak Ada|Cerita tanpa kondisi yang dapat diuji|Kriteria yang dilengkapi ahli|
|Optimasi Proses|Proses bisnis tidak efisien|Catatan perbaikan proses|

---

## Spesifikasi Golden Test

| # |Skenario|Hasil yang diharapkan|Kriteria Penerimaan|
|---|----------|-----------------|---------------------|
|1|Kebutuhan ambigu ("sistem cepat")|Kebutuhan diklarifikasi dengan kriteria diukur|≥90% peningkatan kecerahan|
|2|Kebutuhan pemangku kepentingan berbeda (keamanan vs kegunaan)|Konflik teridentifikasi dan dimediasi|resolusi ≥90%.|
|3|Kriteria penerimaan hilang di user story|Kriteria dihasilkan dengan kondisi yang dapat diuji|≥95% kelengkapan|
|4|Proses dengan inefisiensi (langkah persetujuan manual)|Bottleneck teridentifikasi dengan saran otomasi|≥85% deteksi|
|5|Analisis ROI dengan biaya/manfaat data|NPV, payback, IRR dihitung|≥85% akurasi vs aktual|
|6|Analisis kesenjangan (kondisi saat ini vs target)|Kesenjangan teridentifikasi dengan prioritas|≥90% cakupan|
|7|Pembuatan BRD dari catatan mentah|BRD lengkap dengan semua bagian|≥95% kelengkapan|
|8|Gunakan pemodelan kasus berdasarkan kebutuhan|Use case terperinci dengan aktor dan alur|≥90% kelengkapan|
|9|Spesifikasi fungsional untuk Code Engineer|Spek terstruktur yang dapat dikonsumsi Code Engineer|≥90% kegunaan|
|10|Model proses bisnis dari deskripsi alur kerja|Modelnya mirip BPMN dengan aktivitas dan gateway|akurasi ≥90%.|

### Kriteria Penerimaan Golden Test

- Semua 10 skenario Golden Test lulus pada ≥90% dari kriteria penerimaan individu (100% lulus)
- Tingkat kelulusan Golden Test Business Analyst keseluruhan ≥90%
- Semua user story yang dihasilkan memiliki kriteria penerimaan lengkap
- Perhitungan ROI divalidasi terhadap standar keuangan

---

## Persyaratan Kasus Nyata

### Direktori Kasus Nyata

`real_cases/business_analyst/` harus berisi:

|Urutannya|Jumlah Minimal|
|-------------|---------------|
|Analisis kasus bisnis nyata dari penggunaan aktual|20|
|Kasus dengan kebutuhan ambigu|5|
|Kasus dengan kebutuhan pemangku kepentingan bertentangan|5|
|Kasus dengan kriteria penerimaan hilang|5|
|Kasus dengan analisis ROI|10|
|Kasus dengan proses optimasi|5|
|Kasus dengan review/validasi ahli|15|

### Struktur Kasus Nyata

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

### Targetkan Kasus Nyata

|Metrik|Target|
|--------|--------|
|Kasus nyata yang dicatat|≥20 (Tingkat 3) → ≥100 (Tingkat 4)|
|Skor kasus kualitas nyata (review ahli)|≥90%|
|Kebutuhan diterima di hilir|≥85% spec yang dihasilkan digunakan tanpa revisi besar|

---

## Definisi Selesai

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

|Risiko|Dampak|kemungkinan|Mitigasi|
|------|--------|------------|------------|
|Kebutuhan ambigu salah diinterpretasikan|Tinggi — pengerjaan ulang di hilir|Tinggi|Interpretasi konservatif; penilaian kepercayaan diri; tinjauan pemangku kepentingan diperlukan|
|Analisis ROI tidak akurat|Sedang — keputusan investasi buruk|Sedang|Analisis sensitivitas; kepercayaan interval; kalibrasi historis|
|Rekomendasi optimasi proses tidak praktis|Sedang — usaha terbuang|Sedang|Estimasi usaha disertakan; validasi ahli pada kasus nyata|
|Cerita pengguna tidak sesuai ekspektasi pengembang|Sedang — memulai pengembangan|Tinggi|Loop umpan balik pengembang; mengulas cerita dengan Code Engineer|
|Spesifikasi BRD/fungsional terlalu panjang atau terlalu ringkas|Sedang — konsumsi hilir buruk|Tinggi|Template berbasis dengan tingkat detail yang dapat dikonfigurasi; validasi hilir|
|Analisis kesenjangan melewatkan kesenjangan kritis|Tinggi — implementasi tidak lengkap|Sedang|Analisis multiperspektif; memeriksa silang pemangku kepentingan|
|Pemodelan proses kerutan alur kerja kompleks secara berlebihan|Sedang — analisis salah|Sedang|Penyempurnaan bertahap; pemangku kepentingan validasi pos pemeriksaan|

---

## Dampak ADR

**Apakah ini memerlukan perubahan Core?** Tidak.

Business Analyst adalah **Capability Pack baru** yang mengikuti pola yang sudah ada:

- **ADR-001 (Core Pipeline Freeze):** Tidak ada perubahan Core. Semua logika di `apps/business_analyst/`.
- **ADR-002 (Capability Pack Kemerdekaan):** Business Analyst berkomunikasi dengan paket lain melalui tugas Execution Runtime dan kontrak bersama saja. Tanpa import langsung.
- **ADR-003 (Pekerja = Hanya Adaptor):** Pekerja tipis merutekan tugas ke Mesin Domain.
- **ADR-004 (Logika Bisnis Milik Mesin Domain):** Semua analisis bisnis logika berada di `apps/business_analyst/engine.py`.
- **ADR-005 (Human Approval Required):** Semua kebutuhan dan rekomendasi memerlukan persetujuan pemangku kepentingan manusia sebelum dikonsumsi di hilir.
- **ADR-006 (Capability Contract v1 Frozen):** Menggunakan Capability Contract yang ada pendaftaran untuk node dan subtask template. Tidak ada perubahan kontrak.
- **ADR-007 (Batas Percakapan):** Business Analyst dipanggil melalui Execution Runtime, bukan langsung oleh Conversation Manager.
- **ADR-008 (Perubahan Inti Memerlukan Bukti Lintas Kemampuan):** Tidak berlaku — tidak ada perubahan Core.

**ADR yang diperlukan:** Tidak ada. Ini adalah Capability Pack baru, bukan modifikasi Core.

---

## Peluncuran Rencana

### Fase 1: Prototipe (RFC → Eksperimental)

**Durasi:** 5 minggu

- [x] Membuat struktur paket `apps/business_analyst/`
- [x] Mengimplementasikan pengumpulan kebutuhan dengan penilaian kualitas
- [x] Mengimplementasikan user story generation dengan kriteria penerimaan
- [x] Mengimplementasikan generasi BRD (sebagian — bagian inti)
- [x] Mendefinisikan kontrak publik (BA Request, BA Report)
- [x] Mengimplementasikan adaptor Worker tipis
- [x] Membuat 10 skenario Golden Test
- [x] Integrasi: Code Engineer ← Business Analyst (konsumsi spesifikasi fungsional)
- [x] Integrasi: Pengembangan Diri ← Business Analyst (proses optimasi)
- **Gerbang:** 10 Golden Test lulus pada ≥80%

### Fase 2: Kapabilitas Lengkap (Eksperimental → Stabil)

**Durasi:** 8 minggu

- [x] Mengimplementasikan pemodelan proses bisnis (mirip BPMN)
- [x] Mengimplementasikan pemodelan use case
- [x] Mengimplementasikan analisis kesenjangan
- [x] Mengimplementasikan analisis ROI (NPV, payback, IRR)
- [x] Mengimplementasikan optimasi proses
- [x] Menyelesaikan generasi BRD (semua bagian)
- [x] Mengimplementasikan spesifikasi fungsional generasi
- [x] Memperluas Golden Test menjadi 10 skenario penuh
- [x] Mencatat ≥20 kasus nyata dari penggunaan Code Engineer dan proyek perencanaan
- [x] **Benchmark:** 100 kasus bisnis, ≥90% kejelasan, ≥95% kualitas cerita
- [x] **Integrasi:** System Architect mulai mengonsumsi spesifikasi fungsional dari Business Analyst
- [x] **Integrasi:** DevOps Assistant mulai mengonsumsi kebutuhan infrastruktur dari Business Analyst
- **Gerbang:** Semua 10 Golden Test lulus pada ≥90%; Benchmark ≥90%

### Fase 3: Ekosistem (Stabil → Bersertifikat)

**Durasi:** 6 minggu

- [x] Keempat paket konsumen terintegrasi
- [x] Analisis ROI divalidasi terhadap standar keuangan
- [x] Optimasi proses divalidasi pada proses bisnis nyata
- [x] Spesifikasi fungsional divalidasi melalui konsumsi Code Engineer
- [x] Audit independen terhadap kualitas kebutuhan dan gap analysis
- [x] Dasbor Benchmark publik tersedia
- [x] **Benchmark:** ≥90% di semua dimensi berkelanjutan
- [x] **Kasus Nyata:** ≥100 kasus dengan ≥80% adopsi hilir
- **Gerbang:** Audit kelulusan independen; Benchmark ≥90% berkelanjutan

---

## Peningkatan di Masa Depan

### Fase 2 (Pasca-Rilis v1.0.0)

1. **Simulasi Pemangku Kepentingan** — Memodelkan perspektif pemangku kepentingan yang berbeda dan menyelesaikan konflik secara otomatis
2. **Matriks Ketertelusuran Persyaratan** — Ketertelusuran end-to-end dari kebutuhan bisnis ke kode dan pengujian
3. **Acceptance Criteria Auto-Generation untuk QA** — Memberikan makan kriteria penerimaan langsung ke QA Engineer untuk pengujian generasi
4. **Perkiraan Dampak Bisnis** — Memprediksi dampak hilir dari perubahan kebutuhan pada kode, pengujian, dan penerapan

### Fase 3 (Perusahaan)

1. **Analisis Portofolio Multi-Proyek** — Menganalisis dan memprioritaskan kebutuhan di seluruh portofolio proyek
2. **Integrasi Arsitektur Bisnis** — mengunci kapabilitas bisnis ke arsitektur teknis
3. **Persyaratan Kepatuhan Peraturan** — Menghasilkan kebutuhan yang dipetakan kepatuhan (GDPR, HIPAA, SOX)
4. **Business Process Automation Discovery** — Mengidentifikasi peluang otomasi dari model proses

### Jangka Panjang

1. **Penemuan Persyaratan Bertenaga AI** — Mewawancarai pemangku kepentingan dan mengekstrak kebutuhan dari percakapan
2. **Persyaratan Evolution Management** — Melacak perubahan kebutuhan dan dampak berjenjangnya
3. **Business Value Stream Mapping** — Analisis value stream end-to-end dari kebutuhan bisnis hingga hasil pelanggan
4. **Automated Business Case Generation** — Dokumen kasus bisnis lengkap dari kebutuhan dan analisis ROI
