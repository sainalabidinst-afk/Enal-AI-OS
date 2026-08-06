<!-- DOCUMENT_METADATA_START -->
**Pemilik:** Tim Dokumentasi
**Pemilik Canonical:** Pimpinan Tata Kelola Dokumentasi
**Diverifikasi Terakhir:** 08-04-2026
**Versi:** 1.1.0
**Status:** Aktif
**SSOT:** Model kematangan Capability Pack, profil, dan siklus hidup strategis
<!-- DOCUMENT_METADATA_END -->

# Strategi Kemampuan ECP

**Versi:** 1.1.0
**Berlaku:** 04-08-2026
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

**Status Saat Ini (2026-08-05):**

|Capability Pack|Tingkat Kematangan|Sasaran Tingkat|
|-----------------|------------------|--------------|
|Insinyur Jaringan|4 — Ahli Domain|4 — Ahli Domain|
|Kode Insinyur|4 — Ahli Domain|4 — Ahli Domain|
|Asisten Peneliti|4 — Ahli Domain|4 — Ahli Domain|
|Asisten DevOps|4 — Ahli Domain|4 — Ahli Domain|
|Analis Perdagangan|4 — Ahli Domain|4 — Ahli Domain|
|Pengembangan Diri|4 — Ahli Domain|4 — Ahli Domain|
|Decision Intelligence|4 — Ahli Domain|4 — Ahli Domain|
|Sistem Arsitek|4 — Ahli Domain|4 — Ahli Domain|
|Security Engineer|4 — Ahli Domain|4 — Ahli Domain|
|Data Engineer|4 — Ahli Domain|4 — Ahli Domain|
|Database Engineer|4 — Ahli Domain|4 — Ahli Domain|
|QA Engineer|4 — Ahli Domain|4 — Ahli Domain|
|Business Analyst|4 — Ahli Domain|4 — Ahli Domain|
|Infrastructure Engineer|4 — Ahli Domain|4 — Ahli Domain|
|AI Engineer|4 — Ahli Domain|4 — Ahli Domain|
|Documentation Engineer|4 — Ahli Domain|4 — Ahli Domain|
|Product Manager|4 — Ahli Domain|4 — Ahli Domain|
|UI/UX Designer|4 — Ahli Domain|4 — Ahli Domain|
|Full Stack Engineer|4 — Ahli Domain|4 — Ahli Domain|

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
|A+|**Implementasi referensi** — tolok ukur industri|≥95%|

**Nilai Kualitas Saat Ini (2026-08-04):**

