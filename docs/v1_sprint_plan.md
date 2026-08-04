# Rencana Milestone ECP v1.0-dev

<!-- DOCUMENT_METADATA_START -->
**Pemilik:** Tim Dokumentasi
**Pemilik Canonical:** Pimpinan Tata Kelola Dokumentasi
**Diverifikasi Terakhir:** 02-08-2026
**Versi:** 1.0.0
**Status:** Aktif
**SSOT:** Dokumentasi untuk v1_sprint_plan
<!-- DOCUMENT_METADATA_END -->

**Metodologi:** Berbasis produk tonggak sejarah, bukan berbasis fitur.
**Definisi Selesai:** Milestone memenuhi semua kriteria pengiriman dan gerbang terpenuhi.

---

## Tonggak Pencapaian 1 — MVP Insinyur Jaringan

**Status:** ✅ Diterima
**Dasar:** `v1.0.0-dev+network-sprint2`

**Tujuan:** Membuktikan ECP dapat menganalisis, menghasilkan, mendokumentasikan, dan mendokumentasikan konfigurasi jaringan.

**Durasi:** 2–3 minggu

**Definisi Selesai:**
- [x] Mengunggah file `.rsc`
- [x] Mem-parsing konfigurasi RouterOS
- [x] Membangun topologi internal
- [x] Mendeteksi masalah konfigurasi
- [x] Menghasilkan rekomendasi
- [x] Menghasilkan konfigurasi yang diperbaiki
- [x] Penyebaran dokumentasi yang baik
- [x] Lolos semua Golden Test untuk jaringan domain (31/31 skenario)

**Hasil Pengiriman:**
- Pengurai RouterOS (v6/v7)
- Pembuat grafik jaringan
- 45 aturan analisis
- Mesin rekomendasi (P0–P3)
- Generator dokumentasi (Penurunan harga)

---

## Tonggak Pencapaian 1.5 — Pengerasan

**Status:** ✅ Diterima

**Tujuan:** Memperkuat Milestone 1 dengan rangkaian regresi, benchmark, dan cakupan pelacakan.

**Durasi:** 3–5 hari

**Definisi Selesai:**
- [x] 31 skenario Golden Test (7 asli + 24 baru)
- [x] Dataset regresi (rusak, tidak valid, parsial, v6, v7)
- [x] Pelacak cakupan aturan (jumlah hit, presisi, penarikan kembali, F1)
- [x] Benchmark kinerja (500/5k/50k baris)
- [x] Kalibrasi keyakinan dari bukti
- [x] Semua tes lulus

---

## Tonggak Pencapaian 2 — Penerapan Terkendali

**Status:** ✅ Diterima

**Tujuan:** Membangun penerapan saluran pipa dengan keamanan, audit, dan persetujuan manusia.

**Durasi:** 2–3 minggu

**Definisi Selesai:**
- [x] Mesin Diff Konfigurasi Semantik
- [x] Manajer Cadangan (ekspor → hash → stempel waktu → penyimpanan artefak)
- [x] Mesin Penilaian Risiko (konfigurasi/kembalikan/keamanan/waktu henti)
- [x] Mesin Verifikasi (antarmuka, gateway, DNS, DHCP, rute)
- [x] Jejak Audit (semua langkah dicatat sebagai artefak)
- [x] Orkestrator Penerapan Terkendali
- [x] UX Runbook Penerapan (Perubahan/Risiko/Pra-Penerapan/Penerapan/Pasca-Penerapan/Pemulihan)
- [x] Garis Waktu Penerapan (langkah kemajuan visual)
- [x] Jelaskan Sebelum Deploy (bahasa berorientasi proses)
- [x] Status Rollback: Tertunda / Siap / Tidak Tersedia / Selesai
- [x] Persetujuan manusia diperlukan di v1.0-dev
- [x] Semua test Milestone 2 lulus (7/7)

---

## Tonggak Pencapaian 3 — Operasi Jaringan

**Status:** 📋 Direncanakan

**Tujuan:** Alur kerja operasional yang digunakan network engineer setiap hari.

**Durasi:** 2–3 minggu

**Definisi Selesai:**
- [ ] Perbandingan Konfigurasi (perbedaan semantik backup-to-backup + dampak)
- [ ] Audit Kepatuhan (Lulus/Gagal berbasis kebijakan)
- [ ] Laporan Kesehatan (skor kesehatan/keamanan/kinerja/kemampuan pemeliharaan)
- [ ] Analisis Dampak Perubahan (memprediksi dampak sebelum penerapan)
- [ ] Jelaskan Like Engineer (penjelasan bahasa sederhana untuk onboarding)
- [ ] Semua test Milestone 3 lulus (≥95%)
- [ ] Umpan balik dogfooding terintegrasi

