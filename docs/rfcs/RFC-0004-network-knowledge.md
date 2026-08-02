# RFC: Perluasan Pengetahuan Jaringan

<!-- DOCUMENT_METADATA_START -->
**Pemilik:** Tim Dokumentasi
**Pemilik Canonical:** Pimpinan Tata Kelola Dokumentasi
**Diverifikasi Terakhir:** 08-02-2026
**Versi:** 1.0.0
**Status:** Aktif
**SSOT:** RFC untuk RFC-0004-network-knowledge
<!-- DOCUMENT_METADATA_END -->

**Status:** Direncanakan
**Target:** Keunggulan Kemampuan Fase
**Capability Pack:** Insinyur Jaringan

## Ringkasnya

Memperluas kedalaman pengetahuan Network Engineer di seluruh jaringan perusahaan, security hardening, dan protokol lanjutan.

## Domain Pengetahuan

### Panduan Desain Cisco
- Desain perusahaan kampus
- Struktur pusat data
- Arsitektur jaringan tanpa batas
- Prinsip desain SD-WAN
- Pola ketersediaan tinggi

### Praktik Terbaik MikroTik
- Pola ISP edge dan PPPoE
- Hotspot dan pembentukan trafik
- Optimasi Jalur Cepat
- Penerapan IPv6 di RouterOS
- Akses administrasi aman

### Pengerasan Fortinet
- Praktik terbaik keamanan FortiOS
- Optimalisasi kebijakan
- Desain VPN (IPsec, SSL)
- Perlindungan ancaman integrasi
- Logging dan analitik

### BGP
- Pemilihan jalur BGP
- Penyaringan rute dan manipulasi
- komunitas BGP
- Pola desain RR/CE
- Pemantauan dan pemecahan masalah BGP

### MPLS
- Penerusan dan label MPLS
- LDP Dasar, RSVP-TE
- VRF dan rutenya bocor
- Ikhtisar Rekayasa Lalu Lintas MPLS
- Tepi penyedia layanan Pola

### IPv6
- Desain dual-stack
- SLAAC vs DHCPv6
- Pertimbangan keamanan IPv6
- Ikhtisar mekanisme transisi
- Pola penerapan ISP IPv6

### Nol Kepercayaan
- Prinsip arsitektur Zero Trust
- Konsep mikro-segmentasi
- Pola akses berbasis identitas
- Konsep verifikasi berkelanjutan
- Akses jaringan Zero Trust (ZTNA)

## Pendekatan Implementasi

Semua penemuan ditambahkan ke mesin domain Jaringan Capability Pack. Tidak ada perubahan Core yang diperlukan.

## Kriteria Keberhasilan

- Setiap domain pengetahuan diulas di penganalisa/pemberi rekomendasi
- Golden Test diperbarui untuk pengetahuan baru
- Skor Benchmark dipertahankan atau ditingkatkan

## Referensi

- RFC-0004: Dasar Pengetahuan Jaringan
- RFC-0005: Pola Pengerasan Keamanan
- CAPABILITY_GUIDE.md — bagian Insinyur Jaringan
