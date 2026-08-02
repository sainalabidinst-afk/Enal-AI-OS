## Bahasa Indonesia/Bahasa Inggris


### Ringkas / Ringkas
Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.


### Informasi Dokumen / Info Dokumen
- Berkas: `backend/app/core/CANONICAL_OWNER_model_router.md`
- Judul: Router Model Pemilik Canonical
- Status: editor bilingual ditambahkan


# KANONIK_PEMILIK

## Layanan: Model Router

**Kanonik:** `backend/app/core/model_router.py`
**Auxiliary:** `backend/app/core/model_gateway.py` (kesehatan/status API — BUKAN duplikat)
**Warisan (Mati):** T/A — dihapus
**Status:** kanonikal / tambahan / pembersihan lama

---

## Sejarah Migrasi

|Tanggal|Tindakan|Oleh|
|------|--------|----|
|07-11-2026|Menghapus 6 impor mati `model_router` di kognitif_kernel, pengoptimal_biaya, evaluasi, meta_kognisi, modul/kain, modul/alat|Epik Konsolidasi Kanonik 1|
|07-11-2026|Menghapus `apps/society/model_router.py` (0 importir, 189 baris kode mati)|Epik Konsolidasi Kanonik 2|

## Konsumen Kanonis

21 file diimpor `model_router`. 15 penelepon aktif memanggil `.complete()`.

## Perbedaan Penting

`model_gateway.py` BUKAN duplikat dari `model_router.py`. Ini memiliki tujuan yang berbeda:

|Mengajukan|Tujuan|Titik akhir|
|------|---------|----------|
|`model_router.py`|Eksekusi LLM (`.complete()`)|T/A (internal)|
|`model_gateway.py`|Kesehatan/status API|`/api/v1/models/health`, `/api/v1/models/providers`|

Simpan `model_gateway.py`.
