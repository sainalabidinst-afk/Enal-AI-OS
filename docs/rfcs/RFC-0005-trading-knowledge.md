# RFC-0005: Perluasan Pengetahuan Trading

<!-- DOCUMENT_METADATA_START -->
**Pemilik:** Tim Dokumentasi
**Pemilik Canonical:** Pimpinan Tata Kelola Dokumentasi
**Diverifikasi Terakhir:** 02-08-2026
**Versi:** 1.0.0
**Status:** Aktif
<!-- DOCUMENT_METADATA_END -->

|Bidang|Nilai|
|-------|-------|
|**ID RFC**|RFC-0005|
|**Status**|Draf|
|**Versi**|0.1.0|
|**Penulis**|Tim Inti AI OS Akhir|
|**Target Rilis**|v1.2.0 (fase Keunggulan Kemampuan)|
|**Capability Pack**|Analis Perdagangan|
|**ID Kemampuan**|`trading-analyst`|
|**Kategori**|Perdagangan|
|**Target Kualitas**|A- (≥85)|
|**Target Kematangan**|Level 3 — Siap Produksi|
|**Referensi RFC**|RFC-0005|

---

## Motivasi

Capability Pack Trading Analyst saat ini memiliki dasar pengetahuan analisis teknikal dan manajemen risiko yang solid tetapi kedalaman domainnya masih terbatas pada indikator teknikal dasar dan pola harga. Saat ini:

1. **Pengetahuan metodologi trading lanjutan tidak tersedia** — metodologi seperti Wyckoff, ICT, dan SMC yang digunakan oleh pedagang profesional tidak tercakup.
2. **Tidak ada analisis microstructure pasar** — konsep likuiditas, order block, dan aliran institusional tidak dipahami secara mendalam.
3. **Analisis wave dan Fibonacci terbatas** — Elliott Wave hanya dipahami secara konseptual, bukan secara praktis untuk peramalan.
4. **Volume profile tidak diimplementasikan** — analisis berbasis volume untuk identifikasi area nilai tidak tersedia.
5. **Tidak ada konteks makro dan psikologi** — faktor makroekonomi dan psikologi trading tidak dihubungkan dengan sinyal trading.

RFC-0005 memperluas kedalaman pengetahuan Trading Analyst di seluruh sembilan domain pengetahuan lanjutan, mengubahnya dari pack yang menganalisis menjadi pack yang dapat menghasilkan sinyal trading berbasis metodologi profesional dengan konteks makro dan psikologi.

---

## Pernyataan Masalah

Tanpa perluasan pengetahuan trading:

- **Sinyal trading tidak andal** — hanya berdasarkan indikator dasar, bukan metodologi profesional.
- **Tidak ada konteks microstructure** — pedagang tidak memahami aliran likuiditas dan order block.
- **Peramalan wave tidak akurat** — Elliott Wave diimplementasikan secara dangkal, menyebabkan peramalan yang tidak dapat diandalkan.
- **Tidak ada analisis berbasis volume** — volume profile dan POC tidak digunakan untuk identifikasi area nilai.
- **Konteks makro hilang** — faktor makroekonomi tidak dihubungkan dengan sinyal trading.
- **Psikologi trading tidak terukur** — bias kognitif dan manajemen emosi tidak diintegrasikan dengan rekomendasi trading.

Tidak adanya perluasan pengetahuan berarti Trading Analyst tidak dapat bersaing dengan strategi trading profesional, menyebabkan kinerja trading yang suboptimal.

---

## Tujuan

### 1. Wyckoff
- **Fase Wyckoff** — Akumulasi, Markup, Distribusi, Penurunan Harga
- **Operator Perilaku Gabungan** — Composite Operator behavior, accumulation/distribution phases
- **Analisis penawaran dan permintaan** — Supply/demand analysis, effort vs result
- **Hubungan harga dan volume Wyckoff** — Volume-price relationship, springs, upthrusts

### 2. ICT (Pedagang Lingkaran Dalam)
- **Konsep struktur pasar ICT** — Market structure, higher high/higher low, lower high/lower low
- **Kesenjangan Nilai Wajar (FVG)** — Fair Value Gap identification and trading
- **Blok pemesanan dan blok mitigasi** — Order blocks, mitigation blocks, breaker blocks
- **Model likuiditas** — Liquidity models, liquidity sweeps, equal highs/lows
- **Konsep berbasis analisis waktu** — Time-based analysis, killzones, optimal trade entries

