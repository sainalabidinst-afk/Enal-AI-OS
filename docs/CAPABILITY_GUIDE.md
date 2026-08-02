# Panduan kemampuan

<!-- DOCUMENT_METADATA_START -->
**Pemilik:** Tim Dokumentasi
**Pemilik Canonical:** Pimpinan Tata Kelola Dokumentasi
**Diverifikasi Terakhir:** 08-02-2026
**Versi:** 1.0.0
**Status:** Aktif
**SSOT:** Spesifikasi Capability Pack, cakupan, target Benchmark, dan tingkat kualitas
<!-- DOCUMENT_METADATA_END -->

Dokumen ini menjelaskan setiap Capability Pack resmi, termasuk scope, fokus pengetahuan, target Benchmark, dan batasan out-of-scope yang eksplisit.
Gunakan dokumen yang diketahui ini sebagai sumber kebenaran untuk apa yang diharapkan dan tidak diketahui oleh setiap Capability Pack.

---

## Status Kemampuan (2026-08-02)
**Platform Kandidat Pelepasan**

|Capability Pack|Nilai|Catatan|
|-----------------|-------|-------|
|Insinyur Jaringan|SEBUAH (≥90)|Siap Produksi|
|Kode Insinyur|SEBUAH- (≥85)|Siap Produksi|
|Asisten Peneliti|SEBUAH- (≥85)|Siap Produksi|
|Asisten DevOps|B+ (≥80)|Siap Produksi|
|Analis Perdagangan|B+ (≥80)|Sertifikasi Tertunda|
|Pengembangan Diri|SEBUAH (≥90)|Siap Produksi|
|Decision Intelligence|SEBUAH (≥90)|Siap Produksi|
|Sistem Arsitek|SEBUAH (≥90)|Siap Produksi|
|Security Engineer|SEBUAH- (≥85)|Siap Produksi|
|Data Engineer|SEBUAH- (≥85)|Siap Produksi|
|Database Engineer|SEBUAH- (≥85)|Siap Produksi|
|QA Engineer|SEBUAH (≥90)|Siap Produksi|
|Business Analyst|SEBUAH- (≥85)|Siap Produksi|

---

## Insinyur Jaringan

**Kemampuan ID:** `network`
**Kategori:** Jaringan
**Target Kualitas:** A

### Cakupan

- Analisis konfigurasi MikroTik RouterOS v6/v7
- Inferensi topologi dari konfigurasi
- Audit keamanan dan kinerja
- Perbandingan konfigurasi (diff) dan perencanaan rollback
- Verifikasi penerapan dan penilaian risiko
- Audit kehadiran dan pelaporan kesehatan

### Fokus Pengetahuan

- Sintaks dan semantik RouterOS
- Firewall, NAT, perutean, DHCP, DNS
- Praktik terbaik khusus MikroTik
- Pola desain jaringan perusahaan
- Pola ISP backbone dan edge

### Di Luar Cakupan

- Otomasi penuh Cisco IOS/NX-OS
- Otomasi penuh Fortinet FortiOS
- Otomasi BGP/OSPF/MPLS
- Orkestra multi-router
- Eksekusi API/SSH perangkat langsung
- Pengadaan perangkat keras atau kabel

### Target Benchmark

- 100 konfigurasi MikroTik nyata
- ≥95% akurasi deteksi masalah
- ≥90% kualitas rekomendasi

---

## Kode Insinyur

**Kemampuan ID:** `code`
**Kategori:** Pengembangan
**Target Kualitas:** A- (≥85) - Siap Produksi

### Cakupan

- Desain dan implementasi backend API
- Frontend Generasi UI dari API spesifikasi
- Desain dan skema database migrasi
- Unit tes generasi, integrasi, dan E2E
- Dokumentasi generasi (API, README, runbook)
- Tinjauan kode untuk kebenaran, keamanan, dan pemeliharaan

### Fokus Pengetahuan

- Python, JavaScript/Skrip Ketik, SQL
- Arsitektur Bersih, DDD, Heksagonal, CQRS
- Desain API REST dan GraphQL
- Pengindeksan database, optimasi kueri
- Strategi pemeliharaan dan perlindungan pola
- Keamanan: injeksi, autentikasi, penanganan rahasia

### Di Luar Cakupan

- Aplikasi produksi seluler asli (Swift/Kotlin)
- Pengembangan kernel/driver
- Pengembangan permainan
- Model pelatihan pipeline ML
- Penyediaan infrastruktur

