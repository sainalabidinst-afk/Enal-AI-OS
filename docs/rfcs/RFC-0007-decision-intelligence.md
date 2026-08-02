# RFC-0007: Capability Pack Decision Intelligence

<!-- DOCUMENT_METADATA_START -->
**Pemilik:** Tim Dokumentasi
**Pemilik Canonical:** Pimpinan Tata Kelola Dokumentasi
**Diverifikasi Terakhir:** 02-08-2026
**Versi:** 1.0.0
**Status:** Aktif
<!-- DOCUMENT_METADATA_END -->

|Bidang|Nilai|
|-------|-------|
|**ID RFC**|RFC-0007|
|**Status**|Draf|
|**Versi**|0.1.0|
|**Penulis**|Tim Inti AI OS Akhir|
|**Target Rilis**|v1.2.0 (fase Keunggulan Kemampuan)|
|**Capability Pack**|Decision Intelligence|
|**ID Kemampuan**|`decision-intelligence`|
|**Kategori**|Pemikiran|
|**Target Kualitas**|SEBUAH (≥90)|
|**Target Kematangan**|Level 3 — Siap Produksi|
|**Referensi RFC**|RFC-0007|

---

## Motivasi

13 Capability Pack yang mencakup kode, jaringan, penelitian, DevOps, perdagangan, dan pengembangan diri. Setiap paket menghasilkan keluaran — kode, konfigurasi, laporan penelitian, sinyal perdagangan — yang melibatkan keputusan yang memerlukan penalaran berdasarkan bukti.

Saat ini, keputusan ini dibuat secara tertanam dan spesifik-pack. Tidak ada lapisan penalaran bersama yang menerapkan kerangka keputusan yang konsisten, dapat diaudit, dan dapat dijelaskan di seluruh domain. Hal ini menyebabkan:

1. **Kualitas keputusan yang tidak konsisten** — setiap paket menemukan ulang pengumpulan bukti, penilaian risiko, dan estimasi kepercayaan.
2. **Tidak ada penggunaan ulang lintas keputusan domain** — analisis risiko Trading Analyst tidak dapat menginformasikan pilihan refactoring Code Engineer, meskipun keduanya melibatkan risiko trade-off vs imbal hasil.
3. **Explainability yang terbatas** — keputusan dijelaskan melalui narasi spesifik-domain, bukan melalui rantai bukti-ke-keputusan yang terstruktur.
4. **Tidak ada jejak keputusan audit** — keputusan dibuat tetapi tidak pernah dicatat dalam memori pengalaman terstruktur yang dapat ditelusuri untuk pembelajaran dan rollback.

Decision Intelligence menjadi **lapisan penalaran** yang berada di antara produsen bukti (semua Capability Pack) dan konsumen keputusan (semua Capability Pack), menyediakan kerangka kerja terpadu untuk pengambilan keputusan berdasarkan bukti, dapat dijelaskan, dan dapat diaudit.

---

## Pernyataan Masalah

Tanpa Capability Pack Decision Intelligence yang khusus:

- **Bukti disimpan per paket** — tidak ada mekanisme untuk mengumpulkan, mengumpulkan, dan mensintesis bukti dari banyak Capability Pack sebelum mencapai keputusan.
- **Alternatif jarang dieksplorasi** — kebanyakan paket menghasilkan satu rekomendasi tanpa membuat atau membandingkan alternatif.
- **Analisis risiko bersifat ad hoc** — penilaian risiko ada di sebagian paket (Trading, Jaringan) tetapi tanpa metodologi terstandarisasi di seluruh platform.
- **Confidence tidak dikuantifikasi** — estimasi keyakinan tersirat dalam rekomendasi, tidak dimodelkan atau dikomunikasikan secara eksplisit.
- **Keputusan tidak dicatat** — tidak ada Riwayat Keputusan yang terstruktur untuk mendukung pembelajaran, rekomendasi rollback, atau kepatuhan audit.
- **Analisis trade-off tidak ada** — optimasi multi-objektif (akurasi vs latensi, biaya vs kebisingan) ditangani per-pack, bukan melalui kerangka kerja terpadu.

Tidak adanya Decision Intelligence berarti ketika ECP berkembang mencakup lebih banyak Capability Pack, kualitas dan konsistensi keputusan tidak akan mencakup — sebaliknya, keputusan justru akan semakin terfragmentasi.

