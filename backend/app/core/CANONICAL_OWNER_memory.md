## Bahasa Indonesia/Bahasa Inggris


### Ringkas / Ringkas
Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.


### Informasi Dokumen / Info Dokumen
- Berkas: `backend/app/core/CANONICAL_OWNER_memory.md`
- Judul: Memori Pemilik Canonical
- Status: editor bilingual ditambahkan


# KANONIK_PEMILIK

## Layanan: Memori

**Kanonik:** `backend/app/core/memory.py`
**Warisan:** `backend/app/modules/memory.py`
**Status:** kanonis / dihapus

---

## Sejarah Migrasi

|Tanggal|Tindakan|Oleh|
|------|--------|----|
|07-11-2026|Membuat `core/memory.py` sebagai penyimpanan percakapan kanonik yang didukung Redis|Epik Konsolidasi Kanonik 3|
|07-11-2026|Migrasi `conversation_manager.py` dari `modules/memory` → `core/memory`|Epik Konsolidasi Kanonik 3|

## Konsumen Kanonis

- `apps/society/conversation_manager.py`

## Catatan

`core/memory.py` mengekspos `conversation_store` dengan metode `get_conversation()`, `append_message()`, dan `clear_conversation()`, semuanya didukung oleh Redis dengan kunci awal `conversation:`. Ini cocok dengan antarmuka yang membutuhkan `conversation_manager.py`.
