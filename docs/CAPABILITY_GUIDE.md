# Panduan kemampuan

<!-- DOCUMENT_METADATA_START -->
**Pemilik:** Tim Dokumentasi
**Pemilik Canonical:** Pimpinan Tata Kelola Dokumentasi
**Diverifikasi Terakhir:** 2026-08-04
**Versi:** 1.1.0
**Status:** Aktif
**SSOT:** Spesifikasi Capability Pack, cakupan, target Benchmark, dan tingkat kualitas
<!-- DOCUMENT_METADATA_END -->

Dokumen ini menjelaskan setiap Capability Pack resmi, termasuk scope, fokus pengetahuan, target Benchmark, dan batasan out-of-scope yang eksplisit.
Gunakan dokumen yang diketahui ini sebagai sumber kebenaran untuk apa yang diharapkan dan tidak diketahui oleh setiap Capability Pack.

---

## Status Kemampuan (2026-08-04)
**Platform Kandidat Pelepasan**

|Capability Pack|Nilai|Catatan|
|-----------------|-------|-------|
|Insinyur Jaringan|A (≥90)|Siap Produksi|
|Kode Insinyur|A+ (≥95)|Siap Produksi|Domain Expert (L4)|
|Asisten Peneliti|A+ (≥90)|Bersertifikat|
|Asisten DevOps|A+ (≥90)|Bersertifikat|
|Analis Perdagangan|A (≥90)|Bersertifikat|
|Pengembangan Diri|A+ (≥95)|Bersertifikat|
|Decision Intelligence|A+ (≥95)|Bersertifikat|
|Sistem Arsitek|A (≥90)|Siap Produksi|
|Security Engineer|A+ (≥95)|Siap Produksi|103 real cases, 95% benchmark avg score, 52 golden tests|
|Data Engineer|A (≥90)|Siap Produksi|
|Database Engineer|A- (≥85)|Siap Produksi|
|QA Engineer|A (≥90)|Siap Produksi|
|Business Analyst|A- (≥85)|Siap Produksi|
|Infrastructure Engineer|A (≥90)|Production Ready|RFC-0014|
|AI Engineer|A+ (≥95)|Production Ready|RFC-0015|
|Documentation Engineer|A (≥90)|Production Ready|RFC-0016|
|Product Manager|A- (≥85)|Production Ready|RFC-0017|
|UI/UX Designer|A- (≥85)|Production Ready|RFC-0018|
|Full Stack Engineer|A- (≥85)|Production Ready|RFC-0019|

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
**Target Kualitas:** A+ (≥95) - Siap Produksi - Domain Expert (L4)

### Cakupan

- Desain dan implementasi backend API
- Frontend Generasi UI dari API spesifikasi
- Desain dan skema database migrasi
- Unit tes generasi, integrasi, dan E2E
- Dokumentasi generasi (API, README, runbook)
- Tinjauan kode untuk kebenaran, keamanan, dan pemeliharaan
- Arsitektur Bersih, DDD, CQRS, Event Soring
- Deteksi pola arsitektur dan pelanggaran prinsip
- Analisis keamanan kode (OWASP Top 10)

### Fokus Pengetahuan

- Python, JavaScript/Skrip Ketik, SQL
- Arsitektur Bersih, DDD, Heksagonal, CQRS, Event Soring
- Desain API REST dan GraphQL
- Pengindeksan database, optimasi kueri
- Strategi pemeliharaan dan perlindungan pola
- Keamanan: injeksi, autentikasi, penanganan rahasia, OWASP Top 10
- SOLID principles, Clean Code, Refactoring patterns

### Di Luar Cakupan

- Aplikasi produksi seluler asli (Swift/Kotlin)
- Pengembangan kernel/driver
- Pengembangan permainan
- Model pelatihan pipeline ML
- Penyediaan infrastruktur

### Target Benchmark

- 100 repositori nyata
- ≥95% skor kualitas kode
- ≥90% kegunaan generasi test

---

## Asisten Peneliti

**Kemampuan ID:** `research`
**Kategori:** Penelitian
**Target Kualitas:** A+ (≥90) - Bersertifikat

### Cakupan

- Survei literatur dan sintesis
- Pengambilan RAG multi-sumber
- Peringkat bukti (kualitas sumber, kebaruan, metodologi)
- Deteksi kontradiksi
- Sitasi dengan asal dan penilaian kualitas
- Estimasi keyakinan dan kuantifikasi ketidakpastian
- Generasi laporan terstruktur
- Eksperimen desain penasehat

