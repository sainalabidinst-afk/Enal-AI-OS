<!-- DOCUMENT_METADATA_START -->
**Pemilik:** Tim Dokumentasi
**Pemilik Canonical:** Pimpinan Tata Kelola Dokumentasi
**Diverifikasi Terakhir:** 08-02-2026
**Versi:** 1.0.0
**Status:** Aktif
**SSOT:** Model kematangan Capability Pack, profil, dan siklus hidup strategis
<!-- DOCUMENT_METADATA_END -->

# Strategi Kemampuan ECP

**Versi:** 1.0.0
**Berlaku:** 02-08-2026
**Induk:** `GOVERNANCE_CHARTER.md`
**Tujuan:** Mendefinisikan strategi evolusi Capability Pack, kematangan, kualitas grading, lifecycle, dan perluasan pengetahuan.

---

## 1. Filosofi Strategi

> **Core adalah platform yang stabil. Capability Pack adalah tempat terjadinya inovasi.**

Semua perluasan pengetahuan, pertumbuhan fitur, dan evolusi domain terjadi **di dalam Capability Pack**. Inti tetap tidak berubah.

Siklus pengembangan adalah:

```
Penggunaan Nyata → Pengukuran → Peningkatan Capability → Benchmark → Rilis
```

- Kasus dunia nyata adalah **sumber utama** peningkatan Capability Pack.
- Benchmark sintetis **memvalidasi** peningkatan; kasus dunia nyata **mendorong** peningkatan tersebut.
- Setiap Capability Pack berputar secara independen sesuai kecepatannya masing-masing.

---

## 2. Kemampuan Model Kematangan

Kematangan menggambarkan **tahap lifecycle** dari sebuah Capability Pack — bukan kualitas grading-nya. Sebuah paket harus melalui level-level berikut untuk mencapai kesiapan produksi.

|Tingkat|Label|Deskripsi|Urutannya|
|-------|-------|-------------|--------------|
|1|**Eksperimental**|Prototipe konsep, eksplorasi|RFC, implementasi dasar|
|2|**Fungsional**|Berfungsi untuk skenario dasar|Golden Test, mencakup terdokumentasi, batasan yang tidak diketahui|
|3|**Siap Produksi**|Stabil, memenuhi syarat rilis|Benchmark ≥80%, ≥50 kasus nyata, dokumentasi, tidak ada masalah keamanan P0/P1|
|4|**Ahli Domain**|Pengetahuan domain mendalam, multi-vendor/multi-domain|Benchmark ≥90%, ≥200 kasus nyata, mencakup multi-vendor|
|5|**Bersertifikat**|Diaudit, dibenchmark, kualitas referensi|Audit independen, dashboard Benchmark publik, ≥500 kasus nyata|
|6|**Referensi Kemampuan**|Tolok ukur industri untuk domain tersebut|Validasi lintas proyek, metodologi terpublikasi, adopsi komunitas|

**Status Saat Ini (2026-08-02):**

|Capability Pack|Tingkat Kematangan|Sasaran Tingkat|
|-----------------|------------------|--------------|
|Insinyur Jaringan|3 — Siap Produksi|4 — Ahli Domain|
|Kode Insinyur|3 — Siap Produksi|4 — Ahli Domain|
|Asisten Peneliti|3 — Siap Produksi|4 — Ahli Domain|
|Asisten DevOps|3 — Siap Produksi|4 — Ahli Domain|
|Analis Perdagangan|2 — Fungsional|3 — Siap Produksi|
|Pengembangan Diri|3 — Siap Produksi|4 — Ahli Domain|
|Decision Intelligence|3 — Siap Produksi|4 — Ahli Domain|
|Sistem Arsitek|3 — Siap Produksi|4 — Ahli Domain|
|Security Engineer|3 — Siap Produksi|4 — Ahli Domain|
|Data Engineer|3 — Siap Produksi|4 — Ahli Domain|
|Database Engineer|3 — Siap Produksi|4 — Ahli Domain|
|QA Engineer|3 — Siap Produksi|4 — Ahli Domain|
|Business Analyst|3 — Siap Produksi|4 — Ahli Domain|

---

## 3. Nilai Kualitas

Quality Grades menggambarkan **hasil Benchmark terkini** dari sebuah Capability Pack. Grade ini adalah hasil evaluasi, bukan level kematangan.

