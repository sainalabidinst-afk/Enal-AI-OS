# RFC: Perluasan Pengetahuan Kode

<!-- DOCUMENT_METADATA_START -->
**Pemilik:** Tim Dokumentasi
**Pemilik Canonical:** Pimpinan Tata Kelola Dokumentasi
**Diverifikasi Terakhir:** 08-02-2026
**Versi:** 1.0.0
**Status:** Aktif
**SSOT:** RFC untuk pengetahuan kode RFC-0006
<!-- DOCUMENT_METADATA_END -->

**Status:** Direncanakan
**Target:** Keunggulan Kemampuan Fase
**Capability Pack:** Kode Insinyur

## Ringkasnya

Memperluas kedalaman pengetahuan Code Engineer di seluruh prinsip desain perangkat lunak, pola arsitektur, dan melakukan praktik pengkodean aman.

## Domain Pengetahuan

### Arsitektur Bersih
- Lapisan: entitas, kasus penggunaan, adaptor antarmuka, kerangka kerja
- Aturan ketergantungan
- Batasan dan antarmuka
- Pengujian isolasi melalui arsitektur
- Kapan diterapkan vs rekayasa berlebihan

### DDD (Domain Desain Berbasis)
- Konteks yang dibatasi
- Entitas, Objek Nilai, Agregat
- Domain peristiwa
- Pola repositori dan spesifikasi
- Lapisan anti korupsi
- Bahasa yang ada di mana-mana

### PADAT
- Tanggung Jawab Tunggal
- Terbuka/Tertutup
- Liskov Pergantian
- Pemisahan antarmuka
- Inversi Ketergantungan
- Contoh praktis di Python/TypeScript

### CQRS
- Pemisahan Perintah vs Permintaan
- Model tulis dan model baca
- Sumber acara Integrasi
- Model Konsistensi
- Kapan menggunakan CQRS

### Sumber Acara
- Konsep toko acara
- Desain skema acara
- Putar ulang dan proyeksi
- Memotret
- Integrasi dengan CQRS

### Pengodean Aman
- Pemetaan OWASP Top 10
- Injeksi pencegahan
- Pola otorisasi dan otorisasi
- Rahasia manajemen
- Penanganan ketergantungan yang aman

## Pendekatan Implementasi

Semua penemuan ditambahkan ke mesin domain Kode Capability Pack. Tidak ada perubahan Core yang diperlukan.

## Kriteria Keberhasilan

- Setiap domain pengetahuan menampilkan logika generasi kode, review, dan refactoring
- Golden Test mencakup pola baru
- Skor Benchmark untuk kualitas kode dan kemampuan penjelasan meningkat

## Referensi

- RFC-0006: Dasar Pengetahuan Kode
- CAPABILITY_GUIDE.md — bagian Insinyur Kode
