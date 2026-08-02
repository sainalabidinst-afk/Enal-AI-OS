# RFC-0007: Capability Pack Decision Intelligence

<!-- DOCUMENT_METADATA_START -->
**Pemilik:** Tim Dokumentasi
**Pemilik Canonical:** Pimpinan Tata Kelola Dokumentasi
**Terakhir Diverifikasi:** 2026-08-02
**Versi:** 1.0.0
**Status:** Aktif
<!-- DOCUMENT_METADATA_END -->

| Field | Nilai |
|-------|-------|
| **RFC ID** | RFC-0007 |
| **Status** | Draft |
| **Versi** | 0.1.0 |
| **Penulis** | Enal AI OS Core Team |
| **Target Rilis** | v1.2.0 (fase Capability Excellence) |
| **Capability Pack** | Decision Intelligence |
| **Capability ID** | `decision-intelligence` |
| **Kategori** | Reasoning |
| **Target Kualitas** | A (≥90) |
| **Target Maturity** | Level 3 — Production Ready |
| **RFC Referensi** | RFC-0007 |

---

## Motivasi

13 Capability Pack yang ada mencakup code, network, research, DevOps, trading, dan self-development. Setiap pack menghasilkan output — kode, konfigurasi, laporan research, sinyal trading — yang melibatkan keputusan yang memerlukan penalaran berbasis evidence.

Saat ini, keputusan ini dibuat secara embedded dan spesifik-pack. Tidak ada shared reasoning layer yang menerapkan kerangka keputusan yang konsisten, dapat diaudit, dan dapat dijelaskan di seluruh domain. Hal ini menyebabkan:

1. **Kualitas keputusan yang tidak konsisten** — setiap pack menemukan ulang pengumpulan evidence, risk scoring, dan estimasi confidence.
2. **Tidak ada penggunaan ulang keputusan lintas domain** — analisis risiko Trading Analyst tidak dapat menginformasikan pilihan refactoring Code Engineer, meskipun keduanya melibatkan trade-off risiko vs imbal hasil.
3. **Explainability yang terbatas** — keputusan dijelaskan melalui narasi spesifik-domain, bukan melalui rantai evidence-ke-keputusan yang terstruktur.
4. **Tidak ada jejak audit keputusan** — keputusan diproduksi tetapi tidak pernah dicatat dalam experience memory terstruktur yang dapat ditelusuri untuk pembelajaran dan rollback.

Decision Intelligence menjadi **reasoning layer** yang berada di antara produsen evidence (semua Capability Pack) dan konsumen keputusan (semua Capability Pack), menyediakan kerangka kerja terpadu untuk pengambilan keputusan berbasis evidence, dapat dijelaskan, dan dapat diaudit.

---

## Pernyataan Masalah

Tanpa Capability Pack Decision Intelligence yang khusus:

- **Evidence terisolasi per pack** — tidak ada mekanisme untuk mengumpulkan, memeringkat, dan mensintesis evidence dari banyak Capability Pack sebelum mencapai keputusan.
- **Alternatif jarang dieksplorasi** — kebanyakan pack menghasilkan satu rekomendasi tanpa membuat atau membandingkan alternatif.
- **Analisis risiko bersifat ad hoc** — risk scoring ada di sebagian pack (Trading, Network) tetapi tanpa metodologi terstandarisasi di seluruh platform.
- **Confidence tidak dikuantifikasi** — estimasi confidence tersirat dalam rekomendasi, tidak dimodelkan atau dikomunikasikan secara eksplisit.
- **Keputusan tidak dicatat** — tidak ada Decision History terstruktur untuk mendukung pembelajaran, rekomendasi rollback, atau audit kepatuhan.
- **Analisis trade-off tidak ada** — optimasi multi-objektif (akurasi vs latensi, biaya vs keandalan) ditangani per-pack, bukan melalui kerangka kerja terpadu.

Tidak adanya Decision Intelligence berarti ketika ECP berkembang mencakup lebih banyak Capability Pack, kualitas dan konsistensi keputusan tidak akan berskala — sebaliknya, keputusan justru akan semakin terfragmentasi.

---

## Tujuan