|Nilai|Makna|Skor Benchmark|
|-------|-------|-----------------|
|C|**Fungsional** — berfungsi untuk skenario dasar|≥65%|
|B|**Siap produksi** — stabil dan andal|≥75%|
|B+|**Siap produksi** — kehebatan di atas rata-rata|≥80%|
|A-|**Ahli domain** — pengetahuan mendalam di domain utama|≥85%|
|A|**Ahli** — penguasaan domain yang komprehensif|≥90%|
|SEBUAH+|**Implementasi referensi** — tolok ukur industri|≥95%|

**Nilai Kualitas Saat Ini (2026-08-02):**

|Capability Pack|Nilai|Skor|Status|
|-----------------|-------|-------|--------|
|Insinyur Jaringan|A|≥90|Siap Produksi|
|Kode Insinyur|A-|≥85|Siap Produksi|
|Asisten Peneliti|A-|≥85|Siap Produksi|
|Asisten DevOps|B+|≥80|Siap Produksi|
|Analis Perdagangan|B+|≥80|Sertifikasi Tertunda|
|Pengembangan Diri|A|≥90|Siap Produksi|
|Decision Intelligence|A|91,25%|Siap Produksi (RFC-0007)|
|Sistem Arsitek|A|97,50%|Siap Produksi (RFC-0011)|
|Security Engineer|A-|≥85|Siap Produksi (RFC-0008)|
|Data Engineer|A-|≥85|Siap Produksi (RFC-0009)|
|Database Engineer|A-|≥85|Siap Produksi (RFC-0010)|
|QA Engineer|A|≥90|Siap Produksi (RFC-0012)|
|Business Analyst|A-|≥85|Siap Produksi (RFC-0013)|

### Mutu Kelas vs Tingkat Kematangan

Kedua konsep ini bersifat mandiri:

- **Level Kematangan** = Di mana paket berada dalam lifecycle-nya (misalnya, Siap Produksi)
- **Quality Grade** = Keberhasilan kinerja paket dalam Benchmark (misalnya, A)

Sebuah paket di Level 3 (Siap Produksi) mungkin sedang menuju grade A+. Sebuah paket di Level 4 (Ahli Domain) mungkin memiliki tingkat lebih rendah jika cakupan domainnya berkembang lebih cepat daripada skor Benchmark-nya.

---

## 4. Kemampuan Siklus Hidup

Setiap Capability Pack mengikuti siklus hidup yang terdefinisi dari proposal hingga penebangan:

```
Proposal
    ↓
  RFC
    ↓
Prototipe
    ↓
Eksperimental
    ↓
Stabil
    ↓
Bersertifikat
    ↓
Pemeliharaan
    ↓
Deprecated
```

### Deskripsi Fase

|Fase|Gerbang|Aktivitas|
|-------|------|------------|
|**Usul**|Dokumen ide|Menentukan cakupan, domain target, use case|
|**RFC**|RFC disetujui|Tinjau komunitas, penyelarasan arsitektur|
|**Prototipe**|Demo prototipe|Logika inti diimplementasikan, pengujian dasar|
|**Eksperimental**|Golden Test lulus|Keterbatasan terdokumentasi, Benchmark v1|
|**Stabil**|Benchmark ≥80%, ≥50 kasus nyata|Dokumentasi lengkap, pengamatan keamanan, akses SDK|
|**Bersertifikat**|Audit independen|Dashboard Benchmark publik, dokumentasi referensi|
|**Pemeliharaan**|Tidak ada pengembangan aktif|Hanya perbaikan bug, tanpa fitur baru|
|**Tidak digunakan lagi**|Pengganti teridentifikasi|Periode pemberitahuan, panduan migrasi, arsip|

### Status Siklus Hidup Saat Ini

