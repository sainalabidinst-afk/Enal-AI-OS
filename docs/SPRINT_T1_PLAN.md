<!-- BILINGUAL_DOCS_START -->
## Bahasa Indonesia / English

### Ringkasan / Summary
Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.
> Terjemahan Indonesia: Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.

- Bahasa Indonesia: konten utama tetap dipertahankan dalam dokumen asli, dan bagian ini memberi konteks ringkas dalam bahasa Indonesia.
- English: the main content remains in the original document, and this section provides a concise bilingual context for international readers.

### Informasi Dokumen / Document Info
- File: `docs/SPRINT_T1_PLAN.md`
- Judul: Sprint T1 Plan
- Status: bilingual header added

<!-- BILINGUAL_DOCS_END -->

# Sprint T1 â€” Market Intelligence Engine

<!-- DOCUMENT_METADATA_START -->
**Owner:** Documentation Team
**Canonical Owner:** Documentation Governance Lead
**Last Verified:** 2026-08-02
**Version:** 1.0.0
**Status:** Active
**SSOT:** Documentation for SPRINT_T1_PLAN
<!-- DOCUMENT_METADATA_END -->

## Status: âœ… APPROVED â€” Mulai Implementasi

## Arsitektur (Final)

```
Binance Public API (gratis, tanpa API key)
        â”‚
        â–¼
Market Provider (interface)
        â”‚
        â–¼
TradingContext
        â”‚
        â–¼
Analyzer â”€â”€â†’ hanya menghasilkan FAKTA, bukan keputusan
        â”‚
        â–¼
Evidence Builder â”€â”€â†’ evidence terstruktur (id, type, strength, source, confidence)
        â”‚
        â–¼
Confidence Scorer â”€â”€â†’ weighted: Structure 35%, Trend 25%, Volume 20%, Volatility 10%, Session 10%
        â”‚
        â–¼
Reasoning Engine (existing) â”€â”€â†’ kesimpulan akhir
        â”‚
        â–¼
Summary Generator â”€â”€â†’ JSON terstruktur
        â”‚
        â–¼
API â†’ Frontend
```

## Prinsip

1. **Analyzer hanya menghasilkan fakta** â€” tidak boleh menghasilkan "BUY" atau "SELL"
2. **Evidence terstruktur** â€” `{id, type, description, timeframe, strength, source, confidence}`
3. **Confidence dengan bobot** â€” Market Structure 35%, Trend 25%, Volume 20%, Volatility 10%, Session 10%
4. **Output JSON terstruktur** â€” bukan teks bebas
5. **Binance Public API** â€” sumber data awal (gratis, tanpa API key)
6. **Reasoning Engine** â€” untuk summary akhir (tidak bypass)
7. **AnalysisMetadata** â€” untuk auditability

## Deliverables

### Layer 1: Market Data Provider
- `apps/trading_analyst/market_intelligence/provider.py` â€” Binance API client
- `apps/trading_analyst/market_intelligence/models.py` â€” Data models

### Layer 2: Analyzer (Fakta saja)
- `apps/trading_analyst/market_intelligence/analyzer.py` â€” Multi-timeframe analysis
- `apps/trading_analyst/market_intelligence/indicators.py` â€” Technical indicators

### Layer 3: Evidence & Confidence
- `apps/trading_analyst/market_intelligence/evidence.py` â€” Evidence builder
- `apps/trading_analyst/market_intelligence/confidence.py` â€” Weighted confidence scorer

### Layer 4: Summary
- `apps/trading_analyst/market_intelligence/summary.py` â€” Summary generator (via Reasoning Engine)

### Layer 5: API
- `backend/app/api/trading.py` â€” REST endpoint

### Layer 6: Frontend
- `frontend/services/trading.ts` â€” API service
- `frontend/components/trading/trading-analysis.tsx` â€” Main component
- `frontend/components/trading/evidence-panel.tsx` â€” Evidence display
- `frontend/components/trading/confidence-meter.tsx` â€” Confidence visualization
- `frontend/app/trading/page.tsx` â€” Page

## Yang TIDAK Dilakukan
- âŒ Portfolio analysis
- âŒ Risk engine lanjutan
- âŒ Position sizing
- âŒ Order management
- âŒ Backtesting
- âŒ AI Automation
- âŒ Clone TradingView
- âŒ Pine Script
- âŒ Indikator baru
- âŒ Signal BUY/SELL otomatis