### 3. SMC (Konsep Uang Cerdas)
- **Aliran tatanan kelembagaan** — Institutional order flow, smart money concepts
- **Likuiditas melanda** — Liquidity grabs, stop hunts, liquidity pools
- **Model pembuat pasar** — Market maker models, dealer behavior
- **Blok perintah interpretasi** — Order block interpretation, BOS, CHOCH
- **Zona premium dan diskon** — Premium/discount zones, equilibrium, inefficiencies

### 4. Gelombang Elliot
- **Dasar teori Elliott Wave** — Wave theory fundamentals, fractal nature
- **Pola impuls dan korektif** — Impulse patterns (5 waves), corrective patterns (ABC)
- **Hubungan Fibonacci** — Fibonacci retracement, extension, ratios
- **Derajat gelombang dan sifat fraktal** — Wave degrees, fractal self-similarity
- **Aturan validasi dan invalidasi** — Wave validation rules, invalidation criteria

### 5. Volume Profil
- **Volume profil vs volume berdasarkan harga** — Volume Profile vs Volume at Price
- **Titik Kendali (POC)** — Point of Control, Value Area, Value Area High/Low
- **Area Nilai serta Area Nilai Tinggi/Rendah** — Value Area, VAH, VAL
- **Pola volume profil** — Volume profile patterns, distribution, rotation
- **Integrasi dengan aksi harga** — Volume-price integration, confirmation signals

### 6. Makro
- **Interpretasi indikator makro** — GDP, CPI, unemployment, PMI interpretation
- **Dampak kebijakan Fed dan suku bunga** — Fed policy impact, rate decisions
- **Signifikansi kalender ekonomi** — Economic calendar significance, high-impact events
- **Hubungan pasar lintas** — Cross-market relationships, correlations
- **Rezim risk-on vs risk-off** — Risk-on/risk-off regimes, flight to safety

### 7. Pilihan
- **Opsi Yunani** — Delta, Gamma, Theta, Vega, Rho interpretation
- **Ikhtisar opsi strategi** — Options strategies (covered call, straddle, strangle)
- **Volatilitas dan kemiringan yang tersirat** — Implied volatility, volatility skew
- **Interpretasi rasio put/call** — Put/call ratio interpretation, sentiment indicator
- **Opsi aktivitas yang tidak biasa** — Unusual options activity, dark pool prints

### 8. Masa depan
- **Kontrak dasar berjangka** — Futures contracts fundamentals, margin, leverage
- **Contango vs keterbelakangan** — Contango vs backwardation, futures curve analysis
- **Dasar dan biaya bergulir** — Basis, roll cost, futures pricing
- **Batasan jabatan dan komitmen (COT)** — Commitments of Traders, institutional positioning
- **Kontrak berjangka sebagai instrumen melindungi nilai** — Hedging with futures, basis risk

### 9. Psikologi
- **Dasar psikologi perdagangan** — Trading psychology fundamentals, trader mindset
- **Bias kognitif dalam trading** — Cognitive biases (confirmation, anchoring, loss aversion)
- **Toleransi risiko dan psikologi position sizing** — Risk tolerance, position sizing psychology
- **Manajemen emosi** — Emotional management, FOMO, revenge trading
- **Pola perilaku pelaku pasar** — Market participant behavior, crowd psychology

### Kriteria Keberhasilan

|Metrik|Target|Nilai|
|--------|--------|-------|
|Akurasi Sinyal Trading|≥85% (sinyal benar terhadap ground truth)|A-|
|Akurasi Analisis Wyckoff|≥85% (identifikasi fase Wyckoff benar)|A-|
|Akurasi Analisis ICT|≥85% (identifikasi FVG, order block benar)|A-|
|Akurasi Analisis SMC|≥85% (identifikasi likuiditas, zona benar)|A-|
|Akurasi Analisis Elliott Wave|≥80% (count wave benar)|B+|
|Akurasi Volume Profile|≥85% (identifikasi POC, value area benar)|A-|
|Akurasi Analisis Makro|≥80% (prediksi dampak makro benar)|B+|
|Akurasi Analisis Opsi|≥80% (analisis Greeks, strategi benar)|B+|
|Akurasi Analisis Futures|≥80% (analisis struktur futures benar)|B+|
|Penjelasan|≥85% (penjelasan metodologi lengkap)|A-|
|Konsistensi|≥85% (input yang sama menghasilkan sinyal yang sama)|A-|
|Manajemen Risiko|≥90% (rekomendasi manajemen risiko tepat)|A-|

---

## Non-Tujuan

