# ADR-003: Desain AST Universal


**Status:** ✅ Diterima
**Tanggal:** 2024
**Pengambilan Keputusan:** Kepala Arsitek, Tim Teknik

---

## Konteks

Analisis konfigurasi jaringan harus mendukung beberapa vendor (Cisco, MikroTik, Fortinet, Juniper, dll). Setiap vendor memiliki sintaks konfigurasi, model data, dan semantik yang berbeda.

Tanpa representasi umum, setiap fitur (validasi, refactoring, audit keamanan) harus diterapkan secara terpisah untuk setiap vendor.

---

## Keputusan

Rancang **Universal AST (Pohon Sintaks Abstrak)** yang memodelkan konfigurasi jaringan dengan cara yang tidak bergantung pada vendor.

### Komponen Utama

- `UniversalFirewallRule` — Aturan firewall yang dinormalisasi di seluruh vendor
- `UniversalNATRule` — Aturan NAT yang dinormalisasi di seluruh vendor
- `UniversalBGP` — Konfigurasi BGP yang dinormalisasi
- `UniversalInterface` — Konfigurasi antarmuka yang dinormalisasi
- Parser khusus vendor di `apps/network_engineer/vendor/` dipetakan ke Universal AST

### Prinsip Desain

Setiap parser vendor menerjemahkan sintaks khusus vendor ke dalam model Universal AST. Konsumen hilir (penganalisa, pengayaan, audit keamanan) hanya beroperasi pada Universal AST, tidak pernah pada format khusus vendor.

---

## Alternatif yang Dipertimbangkan


|Alternatif|Alasan Ditolak|
|-------------|-----------------|
|Analisis spesifik vendor per fitur|Kompleksitas N*M (vendor × fitur), tidak dapat diskalakan|
|Format perantara umum (JSON/YAML)|Kehilangan keamanan tipe dan validasi struktural|
|Kelas dasar abstrak per fitur|Masih memerlukan implementasi per vendor untuk setiap fitur|

---

## Lanjutnya

- **Positif:** Kompleksitas linier (N + M) dan bukan (N × M)
- **Positif:** Dukungan vendor baru menambahkan N parser, fitur M langsung berfungsi
- **Positif:** Pengetikan yang kuat melalui kelas data dan Pydantic
- **Negatif:** Model universal harus dibuat cukup umum untuk semua vendor
- **Negatif:** Nuansa khusus vendor mungkin hilang dalam normalisasi
- **Negatif:** Pemeliharaan parser diperlukan untuk setiap pembaruan firmware vendor

---

## Kepatuhan

Semua analisis konfigurasi jaringan HARUS menggunakan model Universal AST. Akses langsung ke struktur khusus vendor dengan kode analisis dilarang.