---

## Tujuan

1. **Pengumpulan Bukti** — Mengumpulkan dan menyusun bukti dari satu atau lebih sumber (output Capability Pack, data kasus nyata, hasil Benchmark).
2. **Generasi Alternatif** — Menghasilkan banyak alternatif yang layak untuk setiap konteks keputusan.
3. **Analisis Risiko** — Mengkuantifikasi dan mengategorikan risiko yang terkait dengan setiap alternatif (probabilitas × dampak).
4. **Analisis Trade-off** — Menganalisis trade-off multi-objektif antar alternatif (akurasi vs biaya, kecepatan vs keamanan, dll.).
5. **Decision Scoring** — Memberikan skor pada setiap alternatif terhadap kriteria dan bobot yang dapat dikonfigurasi.
6. **Confidence Estimation** — Menghasilkan skor keyakinan eksplisit untuk setiap keputusan, dengan kuantifikasi yang meyakinkan.
7. **Keputusan yang Dapat Dijelaskan** — Menghasilkan rantai penjelasan yang dapat dibaca manusia: bukti → penalaran → simulasi → alternatif → risiko → keputusan → alasan.
8. **Riwayat Keputusan** — Mencatat setiap keputusan, bukti, alternatif yang dipertimbangkan, dan hasil ke Experience Memory untuk pembelajaran dan rollback.

### Kriteria Keberhasilan

|Metrik|Target|Nilai|
|--------|--------|-------|
|Akurasi Keputusan|≥90% (keputusan benar ketika ground truth tersedia)|A|
|Penjelasan|≥95% (rantai bukti-ke-keputusan lengkap disajikan)|SEBUAH+|
|Konsistensi|≥90% (input yang sama menghasilkan keputusan yang sama di setiap run)|A|
|Keyakinan Kalibrasi|≥85% (skor keyakinan mencerminkan akurasi aktual ±5%)|A|
|Deteksi Risiko|≥90% (risiko teridentifikasi sesuai kebenaran dasar)|A|
|Pengorbanan Kelengkapan|≥85% (semua tujuan relevan dipertimbangkan)|A|

---

## Non-Tujuan

1. **Eksekusi keputusan langsung** — Decision Intelligence menghasilkan rekomendasi; eksekusi memerlukan persetujuan eksplisit pengguna sesuai ADR-005.
2. **Mengganti domain keahlian** — Decision Intelligence adalah lapisan penalaran, bukan pengganti domain pengetahuan. Ia memperkuat tetapi tidak menggantikan Trading, Code, Network, dll.
3. **Sinyal trading pasar real-time** — Trading Analyst tetap memiliki kepemilikan pembuatan sinyal trading. Decision Intelligence dapat memberi skor pada keputusan trading tetapi tidak menghasilkan sinyal.
4. **Penegakan titik keputusan tunggal** — Setiap Capability Pack tetap dapat menghasilkan rekomendasinya sendiri yang spesifik-domain. Decision Intelligence menyediakan penilaian lapisan dan penjelasan lintas-bagian.
5. **Modifikasi Core** — Semua implementasi harus berada di dalam Capability Pack Decision Intelligence, mengikuti ADR-002 dan ADR-004.

---

## Ruang Lingkup Kapabilitas

### Kapabilitas Inti