**Hasil Pengiriman:**
- `apps/network_engineer/compare.py`
- `apps/network_engineer/compliance.py`
- `apps/network_engineer/health.py`
- `apps/network_engineer/impact_analyzer.py`
- `apps/network_engineer/explainer.py`

**Apa yang TIDAK Akan Dibangun:**
- Otomatisasi BGP
- Otomatisasi MPLS
- Otomatisasi CAPsMAN
- Otomatisasi WireGuard
- Orkestra multi-router

---

## Fase Dogfood

**Status:** 🧪 Sedang Berlangsung (1–2 minggu)

**Tujuan:** Menggunakan Network Engineer pada config nyata sebelum membangun fitur baru.

**Aktivitas:**
- Mengaudit config MikroTik nyata (Sun Clint, lab, produksi)
- Membandingkan temuan ECP dengan penilaian ahli
- Mencatat positif palsu, negatif palsu, isu UX
- Mengumpulkan data Waktu Terhemat

**Keluaran:**
- `dogfooding/feedback_YYYY-MM-DD.md`
- Skenario Golden Test yang diperbarui
- 5 prioritas teratas untuk Milestone 3

**Lihat:** `docs/dogfooding_guide.md`

---

## Tonggak Pencapaian 4 — Keunggulan Penalaran

**Status:** 🎯 Target: Rilis v1.0-dev

**Tujuan:** Meningkatkan kualitas penalaran di semua Capability Pack tanpa mengubah Core.

**Durasi:** Berkelanjutan

**Fokus Area:**
- Reasoning domain yang lebih dalam di Capability Packs
- Generasi penjelasan yang lebih baik
- Analisis risiko dan dampak yang lebih baik
- Rekomendasi yang sadar konteks

**Kriteria Keberhasilan:**
- Jaringan: mendeteksi bukan hanya port terbuka, tetapi kemungkinan tujuan dan celah firewall terkait
- Trading: menjelaskan BUY/SELL dengan alternatif, risiko, dan skenario kegagalan
- Penelitian: identifikasi evolusi antar sumber dengan estimasi keyakinan
- Kode: merekomendasikan pola arsitektur dengan alasan
- Semua Capability Pack mempertahankan skor Konsistensi ≥85%

---

## Tonggak Pencapaian 5 — Pratinjau Pengembang

**Status:** 🎯 Target: Rilis v1.0.0

**Tujuan:** Rilis produk siap dengan semua sertifikasi, dokumentasi, dan perkakas lengkap.

**Definisi Selesai:**
- [ ] Semua Capability Pack memenuhi target mutu
- [ ] Sertifikasi Analis Perdagangan lulus
- [ ] Artifact Store v1 diimplementasikan
- [ ] Pengembang situs web diluncurkan
- [ ] Dokumentasi SDK lengkap
- [ ] Video Tutorial dan Quick Start diterbitkan
- [ ] Pasar berfungsi
- [ ] Penemuan Kemampuan API publik
- [ ] Kemampuan Benchmark Dashboard operasional
- [ ] Penampil jejak studio berfungsi

**Daftar Periksa Rilis:**
- [ ] Catatan rilis disusun
- [ ] Panduan migrasi untuk penulis Capability Pack
- [ ] Contoh SDK diterbitkan
- [ ] Video/tutorial Mulai Cepat disiapkan
- [ ] Pengumuman Pratinjau Pengembang Publik

---

## Ritme Pengembangan Mingguan

|Hari|Fokus|
|-----|-------|
|Senin|Ekspansi pengetahuan|
|Selasa|Peningkatan Benchmark|
|Rabu|Peningkatan penalaran|
|Kamis|Meningkatkan kemampuan menjelaskan|
|Jumat|Peningkatan skor Benchmark|

Semua pekerjaan terjadi di dalam Capability Packs. Inti tetap tidak tersentuh.

---

## Daftar "Jangan"

Berikut tidak lagi dapat diterima sebagai aktivitas pengembangan reguler:

- ❌ Menambahkan Runtime baru
- ❌Tambahkan Planner baru
- ❌ Menambahkan Kernel baru
- ❌ Menambahkan Layer baru
- ❌ Memodifikasi Core untuk satu Capability Pack

Setiap pengiriman memerlukan ADR yang disetujui dengan bukti kemampuan lintas.

---

## Kualitas Kemampuan Target — Pratinjau Pengembang v1.0

