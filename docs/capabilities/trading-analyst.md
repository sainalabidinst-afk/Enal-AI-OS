# Trading Analyst — Spesifikasi Capability

**Versi:** 2.0.0
**Status:** Bersertifikat (RFC-0005)
**Target Kualitas:** A+ (≥95) — Level 4 — Pakar Domain

---

## 1. Tujuan

Trading Analyst adalah **otoritas analisis pasar** untuk ECP — Capability Pack yang menganalisis data pasar, mendeteksi tren, menilai risiko, dan menghasilkan strategi perdagangan berbasis bukti.

Capability Pack ini mengintegrasikan 7 domain pengetahuan (Wyckoff, SMC/ICT, Elliott Wave, Volume Profile, Psychology, Macro, Derivatives) melalui pipeline analisis terstruktur — **tanpa memodifikasi Core**.

---

## 2. Ruang Lingkup

### Dalam Ruang Lingkup
- **Market Analysis** — Analisis struktur pasar, tren, volume, volatilitas
- **Wyckoff Analysis** — Fase akumulasi/distribusi, composite operator, supply/demand
- **SMC/ICT Analysis** — FVG, order blocks, liquidity sweeps, premium/discount
- **Elliott Wave Analysis** — Impulse/corrective patterns, Fibonacci relationships
- **Volume Profile Analysis** — POC, value area, HVN/LVN, profile shape
- **Psychology Analysis** — Sentimen extremes, FOMO, volume psychology
- **Macro Analysis** — Policy rate, inflation, economic health, risk sentiment
- **Derivatives Analysis** — IV, put/call skew, futures basis, COT, max pain
- **Risk Assessment** — VaR, drawdown, position sizing, risk level
- **Strategy Generation** — Momentum, counter-trend, wait strategies
- **Multi-Strategy Debate** — Perbandingan multi-strategi melalui Debate Engine

### Di Luar Cakupan
- Eksekusi perdagangan langsung
- Integrasi akun broker
- Kepatuhan pengaturan untuk memastikan tertentu
- Optimasi pajak
- Penasihat keuangan pribadi

---

## 3. Kontrak

### Input: TradingAnalysisRequest
```json
{
  "symbol": "BTCUSDT",
  "timeframes": ["15m", "1h", "4h", "1d"],
  "exchange": "binance",
  "use_live_data": true,
  "macro_data": {
    "central_bank": "Fed",
    "current_rate": 3.75,
    "cpi": 2.8,
    "gdp_growth": 2.2,
    "vix": 18.0,
    "dxy": 102.0
  },
  "derivatives_data": {
    "current_iv": 32.0,
    "historical_iv": 28.0,
    "iv_percentile": 65.0,
    "put_volume": 12000.0,
    "call_volume": 15000.0,
    "futures_price": 101.5,
    "commercial_long": 55000.0,
    "commercial_short": 42000.0
  }
}
```

### Output: AnalysisResult
```json
{
  "symbol": "BTCUSDT",
  "bias": "bullish | bearish | neutral",
  "confidence": 75,
  "risk_level": "low | medium | high",
  "evidence": [
    {
      "type": "wyckoff_accumulation | smc_fvg | elliott_impulse | volume_poc | psychology_fomo | macro_policy | derivatives_iv_skew",
      "timeframe": "1h",
      "direction": "bullish | bearish | neutral",
      "confidence": 0.8,
      "summary": "string",
      "source": "wyckoff | smc | elliott_wave | volume_profile | psychology | macro | derivatives"
    }
  ],
  "reasoning_steps": ["string"],
  "counter_scenario": "string",
  "summary": "string",
  "raw": {
    "analyzers": {
      "market_analyzer": {},
      "domain": {
        "wyckoff": 5,
        "smc": 12,
        "elliott_wave": 3,
        "volume_profile": 4,
        "psychology": 2,
        "macro": 3,
        "derivatives": 6
      }
    },
    "top_evidence": []
  },
  "risk_assessment": {
    "symbol": "BTCUSDT",
    "bias": "bullish",
    "confidence": 75,
    "risk_level": "medium",
    "max_drawdown": 0.10,
    "var_95": 0.03,
    "position_size": 1000.0
  },
  "strategy": {
    "symbol": "BTCUSDT",
    "strategy": "momentum | counter-trend-watch | wait",
    "entry": "string",
    "exit": "string",
    "stop_loss": "string",
    "confidence": 75,
    "rationale": "string"
  }
}
```

---

## 4. Operasi

| Operasi | Deskripsi | Input | Output |
|-----------|-------------|--------|---------|
| `analyze_market` | Analisis penuh pasar | symbol, timeframes, exchange | AnalysisResult |
| `analyze_full` | Analisis lengkap + risiko + strategi | symbol, timeframes, exchange | FullAnalysisDict |
| `assess_risk` | Penilaian risiko | symbol, position_size | RiskAssessment |
| `analyze_portfolio` | Snapshot portofolio | — | PortfolioSnapshot |
| `generate_strategy` | Generasi strategi | symbol, risk_tolerance | StrategySuggestion |
| `run_debate` | Multi-strategy debate | symbol, strategies | DebateResult |

---

## 5. Modul Analyzer

