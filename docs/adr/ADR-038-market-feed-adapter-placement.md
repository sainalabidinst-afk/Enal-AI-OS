# ADR-038: Relokasi Market Feed Adapter ke Trading Analyst Pack

<!-- DOCUMENT_METADATA_START -->
**Pemilik:** Tim Platform
**Canonical Owner:** Lead Platform Engineer
**Terakhir Diverifikasi:** 2026-10-04
**Versi:** 1.0.0
**Status:** Accepted
**SSOT:** Penempatan `MarketFeedAdapter` terhadap Architecture Freeze Policy
<!-- DOCUMENT_METADATA_END -->

## Abstrak

ADR ini menetapkan `MarketFeedAdapter` sebagai bagian dari Capability Pack
Trading Analyst, bukan modul kernel, sehingga dependency `kernel → apps` yang
melanggar Architecture Freeze Policy dapat dihilangkan.

## Konteks

`MarketFeedAdapter` dibuat di `backend/app/core/market_feed_adapter.py` dengan
import top-level:

```python
from apps.trading_analyst.market_intelligence.provider import RateLimitError, fetch_multi_timeframe
```

Boundary kernel melarang `kernel → apps` (`benchmarks/package_boundaries.py`,
`PACKAGE_BOUNDARIES["kernel"]["forbidden"]`), sehingga modul ini:

1. Gagal `python benchmarks/package_boundaries.py` dengan 1 pelanggaran, dan
   karena itu memblokir job `governance-check` di `.github/workflows/ci.yml`.
2. Melanggar Architecture Freeze Policy — kernel tidak boleh bergantung pada
   Capability Pack tertentu.

Adapter ini murni logika domain trading (regime detection via
`MarketRegimeDetector`, k candles Binance, rate-limit/reconnect handling).
Tidak ada consumers di luar `backend/app/api/trading.py`.

## Keputusan

Pindahkan `MarketFeedAdapter` ke `apps/trading_analyst/market_feed_adapter.py`.

- Pack Trading Analyst adalah pemilik domain; adapter memakai
  `market_intelligence.provider` dan `market_regime.MarketRegimeDetector`
  dari pack yang sama.
- `backend/app/api/trading.py` mengimpor dari `apps.trading_analyst`, konsisten
  dengan import yang sudah ada di `_ensure_regime_detector`. Lapisan API berada di
  luar `package_map` boundary check dan memang sudah menjadi titik koordinasi pack.
- Tidak ada import balik dari pack ke kernel untuk modul ini.
- Kontrak publik (`MarketFeedSnapshot`, `FeedStatus`, `MarketFeedAdapter`,
  `market_feed_adapter`) tetap sama, sehingga `/regime/live`, `/feed/status`,
  `/feed/stream`, `/feed/start`, `/feed/stop` tidak berubah.

### Aturan untuk kemungkinan serupa

Feed adapter generik yang dipakai lintas-pack harus diletakkan di
`backend/app/core/` **tanpa** mengimpor pack apa pun, atau diekspos lewat
`backend/app/runtime` facade. Adapter yang spesifik domain tetap di dalam pack.

## Konsekuensi

- **Positif:** `package_boundaries.py` kembali 0 pelanggaran; `governance-check`
  hijau.
- **Positif:** Architecture Freeze Policy dipatuhi — kernel tidak lagi tahu
  tentang domain trading.
- **Negatif:** Pack Trading Analyst kini bergantung pada `httpx`/Binance saat
  adapter diimpor. `market_intelligence.provider` sudah melakukan lazy import,
  sehingga import pack tetap aman tanpa jaringan.

## Referensi

- `apps/trading_analyst/market_feed_adapter.py`
- `backend/app/api/trading.py`
- `benchmarks/package_boundaries.py`
- ADR-037: Local GPU Inference Provider
- ADR-036: Consent Gating for High-Risk Remediation
