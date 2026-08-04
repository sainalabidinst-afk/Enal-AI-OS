# Proses RFC

<!-- DOCUMENT_METADATA_START -->
**Pemilik:** Tim Dokumentasi
**Pemilik Canonical:** Pimpinan Tata Kelola Dokumentasi
**Diverifikasi Terakhir:** 08-02-2026
**Versi:** 1.0.0
**Status:** Aktif
**SSOT:** Proses RFC, indeks RFC, dan siklus hidup RFC
<!-- DOCUMENT_METADATA_END -->

Dokumen ini menjelaskan proses Request for Comments (RFC) untuk ECP.

## Tujuan

Proses RFC memastikan adanya perubahan signifikan pada ECP yang dirancang dengan baik, direview, dan didokumentasikan sebelum diimplementasikan.

## Kapan Menulis RFC

Tulis RFC untuk:
- Fitur baru atau fungsionalitas utama
- Perubahan pada kontrak/API yang ada
- Perubahan arsitektur
- Perubahan yang bersifat melintang
- Plugin atau alat baru yang mempengaruhi perilaku Core

## Templat RFC

```markdown
# RFC-XXXX: Judul

## Ringkasan
Ringkasan proposal dalam satu paragraf.

## Motivasi
Mengapa kita perlu melakukan ini? Masalah apa yang diselesaikannya?

## Desain Terperinci
Detail teknis dari proposal.

## Alternatif yang Dipertimbangkan
Pendekatan lain apa yang dipertimbangkan?

## Kompatibilitas
Bagaimana ini memengaruhi kompatibilitas ke belakang?

## Pertimbangan Keamanan
Apakah ada implikasi keamanan?

## Strategi Testing
Bagaimana ini akan diuji?

## Linimasa
Linimasa yang diusulkan untuk implementasi.

## Referensi
RFC terkait, dokumentasi, dll.
```

## Proses RFC

1. **Draft:** Penulis membuat RFC di `docs/rfcs/`
2. **Review:** Komunitas mereview selama 7 hari
3. **Revisi:** Penulis menyetujui masukan
4. **Penerimaan:** Tim inti menerima atau menolak
5. **Implementasi:** Penulis mengimplementasikan dengan panduan
6. **Integrasi:** Digabungkan ke cabang utama

## RFC Saat Ini

- RFC-0001: Kontrak Stabil (Diterima)
- RFC-0002: Plugin Format Manifes (Diterima)
- RFC-0003: SDK Dekorator (Diterima)
- RFC-0004: Perluasan Pengetahuan Jaringan (Diterima)
- RFC-0005: Perluasan Pengetahuan Trading (Diterima)
- RFC-0006: Perluasan Pengetahuan Kode (Diterima)
- RFC-0007: Decision Intelligence (Diterima)
- RFC-0008: Security Engineer (Diimplementasikan)
- RFC-0009: Data Engineer (Diimplementasikan)
- RFC-0010: Database Engineer (Diimplementasikan)
- RFC-0011: Sistem Arsitek (Diimplementasikan)
- RFC-0012: QA Engineer (Diimplementasikan)
- RFC-0013: Business Analyst (Diimplementasikan)
- RFC-0014: Infrastructure Engineer (Diterima)
- RFC-0015: AI Engineer (Diterima)
- RFC-0016: Documentation Engineer (Diterima)
- RFC-0017: Product Manager (Diterima)
- RFC-0018: UI/UX Designer (Draf)
- RFC-0019: Full Stack Engineer (Draf)

## Indeks RFC

|ID RFC|Judul|Status|Capability Pack|
|--------|-------|--------|-----------------|
|RFC-0001|Kontrak Stabil|Diterima|Inti|
|RFC-0002|Plugin Format Manifes|Diterima|Inti|
|RFC-0003|SDK Dekorator|Diterima|Inti|
|RFC-0004|Perluasan Pengetahuan Jaringan|Diterima|Insinyur Jaringan|
|RFC-0005|Perluasan Pengetahuan Trading|Diterima|Analis Perdagangan|
|RFC-0006|Perluasan Pengetahuan Kode|Diterima|Insinyur Kode|
|RFC-0007|Decision Intelligence|Diterima|Decision Intelligence|
|RFC-0008|Security Engineer|Diimplementasikan|Security Engineer|
|RFC-0009|Data Engineer|Diimplementasikan|Data Engineer|
|RFC-0010|Database Engineer|Diimplementasikan|Database Engineer|
|RFC-0011|Sistem Arsitek|Diimplementasikan|Sistem Arsitek|
|RFC-0012|QA Engineer|Diimplementasikan|QA Engineer|
|RFC-0013|Business Analyst|Diimplementasikan|Business Analyst|
|RFC-0014|Infrastructure Engineer|Diterima|Infrastructure Engineer|
|RFC-0015|AI Engineer|Diterima|AI Engineer|
|RFC-0016|Documentation Engineer|Diterima|Documentation Engineer|
|RFC-0017|Product Manager|Diterima|Product Manager|
|RFC-0018|UI/UX Designer|Draf|UI/UX Designer|
|RFC-0019|Full Stack Engineer|Draf|Full Stack Engineer|
