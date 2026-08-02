<!-- BILINGUAL_DOCS_START -->
## Bahasa Indonesia / English


### Ringkasan / Summary
Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.
> Terjemahan Indonesia: Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.

- Bahasa Indonesia: konten utama tetap dipertahankan dalam dokumen asli, dan bagian ini memberi konteks ringkas dalam bahasa Indonesia.
- English: the main content remains in the original document, and this section provides a concise bilingual context for international readers.

### Informasi Dokumen / Document Info
- File: `backend/app/core/CANONICAL_OWNER_model_router.md`
- Judul: Canonical Owner Model Router
- Status: bilingual header added

<!-- BILINGUAL_DOCS_END -->

# CANONICAL_OWNER

## Service: Model Router

**Canonical:** `backend/app/core/model_router.py`  
**Auxiliary:** `backend/app/core/model_gateway.py` (health/status API — NOT a duplicate)  
**Legacy (Dead):** N/A — deleted  
**Status:** canonical / auxiliary / legacy-purged

---

## Migration History

| Date | Action | By |
|------|--------|----|
| 2026-07-11 | Removed 6 dead imports of `model_router` in cognitive_kernel, cost_optimizer, evaluation, meta_cognition, modules/rag, modules/tools | Canonical Consolidation Epic 1 |
| 2026-07-11 | Deleted `apps/society/model_router.py` (0 importers, 189 lines dead code) | Canonical Consolidation Epic 2 |

## Canonical Consumers

21 files import `model_router`. 15 active callers invoke `.complete()`.
> Terjemahan Indonesia: 21 file mengimpor model_router. 15 penelepon aktif memanggil .complete().

## Important Distinction

`model_gateway.py` is NOT a duplicate of `model_router.py`. It serves a different purpose:
> Terjemahan Indonesia: Model_gateway.py adalah NOT sebuah duplicate dari model_router.py. It serves sebuah different purpose:

| File | Purpose | Endpoint |
|------|---------|----------|
| `model_router.py` | LLM execution (`.complete()`) | N/A (internal) |
| `model_gateway.py` | Health/status API | `/api/v1/models/health`, `/api/v1/models/providers` |

Keep `model_gateway.py`.
> Terjemahan Indonesia: Pertahankan model_gateway.py.