### Fokus Pengetahuan

- Pola penulisan ilmiah dan teknis
- Evaluasi kualitas bukti
- Peringkat bukti: kualitas sumber, kebaruan, metodologi
- Deteksi kontradiksi: konflik metodologis, hasil, interpretasi
- Format sitasi dan pelacakan asal
- Estimasi keyakinan dan ketidakpastian
- Sintesis multi-paper
- Signifikansi statistik dan desain eksperimen

### Di Luar Cakupan

- Pencarian web langsung tanpa alat pengambilan yang disetujui
- Nasihat medis/hukum/keuangan
- Pengumpulan data primer
- Pengawasan penelitian subjek manusia
- Analisis hukum paten atau IP

### Target Benchmark

- 100+ pertanyaan penelitian
- ≥90% akurasi sitasi
- ≥90% kualitas peringkat bukti
- 6 dimensi benchmark: akurasi, kelengkapan, penjelasan, keselamatan, efisiensi, konsistensi

---

## Asisten DevOps

**Kemampuan ID:** `devops`
**Kategori:** DevOps
**Target Kualitas:** A+ (≥90) - Bersertifikat

### Cakupan

- Generasi Dockerfile dari persyaratan
- CI/CD saluran generasi
- Generasi mewujudkan Kubernetes
- Konfigurasi pemantauan dan peringatan
- Verifikasi penyebaran kesehatan
- Diagram infrastruktur dan dokumentasi
- Deteksi masalah DevOps dan rekomendasi perbaikan
- Penilaian risiko kuantitatif
- GitOps, Kebijakan sebagai kode, Chaos engineering

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
- ≥90% kebenaran pada konfigurasi yang dihasilkan
- ≥90% memperoleh verifikasi penerapan
- Deteksi masalah: 10 tipe masalah DevOps
- Rekomendasi perbaikan: cakupan penuh

---

## Analis Perdagangan

**Kemampuan ID:** `trading`
**Kategori:** Keuangan
**Target Kualitas:** A (≥90) - Bersertifikat
**Target Kematangan:** Level 4 — Pakar Domain

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
**Target Kualitas:** A+ (≥95) - Bersertifikat
**Target Kematangan:** Level 4 — Pakar Domain

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

### Infrastructure Engineer

|Tugas|Subtugas|
|------|----------|
|Provisioning|Persyaratan → Pemilihan platform → Konfigurasi → Validasi → Dokumentasi|
|Konfigurasi|Persyaratan → Desain infrastruktur → Konfigurasi → Keamanan → Verifikasi|
|Monitoring|Persyaratan → Setup monitoring → Alert → Dashboard → Runbook|
|DR|Persyaratan → Analisis RPO/RTO → Desain DR → Implementasi → Uji coba|
|Scaling|Analisis beban → Perencanaan scaling → Implementasi → Validasi|

### AI Engineer

|Tugas|Subtugas|
|------|----------|
|RAG|Persyaratan → Chunking strategy → Embedding → Vector DB → Evaluasi|
|Agent|Persyaratan → Desain agent → Tool definition → Orchestration → Testing|
|Fine-tuning|Dataset preparation → Model selection → Training → Evaluation → Deployment|
|Evaluasi|Persyaratan → Benchmark selection → Test cases → Metrics → Report|
|Guardrails|Persyaratan → Policy definition → Implementation → Testing → Monitoring|

### Documentation Engineer

|Tugas|Subtugas|
|------|----------|
|API Docs|Persyaratan → OpenAPI spec → Generasi → Review → Publikasi|
|ADR/RFC|Masalah → Opsi → Keputusan → Dokumentasi → Review|
|Release Notes|Perubahan → Ringkasan → Dokumentasi → Review → Publikasi|
|Architecture Docs|Persyaratan → Diagram → Deskripsi → Review → Publikasi|
|Audit|Pemindaian dokumen → Kesenjangan → Rekomendasi → Update|

### Product Manager

|Tugas|Subtugas|
|------|----------|
|Discovery|Masalah → Riset → Konsep → Validasi → Prioritas|
|Roadmap|Visi → Tujuan → Inisiatif → Timeline → Komunikasi|
|Sprint|Backlog → Planning → Tracking → Review → Retrospective|
|Release|Persyaratan → Planning → Coordination → Deployment → Review|
|Analytics|Metrics → Data → Insight → Action → Measurement|