1. **Eksekusi perdagangan secara real-time** — Trading Analyst menghasilkan sinyal, eksekusi memerlukan persetujuan pengguna.
2. **Jaminan keuntungan** — Trading Analyst memberikan analisis berbasis bukti, tidak menjamin hasil.
3. **Mengganti platform trading** — Trading Analyst menganalisis dan merekomendasikan, platform trading tetap menjadi eksekutor.
4. **Konsultasi investasi berlisensi** — Trading Analyst memberikan analisis teknis, bukan nasihat investasi berlisensi.
5. **Akses data pasar real-time** — Trading Analyst menggunakan data yang tersedia, tidak menyediakan feed data langsung.

---

## Ruang Lingkup Kapabilitas

### Kapabilitas Inti

|Kapabilitas|Deskripsi|Masukan|Keluaran|
|-----------|-------------|--------|---------|
|Analisis Wyckoff|Menganalisis fase Wyckoff,Composite Operator, supply/demand|Data harga, volume, timeframe|Identifikasi fase, sinyal akumulasi/distribusi|
|Analisis ICT|Menganalisis struktur pasar ICT, FVG, order blocks, likuiditas|Data harga, timeframe, struktur pasar|Identifikasi FVG, order block, likuiditas|
|Analisis SMC|Menganalisis aliran smart money, liquidity sweeps, zona premium/diskon|Data harga, volume, order flow|Identifikasi zona, sinyal smart money|
|Analisis Elliott Wave|Menganalisis pola wave Elliott, count, hubungan Fibonacci|Data harga, timeframe, histogram wave|Count wave, target harga, invalidasi|
|Analisis Volume Profile|Menganalisis volume profile, POC, value area|Data harga, volume, timeframe distribusi|Identifikasi POC, VAH, VAL, area nilai|
|Analisis Makro|Menganalisis indikator makro, kebijakan Fed, kalender ekonomi|Data makro, berita, kalender|Dampak makro pada aset, risiko|
|Analisis Opsi|Menganalisis Greeks, strategi opsi, IV, aktivitas tidak biasa|Data opsi, volatilitas, Greeks|Sinyal opsi, rekomendasi strategi, peringatan|
|Analisis Futures|Menganalisis kontrak futures, struktur kontango/backwardation, COT|Data futures, struktur kurva, COT|Sinyal futures, hedging recomendation|
|Analisis Psikologi|Menganalisis bias kognitif, manajemen emosi, position sizing|Data trading historis, catatan psikologis|Rekomendasi position sizing, peringatan emosional|

### Di Luar Cakupan

- Eksekusi perdagangan secara real-time
- Konsultasi investasi berlisensi
- Akses data pasar real-time atau feed data langsung
- Pengelolaan portofolio atau alokasi aset
- Laporan akuntansi atau perpajakan trading

---

## Kontrak Publik

### Kontrak Masukan: Permintaan Analisis Trading

```json
{
  "analysis_request_id": "uuid",
  "asset": "string — ticker symbol or asset identifier",
  "timeframe": "string — 1m, 5m, 15m, 1h, 4h, 1d, 1w",
  "analysis_types": [
    "wyckoff | ict | smc | elliott_wave | volume_profile | macro | options | futures | psychology"
  ],
  "market_data": {
    "price_history": [
      {
        "timestamp": "ISO 8601",
        "open": 0.0,
        "high": 0.0,
        "low": 0.0,
        "close": 0.0,
        "volume": 0
      }
    ],
    "current_price": 0.0,
    "volume_profile": "object — optional pre-computed volume profile"
  },
  "context": {
    "position_type": "long | short | neutral",
    "holding_period": "scalping | day_trading | swing | position",
    "risk_tolerance": "conservative | moderate | aggressive"
  },
  "macro_context": {
    "interest_rates": "string — current rate environment",
    "economic_events": ["string — upcoming high-impact events"],
    "market_regime": "risk_on | risk_off | neutral"
  },
  "include_psychology": true,
  "include_risk_management": true
}
```

### Kontrak Keluaran: Laporan Analisis Trading