|Kapabilitas|Deskripsi|Masukan|Keluaran|
|-----------|-------------|--------|---------|
|Pengumpulan Bukti|Mengumpulkan, memvalidasi, dan menyusun bukti dari satu atau lebih sumber.|Output Capability Pack, respon API, data Benchmark, file kasus nyata|Kumpulan bukti terstruktur dengan skor kualitas|
|Generasi Alternatif|Menghitung alternatif yang layak untuk konteks keputusan tertentu.|Konteks keputusan, kumpulan bukti, batasan|Tetapkan alternatif dengan skor kelayakan awal|
|Analisis Risiko|Menilai probabilitas dan dampak setiap alternatif.|Alternatif, bukti, data historis|Profil risiko per alternatif (probabilitas × dampak)|
|Analisis Pertukaran|Menganalisis trade-off multi-objektif antar alternatif.|Alternatif, kriteria berbobot, batasan|Perbatasan pareto dari skor trade-off|
|Penilaian Keputusan|Memberikan skor dan memberikan alternatif terhadap kriteria yang dapat dikonfigurasi.|Alternatif, bobot kriteria, bukti, risiko|Alternatif terurut dengan skor gabungan|
|Estimasi Keyakinan|Mengkuantifikasi dan percaya diri pada keputusan akhir.|Kualitas bukti, model keyakinan, kalibrasi historis|Skor kepercayaan diri (0–100%) dengan batas bawah|
|Keputusan yang Dapat Dijelaskan|Menghasilkan penjelasan yang dapat ditelusuri dan dibaca manusia.|Jejak keputusan lengkap, bukti, rantai penalaran|Dokumen penjelasan (bukti → keputusan → dasar pemikiran)|
|Sejarah Keputusan|Mencatat keputusan ke Experience Memory untuk pembelajaran dan rollback.|Keputusan akhir, alternatif, bukti, hasil|Catatan keputusan di Experience Memory|

### Di Luar Cakupan

- Eksekusi perdagangan secara real-time
- Penyediaan sumber daya cloud secara langsung
- Integrasi langsung dengan sistem keputusan eksternal tanpa mediasi
- Penasihat hukum, medis, atau keuangan di luar batas Lingkup ECP yang ada
- Keputusan penerapan secara otonom (memerlukan persetujuan sesuai ADR-005)
- Menggantikan penalaran internal Capability Pack lain

---

## Kontrak Publik

### Kontrak Masukan: Permintaan Keputusan

```json
{
  "decision_id": "uuid",
  "context": "string — natural language description of the decision to be made",
  "evidence_sources": [
    {
      "source_id": "string — capability_id or external source identifier",
      "evidence_type": "analysis | recommendation | data | benchmark | historical",
      "payload": "object — structured evidence payload",
      "quality_score": 0.0,
      "weight": 0.0
    }
  ],
  "constraints": ["string — hard constraints that eliminate alternatives"],
  "objectives": [
    {
      "name": "Accuracy",
      "weight": 0.30,
      "goal": "maximize | minimize"
    },
    {
      "name": "Risk",
      "weight": 0.25,
      "goal": "minimize"
    },
    {
      "name": "Cost",
      "weight": 0.20,
      "goal": "minimize"
    },
    {
      "name": "Latency",
      "weight": 0.25,
      "goal": "minimize"
    }
  ],
  "risk_tolerance": "low | medium | high",
  "max_alternatives": 5,
  "include_explanation": true
}
```

### Kontrak Keluaran: Hasil Keputusan

```json
{
  "decision_id": "uuid",
  "recommended_decision": "string — the chosen alternative or action",
  "alternatives": [
    {
      "id": "string",
      "description": "string",
      "score": 0.0,
      "confidence": 0.0,
      "risk_profile": {
        "overall_risk": 0.0,
        "probability": 0.0,
        "impact": 0.0,
        "risk_factors": ["string"]
      },
      "trade_offs": {
        "accuracy": 0.0,
        "cost": 0.0,
        "latency": 0.0
      }
    }
  ],
  "confidence_score": 0.0,
  "confidence_explanation": "string",
  "explanation": {
    "evidence_summary": "string",
    "reasoning_chain": ["string"],
    "simulation_results": "object",
    "risk_assessment": "string",
    "final_rationale": "string"
  },
  "decision_history_ref": "string — reference to Experience Memory entry"
}
```

### Catatan Keputusan (Memori Pengalaman)

```json
{
  "record_id": "uuid",
  "decision_id": "uuid",
  "timestamp": "ISO 8601",
  "context": "string",
  "chosen_alternative": "string",
  "alternatives_count": 0,
  "confidence_score": 0.0,
  "evidence_count": 0,
  "risk_score": 0.0,
  "explanation": "string",
  "outcome": "pending | accepted | rejected | revised",
  "user_feedback": "string — optional",
  "revision_history": [{"revision_id": "uuid", "changes": "string"}]
}
```

---

## Titik Integrasi (Grafik Kapabilitas)

Capability Pack Decision Intelligence berintegrasi dengan semua Capability Pack yang ada dan yang akan datang melalui **Execution Runtime** dan **shared contract saja** (sesuai ADR-002). Ia tidak mengimpor mesin Capability Pack lain secara langsung.