|Capability Pack|Nilai|Skor|Status|
|-----------------|-------|-------|--------|
|Insinyur Jaringan|A+|≥95|Bersertifikat|
|Kode Insinyur|A+|≥95|Bersertifikat|
|Asisten Peneliti|A+|≥95|Bersertifikat|
|Asisten DevOps|A+|≥95|Bersertifikat|
|Analis Perdagangan|A+|≥95|Bersertifikat|
|Pengembangan Diri|A+|≥95|Bersertifikat|
|Decision Intelligence|A+|≥95|Bersertifikat (RFC-0007)|
|Sistem Arsitek|A+|≥95|Bersertifikat (RFC-0011)|
|Security Engineer|A+|≥95|Bersertifikat (RFC-0008)|
|Data Engineer|A|≥90|Bersertifikat (RFC-0009)|
|Database Engineer|A|≥90|Bersertifikat (RFC-0010)|
|QA Engineer|A+|≥95|Bersertifikat (RFC-0012)|
|Business Analyst|A|≥90|Bersertifikat (RFC-0013)|
|Infrastructure Engineer|A+|≥95|Bersertifikat (RFC-0014)|
|AI Engineer|A+|≥95|Bersertifikat (RFC-0015)|
|Documentation Engineer|A+|≥95|Bersertifikat (RFC-0016)|
|Product Manager|A|≥90|Bersertifikat (RFC-0017)|
|UI/UX Designer|A|≥90|Bersertifikat (RFC-0018)|
|Full Stack Engineer|A+|≥95|Bersertifikat (RFC-0019)|

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
|Insinyur Jaringan|Bersertifikat|Selesai|
|Kode Insinyur|Bersertifikat|Selesai|
|Asisten Peneliti|Bersertifikat|Selesai|
|Asisten DevOps|Bersertifikat|Selesai|
|Analis Perdagangan|Bersertifikat|Selesai|
|Pengembangan Diri|Bersertifikat|Selesai|
|Decision Intelligence|Bersertifikat|Selesai (RFC-0007)|
|Sistem Arsitek|Bersertifikat|Selesai (RFC-0011)|
|Security Engineer|Bersertifikat|Selesai (RFC-0008)|
|Data Engineer|Bersertifikat|Selesai (RFC-0009)|
|Database Engineer|Bersertifikat|Selesai (RFC-0010)|
|QA Engineer|Bersertifikat|Selesai (RFC-0012)|
|Business Analyst|Bersertifikat|Selesai (RFC-0013)|
|Infrastructure Engineer|Bersertifikat|Selesai (RFC-0014)|
|AI Engineer|Bersertifikat|Selesai (RFC-0015)|
|Documentation Engineer|Bersertifikat|Selesai (RFC-0016)|
|Product Manager|Bersertifikat|Selesai (RFC-0017)|
|UI/UX Designer|Bersertifikat|Selesai (RFC-0018)|
|Full Stack Engineer|Bersertifikat|Selesai (RFC-0019)|

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
**Target Kualitas:** A+ — 100 konfigurasi nyata, akurasi ≥95%.
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
**Target Kualitas:** A+ (≥95) — 100 repositori, ≥95% kualitas kode
**Target Kematangan:** Level 4 — Domain Ahli

### 5.3 Asisten Peneliti

**Kategori:** Penelitian
**Kemampuan:** RAG, Knowledge Graph, sitasi, pembelajaran
**Kriteria Keberhasilan:**
- Mengambil dokumen yang relevan dari dasar pengetahuan
- Menyintesis informasi dari berbagai sumber
- Menyediakan situs untuk setiap klaim
- Belajar dari sesi penelitian
**Target Kualitas:** A+ (≥95) — 100 pertanyaan penelitian, ≥95% akurasi sitasi
**Target Kematangan:** Level 4 — Domain Ahli

### 5.4 Asisten DevOps

**Kategori:** DevOps
**Kemampuan:** CI/CD, containerisasi, penerapan
**Kriteria Keberhasilan:**
- Menghasilkan Dockerfile dari kebutuhan aplikasi
- Membuat alur kerja GitHub Actions
- Penerapan ke registri kontainer
- Memverifikasi penyebaran kesehatan
**Target Kualitas:** A+ (≥95) — 100 skenario infrastruktur, ≥95% kebenaran
**Target Kematangan:** Level 4 — Pakar Domain

### 5.5 Analis Perdagangan

**Kategori:** Keuangan
**Kemampuan:** Analisis pasar, simulasi, teori keputusan
**Kriteria Keberhasilan:**
- Menganalisis data pasar menggunakan saluran kognitif
- Kesimpulannya rekomendasi trading dengan skor keyakinan
- Menggunakan mesin debat untuk perbandingan multi-strategi
- Mencatat keputusan ke pengalaman kenangan
**Target Kualitas:** A+ (≥95) — 200 skenario pasar, pengembalian yang disesuaikan dengan risiko
**Target Kematangan:** Level 4 — Ahli Domain

### 5.6 Pengembangan Diri

**Kategori:** Platform
**Kemampuan:** Analisis arsitektur, proposal perbaikan, pembuatan patch, alur persetujuan
**Kriteria Keberhasilan:**
- Menganalisis struktur proyek dan mengidentifikasi kemacetan
- Akhirnya usulan perbaikan dengan penilaian risiko
- Hasil patch dan laporan pengujian
- Memerlukan persetujuan eksplisit pengguna sebelum menerapkan perubahan
**Target Kualitas:** A+ (≥95) — 200 kasus nyata, ≥95% penerimaan perbaikan
**Target Kematangan:** Level 4 — Pakar Domain

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