|Capability Pack|Fase Siklus Hidup|Catatan|
|-----------------|-----------------|-------|
|Insinyur Jaringan|Stabil|Berkembang menuju Bersertifikat|
|Kode Insinyur|Stabil|Berkembang menuju Bersertifikat|
|Asisten Peneliti|Stabil|Berkembang menuju Bersertifikat|
|Asisten DevOps|Stabil|Berkembang menuju Bersertifikat|
|Analis Perdagangan|Eksperimental → Stabil|Sertifikasi berlangsung|
|Pengembangan Diri|Stabil|Berkembang menuju Bersertifikat|
|Decision Intelligence|Stabil|Lapisan penalaran bersama (RFC-0007)|
|Sistem Arsitek|Stabil|Otoritas arsitektur (RFC-0011)|
|Security Engineer|Stabil|Siap Produksi (RFC-0008)|
|Data Engineer|Stabil|Siap Produksi (RFC-0009)|
|Database Engineer|Stabil|Siap Produksi (RFC-0010)|
|QA Engineer|Stabil|Siap Produksi (RFC-0012)|
|Business Analyst|Stabil|Siap Produksi (RFC-0013)|

---

## 5. Capability Pack Resmi

### 5.1 Insinyur Jaringan

**Kategori:** Jaringan
**Kemampuan:** Pembuatan konfigurasi, validasi, penerapan
**Kriteria Keberhasilan:**
- Mengonfigurasi router MikroTik melalui Plugin
- Memvalidasi konfigurasi sebelum penerapan
- Akhirnya naskah dikembalikan
- Menggunakan Knowledge Graph untuk topologi jaringan
**Target Kualitas:** A — 100 konfigurasi nyata, akurasi ≥95%.
**Target Kematangan:** Level 4 — Domain Ahli

### 5.2 Kode Insinyur

**Kategori:** Pengembangan
**Kemampuan:** Generasi kode full-stack, pengujian, dokumentasi
**Kriteria Keberhasilan:**
- Hasilkan backend API dari persyaratan
- Kesimpulannya frontend UI dari API spec
- Membuat skema database
- Menghasilkan pengujian dan dokumentasi
- Semua komponen bekerja bersama
**Target Kualitas:** A- (≥85) — 100 repositori, ≥90% kualitas kode
**Target Kematangan:** Level 4 — Domain Ahli

### 5.3 Asisten Peneliti

**Kategori:** Penelitian
**Kemampuan:** RAG, Knowledge Graph, sitasi, pembelajaran
**Kriteria Keberhasilan:**
- Mengambil dokumen yang relevan dari dasar pengetahuan
- Menyintesis informasi dari berbagai sumber
- Menyediakan situs untuk setiap klaim
- Belajar dari sesi penelitian
**Target Kualitas:** A- (≥85) — 100 pertanyaan penelitian, ≥85% akurasi sitasi
**Target Kematangan:** Level 4 — Domain Ahli

### 5.4 Asisten DevOps

**Kategori:** DevOps
**Kemampuan:** CI/CD, containerisasi, penerapan
**Kriteria Keberhasilan:**
- Menghasilkan Dockerfile dari kebutuhan aplikasi
- Membuat alur kerja GitHub Actions
- Penerapan ke registri kontainer
- Memverifikasi penyebaran kesehatan
**Target Kualitas:** B+ (≥80) — 100 skenario infrastruktur, ≥85% kebenaran
**Target Kematangan:** Level 4 — Domain Ahli

### 5.5 Analis Perdagangan

**Kategori:** Keuangan
**Kemampuan:** Analisis pasar, simulasi, teori keputusan
**Kriteria Keberhasilan:**
- Menganalisis data pasar menggunakan saluran kognitif
- Kesimpulannya rekomendasi trading dengan skor keyakinan
- Menggunakan mesin debat untuk perbandingan multi-strategi
- Mencatat keputusan ke pengalaman kenangan
**Target Kualitas:** B+ (≥80) — 100 skenario pasar, pengembalian yang disesuaikan dengan risiko
**Target Kematangan:** Level 3 — Siap Produksi (Sertifikasi Tertunda)

### 5.6 Pengembangan Diri

**Kategori:** Platform
**Kemampuan:** Analisis arsitektur, proposal perbaikan, pembuatan patch, alur persetujuan
**Kriteria Keberhasilan:**
- Menganalisis struktur proyek dan mengidentifikasi kemacetan
- Akhirnya usulan perbaikan dengan penilaian risiko
- Hasil patch dan laporan pengujian
- Memerlukan persetujuan eksplisit pengguna sebelum menerapkan perubahan
**Target Kualitas:** A (≥90) — 10 proyek nyata, ≥80% penerimaan perbaikan
**Target Kematangan:** Level 4 — Domain Ahli

