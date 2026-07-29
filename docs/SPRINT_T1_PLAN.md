# Sprint T1 — Market Intelligence Engine

## Status: ✅ APPROVED — Mulai Implementasi

## Arsitektur (Final)

```
Binance Public API (gratis, tanpa API key)
        │
        ▼
Market Provider (interface)
        │
        ▼
TradingContext
        │
        ▼
Analyzer ──→ hanya menghasilkan FAKTA, bukan keputusan
        │
        ▼
Evidence Builder ──→ evidence terstruktur (id, type, strength, source, confidence)
        │
        ▼
Confidence Scorer ──→ weighted: Structure 35%, Trend 25%, Volume 20%, Volatility 10%, Session 10%
        │
        ▼
Reasoning Engine (existing) ──→ kesimpulan akhir
        │
        ▼
Summary Generator ──→ JSON terstruktur
        │
        ▼
API → Frontend
```

## Prinsip

1. **Analyzer hanya menghasilkan fakta** — tidak boleh menghasilkan "BUY" atau "SELL"
2. **Evidence terstruktur** — `{id, type, description, timeframe, strength, source, confidence}`
3. **Confidence dengan bobot** — Market Structure 35%, Trend 25%, Volume 20%, Volatility 10%, Session 10%
4. **Output JSON terstruktur** — bukan teks bebas
5. **Binance Public API** — sumber data awal (gratis, tanpa API key)
6. **Reasoning Engine** — untuk summary akhir (tidak bypass)
7. **AnalysisMetadata** — untuk auditability

## Deliverables

### Layer 1: Market Data Provider
- `apps/trading_analyst/market_intelligence/provider.py` — Binance API client
- `apps/trading_analyst/market_intelligence/models.py` — Data models

### Layer 2: Analyzer (Fakta saja)
- `apps/trading_analyst/market_intelligence/analyzer.py` — Multi-timeframe analysis
- `apps/trading_analyst/market_intelligence/indicators.py` — Technical indicators

### Layer 3: Evidence & Confidence
- `apps/trading_analyst/market_intelligence/evidence.py` — Evidence builder
- `apps/trading_analyst/market_intelligence/confidence.py` — Weighted confidence scorer

### Layer 4: Summary
- `apps/trading_analyst/market_intelligence/summary.py` — Summary generator (via Reasoning Engine)

### Layer 5: API
- `backend/app/api/trading.py` — REST endpoint

### Layer 6: Frontend
- `frontend/services/trading.ts` — API service
- `frontend/components/trading/trading-analysis.tsx` — Main component
- `frontend/components/trading/evidence-panel.tsx` — Evidence display
- `frontend/components/trading/confidence-meter.tsx` — Confidence visualization
- `frontend/app/trading/page.tsx` — Page

## Yang TIDAK Dilakukan
- ❌ Portfolio analysis
- ❌ Risk engine lanjutan
- ❌ Position sizing
- ❌ Order management
- ❌ Backtesting
- ❌ AI Automation
- ❌ Clone TradingView
- ❌ Pine Script
- ❌ Indikator baru
- ❌ Signal BUY/SELL otomatis

