# Sprint T1 — Mesin Intelijen Pasar

<!-- DOCUMENT_METADATA_START -->
**Pemilik:** Tim Dokumentasi
**Pemilik Canonical:** Pimpinan Tata Kelola Dokumentasi
**Diverifikasi Terakhir:** 02-08-2026
**Versi:** 1.0.0
**Status:** Aktif
**SSOT:** Dokumentasi untuk SPRINT_T1_PLAN
<!-- DOCUMENT_METADATA_END -->

## Status: ✅ DISETUJUI — Mulai Implementasi

## Arsitektur (Akhir)

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
2. **Bukti terstruktur** — `{id, type, description, timeframe, strength, source, confidence}`
3. **Keyakinan dengan bobot** — Struktur Pasar 35%, Tren 25%, Volume 20%, Volatilitas 10%, Sesi 10%
4. **Output JSON terstruktur** — bukan teks bebas
5. **Binance Public API** — sumber data awal (gratis, tanpa kunci API)
6. **Reasoning Engine** — untuk ringkasan akhir (tidak dilewati)
7. **AnalysisMetadata** — untuk kemampuan audit

## Hasil kerja

### Lapisan 1: Penyedia Data Pasar
- `apps/trading_analyst/market_intelligence/provider.py` — Klien Binance API
- `apps/trading_analyst/market_intelligence/models.py` — Model data

### Lapisan 2: Penganalisis (Fakta saja)
- `apps/trading_analyst/market_intelligence/analyzer.py` — Analisis multi-kerangka waktu
- `apps/trading_analyst/market_intelligence/indicators.py` — Indikator teknis

### Lapisan 3: Bukti & Keyakinan
- `apps/trading_analyst/market_intelligence/evidence.py` — Pembuat bukti
- `apps/trading_analyst/market_intelligence/confidence.py` — Pencetak angka kepercayaan diri tertimbang

### Lapisan 4: Ringkasan
- `apps/trading_analyst/market_intelligence/summary.py` — Generator ringkasan (melalui Reasoning Engine)

### Lapisan 5: API
- `backend/app/api/trading.py` — titik akhir REST

### Lapisan 6: Bagian Depan
- `frontend/services/trading.ts` — API layanan
- `frontend/components/trading/trading-analysis.tsx` — Komponen utama
- `frontend/components/trading/evidence-panel.tsx` — Tampilan bukti
- `frontend/components/trading/confidence-meter.tsx` — Visualisasi kepercayaan diri
- `frontend/app/trading/page.tsx` — Halaman

## Yang TIDAK Dilakukan
- ❌ Analisis portofolio
- ❌ Resiko mesin lanjutan
- ❌ Ukuran posisi
- ❌ Manajemen pesanan
- ❌ Pengujian balik
- ❌ Otomatisasi AI
- ❌ Tampilan Perdagangan Klon
- ❌ Aksara Pinus
- ❌ Indikator baru
- ❌ Sinyal BELI/JUAL otomatis
