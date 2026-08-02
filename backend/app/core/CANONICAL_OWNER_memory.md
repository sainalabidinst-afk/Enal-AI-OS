<!-- BILINGUAL_DOCS_START -->
## Bahasa Indonesia / English


### Ringkasan / Summary
Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.
> Terjemahan Indonesia: Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.

- Bahasa Indonesia: konten utama tetap dipertahankan dalam dokumen asli, dan bagian ini memberi konteks ringkas dalam bahasa Indonesia.
- English: the main content remains in the original document, and this section provides a concise bilingual context for international readers.

### Informasi Dokumen / Document Info
- File: `backend/app/core/CANONICAL_OWNER_memory.md`
- Judul: Canonical Owner Memory
- Status: bilingual header added

<!-- BILINGUAL_DOCS_END -->

# CANONICAL_OWNER

## Service: Memory

**Canonical:** `backend/app/core/memory.py`  
**Legacy:** `backend/app/modules/memory.py`  
**Status:** canonical / deleted

---

## Migration History

| Date | Action | By |
|------|--------|----|
| 2026-07-11 | Created `core/memory.py` as canonical Redis-backed conversation store | Canonical Consolidation Epic 3 |
| 2026-07-11 | Migrated `conversation_manager.py` from `modules/memory` → `core/memory` | Canonical Consolidation Epic 3 |

## Canonical Consumers

- `apps/society/conversation_manager.py`

## Notes

`core/memory.py` exposes `conversation_store` with `get_conversation()`, `append_message()`, and `clear_conversation()` methods, all backed by Redis with the key prefix `conversation:`. This matches the interface that `conversation_manager.py` requires.
> Terjemahan Indonesia: Core/memory.py exposes conversation_store dengan get_conversation(), append_message(), dan clear_conversation() methods, all backed oleh Redis dengan key prefix conversation:. ini matches interface itu conversation_manager.py requires.