### Integrasi Saluran Pipa

```
Consumer Capability Pack
    │
    │  submits evidence via task/intent
    ▼
Execution Runtime
    │
    │  routes to Decision Intelligence Domain Engine
    ▼
Decision Intelligence Engine
    │
    │  ┌──────────────────────────────────────────┐
    │  │ 1. Evidence Collection                   │
    │  │ 2. Alternative Generation                │
    │  │ 3. Risk Analysis                         │
    │  │ 4. Trade-off Analysis                    │
    │  │ 5. Decision Scoring                      │
    │  │ 6. Confidence Estimation                 │
    │  │ 7. Explainable Decision                  │
    │  │ 8. Decision History → Experience Memory  │
    │  └──────────────────────────────────────────┘
    │
    │  returns Decision Result
    ▼
Consumer Capability Pack
    │
    │  receives scored recommendation + explanation
    ▼
User / Human Approval Loop
```

### Templat Tugas

|Tugas|Subtugas|
|------|----------|
|Keputusan Skor|Pengumpulan Bukti → Pembuatan Alternatif → Analisis Risiko → Analisis Trade-off → Penilaian Keputusan → Estimasi Keyakinan → Penjelasan → Riwayat Keputusan|

---

## Capability Pack Konsumen

Decision Intelligence melayani semua Capability Pack yang ada sebagai lapisan penalaran lintas-bagian:

|Capability Pack Konsumen|Kasus Penggunaan|
|--------------------------|----------|
|**Analis Perdagangan**|Memberikan skor alternatif trading, mengkuantifikasi keyakinan yang disesuaikan risiko, menjelaskan alasan rekomendasi trading|
|**Insinyur Kode**|Memberikan skor alternatif refactoring, menganalisis trade-off (kompleksitas vs kinerja), mengestimasi risiko perubahan|
|**Insinyur Jaringan**|Membandingkan alternatif konfigurasi, menganalisis risiko kegagalan, merekomendasikan perubahan yang aman untuk rollback|
|**Asisten DevOps**|Mengevaluasi penerapan strategi, trade-off biaya vs kejelasan, merekomendasikan peluncuran yang optimal|
|**Asisten Peneliti**|Memberikan skor kualitas bukti, mengkuantifikasi keyakinan pada kesimpulan yang disintesis, menjelaskan penalaran|
|**Pengembangan Diri**|Mengevaluasi proposal perbaikan arsitektur, memberi skor risiko vs manfaat, menghasilkan rencana yang dapat dijelaskan|
|**Decision Intelligence** (internal)|Menggunakan Reasoning Layer-nya sendiri untuk meta-keputusan tentang pembobotan bukti dan kalibrasi keyakinan|

---

## Ketergantungan

### Dependensi Internal (Kontrak Bersama)

1. **Execution Runtime** — Tugas perutean dan orkestrasi (sesuai ADR-002)
2. **Experience Memory** — Persistensi catatan keputusan (sesuai ADR-011)
3. **Kontrak Bersama** — Definisi Task/Intent dan skema hasil (sesuai ADR-006)

### Tidak Ada Perubahan Inti yang Diperlukan

Semua implementasi berada di dalam Capability Pack Decision Intelligence:

```
apps/
└── decision_intelligence/
    ├── engine.py                # Domain Engine (owner of business logic per ADR-004)
    ├── worker.py                # Thin adapter (per ADR-003)
    ├── schemas.py               # Public contracts (Decision Request, Decision Result)
    ├── evidence_collector.py    # Evidence collection submodule
    ├── alternative_generator.py # Alternative generation submodule
    ├── risk_analyzer.py         # Risk analysis submodule
    ├── tradeoff_analyzer.py     # Trade-off analysis submodule
    ├── scoring_engine.py        # Decision scoring submodule
    ├── confidence_estimator.py  # Confidence estimation submodule
    └── explanation_generator.py # Explainable decision submodule
```

**Dampak ADR:** Tidak ada. Tidak diperlukan modifikasi Core, Runtime, Kernel, atau shared contract (ADR-001, ADR-006 tetap tidak berubah).

---

## Spesifikasi Benchmark

### Kerangka Benchmark