1. **Evidence Collection** — Mengumpulkan dan menyusun evidence dari satu atau lebih sumber (output Capability Pack, data kasus nyata, hasil benchmark).
2. **Alternative Generation** — Menghasilkan banyak alternatif yang layak untuk setiap konteks keputusan.
3. **Risk Analysis** — Mengkuantifikasi dan mengategorikan risiko yang terkait dengan setiap alternatif (probabilitas × dampak).
4. **Trade-off Analysis** — Menganalisis trade-off multi-objektif antar alternatif (akurasi vs biaya, kecepatan vs keamanan, dll.).
5. **Decision Scoring** — Memberi skor pada setiap alternatif terhadap kriteria dan bobot yang dapat dikonfigurasi.
6. **Confidence Estimation** — Menghasilkan skor confidence eksplisit untuk setiap keputusan, dengan kuantifikasi ketidakpastian.
7. **Explainable Decision** — Menghasilkan rantai penjelasan yang dapat dibaca manusia: evidence → reasoning → simulation → alternatives → risk → decision → rationale.
8. **Decision History** — Mencatat setiap keputusan, evidence, alternatif yang dipertimbangkan, dan hasilnya ke Experience Memory untuk pembelajaran dan rollback.

### Kriteria Keberhasilan

| Metrik | Target | Grade |
|--------|--------|-------|
| Akurasi Keputusan | ≥90% (keputusan benar ketika ground truth tersedia) | A |
| Explainability | ≥95% (rantai evidence-ke-keputusan lengkap disajikan) | A+ |
| Konsistensi | ≥90% (input yang sama menghasilkan keputusan yang sama di setiap run) | A |
| Kalibrasi Confidence | ≥85% (skor confidence mencerminkan akurasi aktual ±5%) | A |
| Deteksi Risiko | ≥90% (risiko teridentifikasi sesuai ground truth) | A |
| Kelengkapan Trade-off | ≥85% (semua objektif relevan dipertimbangkan) | A |

---

## Non-Tujuan

1. **Eksekusi keputusan langsung** — Decision Intelligence menghasilkan rekomendasi; eksekusi memerlukan persetujuan eksplisit pengguna sesuai ADR-005.
2. **Menggantikan keahlian domain** — Decision Intelligence adalah reasoning layer, bukan pengganti pengetahuan domain. Ia memperkuat tetapi tidak menggantikan Trading, Code, Network, dll.
3. **Sinyal trading pasar real-time** — Trading Analyst tetap memiliki kepemilikan pembuatan sinyal trading. Decision Intelligence dapat memberi skor pada keputusan trading tetapi tidak menghasilkan sinyal.
4. **Penegakan titik keputusan tunggal** — Setiap Capability Pack tetap dapat menghasilkan rekomendasinya sendiri yang spesifik-domain. Decision Intelligence menyediakan layer scoring dan penjelasan lintas-bagian.
5. **Modifikasi Core** — Semua implementasi harus berada di dalam Capability Pack Decision Intelligence, mengikuti ADR-002 dan ADR-004.

---

## Scope Kapabilitas

### Kapabilitas Inti

| Kapabilitas | Deskripsi | Input | Output |
|-----------|-------------|--------|---------|
| Evidence Collection | Mengumpulkan, memvalidasi, dan menyusun evidence dari satu atau lebih sumber. | Output Capability Pack, respons API, data benchmark, file kasus nyata | Set evidence terstruktur dengan skor kualitas |
| Alternative Generation | Menghitung alternatif yang layak untuk konteks keputusan tertentu. | Konteks keputusan, set evidence, batasan | Set alternatif dengan skor kelayakan awal |
| Risk Analysis | Menilai probabilitas dan dampak setiap alternatif. | Alternatif, evidence, data historis | Profil risiko per alternatif (probabilitas × dampak) |
| Trade-off Analysis | Menganalisis trade-off multi-objektif antar alternatif. | Alternatif, kriteria berbobot, batasan | Pareto frontier dari skor trade-off |
| Decision Scoring | Memberi skor dan memeringkat alternatif terhadap kriteria yang dapat dikonfigurasi. | Alternatif, bobot kriteria, evidence, risiko | Alternatif terurut dengan skor gabungan |
| Confidence Estimation | Mengkuantifikasi ketidakpastian dan confidence pada keputusan akhir. | Kualitas evidence, confidence model, kalibrasi historis | Skor confidence (0–100%) dengan batas ketidakpastian |
| Explainable Decision | Menghasilkan penjelasan yang dapat ditelusuri dan dibaca manusia. | Jejak keputusan lengkap, evidence, rantai penalaran | Dokumen penjelasan (evidence → decision → rationale) |
| Decision History | Mencatat keputusan ke Experience Memory untuk pembelajaran dan rollback. | Keputusan akhir, alternatif, evidence, hasil | Catatan keputusan di Experience Memory |

