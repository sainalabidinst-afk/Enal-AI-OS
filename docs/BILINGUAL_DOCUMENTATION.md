# Standardisasi Dokumentasi Bahasa Indonesia

<!-- DOCUMENT_METADATA_START -->
**Pemilik:** Tim Dokumentasi
**Pemilik Canonical:** Pimpinan Tata Kelola Dokumentasi
**Terakhir Diverifikasi:** 2026-08-02
**Versi:** 2.0.0
**Status:** Aktif
**SSOT:** Catatan standardisasi dokumentasi ke Bahasa Indonesia
<!-- DOCUMENT_METADATA_END -->

## Catatan Perubahan

Dokumen ini sebelumnya merupakan daftar file yang diberi header bilingual. Mulai versi 2.0.0, seluruh dokumentasi Markdown di repositori ini menggunakan **Bahasa Indonesia sebagai bahasa utama** dan **tidak lagi menggunakan format bilingual**.

### Yang Dihapus

- Header `BILINGUAL_DOCS_START` / `BILINGUAL_DOCS_END`
- Header `BILINGUAL_DOCS_START` pada tiap dokumen
- Blok terjemahan berlabel ganda (labels konten berbahasa Indonesia untuk konten berbahasa Inggris pada format lama)
- Terjemahan bersarang dan duplikasi bahasa

### Yang Dipertahankan

- Istilah teknis dalam Bahasa Inggris (Capability Pack, Golden Test, Benchmark, API, SDK, dan lainnya — lihat `docs/BILINGUAL_STYLE_GUIDE.md`)
- Seluruh nama class, function, file, folder, endpoint API
- Seluruh blok kode, JSON, diagram ASCII, dan command terminal

## Ruang Lingkup Konversi

Konversi telah dilakukan pada seluruh dokumentasi Markdown, termasuk:

- `docs/` — dokumen strategis, teknis, capability, frontend, RFC, dan ADR
- `sdk/` — dokumentasi SDK
- `benchmarks/` — dokumentasi benchmark
- `real_cases/` — dokumentasi real cases
- `agents/` — dokumentasi agent
- File Markdown tingkat atas (README, CHANGELOG, SECURITY, dan lainnya)

## Referensi

- Pedoman gaya bahasa: `docs/BILINGUAL_STYLE_GUIDE.md`
- Struktur dokumen: `docs/DOCUMENT_STRUCTURE.md`

