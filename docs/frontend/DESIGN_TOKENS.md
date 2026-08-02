# Desain Token

<!-- DOCUMENT_METADATA_START -->
**Pemilik:** Tim Dokumentasi
**Pemilik Canonical:** Pimpinan Tata Kelola Dokumentasi
**Diverifikasi Terakhir:** 08-02-2026
**Versi:** 1.0.0
**Status:** Aktif
**SSOT:** Dokumentasi frontend untuk DESIGN_TOKENS
<!-- DOCUMENT_METADATA_END -->

Dokumen ini mendefinisikan set design token lengkap untuk ECP v1. Semua kode frontend harus menggunakan token ini. Tidak ada nilai hardcoded yang diizinkan.

---

## Warna

### Warna Semantik

|Token|Nilai|Penggunaan|
|-------|-------|-------|
|`--color-bg-primary`|#0f1117|Latar belakang aplikasi utama|
|`--color-bg-secondary`|#1a1d27|Bilah sisi, kartu, panel|
|`--color-bg-tertiary`|#252830|Permukaan yang ditinggikan, masukan|
|`--color-bg-hover`|#2d3038|Elemen interaktif melayang|
|`--color-text-primary`|#e4e6eb|Teks utama (judul, isi)|
|`--color-text-secondary`|#9ca3af|Teks sekunder (subtitel, petunjuk)|
|`--color-text-muted`|#6b7280|Teks yang dibisukan (tempel waktu, metadata)|
|`--color-accent`|#3b82f6|Tombol tindakan utama, tautan|
|`--color-accent-hover`|#2563eb|Tindakan utama melayang|
|`--color-success`|#22c55e|Status sukses, tugas selesai|
|`--color-success-bg`|rgba(34,197,94,0.1)|Latar belakang kesuksesan|
|`--color-warning`|#f59e0b|Status peringatan|
|`--color-warning-bg`|rgba(245.158,11,0.1)|Latar belakang peringatan|
|`--color-danger`|#ef4444|Status kesalahan, tindakan destruktif|
|`--color-danger-hover`|#dc2626|Melayang destruktif|
|`--color-danger-bg`|rgba(239,68,68,0.1)|Latar belakang kesalahan|
|`--color-border`|#374151|Perbatasan, pemisah|
|`--color-border-light`|#4b5563|Perbatasan ringan|

### Status Warna

|Token|Nilai|Penggunaan|
|-------|-------|-------|
|`--color-status-pending`|#6b7280|Tugas yang tertunda|
|`--color-status-running`|#3b82f6|kekuatan tugas|
|`--color-status-completed`|#22c55e|Tugas selesai|
|`--color-status-failed`|#ef4444|Tugas yang gagal|
|`--color-status-warning`|#f59e0b|Peringatan|
|`--color-status-info`|#3b82f6|Informasional|

---

## Tipografi

### Font Keluarga

|Token|Nilai|
|-------|-------|
|`--font-family`|'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif|
|`--font-family-mono`|'JetBrains Mono', 'Fira Code', 'Courier New', monospace|

### Ukuran Font

|Token|Nilai|Tinggi Garis|Penggunaan|
|-------|-------|-------------|-------|
|`--font-size-xs`|0,75rem|1rem|Label, petunjuk|
|`--font-size-sm`|0,875rem|1,25rem|Teks sekunder, keterangan|
|`--font-size-md`|1rem|1,5rem|Teks isi|
|`--font-size-lg`|1.125rem|1,75rem|Teks yang ditekankan|
|`--font-size-xl`|1,25rem|1,75rem|Judul kecil|
|`--font-size-2xl`|1,5rem|2rem|halaman judul|
|`--font-size-3xl`|2rem|2,5rem|Teks pahlawan|

### Font Bobot

|Token|Nilai|Penggunaan|
|-------|-------|-------|
|`--font-weight-normal`|400|Teks isi|
|`--font-weight-medium`|500|Teks yang ditekankan|
|`--font-weight-semibold`|600|Subjudul|
|`--font-weight-bold`|700|Judul|

---

## Jarak

|Token|Nilai|Penggunaan|
|-------|-------|-------|
|`--space-0`|0|Tanpa spasi|
|`--space-1`|4 piksel|Jarak yang sempit|
|`--space-2`|8 piksel|Jarak yang kompak|
|`--space-3`|12 piksel|Spasi bawaan|
|`--space-4`|16 piksel|Jarak yang nyaman|
|`--space-5`|24 piksel|Jarak bagian|
|`--space-6`|32 piksel|Spasi halaman|
|`--space-7`|48 piksel|Bagian besar|
|`--space-8`|64 piksel|Bagian halaman|

---

## Radius Perbatasan

|Token|Nilai|Penggunaan|
|-------|-------|-------|
|`--radius-none`|0|Tepi yang tajam|
|`--radius-sm`|4 piksel|Elemen kecil|
|`--radius-md`|8 piksel|Kartu, kancing|
|`--radius-lg`|12 piksel|Panel, modal|
|`--radius-full`|9999 piksel|Pil, avatar|

---

## Bayangan

|Token|Nilai|Penggunaan|
|-------|-------|-------|
|`--shadow-none`|tidak ada|Tidak ada bayangan|
|`--shadow-sm`|0 1px 2px rgba(0,0,0,0.3)|Ketinggian yang halus|
|`--shadow-md`|0 4px 6px rgba(0,0,0,0.4)|Kartu-kartu|
|`--shadow-lg`|0 10px 15px rgba(0,0,0,0.5)|Modal, dialog|
|`--shadow-inner`|sisipkan 0 2px 4px rgba(0,0,0,0.3)|Elemen Sisipkan|

---

## Indeks-Z

|Token|Nilai|Penggunaan|
|-------|-------|-------|
|`--z-base`|0|Lapisan dasar|
|`--z-dropdown`|100|Menu tarik-turun|
|`--z-sticky`|200|Headernya lengket|
|`--z-modal`|300|Modal dialog|
|`--z-toast`|400|Notifikasi roti panggang|
|`--z-tooltip`|500|Keterangan alat|

---

## Transisi

|Token|Nilai|Penggunaan|
|-------|-------|-------|
|`--transition-fast`|kemudahan masuk-keluar 150ms|Interaksi mikro|
|`--transition-normal`|kemudahan masuk-keluar 250ms|Standar transisi|
|`--transition-slow`|Kemudahan masuk-keluar 350ms|Panel transisi|

---

## Titik henti sementara

|Token|Nilai|Penggunaan|
|-------|-------|-------|
|`--bp-mobile`|640 piksel|Mak. seluler|
|`--bp-tablet`|1024 piksel|Tablet Maks|
|`--bp-desktop`|1025 piksel|Desktop min|

---

## Mode Gelap / Mode Terang

Semua warna di atas didefinisikan untuk mode gelap (default).

Mode override terang:

|Token|Nilai Mode Cahaya|
|-------|------------------|
|`--color-bg-primary`|#ffffff|
|`--color-bg-secondary`|#f3f4f6|
|`--color-bg-tertiary`|#e5e7eb|
|`--color-bg-hover`|#d1d5db|
|`--color-text-primary`|#111827|
|`--color-text-secondary`|#4b5563|
|`--color-text-muted`|#9ca3af|
|`--color-border`|#d1d5db|
|`--color-border-light`|#e5e7eb|

Pergantian tema harus menggunakan properti kustom CSS dan bertransisi dengan lancar.