### Out of Scope

- Eksekusi trading real-time
- Provisioning sumber daya cloud langsung
- Integrasi langsung dengan sistem keputusan eksternal tanpa mediasi
- Advisory legal, medis, atau keuangan di luar batas Scope ECP yang ada
- Penerapan keputusan secara otonom (memerlukan persetujuan sesuai ADR-005)
- Menggantikan penalaran internal Capability Pack lain

---

## Kontrak Publik

### Input Contract: Decision Request

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

### Output Contract: Decision Result

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

### Catatan Keputusan (Experience Memory)

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

## Titik Integrasi (Capability Graph)

Capability Pack Decision Intelligence berintegrasi dengan semua Capability Pack yang ada dan yang akan datang melalui **Execution Runtime** dan **shared contract saja** (sesuai ADR-002). Ia tidak mengimpor engine Capability Pack lain secara langsung.

### Pipeline Integrasi

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

### Template Tugas

| Tugas | Subtugas |
|------|----------|
| Score Decision | Evidence Collection → Alternative Generation → Risk Analysis → Trade-off Analysis → Decision Scoring → Confidence Estimation → Explanation → Decision History |

---

## Capability Pack Konsumen

Decision Intelligence melayani semua Capability Pack yang ada sebagai reasoning layer lintas-bagian:

| Capability Pack Konsumen | Use Case |
|--------------------------|----------|
| **Trading Analyst** | Memberi skor alternatif trading, mengkuantifikasi confidence yang disesuaikan risiko, menjelaskan alasan rekomendasi trading |
| **Code Engineer** | Memberi skor alternatif refactoring, menganalisis trade-off (kompleksitas vs performa), mengestimasi risiko perubahan |
| **Network Engineer** | Membandingkan alternatif konfigurasi, menganalisis risiko kegagalan, merekomendasikan perubahan yang aman untuk rollback |
| **DevOps Assistant** | Mengevaluasi strategi deployment, trade-off biaya vs keandalan, merekomendasikan rollout optimal |
| **Research Assistant** | Memberi skor kualitas evidence, mengkuantifikasi confidence pada kesimpulan yang disintesis, menjelaskan penalaran |
| **Self Development** | Mengevaluasi proposal perbaikan arsitektur, memberi skor risiko vs manfaat, menghasilkan rencana yang dapat dijelaskan |
| **Decision Intelligence** (internal) | Menggunakan reasoning layer-nya sendiri untuk meta-keputusan tentang pembobotan evidence dan kalibrasi confidence |

---

## Dependensi

### Dependensi Internal (Shared Contracts)

1. **Execution Runtime** — Routing dan orkestrasi tugas (sesuai ADR-002)
2. **Experience Memory** — Persistensi catatan keputusan (sesuai ADR-011)
3. **Shared Contracts** — Definisi Task/Intent dan skema hasil (sesuai ADR-006)

### Tidak Ada Perubahan Core yang Diperlukan

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

| Dimensi | Definisi | Pengukuran | Target |
|-----------|------------|-------------|--------|
| **Accuracy** | Kebenaran keputusan akhir | % keputusan yang sesuai dengan ground truth atau konsensus ahli | ≥90% |
| **Completeness** | Cakupan evidence, alternatif, dan objektif | % elemen yang diperlukan yang dipertimbangkan dalam keputusan | ≥90% |
| **Explainability** | Kejelasan dan kemampuan telusur rantai keputusan | Evaluasi manusia: rantai evidence→decision lengkap disajikan | ≥95% |
| **Safety** | Tidak ada rekomendasi berbahaya atau tidak aman | % keputusan yang lulus batasan keamanan | ≥95% |
| **Efficiency** | Waktu respons dan penggunaan sumber daya | Latency P95 < 2000ms, penggunaan token optimal | dalam anggaran |
| **Consistency** | Input yang sama menghasilkan output yang sama di setiap run | Varian di 10 run berulang < 5% | ≥90% |
| **Confidence Calibration** | Skor confidence mencerminkan akurasi aktual | Kurva kalibrasi: confidence dalam ±5% dari akurasi aktual | ≥85% |
| **Risk Detection** | Risiko teridentifikasi sesuai ground truth | % risiko yang diketahui terdeteksi sebelum keputusan | ≥90% |