### Target Benchmark

- 100 repositori nyata
- ≥90% skor kualitas kode
- ≥85% kegunaan generasi test

---

## Asisten Peneliti

**Kemampuan ID:** `research`
**Kategori:** Penelitian
**Target Kualitas:** A- (≥85) - Siap Produksi

### Cakupan

- Survei literatur dan sintesis
- Pengambilan RAG multi-sumber
- Peringkat bukti dan penemuan fosil
- Sitasi dengan asal
- Generasi laporan terstruktur
- Eksperimen desain penasehat

### Fokus Pengetahuan

- Pola penulisan ilmiah dan teknis
- Evaluasi kualitas bukti
- Format sitasi dan pelacakan asal
- Signifikansi statistik dan desain eksperimen
- penampakan penelitian penemuan

### Di Luar Cakupan

- Pencarian web langsung tanpa alat pengambilan yang disetujui
- Nasihat medis/hukum/keuangan
- Pengumpulan data primer
- Pengawasan penelitian subjek manusia
- Analisis hukum paten atau IP

### Target Benchmark

- 100 pertanyaan penelitian
- ≥85% akurasi sitasi
- ≥80% kualitas peringkat bukti

---

## Asisten DevOps

**Kemampuan ID:** `devops`
**Kategori:** DevOps
**Target Kualitas:** B+ (≥80) - Siap Produksi

### Cakupan

- Generasi Dockerfile dari persyaratan
- CI/CD saluran generasi
- Generasi mewujudkan Kubernetes
- Konfigurasi pemantauan dan peringatan
- Verifikasi penyebaran kesehatan
- Diagram infrastruktur dan dokumentasi

### Fokus Pengetahuan

- Docker, Kubernetes, Terraform
- Tindakan GitHub, GitLab CI
- Pola awan: AWS, Azure, GCP
- Observabilitas: metrik, log, jejak
- Pemindaian keamanan dan kebijakan sebagai kode

### Di Luar Cakupan

- Penyediaan akun cloud langsung
- Perintah kejadian produksi
- Operasi pusat data perangkat keras
- Integrasi penyedia cloud kustom di luar registrasi
- Biaya optimasi audit

### Target Benchmark

- 100 skenario infrastruktur
- ≥85% kebenaran pada konfigurasi yang dihasilkan
- ≥80% memperoleh verifikasi penerapan

---

## Analis Perdagangan

**Kemampuan ID:** `trading`
**Kategori:** Keuangan
**Target Kualitas:** B+ (≥80) - Sertifikasi Menunggu Keputusan

### Cakupan

- Analisis data pasar dan deteksi tren
- Penilaian risiko dan position sizing
- Analisis eksposur portofolio
- Strategi pengujian ulang
- Perbandingan multi-strategi melalui Debate Engine
- Pencatatan keputusan dan pengalaman kenangan

### Fokus Pengetahuan

- Indikator teknis dan sinyal statistik
- Deteksi rezim pasar
- Model risiko: VaR, drawdown, korelasi
- Konstruksi portofolio dan penyeimbangan kembali
- Penilaian dampak acara makro dan berita
- Psikologi perdagangan dan bias perilaku

### Di Luar Cakupan

- Eksekusi perdagangan langsung
- Integrasi akun broker
- Kepatuhan pengaturan untuk memastikan tertentu
- Optimasi pajak
- Penasihat keuangan pribadi

### Target Benchmark

- 100 skenario pasar
- Kualitas return yang disesuaikan risiko
- Konsistensi di seluruh analisis berulang

---

## Pengembangan Diri

**Kemampuan ID:** `self-development`
**Kategori:** Platform
**Target Kualitas:** A (≥90) - Siap Produksi

### Cakupan

- Analisis struktur proyek
- Deteksi kemacetan dan kode mati
- Pemfaktoran ulang usulan Generasi
- Generasi patch dan laporan tes
- Alur kerja persetujuan orkestrasi
- Pembelajaran pola lintas proyek

### Fokus Pengetahuan

- Pola arsitektur perangkat lunak
- Bau kode taksonomi
- Strategi pemeliharaan dan perlindungan
- Standar kualitas dokumentasi
- Penilaian dampak perubahan dan risiko

### Di Luar Cakupan