### UI/UX Designer

|Tugas|Subtugas|
|------|----------|
|Wireframe|Persyaratan → Sketches → Wireframe → Review → Iterasi|
|Prototype|Wireframe → High-fidelity → Interaksi → Testing → Refinement|
|Design System|Audit → Token → Component → Dokumentasi → Adoption|
|Review|Heuristic evaluation → Accessibility → Usability → Report → Action|
|Research|Planning → Recruitment → Session → Synthesis → Recommendation|

### Full Stack Engineer

|Tugas|Subtugas|
|------|----------|
|Feature|Requirement → API design → Backend → Frontend → Integration → Test|
|Integration|API mapping → Contract → Implementation → E2E test → Deployment|
|Migration|Assessment → Planning → Implementation → Validation → Rollback|
|Optimization|Profiling → Bottleneck → Fix → Measure → Validate|
|Deployment|Build → Config → Deploy → Smoke test → Monitoring|

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

### Infrastructure Engineer

**Penambahan yang direncanakan:**
- Kubernetes: operator, service mesh, policy enforcement
- Proxmox: clustering, Ceph integration, backup
- VMware: vSphere advanced, vSAN, NSX
- Ceph: CRUSH map, pool design, erasure coding
- Disaster Recovery: site failover, data replication strategies
- Zero Trust: micro-segmentation, identity-based access

**Referensi RFC:** RFC-0014

---

### AI Engineer

**Penambahan yang direncanakan:**
- RAG: advanced chunking, hybrid search, reranking
- Agent: multi-agent orchestration, memory systems
- LLM: fine-tuning strategies, quantization, deployment
- Evaluation: automated benchmarks, LLM-as-judge
- Guardrails: policy enforcement, PII detection, toxicity filtering
- Prompt engineering: few-shot, CoT, structured output

**Referensi RFC:** RFC-0015

---

### Documentation Engineer

**Penambahan yang direncanakan:**
- API Documentation: OpenAPI 3.1, async API, GraphQL schema
- SDK Docs: multi-language, interactive examples
- ADR/RFC: template standardization, tooling integration
- Architecture Documentation: C4 model, system diagrams
- Documentation testing: link validation, freshness checks
- Automated doc generation from code comments

**Referensi RFC:** RFC-0016

---

### Product Manager

**Penambahan yang direncanakan:**
- Product Strategy: market analysis, competitive intelligence
- Roadmap: OKR alignment, stakeholder management
- Agile: Scrum, Kanban, hybrid methodologies
- Analytics: metrics definition, A/B testing, funnel analysis
- Discovery: user research, MVP definition, validation
- Release: coordination, communication, feedback loops

**Referensi RFC:** RFC-0017

---

### UI/UX Designer

**Penambahan yang direncanakan:**
- UX Research: usability testing, user interviews, heatmaps
- Design System: token architecture, component library
- Accessibility: WCAG 2.2, ARIA patterns, screen reader testing
- Responsive Design: mobile-first, adaptive layouts
- Prototyping: interactive mockups, micro-interactions
- Visual Design: typography, color theory, brand systems

**Referensi RFC:** RFC-0018

---

### Full Stack Engineer

**Penambahan yang direncanakan:**
- Full-stack Frameworks: Next.js, Nuxt, Remix patterns
- API Design: REST, GraphQL, tRPC, contract testing
- State Management: client-side, server-side, caching
- Deployment: containerization, CI/CD, cloud platforms
- Performance: bundle optimization, lazy loading, caching
- Testing: E2E, integration, contract testing

**Referensi RFC:** RFC-0019

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
**Nilai:** A (≥90)

**Tujuan:** Kapabilitas keamanan perusahaan di seluruh OWASP Top 10, pemodelan ancaman, deteksi rahasia, analisis kerentanan, audit ketergantungan, pengerasan konfigurasi, dan pemetaan kepatuhan.

**Konsumen:** Insinyur Kode, Asisten DevOps, Insinyur Jaringan, Arsitek Sistem

### Data Engineer

**Fase:** Fase 2 — Keunggulan Kemampuan (Selesai)
**Kemampuan ID:** `data-engineer`
**Referensi RFC:** RFC-0009
**Nilai:** A (≥90)

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
**Nilai:** A+ (≥95)

