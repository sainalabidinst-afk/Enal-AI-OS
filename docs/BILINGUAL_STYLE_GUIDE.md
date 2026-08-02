# Panduan Gaya Dokumentasi Bahasa Indonesia

<!-- DOCUMENT_METADATA_START -->
**Pemilik:** Tim Dokumentasi
**Pemilik Canonical:** Pimpinan Tata Kelola Dokumentasi
**Terakhir Diverifikasi:** 2026-08-02
**Versi:** 2.0.0
**Status:** Aktif
**SSOT:** Standar gaya bahasa untuk seluruh dokumentasi Markdown
<!-- DOCUMENT_METADATA_END -->

## Tujuan

Dokumen ini menetapkan standar gaya bahasa untuk seluruh dokumentasi Markdown di repositori ini. Mulai versi 2.0.0, dokumentasi **tidak lagi menggunakan format bilingual** (Inggris/Indonesia). Bahasa Indonesia menjadi satu-satunya bahasa utama untuk seluruh heading, paragraf, tabel, daftar, dan narasi.

## Prinsip Utama

- Gunakan Bahasa Indonesia yang **formal, baku, dan konsisten** di seluruh dokumen.
- Gunakan terjemahan yang natural dan mudah dipahami, bukan terjemahan kata per kata.
- Jaga istilah teknis tertentu agar tetap dalam Bahasa Inggris (lihat daftar di bawah).
- Untuk dokumen teknis, prioritaskan kejelasan penyampaian dibandingkan penerjemahan harfiah.

## Istilah Teknis yang Dipertahankan dalam Bahasa Inggris

Istilah berikut **tidak diterjemahkan** dan harus tetap ditulis dalam Bahasa Inggris:

- Capability Pack
- Golden Test
- Benchmark
- API, SDK
- Docker, FastAPI
- Runtime, Plugin
- Knowledge Graph
- Execution Runtime
- Decision Intelligence
- Security Engineer, Data Engineer, Database Engineer, QA Engineer, Business Analyst, System Architect, Network Engineer, Code Engineer, Research Assistant, DevOps Assistant, Trading Analyst
- Seluruh nama class, function, file, dan folder
- Seluruh endpoint API
- Seluruh blok kode dan command terminal

## Istilah yang Sebelumnya Terindikasi Salah Terjemahkan

Format bilingual lama telah dihapus. Beberapa istilah yang sebelumnya diterjemahkan secara harfiah telah dikembalikan ke bentuk yang benar:

| Istilah yang Salah | Istilah yang Benar |
|--------------------|--------------------|
| Penjual | Vendor |
| Mengingat | Recall |
| Membekukan Dasar | Baseline Freeze |
| Berkas | File |
| Tolok ukur | Benchmark |
| Mencoba lagi | Retry |

## Format Dokumen

1. `heading` menggunakan Bahasa Indonesia.
2. Paragraf narasi menggunakan Bahasa Indonesia formal.
3. Tabel, daftar, dan checklist menggunakan Bahasa Indonesia.
4. Seluruh blok kode, JSON, diagram ASCII, dan command terminal **dipertahankan apa adanya** (tidak diterjemahkan).
5. Metadata dokumen (`DOCUMENT_METADATA_START`) tetap dipertahankan.

## Perubahan dari Versi 1.0 (Format Bilingual)

- Seluruh header bilingual (penanda `BILINGUAL_DOCS_START`/`BILINGUAL_DOCS_END`) dihapus.
- Seluruh blok terjemahan bersarang dan duplikasi bahasa dihapus.
- Seluruh narasi ditulis ulang menjadi Bahasa Indonesia formal.
- Tanggal ditulis dalam format `YYYY-MM-DD` (misalnya `2026-08-02`), bukan `DD-MM-YYYY`.