|Kemampuan|Skor Sasaran|pengukuran|
|------------|--------------|-------------|
|Jaringan|A (≥90)|benchmark/capability_benchmark.py|
|Kode|A- (≥85)|benchmark/capability_benchmark.py|
|Riset|A- (≥85)|benchmark/capability_benchmark.py|
|DevOps|A+ (≥90)|benchmark/devops_assistant_benchmark.py|
|Jual beli|B+ (≥80, lulus Sertifikasi)|benchmark/capability_benchmark.py|
|Pengembangan Diri|A+ (≥90)|benchmark/capability_benchmark.py|

Skor harus berasal dari Benchmark 6 dimensi, bukan penilaian subjektif.

---

## Pratinjau Pengembang Peta Jalan Pasca

### v1.1 — Keunggulan Kemampuan
- Jaringan A+
- Perdagangan B+
- Penelitian A-
- Kode A
- Semua paket naik satu tingkat melalui pengetahuan dan kerja Benchmark

### v1.2 — Ekosistem Komunitas
- Peluncuran Pasar
- Mendukung Paket Kemampuan Komunitas
- Templat SDK Capability Pack
- Proses sertifikasi paket pihak ketiga

### v1.3 — Perusahaan
- Peta Jalan Kapabilitas Perusahaan
- Fitur tata kelola dan audit lanjutan
- Dukungan multi-penyewa
- Peralatan SLA dan kepatuhan

---

## Kemampuan Peta Jalan Spesifik

### Jaringan Kapabilitas Peta Jalan

|Fase|Fokus|Nilai Sasaran|
|-------|-------|--------------|
|Audit|Analisis konfigurasi, keamanan, kepatuhan|A|
|Optimasi|Penyetelan kinerja, praktik terbaik|A|
|Migrasi|Tingkatkan versi, vendor migrasi|A|
|Desain|Desain jaringan greenfield|A+|
|Otomatisasi|Penerapan terkendali, kembalikan|A+|

### Kode Kemampuan Peta Jalan

|Fase|Fokus|Nilai Sasaran|
|-------|-------|--------------|
|Tinjauan|Kualitas kode, keamanan, pemeliharaan|A-|
|Refaktorisasi|Memperbaiki struktur tanpa mengubah perilaku|A-|
|Menghasilkan|Full-stack dari persyaratan|A|
|Arsitektur|Arsitektur Bersih, DDD, Heksagonal, CQRS|A|
|Modernisasi|Warisan migrasi, pengurangan utang teknologi|A|

### Perdagangan Kemampuan Peta Jalan

|Fase|Fokus|Nilai Sasaran|
|-------|-------|--------------|
|Analisa|Data pasar, tren, indikator|B+|
|Strategi|Desain strategi dan backtesting|A-|
|Portofolio|Konstruksi portofolio dan penyeimbangan kembali|A-|
|Mempertaruhkan|Model risiko, VaR, drawdown, korelasi|A|
|Perencanaan Eksekusi|Perencanaan perdagangan dengan risiko dan alternatif|A|

### Penelitian Kemampuan Peta Jalan

|Fase|Fokus|Nilai Sasaran|
|-------|-------|--------------|
|Pengambilan|RAG multi-sumber dengan sitasi|B|
|Bukti|Peringkat bukti, deteksi fosil|A-|
|Sintesis|Sintesis multi-kertas dengan percaya diri|A-|
|Percobaan|Eksperimen desain penasehat|A|
|Tinjauan Sejawat|Simulasi pengecekan kualitas peer review|A|

### DevOps Kemampuan Peta Jalan

|Fase|Fokus|Nilai Sasaran|
|-------|-------|--------------|
|Menghasilkan|Dockerfiles, CI/CD, manifes Kubernetes|B+|
|Memeriksa|Penyebaran kesehatan, kebenaran konfigurasi|A-|
|Multi-cloud|Pola AWS, Azure, GCP|A|
|Platform|Observabilitas, GitOps, kebijakan sebagai kode|A|
|Ketangguhan|Rekayasa kekacauan, persiapan kejadian|A|

### Pengembangan Diri Kemampuan Peta Jalan

|Fase|Fokus|Nilai Sasaran|
|-------|-------|--------------|
|Menganalisa|Struktur proyek, deteksi kemacetan|A-|
|Mengusulkan|Refactoring, usulan perbaikan|A|
|Tambalan|Generasi patch dengan cakupan tes|A|
|Mempelajari|Pembelajaran pola lintas proyek|A|
|Meramalkan|Prediksi dampak sebelum perubahan|A+|

---

## Ringkasan Peta Jalan