- Eksekusi kode otonom tanpa persetujuan
- Modifikasi langsung kontrak Core
- Penggunaan ulang engine Capability Pack lain melalui import langsung
- Deployment produksi tanpa persetujuan eksplisit pengguna

### Target Benchmark

- 10 proyek nyata
- ≥80% tingkat perbaikan penerimaan
- ≥90% memenuhi alur kerja persetujuan

---

## Templat Tugas

Setiap Capability Pack mendefinisikan template tugas standar.
Templat mewakili jalur eksekusi umum dan digunakan oleh Execution Runtime untuk merencanakan dan memparalelkan pekerjaan.

### Insinyur Jaringan

|Tugas|Subtugas|
|------|----------|
|Audit|Parse → Topologi → Keamanan → Kepatuhan → Rekomendasi → Dokumentasi|
|Optimasi|Tinjauan kinerja → hambatan identifikasi → Penyetelan konfigurasi → Validasi|
|Migrasi|Penilaian versi → Perubahan dampak → Rencana rollback → Eksekusi → Verifikasi|
|Desain|Persyaratan → Desain topologi → Desain keamanan → Dokumentasi → Rencana implementasi|
|Otomatisasi|Pembuatan perbedaan → Penilaian risiko → Pencadangan → Verifikasi → Penerapan|

### Kode Insinyur

|Tugas|Subtugas|
|------|----------|
|Tinjauan|Parsing → Arsitektur → Keamanan → Kode mati → Rekomendasi|
|Refaktorisasi|Analisis → Proposal → Patch → Tes → Validasi|
|Hasilnya|Persyaratan → Arsitektur → Backend → Frontend → Database → Pengujian → Dokumentasi|
|Arsitektur|Persyaratan → Pemodelan domain → Desain lapisan → Definisi antarmuka → Dokumentasi|
|Modernisasi|Penilaian → Analisis ketergantungan → Rencana migrasi → Eksekusi → Validasi|

### Analis Perdagangan

|Tugas|Subtugas|
|------|----------|
|Analisa|Data pasar → Indikator → Struktur → Bias → Level|
|Strategi|Ide → Aturan → Backtest → Risiko → Validasi|
|Portofolio|Kepemilikan → Korelasi → Eksposur → Penyeimbangan Kembali → Risiko|
|Mempertaruhkan|Ukuran posisi → Hentikan kerugian → Penarikan → Skenario → Mitigasi|
|Perencanaan Eksekusi|Masuk → Keluar → Ukuran posisi → Pemeriksaan risiko → Alternatif → Keputusan|

### Asisten Peneliti

|Tugas|Subtugas|
|------|----------|
|Pengambilan|Pertanyaan → Pencarian sumber → Pemfilteran → Pemeringkatan → Kutipan|
|Bukti|Sumber → Pemeriksaan kualitas → Deteksi esensi → Keyakinan → Sintesis|
|Sintesis|Sumber → Tema → Integrasi → Kesenjangan → Ringkasan → Kutipan|
|Percobaan|Hipotesis → Desain → Variabel → Metode → Validasi|
|Tinjauan Sejawat|Pengajuan → Pemeriksaan Kriteria → Analisis Kesan → Umpan Balik → Skor|

### Asisten DevOps

|Tugas|Subtugas|
|------|----------|
|Hasilnya|Persyaratan → Konfigurasi kontainer → CI/CD → IaC → Dokumentasi|
|Memeriksa|Tinjauan konfigurasi → Pemindaian keamanan → Pemeriksaan kesehatan → Validasi|
|Multi-cloud|Persyaratan → Pemilihan penyedia → Pemetaan layanan → Perkiraan biaya → Implementasi|
|Platform|Persyaratan → Desain observabilitas → Definisi kebijakan → Penyiapan GitOps → Dokumentasi|
|Ketangguhan|Persyaratan → Mode kegagalan → Rencana kekacauan → Pemantauan → Runbook|

### Pengembangan Diri

|Tugas|Subtugas|
|------|----------|
|Menganalisa|Pemindaian proyek → Analisis Struktur → Deteksi kemacetan → Analisis ketergantungan|
|Mengusulkan|Permasalahan → Penilaian dampak → Desain solusi → Evaluasi risiko → Proposal|
|Tambalan|Proposal → Pembuatan diff → Pembuatan pengujian → Validasi → Rencana rollback|
|Mempelajari|Pola → Analisis lintas proyek → Pembaruan pengetahuan → Rekomendasi|
|Meramalkan|Perubahan → Model dampak → Perkiraan risiko → Mitigasi → Keyakinan|

