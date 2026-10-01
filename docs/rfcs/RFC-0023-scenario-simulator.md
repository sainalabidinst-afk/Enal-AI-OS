# RFC-0023: Real-Time Simulation & Sandboxing Module

|Bidang|Nilai|
|-------|-------|
|**ID RFC**|RFC-0023|
|**Status**|Draft|
|**Versi**|0.1.0|
|**Penulis**|Tim Inti AI OS Akhir|
|**Target Rilis**|v2.1.0 (Fase Keunggulan Kemampuan +)|
|**Capability Pack**|Scenario Simulator|
|**ID Kemampuan**|`scenario-simulator`|
|**Kategori**|Simulasi / Cognitive|
|**Target Kualitas**|A+ (≥95)
|**Target Kematangan**|Level 4 — Domain Expert (L4)|
|**Referensi RFC**|RFC-0023|
|**ADR yang Dilanggar**|Tidak ada (Capability Pack baru)|

---

## Ringkasan

Capability Pack Scenario Simulator menambahkan modul simulasi prediktif dan sandboxing real-time ke ECP. Pengguna dapat memasukkan variabel awal ("Jika suku bunga naik 1% dan kompetitor A turun harga 20%"), lalu mesin ini menjalankan simulasi Monte Carlo melalui Cognitive Pipeline, menampilkan hasil terbaik, terburuk, dan paling mungkin.

---

## Motivasi

Saat ini, banyak keputusan dibuat berdasarkan data historis atau best guess. Dunia nyata penuh ketidakpastian. ECP v1.0 memiliki `simulation_engine.py` di core yang hanya melakukan step-by-step plan verification (dry-run), dan `sandbox.py` untuk eksekusi kode terisolasi — tetapi tidak ada mekanisme untuk:

1. **Skenario What-If multi-variabel** — Menggabungkan beberapa variabel perubahan sekaligus dan melihat interaksinya
2. **Simulasi Monte Carlo berulang** — Menjalankan ratusan iterasi untuk membangun distribusi probabilitas hasil
3. **Sandbox eksperimen aman** — Menjalankan logika bisnis dalam environment terisolasi sebelum eksekusi nyata
4. **Prediksi outcome terdistribusi** — Menghasilkan histogram hasil terbaik, terburuk, dan paling mungkin

Tanpa modul ini, ECP tetap sebagai sistem analisis reaktif, bukan sistem prediksi strategis.

---

## Pernyataan Masalah

| Aspek | Keterbatasan Saat Ini | Dampak |
|-------|---------------------|--------|
| Simulasi skenario | Hanya dry-run step-by-step, tidak mendukung variabel perubahan | Keputusan tidak mempertimbangkan skenario alternatif |
| Monte Carlo | Tidak ada iterasi probabilistik | Tidak ada kuantifikasi ketidakpastian |
| Sandbox | Hanya eksekusi kode Python/Bash, tidak untuk eksperimen bisnis | Eksperimen risiko tinggi tidak dapat diuji di environment aman |
| Prediksi outcome | Heuristic saja (base_score + objective_boost - risk_penalty) | Prediksi tidak realistis untuk skenario kompleks |
| Integrasi pipeline | Simulasi tidak tersedia sebagai layanan kognitif | Penggunaan manual, tidak otomatis |

---

## Tujuan

1. **Skenario What-If** — Memungkinkan pengguna mendefinisikan variabel awal dan rentang perubahanannya
2. **Simulasi Monte Carlo** — Menjalankan N iterasi dengan variabel yang bervariasi secara acak dalam rentang yang ditentukan
3. **Sandbox Eksperimen** — Menjalankan logika/eksekusi dalam environment terisolasi untuk uji coba
4. **Distribusi Outcome** — Menghasilkan statistik hasil (min, max, mean, percentiles, histogram)
5. **Integrasi Cognitive Pipeline** — Tersedia sebagai layanan kognitif yang dapat dipanggil oleh pipeline
6. **Explainability** — Menyajikan rantai aksioma → asumsi → hasil simulasi → prediksi