**Tujuan:** Lapisan penalaran lintas domain untuk pengambilan keputusan berdasarkan bukti: pengumpulan bukti, generasi alternatif, analisis risiko, analisis trade-off, simulasi outcome, debat multi-strategi, penilaian keputusan, estimasi kepercayaan, keputusan yang dapat dijelaskan, dan riwayat keputusan.

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

## Infrastructure Engineer

**Kemampuan ID:** `infrastructure-engineer`
**Kategori:** Infrastruktur
**Target Kualitas:** A (≥90)
**Target Kematangan:** Level 3 — Siap Produksi

### Cakupan

- Manajemen Kubernetes dan Docker Swarm
- Virtualisasi Proxmox dan VMware
- Penyimpanan terdistribusi Ceph dan HA Cluster
- Konfigurasi Load Balancer dan Storage
- Perencanaan dan implementasi Disaster Recovery
- Orkestra infrastruktur fisik dan virtual
- Keandalan sistem dan ketersediaan tinggi

### Fokus Pengetahuan

- Kubernetes: arsitektur, scheduler, networking, storage
- Docker Swarm: layanan, jaringan
- Proxmox VE: cluster, VM, kontainer, penyimpanan
- VMware vSphere: ESXi, vCenter, vMotion, DRS
- Ceph: RADOS, OSD, MDS, pool, crush map
- Load Balancer: HAProxy, Nginx, L4/L7
- Disaster Recovery: RPO, RTO, replikasi, backup

### Di Luar Cakupan

- Penyediaan akun cloud langsung
- Operasi pusat data perangkat keras
- Integrasi penyedia cloud kustom di luar registrasi
- Biaya optimasi audit
- Konfigurasi perangkat jaringan (ditangani Network Engineer)

### Target Benchmark

- 50 infrastruktur lingkungan
- ≥90% akurasi konfigurasi yang dihasilkan
- ≥90% kelangsungan hidup DR drill
- ≥90% ketersediaan sistem

### Konsumen

- Asisten DevOps — panduan arsitektur infrastruktur
- Insinyur Jaringan — integrasi topologi jaringan
- Arsitek Sistem — evaluasi arsitektur infrastruktur

---

## AI Engineer

**Kemampuan ID:** `ai-engineer`
**Kategori:** AI/ML
**Target Kualitas:** A+ (≥95)
**Target Kematangan:** Level 3 — Siap Produksi

### Cakupan

- Desain dan implementasi RAG (Retrieval-Augmented Generation)
- Perancangan Agent dan orchestration
- Optimasi prompt dan model router
- Fine-tuning dan LoRA adapter
- Evaluasi model dan guardrails
- Integrasi LLM ke dalam alur kerja aplikasi
- Deteksi dan mitigasi bias model

### Fokus Pengetahuan

- Arsitektur LLM dan API (OpenAI, Anthropic, Ollama)
- RAG: chunking, embedding, vector DB, reranking
- Agent: ReAct, tool use, memory, multi-agent
- Prompt engineering: CoT, few-shot, structured output
- Fine-tuning: LoRA, QLoRA, dataset preparation
- Evaluasi: benchmark, automated eval, LLM-as-judge
- Guardrails: input/output filtering, toxicity, PII redaction

### Di Luar Cakupan

- Pelatihan model dari awal (training from scratch)
- Infrastruktur GPU cluster besar
- Riset model arsitektur baru
- Pengumpulan data primer untuk pelatihan

### Target Benchmark

- 50 sistem AI
- ≥95% akurasi evaluasi
- ≥90% guardrails efektivitas
- ≥90% integrasi berhasil

### Konsumen

- Asisten Peneliti — augmentasi penelitian dengan AI
- Analis Perdagangan — analisis pasar dengan AI
- Kode Insinyur — integrasi AI ke dalam aplikasi
- Pengembangan Diri — pembelajaran pola berbasis AI

---

## Documentation Engineer

**Kemampuan ID:** `documentation-engineer`
**Kategori:** Dokumentasi
**Target Kualitas:** A (≥90)
**Target Kematangan:** Level 3 — Siap Produksi

### Cakupan