### 5.7 Decision Intelligence

**Kategori:** Platform — Penalaran Bersama
**Kemampuan:** Pengumpulan bukti, generasi alternatif, analisis risiko, analisis trade-off, scoring, estimasi kepercayaan, keputusan yang dapat dijelaskan, riwayat keputusan
**Kriteria Keberhasilan (RFC-0007):**
- Pengambilan keputusan berdasarkan bukti dari berbagai sumber Capability Pack
- Menghasilkan rekomendasi yang dapat dijelaskan dengan skor keyakinan
- Menganalisis risiko (probabilitas × dampak) dan trade-off antar alternatif
- Mencatat keputusan ke Experience Memory / Decision History
- Rantai penjelasan lengkap: bukti → alasan → alternatif → risiko → keputusan → alasan
**Target Kualitas:** A (≥90) — Benchmark total 91,25%
**Benchmark:** `benchmarks/decision_intelligence_benchmark.py` (8 dimensi)
**Target Kematangan:** Level 3 — Siap Produksi

### 5.8 Sistem Arsitek

**Kategori:** Platform — Otoritas Arsitektur
**Kemampuan:** Tinjauan arsitektur, validasi Clean Architecture, analisis DDD, desain event-driven, evaluasi CQRS, analisis microservices/monolith, penegakan batasan paket, tata kelola, generasi ADR
**Kriteria Keberhasilan (RFC-0011):**
- Mereview struktur repositori terhadap Clean Architecture, DDD, event-driven, CQRS, dan pola microservices
- Mendeteksi siklus ketergantungan, pelanggaran lapisan, dan pelanggaran batas paket
- Menegakkan Arsitektur Tata Kelola: Inti penjaga perubahan, Kapabilitas Aturan Utama, paket independensi
- Hasil rencana ADR disusun dari pengamatan temuan
- Penjelasan rantai lengkap: temuan → metrik → rekomendasi → ADR
**Target Kualitas:** A (≥90) — Benchmark keseluruhan 97,50%
**Benchmark:** `benchmarks/system_architect_benchmark.py` (8 dimensi)
**Target Kematangan:** Level 4 — Domain Ahli

### 5.9 Security Engineer

**Kategori:**Keamanan
**Kemampuan:** Analisis OWASP Top 10, audit keamanan, uji penetrasi, pemodelan ancaman, deteksi rahasia, analisis kerentanan, audit dependensi, pengerasan konfigurasi, persyaratan kepatuhan
**Kriteria Keberhasilan (RFC-0008):**
- Kemampuan keamanan perusahaan mencakup OWASP Top 10
- Pemodelan ancaman dan deteksi rahasia
- Analisis kerentanan dan ketergantungan audit
- Konfigurasi konfigurasi dan pemadatan
**Target Kualitas:** A- (≥85)
**Benchmark:** `benchmarks/security_engineer_benchmark.py` (9 dimensi)
**Target Kematangan:** Level 3 — Siap Produksi

### 5.10 Data Engineer

**Kategori:** Data
**Kemampuan:** Pipeline ETL/ELT, pembersihan data, validasi dataset, evolusi skema, rekayasa fitur, penanganan time-series, jaminan kualitas data
**Kriteria Keberhasilan (RFC-0009):**
- Manajemen data siklus hidup lengkap: ETL/ELT, pembersihan data, validasi dataset
- Evolusi skema dan rekayasa fitur
- Penanganan time-series dan jaminan kualitas data
**Target Kualitas:** A- (≥85)
**Benchmark:** `benchmarks/data_engineer_benchmark.py` (8 dimensi)
**Target Kematangan:** Level 3 — Siap Produksi

### 5.11 Database Engineer

**Kategori:** Data Dasar
**Kemampuan:** Desain skema, optimasi query, manajemen migrasi, perencanaan replikasi, backup/recovery, rekomendasi indeks, analisis kinerja
**Kriteria Keberhasilan (RFC-0010):**
- Kemampuan database enterprise: desain skema, optimasi query
- Manajemen migrasi, perencanaan replikasi, pencadangan/pemulihan
- Rekomendasi indeks dan analisis kinerja
**Target Kualitas:** A- (≥85)
**Benchmark:** `benchmarks/database_engineer_benchmark.py` (8 dimensi)
**Target Kematangan:** Level 3 — Siap Produksi

