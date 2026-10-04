<!-- DOCUMENT_METADATA_START -->
**Pemilik:** Documentation Team
**Canonical Owner:** Documentation Governance Lead
**Terakhir Diverifikasi:** 2026-10-04
**Version:** 1.0.0
**Status:** Active
**SSOT:** Roadmap platform/produk 6–12 bulan (console, GPU, integrasi, enterprise readiness)
<!-- DOCUMENT_METADATA_END -->

# Roadmap Platform 6–12 Bulan (2026-10 → 2027-04)

Dokumen ini adalah SSOT untuk **roadmap platform/produk** jangka menengah.
SSOT untuk **Capability Pack** (grade, benchmark, real cases, RFC/ADR) tetap
`TODO_CAPABILITY_EXECUTION.md`.

Setiap baris di bawah sudah diverifikasi terhadap kode pada 2026-10-04. Status
tidak boleh diubah menjadi `[x]` tanpa bukti eksekusi — lihat
[TODO_CAPABILITY_EXECUTION.md § VALIDATION & FIXES](../TODO_CAPABILITY_EXECUTION.md)
untuk pola claim-versus-aktual yang pernah terjadi.

---

## Ringkasan Verifikasi 2026-10-04

| Gate | Status | Bukti |
|------|--------|-------|
| `python -m pytest tests/` | ✅ 865 passed, 1 skipped, 0 failed | 14m27s |
| `python benchmarks/package_boundaries.py` | ✅ 0 pelanggaran | 4 pelanggaran hilang (ADR-038) |
| `python -m benchmarks.governance_checks` | ⚠️ 3 core_change_protection | ADR-037/038 harus ikut dalam commit yang sama |
| `python -m ruff check <changed>` | ✅ clean | 11 file |
| `pytest tests/test_stable_contract_*.py` | ✅ 131 passed | kontrak inti RFC-0001 |
| `pytest tests/test_integration.py` | ✅ 8 passed | — |
| `pytest tests/test_gpu_inference_service.py` | ✅ 12 passed | degradasi tanpa CUDA |
| `pytest tests/test_plugin_marketplace.py` | ✅ 12 passed | isolasi `plugins_dir` per test |
| Import `backend.app.runtime` | ✅ 58s → 14s | ADR-037 lazy torch/transformers |

> Skip = `test_ecosystem_studio_memory` (Redis tidak tersedia di environment CI).

---

## Fase 1 (0–3 bulan) — Konsolidasi & Stabilitas

| Item | Status | Catatan |
|------|--------|---------|
| Console `/console/*` dengan panel governance, trading, observability | ✅ Selesai | 10 route: `/`, `/packs`, `/packs/[packId]`, `/packs/benchmark`, `/marketplace`, `/observability`, `/evaluation`, `/builder`, `/voice`, `/settings` |
| Integrasi GPU inference ke backend ECP | ✅ Selesai | `backend/app/core/gpu_inference_service.py` + `ModelRouter` prefix `gpu/`; lazy import, chat template, degradasi ke `FALLBACK_MODEL`; 12 test. ADR-037 |
| Upgrade Qwen 3B → 7B | ☐ Config | Hanya ganti `GPU_MODEL_PATH`; 7B butuh VRAM lebih besar |
| Hardening API feed adapter | ✅ Selesai | Rate limit + exponential backoff + jitter + `Retry-After`, reconnect dengan `max_backoff`, fallback synthetic — `apps/trading_analyst/market_feed_adapter.py` |
| Habit tracker di Self Development Pack | 🟡 Work-in-progress | `apps/self_development/habit_tracker.py` + `growth_repository.py` + `tests/test_self_development_growth.py` muncul 2026-10-04; belum diverifikasi |
| Governance check hijau di CI | ⚠️ perlu commit ADR | `core_change_protection` menuntut ADR ada di diff yang sama |
| Isolasi test Plugin Marketplace | ✅ Selesai | Test menulis ke `.ecp/plugins/` repo dan state bocor antar test; sekarang `tmp_path` per test |

## Fase 2 (3–6 bulan) — Ekosistem & Integrasi