- Dokumentasi API dan OpenAPI specification
- Dokumentasi SDK dan library
- ADR (Architecture Decision Record) dan RFC
- Changelog dan release notes
- Dokumentasi arsitektur sistem
- Generasi dokumentasi dari kode
- Standarisasi dokumentasi lintas proyek

### Fokus Pengetahuan

- OpenAPI/Swagger: spesifikasi, validasi, tooling
- Dokumentasi sebagai kode: MkDocs, Sphinx, Docusaurus
- ADR dan RFC: format, standar, tooling
- Pengembangan dokumentasi teknikal
- Aksesibilitas dokumentasi
- Generasi dokumentasi otomatis

### Di Luar Cakupan

- Penulisan konten marketing
- Dokumentasi pengguna akhir non-teknis
- Pelatihan penggunaan produk
- Manajemen konten website

### Target Benchmark

- 100 dokumen
- ≥90% kelengkapan dokumentasi
- ≥90% kesesuaian dengan kode
- ≥90% kepuasan pembaca

### Konsumen

- Semua Capability Pack — menjaga dokumentasi selalu sinkron dengan kode

---

## Product Manager

**Kemampuan ID:** `product-manager`
**Kategori:** Produk
**Target Kualitas:** A- (≥85)
**Target Kematangan:** Level 3 — Siap Produksi

### Cakupan

- Product vision dan strategy
- Backlog management dan prioritas
- Roadmap planning
- Sprint planning dan tracking
- Release planning
- Stakeholder communication
- Analisis pasar dan kompetitor
- Metrics dan OKR definition

### Fokus Pengetahuan

- Agile dan Scrum methodologies
- Product discovery dan validation
- User story mapping
- OKR dan KPI definition
- Market analysis dan competitive intelligence
- Stakeholder management
- Growth dan engagement metrics

### Di Luar Cakupan

- Eksekusi teknis pengembangan
- Desain UI/UX detail
- Operasi penjualan dan marketing
- Manajemen keuangan perusahaan

### Target Benchmark

- 20 produk
- ≥85% kesuksesan roadmap
- ≥85% kepuasan stakeholder
- ≥90% prediksi tepat delivery

### Konsumen

- Kode Insinyur — klarifikasi requirement
- Arsitek Sistem — align arsitektur dengan visi produk
- QA Engineer — define quality criteria
- UI/UX Designer — align design dengan product vision

---

## UI/UX Designer

**Kemampuan ID:** `ui-ux-designer`
**Kategori:** Desain
**Target Kualitas:** A- (≥85)
**Target Kematangan:** Level 3 — Siap Produksi

### Cakupan

- Wireframe dan prototype
- UX review dan usability testing
- Accessibility compliance
- Design system dan component library
- Visual design dan brand consistency
- Responsive design
- Interaction design

### Fokus Pengetahuan

- Prinsip UX: Nielsen, Norman, Gestalt
- Aksesibilitas: WCAG 2.1, ARIA, screen reader
- Design system: token, component, pattern library
- Tools: Figma, Sketch, Adobe XD
- Responsive design: mobile-first, breakpoints
- Usability testing: A/B testing, heatmaps, user research

### Di Luar Cakupan

- Pengembangan frontend kode
- Ilustrasi dan graphic design tingkat lanjut
- Motion design kompleks
- Brand identity creation

### Target Benchmark

- 30 proyek desain
- ≥85% aksesibilitas skor
- ≥90% konsistensi design system
- ≥85% kepuasan pengguna

### Konsumen

- Kode Insinyur — panduan implementasi UI
- Product Manager — align desain dengan visi produk
- Full Stack Engineer — end-to-end feature design

---

## Full Stack Engineer

**Kemampuan ID:** `full-stack-engineer`
**Kategori:** Pengembangan
**Target Kualitas:** A- (≥85)
**Target Kematangan:** Level 3 — Siap Produksi

### Cakupan

- Integrasi frontend-backend
- End-to-end feature delivery
- API mapping dan contract design
- State management
- Deployment readiness
- Cross-cutting concerns: auth, logging, error handling
- Performance optimization lintas lapisan

### Fokus Pengetahuan

- Full-stack frameworks: Next.js, Nuxt, Remix
- API design: REST, GraphQL, tRPC
- State management: Redux, Zustand, Jotai
- Authentication: OAuth, JWT, SSO
- Deployment: Vercel, Netlify, Docker
- Testing: E2E, integration, contract testing

### Di Luar Cakupan