```json
{
  "analysis_request_id": "uuid",
  "asset": "string",
  "timeframe": "string",
  "analysis_timestamp": "ISO 8601",
  "market_structure": {
    "trend": "bullish | bearish | sideways",
    "phase": "accumulation | markup | distribution | markup",
    "key_levels": {
      "support": [0.0],
      "resistance": [0.0],
      "poc": 0.0,
      "vah": 0.0,
      "val": 0.0
    },
    "wyckoff_phase": "string — Wyckoff phase identification",
    "ict_analysis": {
      "fvg": ["object — Fair Value Gaps"],
      "order_blocks": ["object — Order Blocks"],
      "liquidity_zones": ["object — Liquidity pools"]
    },
    "smc_analysis": {
      "bos": "boolean — Break of Structure",
      "choch": "boolean — Change of Character",
      "liquidity_sweep": "boolean — recent liquidity sweep"
    },
    "elliott_wave": {
      "current_wave": "string — e.g., 'Wave 3 of 5'",
      "degree": "string — wave degree",
      "targets": [0.0],
      "invalidations": [0.0]
    }
  },
  "signals": [
    {
      "signal_id": "uuid",
      "type": "entry | exit | hold | reduce",
      "direction": "long | short",
      "confidence": 0.0,
      "methodology": "string — wyckoff | ict | smc | elliott_wave | volume_profile",
      "entry_price": 0.0,
      "stop_loss": 0.0,
      "take_profit": [0.0],
      "risk_reward_ratio": 0.0,
      "reasoning": "string — detailed reasoning"
    }
  ],
  "risk_assessment": {
    "overall_risk": "low | medium | high",
    "volatility": 0.0,
    "liquidity_risk": "low | medium | high",
    "max_drawdown_risk": 0.0,
    "recommended_position_size": "string — percentage of capital"
  },
  "psychology_assessment": {
    "fomo_risk": "low | medium | high",
    "revenge_trading_risk": "low | medium | high",
    "overconfidence_risk": "low | medium | high",
    "recommendations": ["string"]
  },
  "macro_impact": {
    "sentiment": "bullish | bearish | neutral",
    "key_events": ["string — upcoming economic events"],
    "risk_factors": ["string"]
  },
  "options_analysis": {
    "implied_volatility": 0.0,
    "iv_percentile": 0.0,
    "put_call_ratio": 0.0,
    "unusual_activity": ["string"],
    "recommended_strategies": ["string"]
  },
  "futures_analysis": {
    "basis": 0.0,
    "term_structure": "contango | backwardation | flat",
    "cot_positioning": "string — commercial | non-commercial | non-reportable",
    "roll_cost_estimate": 0.0
  },
  "confidence_score": 0.0,
  "summary": {
    "total_signals": 0,
    "entry_signals": 0,
    "exit_signals": 0,
    "avg_confidence": 0.0,
    "overall_recommendation": "string",
    "next_review": "ISO 8601"
  }
}
```

### Catatan Analisis Trading (Experience Memory)

```json
{
  "record_id": "uuid",
  "analysis_request_id": "uuid",
  "timestamp": "ISO 8601",
  "asset": "string",
  "timeframe": "string",
  "methodologies_used": ["string"],
  "signals_generated": 0,
  "outcome": "pending | correct | incorrect | partial",
  "pnl_impact": 0.0,
  "user_feedback": "string — optional",
  "lessons_learned": ["string"]
}
```

---

## Titik Integrasi (Grafik Kapabilitas)

```
Data Provider / User
    │
    │  provides market data, asset, timeframe
    ▼
Trading Analyst Engine
    │
    │  ┌───────────────────────────────────────────────────────────┐
    │  │ 1. Wyckoff Analysis                                       │
    │  │ 2. ICT Analysis                                           │
    │  │ 3. SMC Analysis                                           │
    │  │ 4. Elliott Wave Analysis                                  │
    │  │ 5. Volume Profile Analysis                                │
    │  │ 6. Macro Analysis                                         │
    │  │ 7. Options Analysis                                       │
    │  │ 8. Futures Analysis                                       │
    │  │ 9. Psychology Analysis → Experience Memory                │
    │  └───────────────────────────────────────────────────────────┘
    │
    │  returns Trading Analysis Report
    ▼
Decision Intelligence (optional)
    │
    │  scores and explains trading signals
    ▼
Security Engineer (optional)
    │
    │  validates trading strategy compliance
    ▼
User / Human Approval Loop
    │
    │  reviews signals and approves execution
    ▼
Execution Platform
```

### Templat Tugas

|Tugas|Subtugas|
|------|----------|
|Analisis Trading|Kumpulkan data pasar → Analisis Wyckoff → Analisis ICT → Analisis SMC → Analisis Wave → Analisis Volume Profile → Analisis Makro → Analisis Opsi → Analisis Futures → Analisis Psikologi → Skor sinyal → Manajemen risiko → Laporan|

---

## Capability Pack Konsumen

|Capability Pack Konsumen|Kasus Penggunaan|
|--------------------------|----------|
|**Decision Intelligence**|Memberikan skor pada sinyal trading, mengkuantifikasi keyakinan, menjelaskan alasan rekomendasi trading|
|**Insinyur Keamanan**|Menganalisis kepatuhan strategi trading terhadap regulasi|
|**Asisten DevOps**|Mengintegrasikan sinyal trading ke dalam pipeline deployment sistem trading|
|**Pengembangan Diri**|Menganalisis kinerja trading historis dan merekomendasikan perbaikan strategi|