### 5.12 QA Engineer

**Kategori:** Jaminan Mutu
**Kemampuan:** Uji unit/integrasi generasi, uji regresi otomasi, uji pengobatan, generasi Golden Test untuk paket lain, uji generasi Benchmark, uji deteksi flaky, meliputi analisis, validasi kinerja
**Kriteria Keberhasilan (RFC-0012):**
- Jaminan kualitas otomatis: pengujian unit/integrasi
- Uji regresi otomasi dan uji pengobatan
- Generasi Golden Test untuk paket lain
- Cakupan tes dan analisis Generasi Benchmark
**Target Kualitas:** A (≥90)
**Benchmark:** `benchmarks/qa_engineer_benchmark.py` (9 dimensi)
**Target Kematangan:** Level 3 — Siap Produksi

### 5.13 Business Analyst

**Kategori:** Analisis Bisnis
**Kemampuan:** Pengumpulan kebutuhan, pemodelan proses bisnis, generasi user story, pemodelan use case, generasi BRD, spesifikasi fungsional, gap analysis, analisis ROI, proses optimasi
**Kriteria Keberhasilan (RFC-0013):**
- Penerjemahan bisnis-ke-teknis: persyaratan pengumpulan
- Pemodelan proses bisnis dan generasi user story
- Pemodelan use case, generasi BRD, spesifikasi fungsional
- Analisis gambaran, analisis ROI, dan proses optimasi
**Target Kualitas:** A- (≥85)
**Benchmark:** `benchmarks/business_analyst_benchmark.py` (9 dimensi)
**Target Kematangan:** Level 3 — Siap Produksi

---

## 6. Persyaratan Benchmark

### 6.1 kemampuan Benchmark

Setiap Capability Pack harus mendefinisikan dan memelihara Benchmark:

- Minimum **100 skenario** untuk menargetkan nilai A/B
- Minimum **10 proyek** untuk target kelas A-/B+
- Benchmark harus mencakup 6 dimensi: **Akurasi, Kelengkapan, Penjelasan, Keamanan, Efisiensi, Konsistensi**
- Hasil harus **dapat direproduksi** dan disimpan di `benchmarks/`

### 6.2 Benchmark Dunia Nyata

Setiap Capability Pack harus memelihara direktori `real_cases/<capability_id>/` yang berisi:

- Pasangan input/output nyata dari penggunaan aktual
- Catatan evaluasi untuk setiap kasus
- Tautan ke pembaruan Benchmark sintetis yang didorong oleh temuan nyata

### 6.3 Dimensi Benchmark

|Dimensi|Definisi|pengukuran|
|-----------|------------|-------------|
|Ketepatan|Keluaran kebenaran|% temuan/rekomendasi yang benar|
|Kelengkapan|Cakupan semua aspek relevan|% elemen yang diperlukan tercakup|
|Penjelasan|Kejelasan dan kualitas penalaran|Skor evaluasi manusia|
|Keamanan|Tidak ada keluaran berbahaya atau tidak aman|% output yang lolos pemeriksaan keamanan|
|Efisiensi|Waktu respons dan penggunaan sumber daya|Latensi P95, penggunaan token|
|Konsistensi|Keluaran yang sama untuk masukan yang sama|Varian di keseluruhannya berlipat ganda|

---

## 7. Perluasan Pengetahuan

Semua penambahan pengetahuan yang direncanakan dilacak melalui RFC dan diimplementasikan hanya di dalam Capability Pack. Inti tetap tidak berubah.

### 7.1 Insinyur Jaringan

**Referensi RFC:** RFC-0004

**Penambahan yang direncanakan:**
- Panduan Desain Cisco: kampus, pusat data, SD-WAN, HA
- Praktik Terbaik MikroTik: ISP edge, hotspot, IPv6, FastTrack
- Pengerasan Fortinet: FortiOS, kebijakan, VPN, ancaman perlindungan
- BGP: pemilihan jalur, pemfilteran, komunitas, pemantauan
- MPLS: penerusan, LDP, VRF, dasar-dasar rekayasa lalu lintas
- IPv6: dual-stack, SLAAC, DHCPv6, mekanisme transisi
- Zero Trust: prinsip, segmentasi mikro, ZTNA