### Kriteria Keberhasilan

| Metrik | Target | Nilai |
|--------|--------|-------|
| Akurasi prediksi | Konsistensi antar simulasi yang sama | ≥90% |
| Cakupan skenario | Rentang variabel yang dapat diuji | 5+ variabel simultan |
| Throughput Monte Carlo | Iterasi per detik | ≥10 iterasi/detik |
| Keandalan sandbox | Isolasi egzekusi yang aman | 100% terisolasi |
| Explainability | Rantai aksioma → hasil | ≥95% |
| Integrasi pipeline | Dapat dipanggil dari cognitive kernel | 100% |

---

## Non-Tujuan

1. **Eksekusi produksi langsung** — Simulasi bersifat prediktif; eksekusi nyata memerlukan persetujuan pengguna (ADR-005)
2. **Mengganti domain keahlian** — Simulator tidak menggantikan Trading Analyst, Network Engineer, dll; hanya menyediakan framework simulasi
3. **Real-time market data streaming** — Simulator bekerja pada data yang ada, bukan streaming pasar
4. **Modifikasi Core** — Semua implementasi di dalam Capability Pack (ADR-001, ADR-008 tidak dilanggar)

---

## Ruang Lingkup Kapabilitas

### Kapabilitas Inti

| Kapabilitas | Deskripsi | Masukan | Keluaran |
|-------------|-----------|---------|---------|
| Scenario Definition | Mendefinisikan variabel, rentang, dan asumsi dasar | Natural language description, variable definitions | ScenarioSpec |
| Monte Carlo Runner | Menjalankan N iterasi dengan variabel yang bervariasi | ScenarioSpec, iteration count | SimulationRun |
| Sandbox Executor | Menjalankan logika/eksekusi dalam environment terisolasi | Code/Logic block, input state | SandboxResult |
| Outcome Distribution | Menghitung statistik distribusi hasil | SimulationRun results | OutcomeDistribution |
| Prediction Report | Menyajikan hasil terbaik, terburuk, paling mungkin | OutcomeDistribution, scenario context | PredictionReport |
| Cognitive Integration | Tersedia sebagai layanan kognitif di pipeline | Cognitive context | Pipeline output |

---

## Kontrak Publik

### Kontrak Masukan: ScenarioRequest

```json
{
  "request_id": "uuid",
  "title": "string — scenario name",
  "description": "string — what-if description",
  "base_state": {
    "variables": [
      {
        "name": "interest_rate",
        "value": 0.05,
        "type": "float",
        "unit": "percentage"
      }
    ]
  },
  "variable_changes": [
    {
      "variable": "interest_rate",
      "change_type": "absolute_delta",
      "value": 0.01,
      "distribution": "fixed",
      "range": null
    },
    {
      "variable": "competitor_price",
      "change_type": "percent_delta",
      "value": -0.20,
      "distribution": "normal",
      "range": {"min": -0.30, "max": -0.10, "stddev": 0.05}
    }
  ],
  "iterations": 100,
  "sandbox_enabled": true,
  "context": "object — additional context from capability packs"
}
```

### Kontrak Keluaran: SimulationResult

```json
{
  "request_id": "uuid",
  "title": "string",
  "iterations_run": 0,
  "outcomes": {
    "best_case": {"value": 0.0, "variables": {}, "explanation": "string"},
    "worst_case": {"value": 0.0, "variables": {}, "explanation": "string"},
    "most_likely": {"value": 0.0, "variables": {}, "explanation": "string"},
    "mean": 0.0,
    "median": 0.0,
    "p5": 0.0,
    "p95": 0.0,
    "std_dev": 0.0,
    "histogram": [{"bucket": "string", "count": 0}]
  },
  "assumptions": ["string"],
  "key_drivers": ["string"],
  "confidence": 0.0,
  "explanation_chain": {
    "axioms": ["string"],
    "simulation_logic": "string",
    "outcome_interpretation": "string"
  },
  "sandbox_logs": []
}
```