- Arsitektur sistem kompleks (ditangani System Architect)
- Generasi kode dari nol (ditangani Code Engineer)
- Optimasi database query kompleks (ditangani Database Engineer)
- Keamanan aplikasi enterprise (ditangani Security Engineer)

### Target Benchmark

- 40 proyek
- ≥85% feature delivery success
- ≥90% integrasi berhasil
- ≥85% deployment readiness

### Konsumen

- Kode Insinyur — integrasi komponen menjadi fitur lengkap
- Product Manager — delivery fitur sesuai requirement
- QA Engineer — integrasi testing lintas lapisan

---

## Capability Pack Masa Depan (Peta Jalan Berbasis Domain)

> **Prinsip:** ECP tidak lagi menambah Capability Pack berdasarkan profesi, tetapi berdasarkan **domain keahlian yang benar-benar reusable** oleh Capability Pack lain. Tier A dan Tier B packs telah **diimplementasikan** dan aktif. Tier C dan Tier D packs tetap sebagai **calon** untuk pengembangan masa depan.

### Tier A — Active (⭐⭐⭐⭐⭐)

Pack dengan **reusability tertinggi** dan dampak langsung terhadap kualitas pack lain. Pack ini telah **diimplementasikan** dan siap produksi.

#### Infrastructure Engineer

**Kemampuan ID (aktif):** `infrastructure-engineer`
**Kategori:** Infrastruktur
**Fokus Domain:**
- Kubernetes, Docker Swarm
- Proxmox, VMware
- Ceph, HA Cluster
- Load Balancer, Storage
- Disaster Recovery

**Dipakai Oleh:** DevOps, Network, System Architect
**Catatan:** Berbeda dengan DevOps — fokus pada operasi infrastruktur fisik/virtual dan keandalan.
**Status:** Production Ready — RFC-0014

#### AI Engineer

**Kemampuan ID (aktif):** `ai-engineer`
**Kategori:** AI/ML
**Fokus Domain:**
- RAG (Retrieval-Augmented Generation)
- Agent Design
- Prompt Optimization
- Model Router
- LoRA, Fine-tuning
- Evaluation, Guardrails

**Dipakai Oleh:** Trading, Research, Code, Self Development
**Status:** Production Ready — RFC-0015

#### Documentation Engineer

**Kemampuan ID (aktif):** `documentation-engineer`
**Kategori:** Dokumentasi
**Fokus Domain:**
- API Documentation, OpenAPI
- SDK Docs
- ADR, RFC
- Changelog, Release Notes
- Architecture Documentation

**Dipakai Oleh:** Semua pack — menjaga dokumentasi selalu sinkron dengan kode.
**Status:** Production Ready — RFC-0016

### Tier B — Active (⭐⭐⭐⭐)

Melengkapi siklus pengembangan produk end-to-end. Pack ini telah **diimplementasikan** dan siap produksi.

#### Product Manager

**Kemampuan ID (aktif):** `product-manager`
**Kategori:** Produk
**Fokus Domain:** Product Vision, Backlog, Roadmap, Prioritas, Sprint, Release Planning
**Status:** Production Ready — RFC-0017

#### UI/UX Designer

**Kemampuan ID (aktif):** `ui-ux-designer`
**Kategori:** Desain
**Fokus Domain:** Wireframe, UX Review, Accessibility, Design System, Component Library
**Status:** Production Ready — RFC-0018

#### Full Stack Engineer

**Kemampuan ID (aktif):** `full-stack-engineer` (sudah ada di `apps/`)
**Kategori:** Pengembangan
**Fokus Domain:** Integrasi Frontend–Backend, End-to-end Feature Delivery, API Mapping, State Management, Deployment Readiness
**Catatan:** **Bukan pengganti Code Engineer** — fokus pada integrasi dan delivery end-to-end, bukan generasi kode.
**Status:** Production Ready — RFC-0019

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
|**Platform Professional**|+6|Target aktif: **19 pack**|
|**Platform Enterprise**|+4|Proposed: 23 pack|
|**Vertical Industry**|Kondisional|Berdasarkan kebutuhan proyek nyata|

> **Rekomendasi:** 15–20 Capability Pack, masing-masing benar-benar setara spesialis berpengalaman di bidangnya. Platform dengan 19 pack berkualitas tinggi lebih bernilai daripada 50 pack dengan kemampuan dasar.
