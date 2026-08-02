## Bahasa Indonesia/Bahasa Inggris


### Ringkas / Ringkas
Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.


### Informasi Dokumen / Info Dokumen
- Berkas: `backend/app/core/CANONICAL_OWNER_workspace.md`
- Judul: Ruang Kerja Pemilik Canonical
- Status: editor bilingual ditambahkan


# KANONIK_PEMILIK

## Layanan: Ruang Kerja

**Kanonik:** `backend/app/core/workspace_service.py`
**Warisan:** `backend/app/core/workspace.py`
**Status:** kanonis / dihapus

---

## Sejarah Migrasi

|Tanggal|Tindakan|Oleh|
|------|--------|----|
|07-11-2026|Migrasi `orchestrator_v2.py` ke `workspace_service.add_memory()`|Epik Konsolidasi Kanonik 2|
|07-11-2026|Menghapus `workspace.py` (ruang kerja sistem file, lama)|Epik Konsolidasi Kanonik 2|

## Konsumen Kanonis

- `backend/app/api/workspace.py`
- `backend/app/api/execution.py`
- `backend/app/api/chat.py`
- `backend/app/core/execution_integration.py`

## Catatan Migrasi

`workspace.py` menyimpan data pada file sistem (`./workspace/`) menggunakan `ProjectWorkspace` dan `WorkspaceManager`. `workspace_service.py` menggunakan skema Pydantic dalam memori. Migrasi bersifat langsung karena `orchestrator_v2.py` hanya disebut `workspace_manager.get(project_id).save_memory(key, value)`, yang pemetaannya 1:1 ke `workspace_service.add_memory(workspace_id, key, value)`.
