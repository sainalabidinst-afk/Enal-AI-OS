# Sprint 5A — Insinyur Jaringan: Siap Produksi

<!-- DOCUMENT_METADATA_START -->
**Pemilik:** Tim Dokumentasi
**Pemilik Canonical:** Pimpinan Tata Kelola Dokumentasi
**Diverifikasi Terakhir:** 02-08-2026
**Versi:** 1.0.0
**Status:** Aktif
**SSOT:** Dokumentasi untuk SPRINT_5A_PLAN
<!-- DOCUMENT_METADATA_END -->

**Tujuan:** Membawa kemampuan Network Engineer ke status siap produksi dengan gerbang kualitas yang terukur.

**Definisi Selesai:**
- Akurasi: ≥95%
- Positif Palsu: <5%
- Negatif Palsu: <5%
- Latensi: <2 detik per analisis
- Cakupan: >90% dari kelas isu yang diketahui
- Tes Emas: 100% lulus
- Real Cases: 100+ case dengan hasil Benchmark
- Dokumentasi: Lengkap

---

## Kondisi Saat Ini

|Komponen|Status|
|-----------|--------|
|Pengurai (RouterOS, Cisco, Fortinet)|✅ Dewasa|
|Penganalisis (47 aturan)|✅ Dewasa|
|Pembuat Grafik|✅ Ada|
|Mesin Rekomendasi|✅ Ada|
|Generator|✅ Ada|
|Simulator|✅ Ada|
|Mesin Verifikasi|✅ Ada|
|Pencetak Skor Risiko|✅ Ada|
|Penerapan Terkendali|✅ Ada|
|NIC (Pengetahuan + Inferensi)|✅ Ada|
|Ujian Emas|⚠️ 1 contoh kasus|
|Kasus Nyata|⚠️ 1 contoh kasus|

---

## Minggu 1 — Ujian Emas Ekspansi

Target: 100+ Golden Test kasus yang mencakup:
- MikroTik RouterOS: ACL, BGP, OSPF, HSRP, NAT, AAA, SNMP, QoS, VPN, MPLS
- Cisco IOS: ACL, BGP, OSPF, HSRP, NAT, AAA, SNMP, QoS, VPN, MPLS
- Fortinet: Kebijakan, NAT, VPN, Perutean, HA

Setiap Golden Test harus memiliki:
- `config.rsc` / `config.txt` — cuplikan konfigurasi aktual
- `expected.json` — temuan yang diharapkan, skor risiko, skor kepatuhan
- `metadata.yaml` — vendor, peran perangkat, kompleksitas, tag
- `report.md` — laporan diharapkan dapat dibaca manusia

Lokasi: `real_cases/mikrotik/`, `real_cases/cisco/`, `real_cases/fortinet/`

---

## Minggu 2 — Otomasi Benchmark

Target: Benchmark pelari otomatis yang:
1. Memuat semua kasus nyata dari disk
2. Menghadapi setiap kasus melalui analisa
3. Membandingkan temuan aktual vs yang diharapkan
4. Menghitung akurasi, positif palsu, negatif palsu, latensi
5. Skor kemampuan perincian yang dihasilkan
6. Mengekspor hasil ke JSON/CSV

Lokasi: `benchmarks/network_engineer_benchmark.py`

Integrasi:
- Targetkan `make benchmark-network` di Makefile
- Pekerjaan CI: `python benchmarks/network_engineer_benchmark.py`

---

## Minggu 3 — Ekspansi Cakupan

Target: Menambahkan mencakup aturan yang hilang:
- Keamanan VLAN
- STP/RSTP
- Keamanan BGP (pemfilteran awalan, keamanan TTL)
- Keamanan OSPF (otentikasi)
- Validasi IPsec/VPN
- Validasi kebijakan QoS
- SNMPv3 vs SNMPv1/v2c
- Validasi AAA/TACACS+/RADIUS
- Logging dan syslog
- Konfigurasi NTP
- Keamanan DNS

---

## Minggu 4 — Integrasi & Telemetri

Target:
- merekam rekaman telemetri ke penganalisis
- Melacak waktu eksekusi sesuai aturan
- Melacak akurasi deteksi vendor
- Melacak kemampuan penggunaan per sesi
- Dasbor siap metrik titik akhir

---

## Rencana Eksekusi

1. Membuat Golden Test case (batch 1: 20 kasus MikroTik)
2. Membuat Golden Test case (batch 2: 20 kasus Cisco)
3. Membuat Golden Test case (batch 3: 20 kasus Fortinet)
4. Membuat Golden Test cases (batch 4: 40 kasus advanced campuran)
5. Otomasi Benchmark
6. Ekspansi tertutup
7. Pengujian integrasi
8. Dokumentasi