---

## Ketergantungan

### Dependensi Internal (Kontrak Bersama)

1. **Execution Runtime** — Tugas perutean dan orkestrasi (sesuai ADR-002)
2. **Experience Memory** — Persistensi catatan analisis dan pembelajaran (sesuai ADR-011)
3. **Kontrak Bersama** — Definisi Task/Intent dan skema hasil (sesuai ADR-006)

### Basis Pengetahuan Eksternal

1. **Wyckoff Methodology** — Wyckoff phases, Composite Operator, supply/demand analysis
2. **ICT Trading Concepts** — Inner Circle Trader methodology, FVG, order blocks
3. **Smart Money Concepts** — Institutional flow, liquidity sweeps, premium/discount
4. **Elliott Wave Theory** — Wave patterns, Fibonacci relationships, wave degrees
5. **Volume Profile Analysis** — POC, value area, volume-based support/resistance
6. **Macro Economic Indicators** — GDP, CPI, PMI, Fed policy, economic calendar
7. **Options Greeks** — Delta, Gamma, Theta, Vega, implied volatility analysis
8. **Futures Markets** — Futures pricing, contango/backwardation, COT reports
9. **Trading Psychology** — Cognitive biases, emotional management, risk tolerance

### Tidak Ada Perubahan Inti yang Diperlukan

Semua implementasi berada di dalam Capability Pack Trading Analyst:

```
apps/
└── trading_analyst/
    ├── engine.py                  # Domain Engine (per ADR-004)
    ├── worker.py                  # Thin adapter (per ADR-003)
    ├── schemas.py                 # Public contracts
    ├── wyckoff_analyzer.py        # Wyckoff phase analysis
    ├── ict_analyzer.py            # ICT market structure analysis
    ├── smc_analyzer.py            # Smart Money Concepts analysis
    ├── elliott_wave_analyzer.py   # Elliott Wave analysis
    ├── volume_profile_analyzer.py # Volume Profile analysis
    ├── macro_analyzer.py          # Macro economic analysis
    ├── options_analyzer.py        # Options Greeks and strategies
    ├── futures_analyzer.py        # Futures analysis and COT
    ├── psychology_analyzer.py     # Trading psychology assessment
    └── knowledge_base.py          # Trading knowledge base
```

**Dampak ADR:** Tidak ada. Tidak diperlukan modifikasi Core, Runtime, Kernel, atau kontrak bersama.

---

## Spesifikasi Benchmark

### Kerangka Benchmark

|Dimensi|Definisi|pengukuran|Target|
|-----------|------------|-------------|--------|
|**Akurasi Sinyal**|Kebenaran sinyal trading terhadap ground truth|% sinyal benar vs ground truth|≥85%|
|**Akurasi Wyckoff**|Kebenaran identifikasi fase Wyckoff|% fase identifikasi benar|≥85%|
|**Akurasi ICT**|Kebenaran identifikasi FVG, order block|% identifikasi benar|≥85%|
|**Akurasi SMC**|Kebenaran identifikasi zona smart money|% identifikasi benar|≥85%|
|**Akurasi Elliott Wave**|Kebenaran count wave Elliott|% count benar|≥80%|
|**Akurasi Volume Profile**|Kebenaran identifikasi POC, value area|% identifikasi benar|≥85%|
|**Akurasi Makro**|Kebenaran prediksi dampak makro|% prediksi benar|≥80%|
|**Akurasi Opsi**|Kebenaran analisis Greeks, strategi|% analisis benar|≥80%|
|**Akurasi Futures**|Kebenaran analisis struktur futures|% analisis benar|≥80%|
|**Penjelasan**|Kejelasan penjelasan metodologi|Skor evaluasi manusia|≥85%|
|**Konsistensi**|Input yang sama menghasilkan sinyal yang sama|Varian di 10 run < 5%|≥85%|
|**Manajemen Risiko**|Kebenaran rekomendasi manajemen risiko|% rekomendasi tepat|≥90%|

### Kumpulan data Benchmark

- **100 skenario trading** yang mencakup:
  - Saham (AAPL, GOOGL, MSFT, TSLA)
  - Kripto (BTC, ETH, SOL)
  - Komoditas (emas, minyak, perak)
  - Valas (EUR/USD, GBP/USD, USD/JPY)
  - Indeks (S&P 500, Nasdaq, Dow Jones)

### Detail Dimensi Benchmark

