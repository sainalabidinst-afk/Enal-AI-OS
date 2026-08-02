## Bahasa Indonesia/Bahasa Inggris


### Ringkas / Ringkas
Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.


### Informasi Dokumen / Info Dokumen
- Berkas: `backend/app/core/CANONICAL_OWNER_artifacts.md`
- Judul: Artefak Pemilik Canonical
- Status: editor bilingual ditambahkan


# KANONIK_PEMILIK

## Layanan: Artefak

**Kanonik:** `backend/app/core/artifact_service.py`
**Warisan:** `backend/app/core/artifact_system.py`
**Status:** kanonis / dihapus

---

## Sejarah Migrasi

|Tanggal|Tindakan|Oleh|
|------|--------|----|
|07-11-2026|Migrasi `phase3.py` ke `artifact_service.create_artifact()`|Epik Konsolidasi Kanonik 2|
|07-11-2026|Migrasi `ai_studio.py` ke `artifact_service.list_artifacts()`|Epik Konsolidasi Kanonik 2|
|07-11-2026|Menghapus `artifact_system.py` (rusak saat diimpor)|Epik Konsolidasi Kanonik 2|

## Konsumen Kanonis

- `backend/app/api/artifact.py`
- `backend/app/api/execution.py`
- `backend/app/api/chat.py` (dinamis)

## Catatan Migrasi

`artifact_system.py` menggunakan kunci domain string semver integer `project_id` dan rusak saat impor (impor `dataclass`/`field` tidak ada). Kedua konsumen (`phase3.py`, `ai_studio.py`) telah dimigrasi ke `artifact_service` yang menggunakan versi integer dan `workspace_id`.
