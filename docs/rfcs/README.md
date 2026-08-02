# Proses RFC

<!-- DOCUMENT_METADATA_START -->
**Pemilik:** Tim Dokumentasi
**Pemilik Canonical:** Pimpinan Tata Kelola Dokumentasi
**Terakhir Diverifikasi:** 2026-08-02
**Versi:** 1.0.0
**Status:** Aktif
**SSOT:** Proses RFC, indeks RFC, dan lifecycle RFC
<!-- DOCUMENT_METADATA_END -->

Dokumen ini menjelaskan proses Request for Comments (RFC) untuk ECP.

## Tujuan

Proses RFC memastikan bahwa perubahan signifikan pada ECP dirancang dengan baik, direview, dan didokumentasikan sebelum implementasi.

## Kapan Menulis RFC

Tulis RFC untuk:
- Fitur baru atau fungsionalitas utama
- Perubahan pada kontrak/API yang ada
- Perubahan arsitektur
- Perubahan yang bersifat breaking
- Plugin atau tool baru yang memengaruhi perilaku Core

## Template RFC

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
3. **Revisi:** Penulis menindaklanjuti masukan
4. **Penerimaan:** Tim inti menerima atau menolak
5. **Implementasi:** Penulis mengimplementasikan dengan panduan
6. **Integrasi:** Digabungkan ke branch utama

## RFC Saat Ini

- RFC-0001: Stable Contracts (Diterima)
- RFC-0002: Plugin Manifest Format (Diterima)
- RFC-0003: SDK Decorators (Diterima)
- RFC-0004: Event Bus Protocol (Diterima)
- RFC-0005: Memory Interface (Diterima)
- RFC-0006: Capability Pack Registry (Diterima)
- RFC-0007: Decision Intelligence (Diterima)
- RFC-0008: Security Engineer (Diimplementasikan)
- RFC-0009: Data Engineer (Diimplementasikan)
- RFC-0010: Database Engineer (Diimplementasikan)
- RFC-0011: System Architect (Diimplementasikan)
- RFC-0012: QA Engineer (Diimplementasikan)
- RFC-0013: Business Analyst (Diimplementasikan)

## Indeks RFC

| RFC ID | Judul | Status | Capability Pack |
|--------|-------|--------|-----------------|
| RFC-0001 | Stable Contracts | Diterima | Core |
| RFC-0002 | Plugin Manifest Format | Diterima | Core |
| RFC-0003 | SDK Decorators | Diterima | Core |
| RFC-0004 | Event Bus Protocol | Diterima | Core |
| RFC-0005 | Memory Interface | Diterima | Core |
| RFC-0006 | Capability Pack Registry | Diterima | Core |
| RFC-0007 | Decision Intelligence | Diterima | Decision Intelligence |
| RFC-0008 | Security Engineer | Diimplementasikan | Security Engineer |
| RFC-0009 | Data Engineer | Diimplementasikan | Data Engineer |
| RFC-0010 | Database Engineer | Diimplementasikan | Database Engineer |
| RFC-0011 | System Architect | Diimplementasikan | System Architect |
| RFC-0012 | QA Engineer | Diimplementasikan | QA Engineer |
| RFC-0013 | Business Analyst | Diimplementasikan | Business Analyst |