```
v1.0-dev
  ├── Milestone 1: Core Stable ✅
  ├── Milestone 2: Conversation Ready ✅
  ├── Milestone 3: Capability Platform ✅
  ├── Milestone 4: Reasoning Excellence 🎯 Target
  ├── Network Engineer Capability Pack ✅ Certified
  │   ├── Milestone 3.1: Network Engineer MVP ✅ Accepted
  │   ├── Milestone 3.2: Hardening ✅ Accepted
  │   ├── Milestone 3.3: Controlled Deployment ✅ Accepted
  │   ├── Milestone 3.4: Dogfooding 🧪 In Progress
  │   └── Milestone 3.5: Network Operations 📋 Planned
  ├── Milestone 5: Developer Preview 🎯 Target
  │   ├── Code Engineer Capability Pack
  │   ├── Research Assistant Capability Pack
  │   ├── DevOps Assistant Capability Pack
  │   └── Trading Analyst Capability Pack (final certification gate)
  └── Post Developer Preview
      ├── v1.1: Capability Excellence
      ├── v1.2: Community Ecosystem
      └── v1.3: Enterprise
```

---

## Rencana Sprint 8 Minggu — Rilis Produk Pertama

Rencana sprint ini menerapkan disiplin pengkodean getaran: AI menghasilkan, AI me-review, AI menguji, AI melakukan Benchmark, manusia menyetujui.

### Minggu 1 — Obrolan UX

**Fokus:** Antarmuka percakapan tunggal seperti Kimi/ChatGPT.
- Obrolan UI dengan streaming
- Merender Penurunan Harga
- Unggah berkas
- Pengalih ruang kerja
- Indikasi kemajuan
- Penampil artefak

**Gate:** Pengguna dapat mengunggah config MikroTik dan melihat analisis streaming.

---

### Minggu 2 — Ruang Kerja

**Fokus:** Isolasi proyek dan memori.
- CRUD Ruang Kerja
- Riwayat percakapan per ruang kerja
- Penyimpanan dan pengambilan artefak
- Pembatasan memori per ruang kerja

**Gerbang:** Pengguna dapat berpindah antara dua ruang kerja dan riwayat terlindungi.

---

### Minggu 3 — Streaming & Konteks Panjang

**Fokus:** Umpan balik eksekusi real-time.
- Streaming acara dari Execution Runtime
- Subtugas kemajuan pembaruan
- Streaming artefak
- Kesalahan pesan pemulihan

**Gerbang:** Pengguna melihat kemajuan secara real-time selama tugas 5+ langkah.

---

### Minggu 4 — Keunggulan Kapabilitas: Jaringan

**Fokus:** Membuat Network Engineer benar-benar ahli.
- Menambahkan 20 kasus nyata ke `real_cases/network/`
- Meningkatkan penganalisis kedalaman
- Meningkatkan kemampuan menjelaskan
- Benchmark: 92%+

**Gerbang:** Skor Benchmark Jaringan ≥92%.

---

### Minggu 5 - Keunggulan Kemampuan: Kode, Riset, DevOps

**Fokus:** Membawa paket lainnya ke kualitas minimum yang layak.
- Kode: Review + Patch end-to-end
- Penelitian : Peringkat bukti + sitasi
- DevOps: Generasi Docker + CI/CD

**Gerbang:** Paket ketiga lulus Benchmark ≥80%.

---

### Minggu 6 — Dogfood

**Fokus:** Menggunakan ECP untuk membangun ECP.
- Mengaudit dokumen ECP dengan Self Development
- Saya meninjau kode ECP dengan Code Capability
- Mendokumentasikan temuan di `real_cases/`

**Gerbang:** 50+ kasus nyata dikumpulkan, semuanya diumpankan kembali ke paket kemampuan.

---

### Minggu 7 — Benchmark & Polandia

**Fokus:** Mengukur dan meningkatkan.
- Jangkauan semua tolak ukur kemampuan
- Memperbaiki regresi
- Polandia alur UX terhadap USER_JOURNEYS.md
- Optimasi kinerja

**Gate:** Semua 6 paket memenuhi target kualitas Developer Preview.

---

### Minggu 8 — Pratinjau Pengembang

**Fokus:** Rilis produk.
- Catatan rilis
- Dokumentasi SDK
- Mulai Cepat
- Pengumuman publik

**Gate:** ECP v1.0.0 dirilis dengan paket kemampuan bersertifikat.

---

## Ritme Pengembangan

|Hari|Fokus|
|-----|-------|
|Senin|Ekspansi pengetahuan|
|Selasa|Peningkatan Benchmark|
|Rabu|Peningkatan penalaran|
|Kamis|Penjelasan|
|Jumat|Peningkatan skor Benchmark|

Semua perubahan terjadi di dalam Capability Packs. Inti tetap tidak tersentuh.
