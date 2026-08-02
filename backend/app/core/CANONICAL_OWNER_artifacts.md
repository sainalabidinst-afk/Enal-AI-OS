<!-- BILINGUAL_DOCS_START -->
## Bahasa Indonesia / English


### Ringkasan / Summary
Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.
> Terjemahan Indonesia: Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.

- Bahasa Indonesia: konten utama tetap dipertahankan dalam dokumen asli, dan bagian ini memberi konteks ringkas dalam bahasa Indonesia.
- English: the main content remains in the original document, and this section provides a concise bilingual context for international readers.

### Informasi Dokumen / Document Info
- File: `backend/app/core/CANONICAL_OWNER_artifacts.md`
- Judul: Canonical Owner Artifacts
- Status: bilingual header added

<!-- BILINGUAL_DOCS_END -->

# CANONICAL_OWNER

## Service: Artifact

**Canonical:** `backend/app/core/artifact_service.py`  
**Legacy:** `backend/app/core/artifact_system.py`  
**Status:** canonical / deleted

---

## Migration History

| Date | Action | By |
|------|--------|----|
| 2026-07-11 | Migrated `phase3.py` to `artifact_service.create_artifact()` | Canonical Consolidation Epic 2 |
| 2026-07-11 | Migrated `ai_studio.py` to `artifact_service.list_artifacts()` | Canonical Consolidation Epic 2 |
| 2026-07-11 | Deleted `artifact_system.py` (broken on import) | Canonical Consolidation Epic 2 |

## Canonical Consumers

- `backend/app/api/artifact.py`
- `backend/app/api/execution.py`
- `backend/app/api/chat.py` (dynamic)

## Migration Notes

`artifact_system.py` used integer semver string `project_id` domain keys and was broken on import (missing `dataclass`/`field` imports). Both consumers (`phase3.py`, `ai_studio.py`) have been migrated to `artifact_service` which uses integer versioning and `workspace_id`.
> Terjemahan Indonesia: Artifact_system.py used integer semver string project_id domain keys dan was broken pada import (missing dataclass/field imports). Both consumers (phase3.py, ai_studio.py) memiliki been migrated untuk artifact_service which uses integer versioning dan workspace_id.