---

## Titik Integrasi

### Cognitive Pipeline Integration

Scenario Simulator dapat dipanggil melalui Execution Runtime sebagai tugas:

```json
{
  "domain": "simulation",
  "intent": "Run what-if scenario analysis for: [user query]",
  "payload": {"scenario": {"variables": [...], "changes": [...]}}
}
```

### Pipeline Preset Integration

Untuk tugas kompleks/very_complex, `simulation` dapat ditambahkan ke pipeline:

```
COMPLEX: perception → memory → planning → reasoning → simulation → 
         debate → decision → verification → reflection → action → learning
```

### Core Service Dependency

- `sandbox_runtime` (ADR-001 compliant — no direct import; accessed via contract)
- `model_router` (untuk prediksi dry-run dan interpretasi hasil)
- `memory_manager` (untuk mengakses data historis sebagai baseline)
- `cognitive_kernel` (untuk integrasi layanan kognitif)

---

## Ketergantungan

### Dependensi Internal (Kontrak Bersama)

1. **Execution Runtime** — Task routing (ADR-002)
2. **Sandbox Runtime** — Isolated code execution (ADR-001)
3. **Model Router** — LLM inference for prediction and interpretation
4. **Memory Manager** — Access to historical data for baseline scenarios
5. **Cognitive Kernel** — Pipeline service integration

### Tidak Ada Perubahan Inti yang Diperlukan

```text
apps/
└── scenario_simulator/
    ├── __init__.py              # App class + factory
    ├── engine.py                # Domain Engine (owner of business logic per ADR-004)
    ├── worker.py                # Thin adapter (per ADR-003)
    ├── schemas.py               # Public contracts (ScenarioRequest, SimulationResult)
    ├── scenario_builder.py      # Scenario definition from natural language
    ├── monte_carlo_runner.py    # Monte Carlo iteration engine
    ├── sandbox_executor.py      # Sandbox experiment runner
    ├── outcome_analyzer.py      # Distribution statistics and prediction
    └── explanation_generator.py # Explainability chain
```

**Dampak ADR:** Tidak ada. Capability Pack baru, tidak memodifikasi Core.

---

## Spesifikasi Benchmark

| Dimensi | Definisi | Target |
|---------|----------|--------|
| Akurasi Simulasi | Konsistensi hasil untuk input yang sama | ≥90% |
| Throughput | Iterasi Monte Carlo per detik | ≥10 iter/detik |
| Isolation | Sandbox aman dan terisolasi | 100% |
| Variabel Kompleks | Jumlah variabel simultan yang didukung | 5+ |
| Explainability | Rantai penjelasan lengkap | ≥95% |
| Integrasi Pipeline | Layanan kognitif yang dapat dipanggil | 100% |
| Performance | P95 latency untuk 100 iterasi | < 5000ms |

---

## Definisi Selesai

```text
Definition of Done — Scenario Simulator Capability Pack

Functional
- [ ] Scenario Definition: 5+ variable types (float, int, boolean, enum, string)
- [ ] Monte Carlo Runner: configurable iterations, multiple distributions
- [ ] Sandbox Executor: Python and Bash execution in isolated environment
- [ ] Outcome Distribution: best/worst/most-likely + percentiles + histogram
- [ ] Cognitive Integration: available as cognitive service "simulation"
- [ ] Explainability: full axiom → assumption → outcome → prediction chain

Benchmark
- [ ] Simulation consistency ≥ 90% (same input = same output distribution)
- [ ] 10+ iter/detik throughput
- [ ] 5+ simultaneous variables supported
- [ ] P95 latency < 5000ms for 100 iterations

Golden Tests
- [ ] 10 skenario golden test lulus pada ≥90%
- [ ] What-if analysis with single variable change
- [ ] What-if analysis with multi-variable change
- [ ] Monte Carlo distribution sanity check
- [ ] Sandbox isolation verification
- [ ] Best/worst/most-likely prediction accuracy

Real Cases
- [ ] ≥5 real cases in real_cases/scenario_simulator/
- [ ] Integration cases with Decision Intelligence and Trading Analyst

Documentation
- [ ] docs/capabilities/scenario-simulator.md
- [ ] API reference / contract (schemas.py)
- [ ] Integration guide for capability pack consumers
```