### 5.14 Infrastructure Engineer

**Kategori:** Infrastruktur
**Kemampuan:** Manajemen kluster, orkestrasi kontainer, virtualisasi, storage, jaringan tingkat tinggi, ketahanan, disaster recovery
**Kriteria Keberhasilan (RFC-0014):**
- Mengelola infrastruktur berbasis Kubernetes, Docker Swarm, Proxmox, VMware, Ceph
- Mengonfigurasi kluster HA, load balancer, dan strategi penyimpanan
- Merancang dan menguji skenario pemulihan bencana
- Menjamin ketersediaan layanan infrastruktur melalui otomatisasi
**Target Kualitas:** A (≥90) — 50 skenario infrastruktur, ≥90% ketersediaan
**Benchmark:** `benchmarks/infrastructure_engineer_benchmark.py` (9 dimensi)
**Target Kematangan:** Level 3 — Siap Produksi

### 5.15 AI Engineer

**Kategori:** Kecerdasan Buatan
**Kemampuan:** RAG, desain agent, optimasi prompt, model router, LoRA, fine-tuning, evaluasi, guardrails
**Kriteria Keberhasilan (RFC-0015):**
- Merancang pipeline RAG dengan retrieval, reranking, dan generasi
- Membangun dan mengevaluasi agen otonom dengan guardrails keamanan
- Melakukan fine-tuning dan evaluasi model LLM
- Mengoptimalkan performa dan biaya inferensi melalui model routing
**Target Kualitas:** A+ (≥95) — 100 skenario AI, ≥95% akurasi
**Benchmark:** `benchmarks/ai_engineer_benchmark.py` (10 dimensi)
**Target Kematangan:** Level 3 — Siap Produksi

### 5.16 Documentation Engineer

**Kategori:** Dokumentasi
**Kemampuan:** Dokumentasi API, OpenAPI, SDK Docs, ADR, RFC, Changelog, Release Notes, arsitektur dokumentasi
**Kriteria Keberhasilan (RFC-0016):**
- Menghasilkan dan memelihara dokumentasi API sesuai standar OpenAPI
- Menyusun ADR, RFC, changelog, dan release notes yang konsisten
- Menjaga sinkronisasi dokumentasi dengan perubahan kode
- Menyediakan panduan penggunaan dan integrasi untuk konsumen
**Target Kualitas:** A (≥90) — 100 skenario dokumentasi, kelengkapan ≥95%
**Benchmark:** `benchmarks/documentation_engineer_benchmark.py` (7 dimensi)
**Target Kematangan:** Level 3 — Siap Produksi

### 5.17 Product Manager

**Kategori:** Produk
**Kemampuan:** Visi produk, backlog, roadmap, prioritisasi, sprint, release planning, metrik produk
**Kriteria Keberhasilan (RFC-0017):**
- Menyusun visi produk dan roadmap jangka menengah
- Mengelola backlog dan prioritisasi berdasarkan nilai bisnis
- Merencanakan sprint dan koordinasi rilis
- Mengukur metrik produk dan umpan balik pengguna
**Target Kualitas:** A- (≥85) — 50 skenario produk, kepuasan stakeholder ≥85%
**Benchmark:** `benchmarks/product_manager_benchmark.py` (8 dimensi)
**Target Kematangan:** Level 3 — Siap Produksi

### 5.18 UI/UX Designer