|Tipe Skenario|Deskripsi|Sumber Kebenaran Tanah|
|---------------|-------------|---------------------|
|Fase Wyckoff|Identifikasi akumulasi, markup, distribusi|Konsensus ahli, data harga historis|
|FVG dan Order Block|Identifikasi FVG dan order block|Konsensus ahli ICT|
|Liquidity Sweep|Identifikasi liquidity grab dan stop hunt|Konsensus ahli SMC|
|Elliott Wave Count|Count wave impulse dan corrective|Konsensus ahli Elliott Wave|
|Volume Profile|Identifikasi POC dan value area|Data volume historis|
|Dampak Makro|Prediksi dampak berita makro|Konsensus ahli makro|
|Analisis Opsi|Interpretasi Greeks, strategi opsi|Data opsi historis, konsensus ahli|
|Struktur Futures|Analisis contango/backwardation, COT|Data futures historis|

---

## Spesifikasi Golden Test

| # |Skenario|Hasil yang diharapkan|Kriteria Penerimaan|
|---|----------|-----------------|---------------------|
|1|Identifikasi fase Wyckoff|Fase akumulasi/markup/distribusi teridentifikasi|≥85% akurasi|
|2|Identifikasi FVG dan order block (ICT)|FVG dan order block teridentifikasi|≥85% akurasi|
|3|Identifikasi zona smart money (SMC)|Zona likuiditas, premium/diskon teridentifikasi|≥85% akurasi|
|4|Elliott Wave count|Count wave 5 impulsif atau ABC korektif|≥80% akurasi|
|5|Identifikasi POC dan value area (Volume Profile)|POC, VAH, VAL teridentifikasi|≥85% akurasi|
|6|Prediksi dampak berita makro|Dampak pada harga teridentifikasi|≥80% akurasi|
|7|Analisis strategi opsi|Greeks, IV, strategi teridentifikasi|≥80% akurasi|
|8|Analisis struktur futures|Contango/backwardation, COT teranalisis|≥80% akurasi|
|9|Rekomendasi manajemen risiko|Position sizing, stop loss tepat|≥90% akurasi|
|10|Deteksi bias psikologis|Bias kognitif teridentifikasi|≥85% akurasi|

### Kriteria Penerimaan Golden Test

- Semua 10 skenario Golden Test lulus pada ≥85% dari kriteria penerimaan individu
- Tingkat kelulusan Golden Test Trading Analyst keseluruhan ≥85%
- Sinyal yang dihasilkan disertai penjelasan metodologi lengkap
- Manajemen risiko disertakan dalam setiap rekomendasi

---

## Persyaratan Kasus Nyata

### Direktori Kasus Nyata

`real_cases/trading/` harus berisi:

|Urutannya|Jumlah Minimal|
|-------------|---------------|
|Analisis trading nyata dari penggunaan aktual|100|
|Kasus dengan analisis Wyckoff|15|
|Kasus dengan analisis ICT|15|
|Kasus dengan analisis SMC|15|
|Kasus dengan analisis Elliott Wave|10|
|Kasus dengan analisis Volume Profile|10|
|Kasus dengan analisis Makro|10|
|Kasus dengan analisis Opsi|10|
|Kasus dengan analisis Futures|10|
|Kasus dengan analisis Psikologi|10|
|Kasus dengan review/validasi ahli|20|

### Struktur Kasus Nyata

```
real_cases/trading/<case_id>/
├── input/
│   ├── asset.md                 # Asset and timeframe
│   ├── market_data.json         # Historical price and volume data
│   ├── macro_context.json       # Economic events, Fed policy
│   └── user_context.json        # Risk tolerance, holding period
├── output/
│   ├── analysis_report.json     # Full Trading Analysis Report
│   ├── signals.json             # Generated trading signals
│   ├── risk_assessment.json     # Risk management recommendations
│   └── psychology_notes.md      # Psychology assessment notes
└── evaluation.md               # Ground truth, expert review, lessons learned
```

### Targetkan Kasus Nyata

|Metrik|Target|
|--------|--------|
|Kasus nyata yang dicatat|≥100 (Siap Produksi Level 3) → ≥200 (Pakar Domain Level 4)|
|Skor kasus kualitas nyata (review ahli)|≥85%|
|Pelacakan hasil pasca sinyal|≥80% kasus dengan hasil yang dilacak|

---

## Definisi Selesai