---

## Peta Jalan Perluasan Pengetahuan

Bagian ini mendokumentasikan perluasan pengetahuan yang direncanakan untuk setiap Capability Pack selama fase Capability Excellence. Semua penambahan terjadi di dalam Capability Pack. Inti tetap tidak berubah.

### Insinyur Jaringan

**Penambahan yang direncanakan:**
- Panduan Desain Cisco: kampus, pusat data, SD-WAN, HA
- Praktik Terbaik MikroTik: ISP edge, hotspot, IPv6, FastTrack
- Pengerasan Fortinet: FortiOS, kebijakan, VPN, ancaman perlindungan
- BGP: pemilihan jalur, pemfilteran, komunitas, pemantauan
- MPLS: penerusan, LDP, VRF, dasar-dasar rekayasa lalu lintas
- IPv6: dual-stack, SLAAC, DHCPv6, mekanisme transisi
- Zero Trust: prinsip, segmentasi mikro, ZTNA

**Referensi RFC:** RFC-0004

---

### Kode Insinyur

**Penambahan yang direncanakan:**
- Arsitektur Bersih: lapisan, aturan, ketergantungan, batasan
- DDD: konteks terbatas, agregat, peristiwa domain, anti korupsi
- SOLID: semua 5 prinsip dengan contoh Python/TypeScript
- CQRS: perpecahan perintah/query, model tulis/baca
- Sumber Acara: penyimpanan acara, pemutaran ulang, proyeksi
- Pengkodean Aman: OWASP Top 10, injeksi, autentikasi, rahasia

**Referensi RFC:** RFC-0006

---

### Asisten Peneliti

**Penambahan yang direncanakan:**
- Peringkat bukti: kualitas sumber, kebaruan, metodologi
- Deteksi membedakan: mengidentifikasi klaim yang berbeda
- Kualitas situs: kelengkapan, format, asal
- Estimasi keyakinan: kuantifikasi keseluruhan
- Pola sintesis: integrasi multi-kertas

---

### Asisten DevOps

**Penambahan yang direncanakan:**
- Multi-cloud: pola layanan AWS, Azure, GCP
- GitOps: ArgoCD, Flux, standar deklaratif
- Platform Rekayasa: IDP, pengembang portal
- Kebijakan sebagai kode: OPA, Sentinel, Kyverno
- Prinsip chaos engineering

---

### Analis Perdagangan

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

**Referensi RFC:** RFC-0005

---

### Pengembangan Diri

**Penambahan yang direncanakan:**
- Pembelajaran pola lintas proyek
- Prediksi dampak sebelum perubahan
- Bau arsitektur Taksonomi
- Pemodelan risiko perubahan
- Saran perbaikan otomatis

---

## Sistem Arsitek

**Referensi RFC:** RFC-0011

**Kemampuan ID:** `system-architect`
**Kategori:** Arsitektur
**Target Kualitas:** A (≥90)
**Target Kematangan:** Level 3 — Siap Produksi

### Cakupan

- Analisis lapisan Clean Architecture dan deteksi pelanggaran
- Evaluasi DDD (konteks terbatas, agregat, lapisan anti korupsi)
- Tinjau desain berbasis peristiwa (skema peristiwa, pola saga)
- Evaluasi CQRS
- Analisis dekomposisi layanan mikro/monolit
- Penegakan tata kelola arsitektur
- Generasi ADR untuk keputusan arsitektur
- Penegakan batas paket (siklus ketergantungan, inversi lapisan)

### Fokus Pengetahuan

- Arsitektur Bersih (Robert C. Martin)
- Desain Berbasis Domain (Eric Evans)
- Arsitektur Berbasis Peristiwa (Pola Integrasi Perusahaan)
- Pola dan anti pola CQRS
- Strategi dekomposisi layanan mikro
- Arsitekturnya berbau dan memerintah pemerintahan

### Di Luar Cakupan

- Refactoring atau implementasi kode aktual
- Desain arsitektur infrastruktur/cloud
- Pemantauan keberadaan arsitektur secara real-time
- Deployment langsung atau pemantauan Runtime
- Desain skema database (ditangani Database Engineer)
- Desain topologi jaringan (ditangani Network Engineer)

### Target Benchmark