**Kategori:** Desain
**Kemampuan:** Wireframe, UX review, aksesibilitas, design system, pustaka komponen, prototype, pengujian kegunaan
**Kriteria Keberhasilan (RFC-0018):**
- Merancang wireframe dan prototype sesuai kebutuhan pengguna
- Meninjau UX dan merekomendasikan perbaikan berdasarkan data
- Menyusun dan memelihara design system serta komponen UI
- Memastikan kepatuhan standar aksesibilitas (WCAG)
**Target Kualitas:** A- (≥85) — 50 skenario desain, kepatuhan aksesibilitas ≥90%
**Benchmark:** `benchmarks/ui_ux_designer_benchmark.py` (8 dimensi)
**Target Kematangan:** Level 3 — Siap Produksi

### 5.19 Full Stack Engineer

**Kategori:** Pengembangan
**Kemampuan:** Integrasi frontend-backend, pengiriman fitur end-to-end, pemetaan API, manajemen state, kesiapan penerapan
**Kriteria Keberhasilan (RFC-0019):**
- Mengintegrasikan frontend dan backend melalui API yang jelas
- Menyelesaikan fitur secara end-to-end dari kebutuhan hingga deployment
- Memetakan dan menjaga konsistensi API antar layanan
- Menjamin kesiapan penerapan melalui pengujian dan konfigurasi
**Target Kualitas:** A- (≥85) — 50 skenario pengembangan, cakupan pengujian ≥90%
**Benchmark:** `benchmarks/full_stack_engineer_benchmark.py` (9 dimensi)
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

### 7.7 Infrastructure Engineer

**Referensi RFC:** RFC-0014

**Penambahan yang direncanakan:**
- Orkestrasi klaster: Kubernetes, Docker Swarm, Proxmox, VMware
- Penyimpanan terdistribusi: Ceph, ZFS, konfigurasi HA
- Jaringan tingkat tinggi: load balancer, reverse proxy, DNS, firewall
- Virtualisasi dan kontainerisasi: QEMU/KVM, LXC, konfigurasi jaringan
- Pemulihan bencana: replikasi, snapshot, failover, jadwal backup
- Pengerasan sistem: CIS Benchmarks, kebijakan keamanan OS
- Observasi infrastruktur: Prometheus, Grafana, logging terpusat

### 7.8 AI Engineer

**Referensi RFC:** RFC-0015

**Penambahan yang direncanakan:**
- RAG: chunking strategies, embedding models, reranking, hybrid search
- Desain Agent: orkestrasi, manajemen memori, tool calling, evaluasi agen
- Fine-tuning: LoRA, QLoRA, dataset persiapan, evaluasi model
- Evaluasi LLM: benchmark kustom, red-teaming, guardrails
- Model Router: perutean berdasarkan biaya, latensi, dan domain
- Prompt Optimization: chain-of-thought, few-shot, prompt caching
- AI Safety: mitigasi bias, keamanan output, audit model

### 7.9 Documentation Engineer

**Referensi RFC:** RFC-0016

**Penambahan yang direncanakan:**
- Dokumentasi API: OpenAPI 3.0+, AsyncAPI, SDK reference
- Dokumentasi arsitektur: ADR, C4 model, diagram alur, arsitektur layanan
- Dokumentasi pengguna: getting started, tutorial, FAQ, troubleshooting
- Dokumentasi rilis: changelog, migration guide, breaking changes
- Otomatisasi dokumentasi: generation dari kode, CI/CD integration
- Aksesibilitas dokumentasi: WCAG, terjemahan, multi-format

### 7.10 Product Manager

**Referensi RFC:** RFC-0017

**Penambahan yang direncanakan:**
- Manajemen produk: discovery, delivery, OKR, KPI
- Metodologi: Agile, Scrum, Kanban, Lean, dual-track Agile
- Analisis pasar: kompetitor, ukuran pasar, TAM/SAM/SOM
- Persona dan journey mapping: user persona, empati map, touchpoints
- Strategi rilis: go-to-market, launch plan, feature rollout
- Pengambilan keputusan berbasis data: A/B testing, funnel analysis, cohort analysis

### 7.11 UI/UX Designer

**Referensi RFC:** RFC-0018