|Dimensi|Definisi|pengukuran|Target|
|-----------|------------|-------------|--------|
|**Ketepatan**|Kebenaran keputusan akhir|% keputusan yang sesuai dengan kebenaran dasar atau konteks ahli|≥90%|
|**Kelengkapan**|Cakupan bukti, alternatif, dan tujuan|% elemen yang diperlukan yang dipertimbangkan dalam keputusan|≥90%|
|** Penjelasan **|Kejelasan dan kemampuan menelusuri keputusan rantai|Evaluasi manusia: rantai bukti→keputusan lengkap disajikan|≥95%|
|**Keamanan**|Tidak ada rekomendasi berbahaya atau tidak aman|% keputusan yang lulus batasan keamanan|≥95%|
|**Efisiensi**|Waktu respons dan penggunaan sumber daya|Latensi P95 < 2000ms, penggunaan token optimal|dalam anggaran|
|**Konsistensi**|Input yang menghasilkan output yang sama di setiap dijalankan|Varian di 10 dijalankan berulang < 5%|≥90%|
|**Kalibrasi Keyakinan**|Skor keyakinan mencerminkan keakuratan aktual|Kurva kalibrasi: keyakinan dalam ±5% dari akurasi aktual|≥85%|
|**Deteksi Risiko**|Risiko teridentifikasi sesuai kebenaran lapangan|% risiko yang diketahui terdeteksi sebelum keputusan|≥90%|

### Kumpulan data Benchmark

- **100 skenario keputusan** yang mencakup domain:
  - Trading (pemilihan perdagangan yang disesuaikan risiko, ukuran posisi)
  - Kode (refactoring vs rewrite, pemilihan perpustakaan)
  - Jaringan (konfigurasi migrasi, perubahan kebijakan firewall)
  - DevOps (penerapan strategi, perencanaan rollback)
  - Penelitian (bukti sintesis, kesimpulan keyakinan)
  - Pengembangan Diri (penilaian perbaikan arsitektur)
  - Lintas domain (keputusan trade-off multi-paket)

### Detail Dimensi Benchmark

|Tipe Skenario|Deskripsi|Sumber Kebenaran Tanah|
|---------------|-------------|---------------------|
|Bukti yang Bertentangan|Sumber bukti saling bertentangan|Konsensus ahli|
|Bukti Tidak Lengkap|Sebagian besar bukti hilang|Konsensus ahli|
|Optimasi Multi-tujuan|Banyak tujuan yang saling bersaing|Optimalitas pareto|
|Resiko Tinggi|Keputusan dengan risiko menurun signifikan|Tinjau ahli|
|Kepercayaan Diri Rendah|Ketidakpastian tinggi dalam bukti|Keyakinan Kalibrasi|
|Revisi Keputusan|Meninjau ulang keputusan sebelumnya dengan bukti baru|Riwayat keputusan|
|Rekomendasi Kembalikan|Mengidentifikasi kapan harus mengembalikan keputusan|Hasil historis|

---

## Spesifikasi Golden Test

Golden Test suite (`benchmarks/golden_test_set.py`) harus menyertakan skenario Decision Intelligence:

| # |Skenario|Hasil yang diharapkan|Kriteria Penerimaan|
|---|----------|-----------------|---------------------|
|1|Keputusan biner sederhana (Go/No-Go)|Pilihan yang benar dengan penjelasan|akurasi ≥90%.|
|2|Buktinya berbeda dari 3 sumber|Sintesis buktinya berbobot|≥85% akurasi resolusi|
|3|Bukti tidak lengkap (2 dari 4 sumber hilang)|Lanjutkan dengan penurunan kepercayaan diri|Confidence < 70%, peringatan eksplisit|
|4|Optimasi multi-objektif (3 tujuan)|Alternatif Pareto-optimal dipilih|≥90% kebenaran|
|5|Keputusan berisiko tinggi|Risiko ditandai dan dijelaskan|≥95% deteksi risiko|
|6|Skenario keyakinan rendah|Skor keyakinan ≤ 30%, rekomendasi ketidakpastian|Keyakinan kalibrasi dalam ±5%|
|7|Tinjau kembali keputusan dengan bukti baru|Keputusan direvisi dengan perbandingan dengan keputusan sebelumnya|Jejak revisi dicatat|
|8|Rekomendasi kembalikan|Rollback disarankan ketika melebihi risiko ambang batas|≥90% akurasi pemicu|
|9|Analisis trade-off (kecepatan vs akurasi)|Visualisasi trade-off yang jelas|Semua tujuan diberi skor|
|10|Penjelasan kelengkapan rantai|Rantai bukti→keputusan lengkap disajikan|≥95% kelengkapan|