- 100 proyek arsitektur (Python, JS/TS, Java, Go, TypeScript)
- ≥95% mengamati arsitektur kelengkapan
- ≥95% deteksi pelanggaran dependensi
- ≥90% penegakan batasan paket
- ≥95% kemampuan menjelaskan

### Konsumen

- Code Engineer — pandangan arsitektur dari kode yang dihasilkan
- Pengembangan Diri — validasi batasan paket dan evaluasi perbaikan
- Decision Intelligence — arsitektur penilaian risiko
- QA Engineer — strategi uji perencanaan berbasis arsitektur
- Asisten DevOps — meninjau layanan mikro arsitektur arsitektur

---

## Capability Pack yang Telah Diimplementasikan (Selesai)

Capability Pack berikut telah sepenuhnya diimplementasikan dan berstatus siap produksi:

### Security Engineer

**Fase:** Fase 2 — Keunggulan Kemampuan (Selesai)
**Kemampuan ID:** `security-engineer`
**Referensi RFC:** RFC-0008
**Nilai:** A- (≥85)

**Tujuan:** Kapabilitas keamanan perusahaan di seluruh OWASP Top 10, pemodelan ancaman, deteksi rahasia, analisis kerentanan, audit ketergantungan, pengerasan konfigurasi, dan pemetaan kepatuhan.

**Konsumen:** Insinyur Kode, Asisten DevOps, Insinyur Jaringan, Arsitek Sistem

### Data Engineer

**Fase:** Fase 2 — Keunggulan Kemampuan (Selesai)
**Kemampuan ID:** `data-engineer`
**Referensi RFC:** RFC-0009
**Nilai:** A- (≥85)

**Tujuan:** Manajemen siklus hidup data lengkap: ETL/ELT, pembersihan data, validasi kumpulan data, evolusi skema, rekayasa fitur, penanganan deret waktu, dan jaminan kualitas data.

**Konsumen:** Analis Perdagangan, Asisten Peneliti, Decision Intelligence, Arsitek Sistem

### Database Engineer

**Fase:** Fase 2 — Keunggulan Kemampuan (Selesai)
**Kemampuan ID:** `database-engineer`
**Referensi RFC:** RFC-0010
**Nilai:** A- (≥85)

**Tujuan:** Kapabilitas database perusahaan: skema desain, optimasi query, manajemen migrasi, perencanaan replikasi, backup/recovery, rekomendasi indeks, dan analisis kinerja.

**Konsumen:** Kode Insinyur, Data Engineer, Asisten DevOps

### Decision Intelligence

**Fase:** Fase 2 — Keunggulan Kemampuan (Selesai)
**Kemampuan ID:** `decision-intelligence`
**Referensi RFC:** RFC-0007
**Nilai:** A (≥90)

**Tujuan:** Lapisan penalaran lintas domain untuk pengambilan keputusan berdasarkan bukti: pengumpulan bukti, generasi alternatif, analisis risiko, analisis trade-off, penilaian keputusan, estimasi kepercayaan, keputusan yang dapat dijelaskan, dan riwayat keputusan.

**Konsumen:** Semua Capability Pack

### QA Engineer

**Fase:** Fase 3 — Perusahaan (Selesai)
**Kemampuan ID:** `qa-engineer`
**Referensi RFC:** RFC-0012
**Nilai:** A (≥90)

**Tujuan:** Jaminan kualitas otomatis: generasi test unit/integrasi, uji regresi otomasi, pengujian mutasi, pembuatan Golden Test untuk paket lain, pengujian generasi Benchmark, deteksi flaky test, cover analisis, dan validasi kinerja.

**Konsumen:** Semua Capability Pack

### Business Analyst

**Fase:** Fase 3 — Perusahaan (Selesai)
**Kemampuan ID:** `business-analyst`
**Referensi RFC:** RFC-0013
**Nilai:** A- (≥85)

**Tujuan:** Penerjemahan bisnis-ke-teknis: pengumpulan kebutuhan, pemodelan proses bisnis, pembuatan user story, pemodelan use case, pembuatan BRD, spesifikasi fungsional, analisis gap, analisis ROI, dan proses optimasi.

**Konsumen:** Insinyur Kode, Arsitek Sistem, Pengembangan Diri

---

## Capability Pack Masa Depan (Peta Jalan Berbasis Domain)

> **Prinsip:** ECP tidak lagi menambah Capability Pack berdasarkan profesi, tetapi berdasarkan **domain keahlian yang benar-benar reusable** oleh Capability Pack lain. Seluruh pack di bawah adalah **calon** — hanya dikembangkan setelah 13 pack inti mencapai target grade A/A- dan memenuhi aturan Governance.