**Penambahan yang direncanakan:**
- Desain UI: design system, komponen reusable, token, theming
- Pengalaman pengguna: heuristik usability, cognitive walkthrough, A/B testing
- Aksesibilitas: WCAG 2.1/2.2, screen reader, keyboard navigation, color contrast
- Prototyping: Figma, interactive mockup, micro-interactions
- Riset pengguna: wawancara, survei, card sorting, usability testing
- Pola desain: layout, tipografi, motion design, responsive design

### 7.12 Full Stack Engineer

**Referensi RFC:** RFC-0019

**Penambahan yang direncanakan:**
- Arsitektur aplikasi: monolith vs microservices, modular monolith, hexagonal
- Integrasi API: REST, GraphQL, gRPC, webhooks, versioning
- Manajemen state: client state, server state, cache strategies, optimistic updates
- Pengujian: unit, integration, e2e, contract testing, visual regression
- Deployment: CI/CD, blue-green, canary, feature flags, rollback strategies
- Observabilitas: logging, metrics, tracing, error tracking, performance monitoring

---

## 8. Capability Pack Masa Depan (Peta Jalan)

Semua Capability Pack yang tercantum di bawah telah diimplementasikan. Future pack hanya akan dikembangkan setelah 19 pack yang ada mencapai target grade A/A- dan memenuhi aturan Governance.

> **Prinsip Perluasan Berbasis Domain:** ECP **tidak lagi menambah Capability Pack berdasarkan profesi**, tetapi berdasarkan **domain keahlian yang benar-benar reusable** oleh Capability Pack lain. Setiap calon pack baru harus:
>
> 1. **Reusable** — dipakai minimal 2 Capability Pack konsumen
> 2. **Domain Expertise, bukan Role** — mewakili keahlian yang dapat dieksekusi, bukan jabatan
> 3. **Tidak memaksa perubahan Core** — seluruh penambahan terjadi di dalam Capability Pack
> 4. **Lulus Governance** — use case lintas sistem, Benchmark, Golden Test
> 5. **Kebutuhan nyata** — ditambahkan saat ada kebutuhan proyek aktual
>
> **Target: 15–20 Capability Pack, masing-masing benar-benar setara spesialis berpengalaman. Platform dengan 19 pack berkualitas tinggi jauh lebih bernilai daripada 50 pack dengan kemampuan dasar.**

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

> **Status: Semua pack Tier A telah diimplementasikan.**

Tier ini berisi pack dengan **reusability tertinggi** dan dampak langsung terhadap kualitas pack lain.

|Prioritas|Capability Pack|Fokus Domain|Dipakai Oleh|
|-----------|----------------|-------------|--------------|
|⭐⭐⭐⭐⭐|**Infrastructure Engineer**|Kubernetes, Docker Swarm, Proxmox, VMware, Ceph, HA Cluster, Load Balancer, Storage, Disaster Recovery|DevOps, Network, System Architect|
|⭐⭐⭐⭐⭐|**AI Engineer**|RAG, Agent Design, Prompt Optimization, Model Router, LoRA, Fine-tuning, Evaluation, Guardrails|Trading, Research, Code, Self Development|
|⭐⭐⭐⭐⭐|**Documentation Engineer**|API Documentation, OpenAPI, SDK Docs, ADR, RFC, Changelog, Release Notes, Architecture Documentation|Semua pack (menjaga dokumentasi sinkron dengan kode)|

### 8.5 Platform Professional (Tier B)

> **Status: Semua pack Tier B telah diimplementasikan.**

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
|**Platform Professional**|+6|Infrastructure Engineer, AI Engineer, Documentation Engineer, Product Manager, UI/UX Designer, Full Stack Engineer|
|**Platform Enterprise**|+5|Cloud Architect, SRE, Compliance Officer, Knowledge Engineer|
|**Target Aktif**|**19**|13 Core + 6 Professional — masing-masing setara spesialis berpengalaman|
|**Proposed**|24|19 + 5 Enterprise|
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