---

## Linimana

### Fase 1: Prototipe (RFC → Eksperimental)

**Durasi:** 3 minggu

- [ ] Struktur paket `apps/scenario_simulator/`
- [ ] Scenario Definition dengan natural language parsing
- [ ] Monte Carlo Runner (basic, fixed + normal distributions)
- [ ] Sandbox Executor (leveraging existing `sandbox_runtime`)
- [ ] Outcome Distribution (best/worst/most-likely + mean/median/percentiles)
- [ ] 5 skenario golden test dasar
- [ ] **Gerbang:** 5/5 golden test lulus ≥80%

### Fase 2: Kapabilitas Lengkap (Eksperimental → Stabil)

**Durasi:** 4 minggu

- [ ] Multi-distributon support (uniform, triangular, custom)
- [ ] Cognitive Pipeline integration (simulation service)
- [ ] Explainability chain generator
- [ ] Integration dengan Decision Intelligence
- [ ] 10 skenario golden test lengkap
- [ ] ≥10 real cases
- [ ] **Gerbang:** Semua golden test lulus ≥90%; Benchmark ≥90%

### Fase 3: Ekosistem (Stabil → Bersertifikat)

**Durasi:** 6 minggu

- [ ] Integration dengan Trading Analyst, Network Engineer, System Architect
- [ ] Performance optimization (parallel iteration)
- [ ] Advanced distributions (beta, log-normal)
- [ ] UI untuk konfigurasi skenario dan visualisasi hasil
- [ ] Audit independen
- [ ] **Gerbang:** RFC, Benchmark ≥90%, Golden Test 100%, Real Cases ≥10

---

## Risiko

|Risiko|Dampak|Kemungkinan|Mitigasi|
|------|------|-----------|--------|
|Sandbox exploit|Ekssekusi kode berbahaya|Rendah|Gunakan sandbox yang sudah ada, timeout, resource limits|
|Simulasi tidak akurat|Prediksi yang menyesatkan|Tinggi|Batasan kepastian (confidence score), disclaimer|
|Performa lambat pada iterasi tinggi|Batasi throughput|Medium|Parallel execution, configurable iterations|
|Model tidak konsisten|Output tidak deterministik|Tinggi|Seed-based RNG, caching hasil|
|Abstraksi variabel terlalu kompleks|Adopsi rendah|Medium|Dokumentasi skenario, preset variabel|

---

## Dampak ADR

**Apakah ini memerlukan perubahan Core?** Tidak.

Scenario Simulator adalah Capability Pack baru yang mengikuti pola yang sudah ada:

- **ADR-001 (Core Pipeline Freeze):** Tidak ada perubahan Core. Semua implementasi di `apps/scenario_simulator/`.
- **ADR-002 (Capability Pack Independence):** Berkomunikasi melalui Execution Runtime dan kontrak bersama.
- **ADR-003 (Worker = Adapter):** Worker tipis merutekan ke Domain Engine.
- **ADR-004 (Domain Engine Owns Business Logic):** Semua logika simulasi di `engine.py`.
- **ADR-005 (Human Approval Required):** Simulasi bersifat prediktif; rekomendasi memerlukan persetujuan.
- **ADR-006 (Capability Contract v1):** Menggunakan kontrak yang ada.
- **ADR-007 (Conversation Boundary):** Dipanggil melalui Execution Runtime.
- **ADR-008 (Core Change Requires Cross-Capability Proof):** Tidak ada perubahan Core.

**ADR yang diperlukan:** Tidak ada. Ini adalah Capability Pack baru.