### Dataset Benchmark

- **100 skenario keputusan** yang mencakup domain:
  - Trading (pemilihan trade yang disesuaikan risiko, position sizing)
  - Code (refactoring vs rewrite, pemilihan library)
  - Network (migrasi konfigurasi, perubahan firewall policy)
  - DevOps (strategi deployment, perencanaan rollback)
  - Research (sintesis evidence, confidence kesimpulan)
  - Self-Development (scoring perbaikan arsitektur)
  - Cross-domain (keputusan trade-off multi-pack)

### Detail Dimensi Benchmark

| Tipe Skenario | Deskripsi | Sumber Ground Truth |
|---------------|-------------|---------------------|
| Conflicting Evidence | Sumber evidence saling bertentangan | Konsensus ahli |
| Incomplete Evidence | Sebagian evidence hilang | Konsensus ahli |
| Multi-objective Optimization | Banyak objektif yang saling bersaing | Pareto optimality |
| High Risk | Keputusan dengan risiko penurunan signifikan | Review ahli |
| Low Confidence | Ketidakpastian tinggi dalam evidence | Kalibrasi confidence |
| Decision Revision | Meninjau ulang keputusan sebelumnya dengan evidence baru | Riwayat keputusan |
| Rollback Recommendation | Mengidentifikasi kapan harus mengembalikan keputusan | Hasil historis |

---

## Spesifikasi Golden Test

Golden test suite (`benchmarks/golden_test_set.py`) harus menyertakan skenario Decision Intelligence:

| # | Skenario | Hasil yang Diharapkan | Kriteria Penerimaan |
|---|----------|-----------------|---------------------|
| 1 | Keputusan biner sederhana (Go/No-Go) | Pilihan yang benar dengan penjelasan | ≥90% akurasi |
| 2 | Evidence bertentangan dari 3 sumber | Sintesis evidence berbobot | ≥85% akurasi resolusi |
| 3 | Evidence tidak lengkap (2 dari 4 sumber hilang) | Lanjutkan dengan penurunan confidence | Confidence < 70%, peringatan eksplisit |
| 4 | Optimasi multi-objektif (3 objektif) | Alternatif Pareto-optimal dipilih | ≥90% kebenaran |
| 5 | Keputusan berisiko tinggi | Risiko ditandai dan dijelaskan | ≥95% deteksi risiko |
| 6 | Skenario confidence rendah | Skor confidence ≤ 30%, rekomendasi ditangguhkan | Kalibrasi confidence dalam ±5% |
| 7 | Revisi keputusan dengan evidence baru | Keputusan direvisi dengan perbandingan ke keputusan sebelumnya | Jejak revisi dicatat |
| 8 | Rekomendasi rollback | Rollback disarankan ketika risiko melebihi ambang | ≥90% akurasi pemicu |
| 9 | Analisis trade-off (kecepatan vs akurasi) | Visualisasi trade-off yang jelas | Semua objektif diberi skor |
| 10 | Kelengkapan rantai explainability | Rantai evidence→decision lengkap disajikan | ≥95% kelengkapan |

### Kriteria Penerimaan Golden Test

- Semua 10 skenario golden test lulus pada ≥90% dari kriteria penerimaan individu
- Tingkat kelulusan golden test Decision Intelligence keseluruhan ≥90%
- Rantai penjelasan lengkap dihasilkan untuk setiap skenario
- Skor confidence terkalibrasi dalam ±5% dari akurasi aktual

---

## Persyaratan Real Case

### Direktori Real Case

`real_cases/decision_intelligence/` harus berisi:

| Persyaratan | Jumlah Minimum |
|-------------|---------------|
| Kasus keputusan nyata dari penggunaan aktual | 20 |
| Kasus dengan riwayat revisi keputusan | 5 |
| Kasus dengan rekomendasi rollback | 5 |
| Kasus yang melibatkan banyak Capability Pack | 10 |
| Kasus dengan review/validasi ahli | 15 |