### Tier A — Sangat Direkomendasikan (⭐⭐⭐⭐⭐)

Pack dengan **reusability tertinggi** dan dampak langsung terhadap kualitas pack lain.

#### Infrastructure Engineer

**Kemampuan ID (calon):** `infrastructure-engineer`
**Kategori:** Infrastruktur
**Fokus Domain:**
- Kubernetes, Docker Swarm
- Proxmox, VMware
- Ceph, HA Cluster
- Load Balancer, Storage
- Disaster Recovery

**Dipakai Oleh:** DevOps, Network, System Architect
**Catatan:** Berbeda dengan DevOps — fokus pada operasi infrastruktur fisik/virtual dan keandalan.

#### AI Engineer

**Kemampuan ID (calon):** `ai-engineer`
**Kategori:** AI/ML
**Fokus Domain:**
- RAG (Retrieval-Augmented Generation)
- Agent Design
- Prompt Optimization
- Model Router
- LoRA, Fine-tuning
- Evaluation, Guardrails

**Dipakai Oleh:** Trading, Research, Code, Self Development

#### Documentation Engineer

**Kemampuan ID (calon):** `documentation-engineer`
**Kategori:** Dokumentasi
**Fokus Domain:**
- API Documentation, OpenAPI
- SDK Docs
- ADR, RFC
- Changelog, Release Notes
- Architecture Documentation

**Dipakai Oleh:** Semua pack — menjaga dokumentasi selalu sinkron dengan kode.

### Tier B — Platform Professional (⭐⭐⭐⭐)

Melengkapi siklus pengembangan produk end-to-end.

#### Product Manager

**Kemampuan ID (calon):** `product-manager`
**Kategori:** Produk
**Fokus Domain:** Product Vision, Backlog, Roadmap, Prioritas, Sprint, Release Planning

#### UI/UX Designer

**Kemampuan ID (calon):** `ui-ux-designer`
**Kategori:** Desain
**Fokus Domain:** Wireframe, UX Review, Accessibility, Design System, Component Library

#### Full Stack Engineer

**Kemampuan ID:** `full-stack-engineer` (sudah ada di `apps/`)
**Kategori:** Pengembangan
**Fokus Domain:** Integrasi Frontend–Backend, End-to-end Feature Delivery, API Mapping, State Management, Deployment Readiness
**Catatan:** **Bukan pengganti Code Engineer** — fokus pada integrasi dan delivery end-to-end, bukan generasi kode.

### Tier C — Platform Enterprise (⭐⭐⭐)

Melayani kebutuhan enterprise: skala, keandalan, kepatuhan, dan pengetahuan terstruktur.

|Capability Pack|Fokus Domain|
|-----------------|-------------|
|**Cloud Architect**|AWS, Azure, GCP, Hybrid Cloud, Multi Cloud, Cost Optimization|
|**SRE (Site Reliability Engineer)**|Observability, Monitoring, Alerting, Incident Response, SLI, SLO, SLA|
|**Compliance Officer**|ISO 27001, NIST, PCI-DSS, GDPR, Audit, Governance|
|**Knowledge Engineer**|Ontology, Knowledge Graph, Semantic Search, Entity Resolution, Taxonomy, Knowledge Curation|

### Tier D — Vertical Industry (Kondisional)

Ditambahkan **hanya ketika ada kebutuhan proyek nyata** dan memenuhi aturan Governance: Finance Analyst, HSE Specialist, Legal Advisor, HR Specialist, Procurement Specialist, Manufacturing Engineer, Mining Engineer, Oil & Gas Engineer, Healthcare Assistant, Education Assistant.

### Target Jumlah Pack

|Tahap|Jumlah|Keterangan|
|-------|------|-----------|
|**Platform Core**|13|Fokus Capability Excellence|
|**Platform Professional**|+5|Target aktif: **18 pack**|
|**Platform Enterprise**|+5|Proposed: 23 pack|
|**Vertical Industry**|Kondisional|Berdasarkan kebutuhan proyek nyata|

> **Rekomendasi:** 15–20 Capability Pack, masing-masing benar-benar setara spesialis berpengalaman di bidangnya. Platform dengan 18 pack berkualitas tinggi lebih bernilai daripada 50 pack dengan kemampuan dasar.