### Kriteria Penerimaan Golden Test

- Semua 10 skenario Golden Test lulus pada ≥90% dari kriteria penerimaan individu
- Tingkat kelulusan Golden Test Decision Intelligence keseluruhan ≥90%
- Rantai penjelasan lengkap dihasilkan untuk setiap skenario
- Skor keyakinan terkalibrasi dalam ±5% dari akurasi aktual

---

## Persyaratan Kasus Nyata

### Direktori Kasus Nyata

`real_cases/decision_intelligence/` harus berisi:

|Urutannya|Jumlah Minimal|
|-------------|---------------|
|Kasus keputusan nyata dari penggunaan aktual|20|
|Kasus dengan riwayat revisi keputusan|5|
|Kasus dengan rekomendasi rollback|5|
|Kasus yang melibatkan banyak Capability Pack|10|
|Kasus dengan review/validasi ahli|15|

### Struktur Kasus Nyata

Setiap kasus nyata harus mencakup:

```
real_cases/decision_intelligence/<case_id>/
├── input/
│   ├── context.md           # Decision context and goals
│   ├── evidence/            # Evidence from source Capability Packs
│   │   └── <source_id>.json
│   └── constraints.md       # Hard constraints
├── output/
│   ├── decision_result.json # Full Decision Result contract output
│   ├── explanation.md       # Human-readable explanation
│   └── experience_memory_entry.json
└── evaluation.md            # Ground truth, expert review, lessons learned
```

### Targetkan Kasus Nyata

|Metrik|Target|
|--------|--------|
|Kasus nyata yang dicatat|≥20 (Siap Produksi Level 3) → ≥50 (Pakar Domain Level 4)|
|Skor kasus kualitas nyata (review ahli)|≥90%|
|Pelacakan hasil pasca keputusan|≥80% kasus dengan hasil yang dilacak|

---

## Definisi Selesai