| Modul | Tanggung Jawab |
|--------|----------------|
| `market_intelligence/analyzer.py` | MarketAnalyzer — struktur pasar, tren, volume, volatilitas |
| `market_intelligence/wyckoff.py` | WyckoffAnalyzer — fase akumulasi/distribusi, composite operator |
| `market_intelligence/smc.py` | SMCAnalyzer — FVG, order blocks, liquidity sweeps, premium/discount |
| `market_intelligence/elliott_wave.py` | ElliottWaveAnalyzer — impulse/corrective waves, Fibonacci |
| `market_intelligence/volume_profile.py` | VolumeProfileAnalyzer — POC, value area, HVN/LVN |
| `market_intelligence/psychology.py` | PsychologyAnalyzer — sentimen, FOMO, volume psychology |
| `market_intelligence/macro_analyzer.py` | MacroAnalyzer — policy rate, inflation, risk sentiment |
| `market_intelligence/derivatives.py` | DerivativesAnalyzer — IV, put/call skew, futures basis, COT |
| `market_intelligence/summary.py` | MarketSummaryGenerator — confidence scoring, summary |
| `market_intelligence/confidence.py` | ConfidenceScorer — weighted scoring (35/25/20/10/10) |
| `market_intelligence/evidence.py` | EvidenceBuilder — cross-timeframe boost, deduplication |
| `market_intelligence/indicators.py` | Technical indicators — RSI, MACD, ATR, Bollinger Bands |
| `market_intelligence/models.py` | Data models — OHLCV, TradingContext, AnalysisResult |

---

## 6. Dimensi Benchmark

| Dimensi | Target | Grade |
|-----------|--------|-------|
| Reasoning Quality | ≥95% | A+ |
| Evidence Coverage | ≥95% (7/7 domains) | A+ |
| Explainability | ≥95% | A+ |
| Consistency | ≥95% | A+ |
| Safety | ≥95% | A+ |
| Risk-Adjusted Quality | ≥95% | A+ |

**Grade Thresholds:**
- A+ (≥95): Semua dimensi ≥95%
- A (≥90): Semua dimensi ≥90%
- B (≥80): Semua dimensi ≥80%

---

## 7. Knowledge Domains (RFC-0005)

| Domain | Implementasi | Modul |
|--------|-------------|--------|
| Wyckoff | Phases, composite operator, supply/demand zones | `wyckoff.py` |
| ICT/SMC | Market structure, FVG, order blocks, liquidity sweeps | `smc.py` |
| Elliott Wave | Impulse/corrective patterns, Fibonacci retracement | `elliott_wave.py` |
| Volume Profile | POC, value area, HVN/LVN, profile shape | `volume_profile.py` |
| Psychology | Biases, FOMO, volume psychology, sentiment extremes | `psychology.py` |
| Macro | Indicators, Fed policy, risk-on/off, economic health | `macro_analyzer.py` |
| Derivatives | Greeks, IV, skew, futures basis, COT, max pain | `derivatives.py` |

---

## 8. Audit Keamanan

### OWASP Top 10
- A03:2021 – Injection: Data injection melalui market data feeds
- A05:2021 – Security Misconfiguration: Hardcoded API keys untuk exchange
- A06:2021 – Vulnerable Components: Dependencies data provider yang outdated
- A08:2021 – Data Integrity Failures: Manipulated OHLCV data
- A09:2021 – Logging Failures: Missing audit trail untuk analisis

### Deteksi Rahasia
- API keys untuk exchange dalam konfigurasi
- Credentials untuk data feeds
- Private keys untuk signing

### Pencegahan Injeksi
- Data injection melalui market data feeds
- Calculation injection melalui manipulated data
- Result injection melalui crafted inputs

### Validasi Input
- Validasi symbol format
- Validasi timeframe values
- Validasi OHLCV data integrity (high >= low, close dalam range)

### Default Aman
- Read-only analysis (tidak ada eksekusi order)
- Data source verification
- Confidence threshold untuk recommendations

---

## 9. Optimasi Kinerja

### Strategi Caching
- OHLCV data cache untuk timeframe yang tidak berubah
- Indicator calculation cache
- Analysis result cache untuk skenario yang sama
- Multi-timeframe cache untuk analisis berulang

### Peluang Paralelisme
- Parallel analysis untuk banyak symbols
- Independent domain analyzers paralel
- Multi-timeframe analysis paralel

### Optimasi Memori
- Rolling window untuk data OHLCV (hanya data yang diperlukan)
- Lazy loading untuk indicator calculations
- Disk-based cache untuk large datasets

### Efisiensi Token
- Context compression untuk large market data
- Incremental analysis untuk perubahan kecil
- Selective domain analysis berdasarkan bias

---

## 10. Benchmark Command

```bash
# Run 20-scenario benchmark
python benchmarks/trading_analyst_benchmark.py

# Run 100-scenario benchmark
python -c "
import asyncio
from benchmarks.trading_analyst_benchmark import run_trading_benchmark
report = asyncio.run(run_trading_benchmark(num_scenarios=100))
print(f'Overall: {report.overall_score:.1f}% ({report.passed})')
"
```

**Current Status:** A+ (100.0%) — 100 scenarios, all 7 domains detected, 100% consistency.

---

## 11. Real Cases

Directory: `real_cases/trading/`

| Case | Description | Evaluation |
|------|-------------|------------|
| `btc_breakout_2026` | Bitcoin breakout analysis | ✅ |
| `eth_deFi_correlation` | ETH/DeFi correlation study | ✅ |
| `gold_news_analysis` | Gold reaction to news events | ✅ |
| `portfolio_rebalance_2026` | Portfolio rebalancing scenario | ✅ |
| `sol_breakdown_analysis` | Solana breakdown analysis | ✅ |

---

## 12. Integrasi

| Capability Pack | Konsumen | Penggunaan |
|-----------------|----------|------------|
| Decision Intelligence | Primary consumer | Evidence → Decision pipeline |
| Research Assistant | Secondary consumer | Market research synthesis |
| System Architect | Secondary consumer | Trading system design |

---

*Dokumen ini adalah kontrak versi 2.0.0 untuk Capability Pack Trading Analyst. Perubahan kontrak memerlukan ADR dan persetujuan Governance.*