### 7.2 Kode Insinyur

**Referensi RFC:** RFC-0006

**Penambahan yang direncanakan:**
- Arsitektur Bersih: lapisan, aturan, ketergantungan, batasan
- DDD: konteks terbatas, agregat, peristiwa domain, anti korupsi
- SOLID: seluruh 5 prinsip dengan contoh Python/TypeScript
- CQRS: perpecahan perintah/query, model tulis/baca
- Sumber Acara: penyimpanan acara, pemutaran ulang, proyeksi
- Pengkodean Aman: OWASP Top 10, injeksi, autentikasi, rahasia

### 7.3 Asisten Peneliti

**Penambahan yang direncanakan:**
- Peringkat bukti: kualitas sumber, kebaruan, metodologi
- Deteksi membedakan: mengidentifikasi klaim yang berbeda
- Kualitas situs: kelengkapan, format, asal
- Estimasi keyakinan: kuantifikasi keseluruhan
- Pola sintesis: integrasi multi-kertas

### 7.4 Asisten DevOps

**Penambahan yang direncanakan:**
- Multi-cloud: pola layanan AWS, Azure, GCP
- GitOps: ArgoCD, Flux, standar deklaratif
- Platform Rekayasa: IDP, pengembang portal
- Kebijakan sebagai kode: OPA, Sentinel, Kyverno
- Prinsip chaos engineering

### 7.5 Analis Perdagangan

**Referensi RFC:** RFC-0005

**Penambahan yang direncanakan:**
- Wyckoff: fase, operator gabungan, penawaran/permintaan
- ICT: struktur pasar, FVG, blok pesanan, likuiditas
- SMC: aliran institusional, likuiditas, premi/diskon
- Elliott Wave: pola impuls/korektif, Fibonacci
- Volume Profil: POC, nilai area, volume pola
- Makro: indikator, kebijakan Fed, risk-on/off
- Pilihan: Yunani, Strategi, IV, Aktivitas Tidak Biasa
- Kontrak berjangka: contango/backwardation, basis, COT
- Psikologi: bias, toleransi risiko, manajemen emosi

### 7.6 Pengembangan Diri

**Penambahan yang direncanakan:**
- Pembelajaran pola lintas proyek
- Prediksi dampak sebelum perubahan
- Bau arsitektur Taksonomi
- Pemodelan risiko perubahan
- Saran perbaikan otomatis

---

## 8. Capability Pack Masa Depan (Peta Jalan)

Semua Capability Pack yang tercantum di bawah telah diimplementasikan. Future pack hanya akan dikembangkan setelah 13 pack yang ada mencapai target grade A/A- dan memenuhi aturan Governance.

> **Prinsip Perluasan Berbasis Domain:** ECP **tidak lagi menambah Capability Pack berdasarkan profesi**, tetapi berdasarkan **domain keahlian yang benar-benar reusable** oleh Capability Pack lain. Setiap calon pack baru harus:
>
> 1. **Reusable** — dipakai minimal 2 Capability Pack konsumen
> 2. **Domain Expertise, bukan Role** — mewakili keahlian yang dapat dieksekusi, bukan jabatan
> 3. **Tidak memaksa perubahan Core** — seluruh penambahan terjadi di dalam Capability Pack
> 4. **Lulus Governance** — use case lintas sistem, Benchmark, Golden Test
> 5. **Kebutuhan nyata** — ditambahkan saat ada kebutuhan proyek aktual
>
> **Target: 15–20 Capability Pack, masing-masing benar-benar setara spesialis berpengalaman. Platform dengan 18 pack berkualitas tinggi jauh lebih bernilai daripada 50 pack dengan kemampuan dasar.**

### 8.0 Prinsip Perluasan Berbasis Domain

> **ECP tidak lagi menambah Capability Pack berdasarkan profesi, tetapi berdasarkan domain keahlian yang benar-benar reusable oleh Capability Pack lain.**

Setiap calon Capability Pack baru harus memenuhi kriteria berikut sebelum dimasukkan ke roadmap:

1. **Reusable** — kemampuannya dipakai oleh minimal 2 Capability Pack konsumen.
2. **Domain Expertise, bukan Role** — paket mewakili keahlian yang dapat dieksekusi, bukan jabatan/judul.
3. **Tidak memaksa perubahan Core** — seluruh penambahan terjadi di dalam Capability Pack.
4. **Lulus Governance** — memiliki use case lintas sistem, Benchmark, Golden Test, dan tidak memaksa perubahan Core.
5. **Kebutuhan nyata** — ditambahkan ketika ada kebutuhan proyek aktual, bukan sekadar melengkapi daftar.

Roadmap perluasan dibagi dalam **4 Tier** berdasarkan nilai dampak dan reusability:

### 8.1 Security Engineer (Prioritas Tinggi — ⭐⭐⭐⭐)

**Fase:** Fase 2 — Setelah Capability Excellence
**Status:** ✅ Diimplementasikan (RFC-0008)
**Fungsi:**Keamanan aplikasi dan infrastruktur
**Kemampuan:**
- Analisis 10 OWASP
- Audit keamanan dan uji penetrasi
- Ancaman pemodelan
- Deteksi kerahasiaan dan penilaian kerentanan
**Paket Tergantung:** Kode, DevOps, Jaringan
**Status RFC:** RFC-0008 — Diimplementasikan
**Target Kematangan:** Level 3 — Siap Produksi

### 8.2 Data Engineer (Prioritas Tinggi — ⭐⭐⭐⭐)

**Fase:** Fase 2 — Setelah Capability Excellence
**Status:** ✅ Diimplementasikan (RFC-0009)
**Fungsi:** Fondasi data untuk meningkatkan Trading, Research, dan analitik
**Kemampuan:**
- pipa ETL
- Pembersihan dan kualitas data
- Pembuatan versi kumpulan data
- Fitur Rekayasa
- Saluran pipa deret waktu
**Paket bergantung:** Perdagangan, Riset, DevOps
**Status RFC:** RFC-0009 — Diimplementasikan
**Target Kematangan:** Level 3 — Siap Produksi

### 8.3 Paket Perusahaan (Fase 3)

|Capability Pack|Fungsi|Paket Tanggungan|
|-----------------|--------|-----------------|
|**Database Engineer**|Optimasi SQL, desain skema, migrasi, rekomendasi indeks, analisis kinerja|Kode, DevOps|
|**QA Engineer**|Uji generasi, regresi, uji mutasi, pembangun Golden Test, generator Benchmark|Kode, DevOps, Pengembangan Diri|
|**Business Analyst**|Persyaratan analisis, cerita pengguna, BRD, use case, alur kerja|Semua paket|

### 8.4 Platform Professional (Tier A — Sangat Direkomendasikan ⭐⭐⭐⭐⭐)

Tier ini berisi pack dengan **reusability tertinggi** dan dampak langsung terhadap kualitas pack lain.

|Prioritas|Capability Pack|Fokus Domain|Dipakai Oleh|
|-----------|----------------|-------------|--------------|
|⭐⭐⭐⭐⭐|**Infrastructure Engineer**|Kubernetes, Docker Swarm, Proxmox, VMware, Ceph, HA Cluster, Load Balancer, Storage, Disaster Recovery|DevOps, Network, System Architect|
|⭐⭐⭐⭐⭐|**AI Engineer**|RAG, Agent Design, Prompt Optimization, Model Router, LoRA, Fine-tuning, Evaluation, Guardrails|Trading, Research, Code, Self Development|
|⭐⭐⭐⭐⭐|**Documentation Engineer**|API Documentation, OpenAPI, SDK Docs, ADR, RFC, Changelog, Release Notes, Architecture Documentation|Semua pack (menjaga dokumentasi sinkron dengan kode)|

### 8.5 Platform Professional (Tier B)

Tier B melengkapi siklus pengembangan produk end-to-end.

|Prioritas|Capability Pack|Fokus Domain|Catatan|
|-----------|----------------|-------------|--------|
|⭐⭐⭐⭐|**Product Manager**|Product Vision, Backlog, Roadmap, Prioritas, Sprint, Release Planning|Orientasi produk|
|⭐⭐⭐⭐|**UI/UX Designer**|Wireframe, UX Review, Accessibility, Design System, Component Library|Orientasi pengalaman pengguna|
|⭐⭐⭐⭐|**Full Stack Engineer**|Integrasi Frontend–Backend, End-to-end Feature Delivery, API Mapping, State Management, Deployment Readiness|**Bukan pengganti Code Engineer** — fokus integrasi dan delivery end-to-end|