### Struktur Real Case

Setiap kasus nyata harus menyertakan:

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

### Target Real Case

| Metrik | Target |
|--------|--------|
| Kasus nyata yang dicatat | ≥20 (Level 3 Production Ready) → ≥50 (Level 4 Domain Expert) |
| Skor kualitas kasus nyata (review ahli) | ≥90% |
| Pelacakan hasil pasca-keputusan | ≥80% kasus dengan hasil yang dilacak |

---

## Definition of Done

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

| Risiko | Dampak | Kemungkinan | Mitigasi |
|------|--------|------------|------------|
| Decision Intelligence menjadi bottleneck | Tinggi — semua pack bergantung padanya | Sedang | Desain non-blocking; cache scoring evidence; pemrosesan evidence paralel |
| Penjelasan terlalu panjang atau terlalu ringkas | Sedang — memengaruhi metrik explainability | Tinggi | Kedalaman penjelasan dapat dikonfigurasi; default sedang; loop umpan balik pengguna |
| Skor confidence kurang terkalibrasi | Tinggi — merusak kepercayaan | Sedang | Kalibrasi pada 100 skenario sebelum rilis; continuous learning dari kasus nyata |
| Analisis risiko membebani lebih pada event langka | Sedang — keputusan suboptimal | Sedang | Risk scoring berbatas; parameter toleransi risiko |
| Dependensi sirkular: Decision Intelligence bergantung pada pack yang bergantung padanya | Tinggi — deadlock arsitektur | Rendah | Gunakan pengajuan evidence asinkron; tanpa panggilan pack-ke-pack sinkron |
| Optimasi multi-objektif tidak menemukan solusi layak | Sedang — kegagalan keputusan | Rendah | Fallback ke scoring objektif tunggal; laporkan infeasibility |
| Experience Memory tumbuh tanpa batas | Rendah — biaya penyimpanan | Sedang | Pruning berbasis TTL; summarisasi keputusan lama |

---

## Dampak ADR

**Apakah ini memerlukan perubahan Core?** Tidak.

Decision Intelligence adalah **Capability Pack baru** yang mengikuti pola yang sudah ada:

- **ADR-001 (Core Pipeline Freeze):** Tidak ada perubahan Core. Semua logika di `apps/decision_intelligence/`.
- **ADR-002 (Capability Pack Independence):** Decision Intelligence berkomunikasi dengan pack lain melalui tugas Execution Runtime dan shared contract saja. Tanpa import langsung.
- **ADR-003 (Worker = Adapter Only):** Worker tipis merutekan tugas ke Domain Engine.
- **ADR-004 (Domain Engine Owns Business Logic):** Semua logika penalaran berada di `apps/decision_intelligence/engine.py`.
- **ADR-005 (Human Approval Required):** Keputusan adalah rekomendasi; eksekusi memerlukan persetujuan eksplisit pengguna.
- **ADR-006 (Capability Contract v1 Frozen):** Menggunakan Capability Contract yang ada untuk pendaftaran node dan subtask template. Tidak ada perubahan kontrak.
- **ADR-007 (Conversation Boundary):** Decision Intelligence dipanggil melalui Execution Runtime, bukan langsung oleh Conversation Manager.
- **ADR-008 (Core Change Requires Cross-Capability Proof):** Tidak berlaku — tidak ada perubahan Core.

**ADR yang Diperlukan:** Tidak ada. Ini adalah Capability Pack baru, bukan modifikasi Core.

---

## Rencana Rollout

### Fase 1: Prototipe (RFC → Experimental)

**Durasi:** 4 minggu

- [ ] Membuat struktur paket `apps/decision_intelligence/`
- [ ] Mengimplementasikan Evidence Collection dan Decision Scoring (kriteria tunggal)
- [ ] Mendefinisikan kontrak publik (Decision Request, Decision Result)
- [ ] Mengimplementasikan adapter Worker tipis
- [ ] Membuat 10 skenario golden test (disederhanakan: keputusan biner)
- [ ] Integrasi: Trading Analyst → Decision Intelligence (pengajuan evidence)
- **Gate:** 10 golden test lulus pada ≥80%

### Fase 2: Kapabilitas Lengkap (Experimental → Stable)

**Durasi:** 6 minggu