| Item | Status | Catatan |
|------|--------|---------|
| Marketplace template diperluas | 🟡 Sebagian | `plugin_marketplace.py` + `marketplace-view.tsx` ada; jumlah blueprint belum diaudit |
| Observability dashboard + live trading metrics + governance compliance | ✅ Selesai | `TradingPanel` terintegrasi ke `observability-view.tsx` |
| Integrasi provider eksternal (Binance, Alpaca, Hugging Face Hub) | 🟡 Sebagian | Binance ada (`market_intelligence/provider.py`, 429 handling). Alpaca & HF Hub belum |
| Auto-report generator (PDF/HTML) untuk backtest + evaluation | ☐ Belum ada | `reportlab` hanya dipakai `document_processing/pdf_writer.py`; belum ada report backtest |

## Fase 3 (6–9 bulan) — User Value & Growth

| Item | Status | Catatan |
|------|--------|---------|
| Alert pipeline: push/email untuk regime & governance violation | 🟡 Sebagian | Alert threshold + toast ada di `TradingPanel`. `EmailConnector` (SMTP/IMAP) ada; belum ada push channel |
| Builder canvas multi-agent orchestration | 🟡 Sebagian | `workflow-canvas.tsx` + `blueprint-graph.ts` ada; runtime deploy dari blueprint belum |
| Voice console multi-persona + contextual memory | 🟡 Sebagian | `get_voice_profile` + `jenny_voice_config` ada; contextual memory per persona belum |
| Self Development Pack rekomendasi project otomatis | 🟡 Work-in-progress | `apps/self_development/recommendation_engine.py` + `learning_analytics.py` + `goal_aligner.py` muncul 2026-10-04; belum diverifikasi |

## Fase 4 (9–12 bulan) — Enterprise Readiness

| Item | Status | Catatan |
|------|--------|---------|
| RBAC untuk console | 🟡 Sebagian | `backend/app/core/auth.py` + `SecurityModel` RBAC + `AuditLoggingMiddleware` ada; scoping per-role di console belum |
| Audit log + compliance export (ISO/SEC) | 🟡 Sebagian | Audit trail di `backend/app/core/governance.py`; export ISO/SEC belum |
| Metrics streaming ke Grafana/Prometheus | ☐ Belum ada | Hanya konsep di `telemetry/log_aggregator_config.yml`; tidak ada exporter |
| Multi-tenant | ☐ Belum ada | Hanya disinggung sebagai future work di RFC-0001/0003 |

---

## Aturan Eksekusi

1. **Verified, bukan klaim.** Kotak hanya jadi `[x]` bila ada perintah verifikasi
   yang bisa dijalankan ulang dan lulus.
2. **Core tetap beku.** Perubahan di `backend/app/core`, `kernel`, `runtime`, `sdk`
   wajib punya ADR di `docs/adr/` pada diff yang sama — lihat ADR-037, ADR-038.
3. **Domain tetap di pack.** Adapter/servis yang spesifik domain tidak boleh diletakkan
   di `backend/app/core` bila ia mengimpor pack.
4. **Optional dependency selalu lazy.** `torch`, `transformers`, `litellm`, `minio`,
   `aiokafka` tidak boleh di-import di module scope pada jalur startup.
5. **Test tidak boleh menulis ke repo.** Suite yang menyentuh storage default (seperti
   Plugin Marketplace) wajib memakai `tmp_path`, bukan direktori default.

## Utang teknis yang terdeteksi

| Utang | Dampak |
|-------|--------|
| `.ecp/plugins/*.json` berisi 5 manifest buangan test (`test-plugin`, `draft-plugin`, `network-plugin`, `net-plugin`, `rated-plugin`) dan sudah **ter-track di git** | `plugin_marketplace` singleton di-load saat import backend, jadi 5 plugin palsu ikut tayang di runtime |
| `PluginMarketplace.publish()` menaikkan status existing ke `PUBLISHED` walau manifest baru berstatus `DRAFT` | Persistensi bisa menaikkan draft ke published tanpa review |
| `backend/app/runtime` import masih ±14s, didominasi `litellm` yang masih top-level | Startup lambat; kandidat lazy-load berikutnya |
| `apps/self_development/habit_tracker.py` memuat karakter mojibake (`anomaly â†’`) | Encoding file rusak, perlu ditulis ulang UTF-8 |
