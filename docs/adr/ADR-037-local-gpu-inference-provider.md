# ADR-037: Local GPU Inference Provider

<!-- DOCUMENT_METADATA_START -->
**Pemilik:** Tim Platform
**Canonical Owner:** Lead Platform Engineer
**Terakhir Diverifikasi:** 2026-10-04
**Versi:** 1.0.0
**Status:** Accepted
**SSOT:** Arsitektur provider GPU lokal untuk Model Router
<!-- DOCUMENT_METADATA_END -->

## Abstrak

ADR ini menetapkan `backend/app/core/gpu_inference_service.py` sebagai provider
inferensi LLM lokal berbasis CUDA di dalam kernel, beserta aturan import, konfigurasi,
dan strategi degradasinya.

## Konteks

 Roadmap 6–12 bulan menuntut integrasi penuh GPU inference ke backend ECP
(Qwen 3B, dengan opsi naik ke 7B). Model Router adalah satu-satunya kernel service
yang boleh dipakai lintas-pack, sehingga provider GPU harus duduk di kernel agar dapat
digunakan semua Capability Pack tanpa melanggar batas boundary.

Implementasi awal langsung meng-`import torch` dan `transformers` di module scope.
Karena `model_router.py` mengimpor service ini di module scope, setiap import
`backend.app.runtime` — yaitu seluruh startup backend dan seluruh test collection —
menanggung biaya ±25 detik. Selain itu:

- Path model di-hardcode (`E:/Enal-AI-OS/models/qwen2.5-3b`), tidak portable.
- `settings.GPU_INFERENCE_ENABLED` diabaikan sepenuhnya.
- Prompt dirender sebagai `role\ncontent` tanpa chat template, sehingga output Qwen
  tidak konsisten.
- `decode()` mengembalikan prompt + komplemen, bukan hanya komplemen.
- `generate()` yang blocking dipanggil langsung di dalam coroutine async.
- Tidak ada jalur degradasi: kegagalan GPU menjadi `RuntimeError` yang mematikan.

## Keputusan

Gunakan `GPUInferenceService` di `backend/app/core/gpu_inference_service.py` sebagai
provider GPU lokal, dengan aturan berikut:

- **Lazy import.** `torch`, `transformers`, dan `BitsAndBytesConfig` di-import di dalam
  `initialize()`, mengikuti konvensi `kafka_event_bus` dan `storage`. Import module
  `gpu_inference_service` harus tetap murah (< 100 ms).
- **Konfigurasi via settings.** `GPU_INFERENCE_ENABLED`, `GPU_MODEL_PATH`, dan
  `GPU_FALLBACK_ENABLED` adalah sumber kebenaran. Tidak ada path hardcode.
- **Aktif hanya bila diminta.** `get_gpu_service()` mengembalikan `None` ketika
  `GPU_INFERENCE_ENABLED` false, sehingga import `model_router` bebas efek samping.
- **Chat template milik tokenizer.** `tokenizer.apply_chat_template()` dengan fallback
  ke transkrip berprefiks role bila tokenizer tidak memiliki template.
- **Decode hanya token baru.** Potensi prompt di-slice sebelum `decode`.
- **Async-safe.** `chat()` dan `agenerate()` memakai `asyncio.to_thread` sehingga
  decoding tidak memblokir event loop.
- **Degradasi, bukan crash.** `ModelRouter` jatuh ke `settings.FALLBACK_MODEL` saat GPU
  tidak tersedia atau gagal, selama `GPU_FALLBACK_ENABLED` true.
- **Observable.** `GPUInferenceService.status()` mengembalikan health snapshot untuk
  panel observability console.

### Batas Arsitektur

`GPUInferenceService` adalah **kernel service**, bukan Capability Pack. Dilarang
mengimpor dari `apps/`. Provider data pasar (Binance dan sejenisnya) tetap milik
`apps/trading_analyst`; lihat ADR-038 untuk relokasi `MarketFeedAdapter`.

## Konsekuensi

- **Positif:** Startup backend dan collection test kembali cepat; tidak ada regresi
  `governance-check` dan `package_boundaries`.
- **Positif:** Deployment dapat diarahkan ke model 7B hanya lewat `GPU_MODEL_PATH`.
- **Positif:** GPU mati tidak lagi menjatuhkan seluruh platform.
- **Negatif:** Developer tanpa CUDA tetap dapat menjalankan semuanya; fallback Ollama
  menjadi jalur default saat GPU nonaktif.
- **Negatif:** VRAM 4-bit untuk 7B demanding, tetap butuh negatif GPU_COUNT.

## Referensi

- `backend/app/core/gpu_inference_service.py`
- `backend/app/core/model_router.py`
- RFC-0055: Pilar 4 — Enterprise Autonomy & Self-Evolving Platform
- ADR-036: Consent Gating for High-Risk Remediation
