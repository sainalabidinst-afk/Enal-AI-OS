# Insinyur Jaringan ECP — Tonggak Pencapaian 3: Operasi Jaringan

<!-- DOCUMENT_METADATA_START -->
**Pemilik:** Tim Dokumentasi
**Pemilik Canonical:** Pimpinan Tata Kelola Dokumentasi
**Diverifikasi Terakhir:** 02-08-2026
**Versi:** 1.0.0
**Status:** Aktif
**SSOT:** Dokumentasi untuk sprint3_network_operations
<!-- DOCUMENT_METADATA_END -->

**Status:** Direncanakan
**Fokus:** Alur kerja operasional, bukan otomatisasi protokol

---

## Hasil kerja

### 1. Perbandingan Konfigurasi

**Tujuan:** Membandingkan dua konfigurasi cadangan dan menampilkan perbedaan semantik + analisis dampak.

**Kisah Pengguna:**
> "Sebagai teknisi jaringan, saya ingin membandingkan cadangan A dengan cadangan B sehingga saya dapat melihat apa yang tetap berubah dan apakah aman."

**Fitur:**
- Memuat dua file cadangan
- Perbedaan semantik (mesin yang sama seperti Milestone 2, diterapkan pada cadangan)
- Analisis dampak: mana layanan/antarmuka yang mempengaruhi
- Laporan Penurunan Harga

**Kriteria Penerimaan:**
- Dapat memuat dua Golden Test config apa pun
- Menampilkan rule yang ditambahkan/dihapus/dimodifikasi per kategori
- Mengidentifikasi perubahan yang berpotensi berisiko (firewall, NAT, rute)
- Menghasilkan laporan Penurunan harga

---

### 2. Audit Kepatuhan

**Tujuan:** Memeriksa konfigurasi terhadap kebijakan dan menampilkan Lulus/Gagal.

**Kisah Pengguna:**
> "Sebagai network engineer, saya ingin melakukan audit kepatuhan sehingga saya dapat membuktikan router memenuhi kebijakan perusahaan."

**Fitur:**
- Mendefinisikan kebijakan sebagai aturan sederhana (JSON/YAML)
- Memeriksa konfigurasi terhadap kebijakan
- Lulus/Gagal per aturan
- Skor penayangan keseluruhan
- Laporan Penurunan Harga

**Kontoh Kebijakan:**
```yaml
rules:
  - id: SSH-RESTRICTED
    check: "ssh must not be open to 0.0.0.0/0"
    severity: critical
  - id: PASSWORD-SET
    check: "admin password must be set"
    severity: critical
  - id: BACKUP-CONFIGURED
    check: "backup must be configured"
    severity: warning
  - id: NTP-ENABLED
    check: "NTP must be enabled"
    severity: info
```

**Kriteria Penerimaan:**
- Dapat mendefinisikan kebijakan kustom
- Memeriksa config terhadap setiap rule
- Menampilkan Lulus/Gagal dengan bukti
- Akhirnya skor tercapai

---

### 3. Laporan Kesehatan

**Tujuan:** Skor kesehatan satu-klik untuk sebuah router.

**Kisah Pengguna:**
> "Sebagai network engineer, saya ingin skor kesehatan sehingga saya dapat menilai kondisi router dengan cepat."

**Fitur:**
- Skor Kesehatan (0–100)
- Skor Keamanan (0–100)
- Skor Kinerja (0–100)
- Skor Pemeliharaan (0–100)
- Skor Keseluruhan
- Perincian per kategori
- Laporan Penurunan Harga

**Skor Logika:**
- Mulai dari 100
- Kurangi poin untuk setiap temuan berdasarkan tingkat keparahan:
  - Kritis: -20
  - Peringatan: -10
  - Informasi: -5
  - Saran: -2
- Batas bawah di 0

**Kriteria Penerimaan:**
- Hasilnya skor untuk Golden Test config apa pun
- Skor konsisten (config yang sama = skor yang sama)
- Perincian menunjukkan isu mana yang mempengaruhi setiap skor
- Laporan Markdown dengan indikator visual

---

### 4. Analisis Dampak Perubahan

**Tujuan:** Sebelum penerapan, prediksi apa yang akan dipengaruhi oleh perubahan.

**Kisah Pengguna:**
> "Sebagai teknisi jaringan, saya ingin mengetahui apa yang akan rusak sebelum saya menerapkannya, sehingga saya dapat bersiap."