```text
Definition of Done — Decision Intelligence Capability Pack

Functional
- [ ] Evidence Collection accepts evidence from ≥3 source types (analysis, recommendation, data, benchmark, historical)
- [ ] Alternative Generation produces ≥2 viable alternatives for any decision context
- [ ] Risk Analysis produces probability × impact score per alternative with ≥3 risk factor categories
- [ ] Trade-off Analysis supports ≥3 simultaneous objectives with weighted scoring
- [ ] Decision Scoring ranks alternatives and produces a recommended decision
- [ ] Confidence Estimation produces 0–100% confidence with uncertainty bounds
- [ ] Explainable Decision produces full evidence→reasoning→simulation→alternatives→risk→decision→rationale chain
- [ ] Decision History records every decision to Experience Memory

Benchmark
- [ ] Benchmark score ≥ 90% (grade A) across all 13 standard dimensions + confidence calibration
- [ ] Decision accuracy ≥ 90%
- [ ] Explainability ≥ 95%
- [ ] Consistency ≥ 90%
- [ ] Confidence calibration within ±5%

Golden Tests
- [ ] All 10 pack golden test scenarios pass at ≥90% of acceptance criteria (100% pass)

Real Cases
- [ ] ≥ 20 real cases logged in real_cases/decision_intelligence/
- [ ] Evaluation notes recorded for each case
- [ ] ≥ 5 cases with decision revision history
- [ ] ≥ 5 cases with rollback recommendations

Documentation
- [ ] Capability Guide updated (CAPABILITY_GUIDE.md — Decision Intelligence section)
- [ ] API reference / contract updated (this RFC + schemas.py)
- [ ] Real case evaluation summary published

SDK
- [ ] Pack accessible via SDK without Core changes
- [ ] Decision Intelligence callable via Execution Runtime task routing

Performance
- [ ] Latency P95 < 2000ms for standard scenarios
- [ ] Latency P95 < 5000ms for multi-source evidence scenarios

Security
- [ ] No known P0/P1 security issues
- [ ] Decision explanations do not leak sensitive evidence payloads

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
|Decision Intelligence menjadi hambatan|Tinggi — semua paket bergantung padanya|Sedang|Desain non-blocking; bukti penilaian cache; mengirimkan bukti secara paralel|
|Penjelasan terlalu panjang atau terlalu ringkas|Sedang — mempengaruhi metrik keterjelasan|Tinggi|Kedalaman penjelasan dapat dikonfigurasi; default sedang; loop umpan balik pengguna|
|Skor kepercayaan diri kurang terkalibrasi|Tinggi — merusak kepercayaan|Sedang|Kalibrasi pada 100 skenario sebelum rilis; pembelajaran berkelanjutan dari kasus nyata|
|Analisis risiko membebani lebih pada event langka|Sedang — keputusan kurang optimal|Sedang|Penilaian risiko berbatas; parameter toleransi risiko|
|Ketergantungan sirkuler: Decision Intelligence bergantung pada paket yang bergantung padanya|Tinggi — kebuntuan arsitektur|Rendah|Gunakan bukti pengajuan asinkron; tanpa panggilan pack-ke-pack sinkron|
|Optimasi multi-objektif tidak menemukan solusi yang layak|Sedang — kegagalan keputusan|Rendah|Fallback ke penilaian tujuan tunggal; laporkan ketidaklayakan|
|Pengalaman Memori tumbuh tanpa batas|Rendah — biaya penyimpanan|Sedang|Pemangkasan berbasis TTL; ringkasan keputusan lama|

---

## Dampak ADR

**Apakah ini memerlukan perubahan Core?** Tidak.

Decision Intelligence adalah **Capability Pack baru** yang mengikuti pola yang sudah ada:

- **ADR-001 (Core Pipeline Freeze):** Tidak ada perubahan Core. Semua logika di `apps/decision_intelligence/`.
- **ADR-002 (Capability Pack Kemerdekaan):** Decision Intelligence berkomunikasi dengan paket lain melalui tugas Execution Runtime dan kontrak bersama saja. Tanpa import langsung.
- **ADR-003 (Pekerja = Hanya Adaptor):** Pekerja tipis merutekan tugas ke Mesin Domain.
- **ADR-004 (Domain Engine Owns Business Logic):** Semua penalaran logika berada di `apps/decision_intelligence/engine.py`.
- **ADR-005 (Diperlukan Persetujuan Manusia):** Keputusan adalah rekomendasi; eksekusi memerlukan persetujuan eksplisit pengguna.
- **ADR-006 (Capability Contract v1 Frozen):** Menggunakan Capability Contract yang ada pendaftaran untuk node dan subtask template. Tidak ada perubahan kontrak.
- **ADR-007 (Batas Percakapan):** Decision Intelligence dipanggil melalui Execution Runtime, bukan langsung oleh Conversation Manager.
- **ADR-008 (Perubahan Inti Memerlukan Bukti Lintas Kemampuan):** Tidak berlaku — tidak ada perubahan Core.

**ADR yang diperlukan:** Tidak ada. Ini adalah Capability Pack baru, bukan modifikasi Core.

---

## Peluncuran Rencana

### Fase 1: Prototipe (RFC → Eksperimental)

**Durasi:** 4 minggu

- [x] Membuat struktur paket `apps/decision_intelligence/`
- [x] Mengimplementasikan Pengumpulan Bukti dan Penilaian Keputusan (kriteria tunggal)
- [x] Mendefinisikan kontrak publik (Permohonan Keputusan, Hasil Keputusan)
- [x] Mengimplementasikan adaptor Worker tipis
- [x] Membuat 10 skenario Golden Test (disederhanakan: keputusan biner)
- [x] Integrasi: Trading Analyst → Decision Intelligence (pengajuan bukti)
- **Gerbang:** 10 Golden Test lulus pada ≥80%

### Fase 2: Kapabilitas Lengkap (Eksperimental → Stabil)

**Durasi:** 6 minggu

- [x] Mengimplementasikan Generasi Alternatif
- [x] Mengimplementasikan Analisis Risiko (probabilitas × dampak)
- [x] Mengimplementasikan Trade-off Analysis (scoring berbobot multi-objektif)
- [x] Mengimplementasikan Confidence Estimation dengan kalibrasi
- [x] Mengimplementasikan Keputusan yang Dapat Dijelaskan (rantai lengkap)
- [x] Mengimplementasikan Sejarah Keputusan → Memori Pengalaman
- [x] Memperluas Golden Test menjadi 10 skenario penuh
- [x] Mencatat ≥20 kasus nyata dari penggunaan Trading Analyst
- [x] **Benchmark:** 100 skenario, akurasi ≥90%, kemampuan penjelasan ≥95%
- [x] **Integrasi:** Network Engineer, Code Engineer, DevOps Assistant mulai menggunakan Decision Intelligence untuk keputusan yang diberi skor
- **Gerbang:** Semua 10 Golden Test lulus pada ≥90%; Benchmark ≥90%

### Fase 3: Ekosistem (Stabil → Bersertifikat)

**Durasi:** 8 minggu

- [x] Semua 13+ Capability Pack terintegrasi dengan Decision Intelligence
- [x] Kalibrasi Confidence divalidasi pada ≥50 kasus nyata
- [x] Riwayat Keputusan mendukung rekomendasi rollback
- [x] Audit independen terhadap kualitas dan keterjelasan keputusan
- [x] Dasbor Benchmark publik tersedia
- [x] **Benchmark:** ≥90% di semua dimensi
- [x] **Kasus Nyata:** ≥50 kasus dengan ≥80% hasil pelacakan
- **Gerbang:** Audit kelulusan independen; Benchmark ≥90% berkelanjutan

---

## Peningkatan di Masa Depan

### Fase 2 (Pasca-Rilis v1.0.0)

1. **Mesin Simulasi Keputusan** — Simulasi Monte Carlo dari alternatif sebelum penilaian
2. **Debat Multi-Model** — Menggunakan banyak LLM untuk memperdebatkan alternatif (memanfaatkan pola mesin debat yang ada dari Trading Analyst)
3. **Pembobotan Kriteria Adaptif** — Mempelajari bobot objektif optimal dari hasil keputusan historis
4. **Visualisasi Grafik Keputusan** — Grafik interaktif dari rantai bukti → keputusan → hasil

### Fase 3 (Perusahaan)

1. **Decision Templates** — Kerangka keputusan yang sudah jadi untuk skenario umum (architecture review, strategi deployment, keputusan investasi)
2. **Mesin Kebijakan** — Menyandikan kebijakan keputusan organisasi sebagai batasan
3. **Pembelajaran Keputusan Lintas Ruang Kerja** — Mengagregasi hasil keputusan anonim lintas ruang kerja untuk kalibrasi kepercayaan diri di seluruh platform
4. **Lapisan Kepatuhan Peraturan** — Penjelasan keputusan yang disesuaikan untuk SOC 2, ISO 27001, dan kerangka kepatuhan lainnya

### Jangka Panjang

1. **Decision Intelligence Marketplace** — Kerangka keputusan pihak ketiga dan model penalaran kustom
2. **Mesin Inferensi Kausal** — Berpindah dari bukti berbasis korelasi ke penalaran kausal untuk dukungan keputusan
3. **Active Learning Loop** — Mengidentifikasi dan meminta bukti yang hilang secara otomatis untuk mengurangi keputusan
4. **Decision-Time Optimization** — Memilih kedalaman penalaran secara dinamis berdasarkan pentingnya keputusan dan batasan waktu

---

## Persyaratan Kasus Nyata

*(Lihat bagian [Persyaratan Real Case](#persyaratan-real-case) di atas untuk spesifikasi lengkap)*

Real case Decision Intelligence bersumber dari:

1. **Trading Analyst** — Keputusan rekomendasi trading dengan hasil pasca-pasar
2. **Code Engineer** — Keputusan refactoring vs rewrite dengan metrik kualitas kode
3. **Network Engineer** — Keputusan perubahan konfigurasi dengan verifikasi pasca-penempatan
4. **Asisten DevOps** — Keputusan penerapan strategi dengan pelacakan sukses/gagal
5. **Pengembangan Diri** — Proposal perbaikan arsitektur dengan review pasca-implementasi

---

## Definisi Selesai

*(Lihat bagian [Definition of Done](#definition-of-done) di atas untuk daftar periksa lengkap)*