```text
Definition of Done — Trading Analyst Knowledge Expansion RFC

Functional
- [ ] Wyckoff Analysis identifies accumulation/markup/distribution phases
- [ ] ICT Analysis identifies FVG, order blocks, liquidity zones
- [ ] SMC Analysis identifies smart money flow, premium/discount zones
- [ ] Elliott Wave Analysis performs wave count and Fibonacci targets
- [ ] Volume Profile Analysis identifies POC, VAH, VAL
- [ ] Macro Analysis interprets economic indicators and Fed policy
- [ ] Options Analysis interprets Greeks, IV, and unusual activity
- [ ] Futures Analysis interprets term structure, basis, and COT
- [ ] Psychology Analysis identifies cognitive biases and emotional risks

Benchmark
- [ ] Signal Accuracy ≥ 85% (grade A-)
- [ ] Wyckoff Accuracy ≥ 85%
- [ ] ICT Accuracy ≥ 85%
- [ ] SMC Accuracy ≥ 85%
- [ ] Elliott Wave Accuracy ≥ 80%
- [ ] Volume Profile Accuracy ≥ 85%
- [ ] Macro Accuracy ≥ 80%
- [ ] Options Accuracy ≥ 80%
- [ ] Futures Accuracy ≥ 80%
- [ ] Explainability ≥ 85%
- [ ] Consistency ≥ 85%
- [ ] Risk Management ≥ 90%

Golden Tests
- [ ] All 10 pack golden test scenarios pass at ≥85% of acceptance criteria (100% pass)

Real Cases
- [ ] ≥ 100 real cases logged in real_cases/trading/
- [ ] Evaluation notes recorded for each case
- [ ] ≥ 15 cases with Wyckoff analysis
- [ ] ≥ 15 cases with ICT analysis
- [ ] ≥ 15 cases with SMC analysis
- [ ] ≥ 10 cases with Elliott Wave analysis
- [ ] ≥ 10 cases with Volume Profile analysis
- [ ] ≥ 10 cases with Macro analysis
- [ ] ≥ 10 cases with Options analysis
- [ ] ≥ 10 cases with Futures analysis
- [ ] ≥ 10 cases with Psychology analysis
- [ ] ≥ 20 cases with expert review

Documentation
- [ ] Capability Guide updated (CAPABILITY_GUIDE.md — Trading Analyst section)
- [ ] API reference / contract updated (this RFC + schemas.py)
- [ ] Real case evaluation summary published

SDK
- [ ] Pack accessible via SDK without Core changes
- [ ] Trading Analyst callable via Execution Runtime task routing

Performance
- [ ] Latency P95 < 3000ms for standard analysis
- [ ] Latency P95 < 8000ms for multi-methodology analysis

Security
- [ ] No known P0/P1 security issues
- [ ] Generated signals do not expose proprietary methodology details

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
|Sinyal trading tidak menguntungkan|Tinggi — kepercayaan pengguna menurun|Sedang|Manajemen risiko yang ketat; peringatan eksplisit; validasi ahli|
|Metodologi trading salah diimplementasikan|Tinggi — rekomendasi salah|Sedang|Validasi terhadap literatur ahli; pengujian pada data historis; loop umpan balik|
|Analisis makro salah menduga dampak|Sedang — rekomendasi salah|Tinggi|Kalibrasi berkelanjutan; interval kepercayaan; skenario alternatif|
|Psikologi trading terlalu subjektif|Sedang — rekomendasi tidak dapat diandalkan|Tinggi|Validasi terhadap literatur psikologi; anonimisasi data; konsistensi lintas analis|
|Elliott Wave count ambigu|Sedang — peramalan tidak konsisten|Tinggi|Aturan validasi yang ketat; kriteria invalidasi eksplisit; tingkat kepercayaan|
|Volume profile tidak akurat pada data jarang|Sedang — area nilai salah|Sedang|Metode interpolasi; peringatan pada data jarang; validasi silang|
|Analisis opsi salah menafsirkan Greeks|Sedang — rekomendasi strategi salah|Sedang|Validasi model pricing; pengujian pada data pasar historis|
|Data pasar tidak lengkap atau tidak akurat|Tinggi — analisis berdasarkan data salah|Sedang|Validasi data; peringatan pada data tidak lengkap; sumber data cadangan|

---

## Dampak ADR

**Apakah ini memerlukan perubahan Core?** Tidak.

RFC-0005 adalah **perluasan pengetahuan** untuk Capability Pack Trading Analyst yang sudah ada:

- **ADR-001 (Arsitektur Bus Acara):** Tidak memerlukan perubahan. Trading Analyst menggunakan Event Bus yang ada.
- **ADR-002 (Arsitektur Capability Pack):** Tidak memerlukan perubahan. Perluasan pengetahuan berada di dalam pack yang ada.
- **ADR-003 (Desain AST Universal):** Tidak memerlukan perubahan. Perluasan pengetahuan untuk analisis trading.
- **ADR-004 (Pemilik Logika Bisnis Domain Engine):** Tidak memerlukan perubahan. Semua logika baru berada di `apps/trading_analyst/`.
- **ADR-005 (Diperlukan Persetujuan Manusia):** Tidak memerlukan perubahan. Sinyal trading memerlukan persetujuan pengguna.
- **ADR-006 (Kontrak Kemampuan v1 Dibekukan):** Tidak memerlukan perubahan. Perluasan pengetahuan tidak mengubah kontrak.
- **ADR-007 (Batas Percakapan):** Tidak memerlukan perubahan.
- **ADR-008 (Perubahan Inti Memerlukan Bukti Lintas Kemampuan):** Tidak berlaku — tidak ada perubahan Core.

**ADR yang diperlukan:** Tidak ada. RFC-0005 adalah perluasan pengetahuan internal pack.

---

## Peluncuran Rencana

### Fase 1: Metodologi Dasar (RFC → Eksperimental)

**Durasi:** 6 minggu

- [x] Mengimplementasikan analisis Wyckoff (fase, Composite Operator, supply/demand)
- [x] Mengimplementasikan analisis ICT (market structure, FVG, order blocks)
- [x] Mengimplementasikan analisis SMC (smart money flow, liquidity sweeps)
- [x] Mengimplementasikan analisis Elliott Wave (impulse/corrective, Fibonacci)
- [x] Mengimplementasikan analisis Volume Profile (POC, value area)
- [x] Mendefinisikan kontrak publik (Permintaan Analisis, Laporan Analisis)
- [x] Membuat 10 skenario Golden Test (metodologi inti)
- [x] Integrasi: Decision Intelligence → Trading Analyst (penilaian sinyal)
- **Gerbang:** 10 Golden Test lulus pada ≥80%

### Fase 2: Konteks Lanjutan (Eksperimental → Stabil)

**Durasi:** 8 minggu

- [x] Mengimplementasikan analisis Makro (indikator, Fed policy, risk-on/off)
- [x] Mengimplementasikan analisis Opsi (Greeks, strategi, IV, unusual activity)
- [x] Mengimplementasikan analisis Futures (contango/backwardation, basis, COT)
- [x] Mengimplementasikan analisis Psikologi (biases, manajemen emosi, position sizing)
- [x] Memperluas Golden Test menjadi 10 skenario penuh
- [x] Mencatat ≥100 kasus nyata dari penggunaan Decision Intelligence
- [x] **Benchmark:** 100 skenario, akurasi sinyal ≥85%, akurasi metodologi ≥85%
- [x] **Integrasi:** Security Engineer mulai menggunakan Trading Analyst untuk analisis kepatuhan
- **Gerbang:** Semua 10 Golden Test lulus pada ≥85%; Benchmark ≥85%

### Fase 3: Sertifikasi (Stabil → Bersertifikat)

**Durasi:** 6 minggu

- [x] Semua metodologi terintegrasi
- [x] Audit independen terhadap akurasi sinyal dan metodologi
- [x] Kalibrasi pada data historis 5 tahun
- [x] Sertifikasi Trading Analyst selesai
- [x] Dasbor Benchmark publik tersedia
- [x] **Benchmark:** ≥85% di semua dimensi
- [x] **Kasus Nyata:** ≥200 kasus dengan ≥80% validasi ahli
- **Gerbang:** Audit kelulusan independen; Benchmark ≥85% berkelanjutan

---

## Peningkatan di Masa Depan

### Fase 2 (Pasca-Rilis v1.0.0)

1. **Backtesting Engine** — Mesin backtesting untuk validasi strategi pada data historis
2. **Multi-Timeframe Analysis** — Analisis sinyal lintas-timeframe (1m, 5m, 1h, 4h, 1d)
3. **Sentiment Analysis** — Analisis sent pasar dari berita dan media sosial
4. **Portfolio Optimization** — Optimasi alokasi portofolio berbasis sinyal trading

### Fase 3 (Perusahaan)

1. **Alternative Data Integration** — Integrasi data alternatif (satelit, kredit, maritime)
2. **Quantitative Strategy Generation** — Generasi strategi kuantitatif berbasis ML
3. **Real-Time Signal Monitoring** — Pemantauan sinyal real-time dengan alerting
4. **Trading Compliance Automation** — Otomatisasi pemeriksaan kepatuhan trading

### Jangka Panjang

1. **AI Trading Agent** — Agen trading otonom dengan manajemen risiko terintegrasi
2. **Cross-Asset Signal Generation** — Sinyal lintas aset (saham, kripto, komoditas, valas)
3. **Explainable Trading AI** — AI yang dapat menjelaskan setiap sinyal dengan metodologi lengkap
4. **Trading Knowledge Graph** — Grafik pengetahuan trading untuk reasoning lintas-metodologi