**Fitur:**
- Menganalisis konfigurasi saat ini + diff yang diusulkan
- Mengidentifikasi layanan yang mempengaruhi:
  - Perubahan firewall → dampak konektivitas
  - Perubahan NAT → dampak akses internet
  - Perubahan rute → risiko lalu lintas blackhole
  - Perubahan DHCP → dampak sewa
  - Perubahan antarmuka → isolasi perangkat
- Memprediksi tingkat dampak (Rendah/Sedang/Tinggi/Kritis)
- Menyarankan langkah mitigasi

**Kriteria Penerimaan:**
- Dapat menganalisis perbedaan Golden Test apa pun
- Mengidentifikasi setidaknya: dampak firewall, NAT, rute, antarmuka, DHCP
- Memprediksi tingkat dampak dengan benar untuk skenario yang diketahui
- Menyarankan mitigasi yang dapat ditindaklanjuti

---

### 5. Jelaskan Seperti Insinyur

**Tujuan:** Menjelaskan aturan konfigurasi dalam bahasa sederhana untuk onboarding.

**Kisah Pengguna:**
> "Sebagai network engineer junior, saya ingin memahami apa yang dilakukan setiap aturan sehingga saya dapat belajar."

**Fitur:**
- Klik pada find/rule apa pun
- Mendapatkan penjelasan:
  - Apa yang dilakukan rule ini
  - Mengapa aturan ini dibuat
  - Apa yang terjadi jika dihapus
  - Dependensi (apa lagi yang bergantung pada ini)
  - Kesalahan umum
- Bahasa sederhana, tanpa jargon sarat

**Keluaran Kontoh:**
```
Rule: masquerade on WAN
------------------------
What it does:
  Allows all devices on the LAN to access the internet by
  translating their private IPs to the router's public IP.

Why it exists:
  Without this, LAN devices cannot reach the internet.
  Only the router itself would have internet access.

Impact if removed:
  - LAN devices lose internet access
  - Hotspot users cannot browse
  - DHCP clients can get IPs but no internet

Dependencies:
  - Requires WAN interface to have public IP
  - Often paired with srcnat chain rule
  - Works with FastTrack for performance

Common mistakes:
  - Applying to LAN interface instead of WAN
  - Forgetting to create DHCP server
  - Not setting default route
```

**Kriteria Penerimaan:**
- Dapat menjelaskan seluruh 45 aturan analisis
- Penjelasan akurat dan dapat ditindaklanjuti
- Dependensi diidentifikasi dengan benar
- Bahasa sederhana yang cocok untuk engineer junior

---

## Apa yang TIDAK Akan Dibangun di Milestone 3

- Otomatisasi BGP
- Otomatisasi MPLS
- Otomatisasi CAPsMAN
- Otomatisasi WireGuard
- Orkestra multi-router
- Integrasi API MikroTik langsung

Ini adalah konsekuensi dari pemahaman operasional yang baik, bukan perenang.

---

## Metrik Keberhasilan

|Metrik|Target|
|--------|--------|
|Bandingkan Konfigurasi Akurasi|≥95%|
|Audit Kepatuhan Cakupan|≥90% dari kebijakan umum|
|Skor Kesehatan Korelasi|≥0.8 dengan penilaian ahli|
|Dampak Perubahan Akurasi|≥80% untuk skenario yang|
|Kelengkapan Penjelasan|100% dari 45 aturan dijelaskan|
|Golden Test Lulus|≥95%|
|Umpan Balik Item Dogfood|≥20 item dicatat|
|Waktu yang Dihemat (dogfood)|≥50% dibandingkan analisis manual|

---

## Prasyarat

- Pencapaian 2 difreeze dasar (`v1.0.0-dev+network-sprint2`)
- Dogfooding selesai (1–2 minggu)
- Feedback dari setidaknya 10 config nyata yang direview
- 5 prioritas teratas dari dogfooding didokumentasikan

---

## Definisi Selesai

- [ ] Konfigurasi Bandingkan berfungsi di semua skenario Golden Test
- [ ] Audit Kepatuhan lolos semua uji kasus kebijakan
- [ ] Laporan Kesehatan menghasilkan skor yang konsisten
- [ ] Analisis Dampak Perubahan memperkirakan dampak yang benar
- [ ] Jelaskan Seperti Insinyur mencakup semua 45 aturan
- [ ] Semua test Milestone 3 lulus (≥95%)
- [ ] Umpan balik dogfooding terintegrasi
- [ ] Dokumentasi diperbarui
- [ ] Demo siap