- [ ] Mengimplementasikan Alternative Generation
- [ ] Mengimplementasikan Risk Analysis (probabilitas × dampak)
- [ ] Mengimplementasikan Trade-off Analysis (scoring berbobot multi-objektif)
- [ ] Mengimplementasikan Confidence Estimation dengan kalibrasi
- [ ] Mengimplementasikan Explainable Decision (rantai lengkap)
- [ ] Mengimplementasikan Decision History → Experience Memory
- [ ] Memperluas golden test menjadi 10 skenario penuh
- [ ] Mencatat ≥20 kasus nyata dari penggunaan Trading Analyst
- [ ] **Benchmark:** 100 skenario, ≥90% akurasi, ≥95% explainability
- [ ] **Integrasi:** Network Engineer, Code Engineer, DevOps Assistant mulai menggunakan Decision Intelligence untuk keputusan yang diberi skor
- **Gate:** Semua 10 golden test lulus pada ≥90%; benchmark ≥90%

### Fase 3: Ekosistem (Stable → Certified)

**Durasi:** 8 minggu

- [ ] Semua 13+ Capability Pack terintegrasi dengan Decision Intelligence
- [ ] Kalibrasi confidence divalidasi pada ≥50 kasus nyata
- [ ] Decision History mendukung rekomendasi rollback
- [ ] Audit independen terhadap kualitas dan explainability keputusan
- [ ] Dashboard benchmark publik tersedia
- [ ] **Benchmark:** ≥90% di semua dimensi
- [ ] **Real Cases:** ≥50 kasus dengan ≥80% pelacakan hasil
- **Gate:** Audit independen lulus; benchmark ≥90% berkelanjutan

---

## Peningkatan di Masa Depan

### Fase 2 (Pasca-Rilis v1.0.0)

1. **Decision Simulation Engine** — Simulasi Monte Carlo dari alternatif sebelum scoring
2. **Multi-Model Debate** — Menggunakan banyak LLM untuk memperdebatkan alternatif (memanfaatkan pola debate engine yang ada dari Trading Analyst)
3. **Adaptive Criteria Weighting** — Mempelajari bobot objektif optimal dari hasil keputusan historis
4. **Decision Graph Visualization** — Grafik interaktif dari rantai evidence → decision → outcome

### Fase 3 (Enterprise)

1. **Decision Templates** — Kerangka keputusan yang sudah jadi untuk skenario umum (architecture review, strategi deployment, keputusan investasi)
2. **Policy Engine** — Menyandikan kebijakan keputusan organisasi sebagai batasan
3. **Cross-Workspace Decision Learning** — Mengagregasi hasil keputusan anonim lintas workspace untuk kalibrasi confidence di seluruh platform
4. **Regulatory Compliance Layer** — Explainability keputusan yang disesuaikan untuk SOC 2, ISO 27001, dan kerangka kepatuhan lain

### Jangka Panjang

1. **Decision Intelligence Marketplace** — Kerangka keputusan pihak ketiga dan model penalaran kustom
2. **Causal Inference Engine** — Berpindah dari evidence berbasis korelasi ke penalaran kausal untuk dukungan keputusan
3. **Active Learning Loop** — Mengidentifikasi dan meminta evidence yang hilang secara otomatis untuk mengurangi ketidakpastian keputusan
4. **Decision-Time Optimization** — Memilih kedalaman penalaran secara dinamis berdasarkan pentingnya keputusan dan batasan waktu

---

## Persyaratan Real Case

*(Lihat bagian [Persyaratan Real Case](#persyaratan-real-case) di atas untuk spesifikasi lengkap)*

Real case Decision Intelligence bersumber dari:

1. **Trading Analyst** — Keputusan rekomendasi trading dengan hasil pasca-pasar
2. **Code Engineer** — Keputusan refactoring vs rewrite dengan metrik kualitas kode
3. **Network Engineer** — Keputusan perubahan konfigurasi dengan verifikasi pasca-deployment
4. **DevOps Assistant** — Keputusan strategi deployment dengan pelacakan sukses/gagal
5. **Self Development** — Proposal perbaikan arsitektur dengan review pasca-implementasi

---

## Definition of Done

*(Lihat bagian [Definition of Done](#definition-of-done) di atas untuk daftar periksa lengkap)*