### 8.6 Platform Enterprise (Tier C)

Tier C melayani kebutuhan enterprise: skala, keandalan, kepatuhan, dan pengetahuan terstruktur.

|Prioritas|Capability Pack|Fokus Domain|
|-----------|----------------|-------------|
|⭐⭐⭐|**Cloud Architect**|AWS, Azure, GCP, Hybrid Cloud, Multi Cloud, Cost Optimization|
|⭐⭐⭐|**SRE (Site Reliability Engineer)**|Observability, Monitoring, Alerting, Incident Response, SLI, SLO, SLA|
|⭐⭐⭐|**Compliance Officer**|ISO 27001, NIST, PCI-DSS, GDPR, Audit, Governance|
|⭐⭐⭐|**Knowledge Engineer**|Ontology, Knowledge Graph, Semantic Search, Entity Resolution, Taxonomy, Knowledge Curation|
|⭐⭐⭐|**Full Stack Engineer**|Integrasi Frontend–Backend, End-to-end Feature Delivery|

> **Catatan:** Full Stack Engineer dituliskan di Tier B dan Tier C sebagai opsi penempatan. Jika sudah masuk Tier B, Tier C cukup berisi 4 pack baru.

### 8.7 Vertical Industry (Tier D — Kondisional)

Ditambahkan **hanya ketika ada kebutuhan proyek nyata** dan memenuhi aturan Governance. Tidak disarankan ditambahkan semuanya sekaligus.

- Finance Analyst
- HSE Specialist
- Legal Advisor
- HR Specialist
- Procurement Specialist
- Manufacturing Engineer
- Mining Engineer
- Oil & Gas Engineer
- Healthcare Assistant
- Education Assistant

### 8.8 Target Jumlah Pack

|Tahap|Jumlah Pack|Keterangan|
|-------|------------|------------|
|**Platform Core**|13|Fokus menyelesaikan kualitas (Capability Excellence)|
|**Platform Professional**|+5|Infrastructure Engineer, AI Engineer, Documentation Engineer, Product Manager, UI/UX Designer|
|**Platform Enterprise**|+5|Cloud Architect, SRE, Compliance Officer, Knowledge Engineer, Full Stack Engineer|
|**Target Aktif**|**18**|13 Core + 5 Professional — masing-masing setara spesialis berpengalaman|
|**Proposed**|23|18 + 5 Enterprise|
|**Vertical Industry**|Kondisional|Berdasarkan kebutuhan proyek nyata|

### 8.9 Komponen yang Tidak Akan Menjadi Capability Pack

Komponen berikut akan diposisikan sebagai **Plugin**, **Layanan**, atau **platform infrastruktur**, bukan Capability Pack:

- Otentikasi / Otorisasi
- PostgreSQL / Redis / MinIO / Kafka
- Plugin Pasar
- Konektor Pialang / Konektor Pertukaran
- Infrastruktur murni (penyeimbang beban, DNS, wadah Runtime)

---

## 9.Kemampuan Templat Changelog

Setiap Capability Pack memelihara changelog-nya sendiri. Changelog mencatat penambahan pengetahuan, peningkatan Benchmark, dan peningkatan penalaran. Changelog tidak mencatat perubahan Core.

### Format

```markdown
## <Capability Pack> v<version>

### Added
- <knowledge/topic>

### Improved
- <aspek>

### Fixed
- <masalah>

### Benchmark
- <dimensi>: <sebelum> → <sesudah>
```

### Contoh

```markdown
## Network v1.1

### Added
- BGP path selection analysis
- MPLS forwarding rules
- IPv6 dual-stack patterns

### Improved
- Kedalaman penjelasan firewall
- Akurasi risk scoring: 85% → 92%

### Fixed
- VLAN false positive pada trunk interface

### Benchmark
- Accuracy: 89% → 92%
- Explainability: B → A-
```

---

## 10. Persetujuan

|Peran|Status|Tanggal|
|------|--------|------|
|Kepala Bagian Produk|Disetujui|08-02-2026|
|Kepala Arsitek|Disetujui|08-02-2026|
