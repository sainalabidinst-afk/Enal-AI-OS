<!-- DOCUMENT_METADATA_START -->
**Pemilik:** Tim Dokumentasi
**Pemilik Canonical:** Pimpinan Tata Kelola Dokumentasi
**Diverifikasi Terakhir:** 02-08-2026
**Versi:** 1.0.0
**Status:** Aktif
**SSOT:** Linimasa rilis, tonggak sejarah, dan jadwal pengiriman
<!-- DOCUMENT_METADATA_END -->

# Peta Jalan ECP

**Status:** Aktif
**Pemilik:** Chief Product Officer
**Tujuan:** Mendefinisikan linimasa, target rilis, dan visi jangka panjang ECP. Semua terkait konten jadwal dan target versi berada di sini.

---

## Kunjungi Bintang Utara

> **Platform adalah penggerak. Tujuan akhirnya adalah AI Trading yang membuat keputusan investasi cerdas secara otonom.**

ECP dibangun sebagai platform eksekusi AI yang stabil, tetapi **Trading Analyst** adalah Capability Pack utama yang menjadi tujuan akhir. Semua kemampuan lain (Network, Code, Research, DevOps, Self Development, dan yang akan datang) adalah penggerak yang memperkuat ekosistem menuju visi tersebut.

---

## Fase Pengembangan

### Fase 1 — Keunggulan Kemampuan (Sekarang — 13 Paket)

**Fokus:** Menaikkan kualitas semua paket menjadi A/A-.

|Capability Pack|Kelas Saat Ini|Nilai Sasaran|Target Kematangan|
|-----------------|----------------|--------------|-----------------|
|Insinyur Jaringan|A|SEBUAH+|Pakar Domain (L4)|
|Insinyur Kode|A-|A|Pakar Domain (L4)|
|Asisten Peneliti|A-|A|Pakar Domain (L4)|
|Asisten DevOps|B+|A-|Pakar Domain (L4)|
|Analis Perdagangan|B+ (Sertifikasi Menunggu Keputusan)|A-|Siap Produksi (L3)|
|Pengembangan Diri|A|A|Pakar Domain (L4)|
|Decision Intelligence|SEBUAH (91,25%)|A|Pakar Domain (L4)|
|Arsitek Sistem|SEBUAH (97,50%)|A|Pakar Domain (L4)|
|Security Engineer|A-|A-|Siap Produksi (L3)|
|Data Engineer|A-|A-|Siap Produksi (L3)|
|Database Engineer|A-|A-|Siap Produksi (L3)|
|QA Engineer|A|A|Pakar Domain (L4)|
|Business Analyst|A-|A-|Siap Produksi (L3)|

**Hasil Utama:**
- 1.000+ kasus nyata di seluruh paket
- Semua paket berada di grade A- atau lebih tinggi
- Sertifikasi Trading Analyst selesai
- Dasbor Benchmark untuk semua 13 paket

---

### Fase 2 — Decision Intelligence + Keamanan + Data (+3 Paket)

Setelah 13 pack mencapai A-/A, tambahkan 3 Capability Pack baru:

|Prioritas|Capability Pack|Fungsi|Paket Tanggungan|
|-----------|-----------------|--------|-----------------|
| ⭐⭐⭐⭐⭐ |**Decision Intelligence**|"Otak" lintas domain — bukti → penalaran → simulasi → perdebatan → risiko → keputusan → penjelasan|Perdagangan, Jaringan, Kode, semua paket|
| ⭐⭐⭐⭐ |**Security Engineer**|OWASP, audit keamanan, uji penetrasi, pemodelan ancaman, deteksi rahasia, penilaian kerentanan|Kode, DevOps, Jaringan|
| ⭐⭐⭐⭐ |**Data Engineer**|ETL, pembersihan data, pembuatan versi kumpulan data, rekayasa fitur, kualitas data, saluran deret waktu|Perdagangan, Riset, DevOps|

---

### Fase 3 — Perusahaan (+4 Paket)

Setelah 13 pack stabil, tambahkan 4 Capability Pack untuk melayani kebutuhan perusahaan:

|Prioritas|Capability Pack|Fungsi|
|-----------|-----------------|--------|
|4|**Database Engineer**|Optimasi SQL, desain skema, migrasi, rekomendasi indeks, analisis kinerja|
|5|**QA Engineer**|Uji generasi, regresi, uji mutasi, pembangun Golden Test, generator Benchmark|
|6|**Business Analyst**|Persyaratan analisis, cerita pengguna, BRD, use case, alur kerja|

> **Catatan:** **System Architect** (RFC-0011) telah diimplementasikan dan menjadi Capability Pack resmi — lihat `docs/CAPABILITY_STRATEGY.md` §5.8.

---

### Prinsip Perluasan Berbasis Domain

> **ECP tidak lagi menambah Capability Pack berdasarkan profesi, tetapi berdasarkan keahlian domain yang benar-benar dapat digunakan kembali oleh Capability Pack lain.**

Setiap calon Capability Pack baru harus:
1. **Dapat digunakan kembali** — dipakai minimal 2 Capability Pack konsumen
2. **Domain Expertise, bukan Role** — mewakili keahlian yang dapat dieksekusi, bukan jabatan
3. **Tidak memaksa perubahan Core** — seluruh penambahan terjadi di dalam Capability Pack
4. **Lulus Governance** — kasus penggunaan lintas sistem, Benchmark, Golden Test
5. **Kebutuhan nyata** — ditambahkan saat ada kebutuhan proyek aktual

### Fase 4 — Platform Profesional (+5 Paket)

Menambahkan paket dengan **reusability tertinggi** untuk produktivitas dan kualitas waktu:

|Tingkat|Capability Pack|Fokus Domain|Paket Tanggungan|
|------|-----------------|-------------|-----------------|
|Sebuah ⭐⭐⭐⭐⭐|**Insinyur Infrastruktur**|Kubernetes, Docker Swarm, Proxmox, VMware, Ceph, HA Cluster, Load Balancer, Penyimpanan, Pemulihan Bencana|DevOps, Jaringan, Arsitek Sistem|
|Sebuah ⭐⭐⭐⭐⭐|**Insinyur AI**|RAG, Desain Agen, Optimasi Cepat, Model Router, LoRA, Penyempurnaan, Evaluasi, Pagar Pembatas|Perdagangan, Penelitian, Kode, Pengembangan Diri|
|Sebuah ⭐⭐⭐⭐⭐|**Insinyur Dokumentasi**|API Dokumentasi, OpenAPI, SDK Dokumen, ADR, RFC, Changelog, Catatan Rilis, Dokumentasi Arsitektur|Semua paket|
|B ⭐⭐⭐⭐|**Manajer Produk**|Visi Produk, Backlog, Roadmap, Prioritas, Sprint, Perencanaan Rilis|Semua paket|
|B ⭐⭐⭐⭐|**Desainer UI/UX**|Wireframe, Review UX, Aksesibilitas, Sistem Desain, Pustaka Komponen|Semua paket|

### Fase 5 — Platform Perusahaan (+5 Paket)

Setelah Platform Professional stabil, tambahkan paket untuk kebutuhan perusahaan:

|Tingkat|Capability Pack|Fokus Domain|
|------|-----------------|-------------|
|C ⭐⭐⭐|**Arsitek Cloud**|AWS, Azure, GCP, Hybrid Cloud, Multi Cloud, Optimasi Biaya|
|C ⭐⭐⭐|**SRE (Insinyur Keandalan Situs)**|Observabilitas, Pemantauan, Peringatan, Respons Insiden, SLI, SLO, SLA|
|C ⭐⭐⭐|**Petugas Kepatuhan**|ISO 27001, NIST, PCI-DSS, GDPR, Audit, Tata Kelola|
|C ⭐⭐⭐|**Insinyur Pengetahuan**|Ontologi, Knowledge Graph, Pencarian Semantik, Resolusi Entitas, Taksonomi, Kurasi Pengetahuan|
|B/C ⭐⭐⭐⭐|**Insinyur Tumpukan Penuh**|Integrasi Frontend–Backend, Pengiriman Fitur End-to-end, Pemetaan API, Pengelolaan Status, Kesiapan Penerapan|

> **Catatan:** Full Stack Engineer **bukan pengganti Code Engineer** — fokusnya integrasi frontend–backend dan pengiriman end-to-end. Jika sudah diimplementasikan di Fase 4 (Tier B), Fase 5 cukup berisi 4 pack baru.

### Fase 6 — Industri Vertikal (Kondisional)

Ditambahkan **hanya ketika ada kebutuhan proyek nyata** dan memenuhi aturan Governance. Tidak disarankan menambahkan semuanya sekaligus.

- Analis Keuangan, Spesialis HSE, Penasihat Hukum, Spesialis SDM, Spesialis Pengadaan
- Insinyur Manufaktur, Insinyur Pertambangan, Insinyur Minyak & Gas, Asisten Kesehatan, Asisten Pendidikan

### Paket Jumlah Target

|Tahap|Jumlah Paket|Keterangan|
|-------|------------|------------|
|**Inti Platform**|13|Fokus Kapabilitas Keunggulan|
|**Platform Profesional**|+5|Target aktif: **18 paket**|
|**Perusahaan Platform**|+5|Diusulkan: 23 bungkus|
|**Industri Vertikal**|Kondisional|Berdasarkan kebutuhan proyek nyata|

> **Rekomendasi:** 15–20 Capability Pack, tetapi masing-masing benar-benar setara dengan spesialis berpengalaman. Platform dengan 18 paket berkualitas tinggi jauh lebih bernilai daripada 50 paket dengan kemampuan dasar.

---

## Linimasa Rilis

|Rilis|Target Tanggal|Fokus|
|---------|-------------|-------|
|v1.0.0-pengembangan|Q3 2026|Platform lengkap, Architecture Governance aktif|
|v1.0.0|Q4 2026|Pratinjau Pengembang: 13 paket bersertifikat, dokumentasi, SDK, Studio|
|v1.1.0|Q1 2027|Keunggulan Kapabilitas: semua paket A-/A, Sertifikasi Trading|
|v1.2.0|Q2 2027|Decision Intelligence + Security Engineer + Data Engineer|
|v1.3.0|Q3 2027|Perusahaan: Database Engineer + QA Engineer|
|v1.4.0|Q4 2027|Perusahaan: Business Analyst|
|v2.0.0|2028|Profesional Platform: Insinyur Infrastruktur, Insinyur AI, Insinyur Dokumentasi, Manajer Produk, Desainer UI/UX|
|v2.1.0|2029|Perusahaan Platform: Arsitek Cloud, SRE, Pejabat Kepatuhan, Insinyur Pengetahuan, Insinyur Full Stack|

---

## Kemampuan Peta Jalan 12 Bulan

### Q1 — Perdagangan Sertifikasi & Pratinjau Pengembang
- Menyelesaikan Sertifikasi Trading Analyst
- Pratinjau Pengembang Rilis (v1.0.0)
- 500 kasus nyata di seluruh Capability Pack
- Semua paket terdokumentasi dan di-Benchmark

### Q2 — Keunggulan Kemampuan
- Jaringan A+
- Kode A
- Perdagangan A-
- Penelitian A
- DevOps A-
- 1.000 kasus nyata
- Semua paket naik satu tingkat melalui pengetahuan dan kerja Benchmark dunia nyata

### Q3 — Decision Intelligence
- RFC dan prototipe untuk Decision Intelligence
- RFC Security Engineer
- RFC Data Engineer
- Melanjutkan peningkatan kualitas pada semua 13 paket

### Q4 — Perusahaan Fondasi
- Decision Intelligence Stabil
- Security Engineer Stabil
- Data Engineer Stabil
- 1.500+ kasus nyata

---

## Peta Jalan Bebas 5 Tahun

### Fase 0 — Arsitektur Lengkap ✅
- Inti, Kontrak Kemampuan, Pekerja, Percakapan, Tata Kelola, ADR, Kontrak UX
- Biaya: Gratis

### Fase 1 — Keunggulan Kemampuan (0–12 bulan)
- 13 paket yang ada: Jaringan, Kode, Penelitian, DevOps, Perdagangan, Pengembangan Diri, Decision Intelligence, Arsitek Sistem, Security Engineer, Data Engineer, Database Engineer, QA Engineer, Business Analyst
- Target: semua paket grade A-/A, 1.000 kasus nyata
- Inti tetap bertahan

### Fase 2 — Decision Intelligence (12–18 bulan)
- Kemas Decision Intelligence: bukti → penalaran → simulasi → debat → risiko → keputusan → penjelasan
- Digunakan oleh Trading, Network, dan pack lain sebagai "otak" lintas domain
- Security Engineer + Data Engineer

### Fase 3 — Paket Perusahaan (18–24 bulan)
- Database Engineer, QA Engineer, Business Analyst
- Target: Total 9 paket, 3.000+ kasus nyata

### Fase 4 — Tumpukan AI Lokal (24–30 bulan)
- Ollama + Qwen/DeepSeek/Llama/Gemma
- Model Router memilih model open-source terbaik per kemampuan
- Semua inferensi lokal atau free-tier
- Biaya: Gratis

### Fase 5 — Platform Profesional (30–36 bulan)
- Insinyur Infrastruktur, Insinyur AI, Insinyur Dokumentasi, Manajer Produk, Desainer UI/UX
- Target: Total 18 paket, 5.000+ kasus nyata

### Fase 5b — Platform Enterprise (36–42 bulan, kondisional)
- Arsitek Cloud, SRE, Pejabat Kepatuhan, Insinyur Pengetahuan, Insinyur Full Stack
- Target: total 23 paket (diusulkan), 7.000+ kasus nyata

### Fase 6 — Model Enal (36–48 bulan)
- EnalCoder: Qwen/DeepSeek yang disempurnakan untuk coding
- EnalNetwork: Llama yang disempurnakan pada konfigurasi jaringan
- EnalTrading: Qwen yang menyempurnakan pola perdagangan
- Semua melalui LoRA, tanpa pretraining
- Biaya: Rendah (single GPU atau cloud sesekali)

### Fase 7 — Pembelajaran Berkelanjutan (Berlangsung)
- Kasus nyata → Review → Pembaruan → Benchmark
- Siklus peningkatan harian

### Fase 8 — Model Fondasi (48–60 bulan, kondisional)
- Hanya jika pengguna >100k, pendapatan stabil, GPU tersedia
- EnalLM: dibuat khusus untuk eksekusi ECP
- Bukan klon GPT, tetapi model yang dioptimalkan untuk eksekusi

---

## Yang Tidak Akan Menjadi Capability Pack

Berikut adalah komponen yang **tidak akan dijadikan Capability Pack** sendiri. Mereka akan diposisikan sebagai **Plugin**, **layanan**, atau **platform infrastruktur**:

- Otentikasi / Otorisasi
- PostgreSQL / Redis / MinIO / Kafka
- Plugin Pasar
- Konektor Pialang / Konektor Pertukaran
- Infrastruktur murni (penyeimbang beban, DNS, wadah Runtime)

Keputusan ini menjaga ECP tetap fokus pada **keahlian domain** dan mencegah perluasan platform ke infrastruktur yang sudah ada solusinya.

---

## Model Strategi: Kemandirian Progresif

**Tahun 1:** 100% model eksternal (Claude, GPT, Gemini, Qwen, DeepSeek)
**Tahun 2:** 80% eksternal, 20% model Enal
**Tahun 3:** 50% eksternal, 50% model Enal
**Tahun 5:** 90% model Enal

Model Router membuat hal ini transparan bagi pengguna dan Capability Pack.
Semua Capability Pack tetap berfungsi tanpa perubahan apa pun terkait sumber model.

---

## Rencana Perluasan Pengetahuan

Semua penambahan pengetahuan yang direncanakan dilacak melalui RFC dan diimplementasikan hanya di dalam Capability Pack. Inti tetap tidak berubah.

### Penambahan Pengetahuan untuk Capability Pack

|Capability Pack|Topik yang Direncanakan|Referensi RFC|
|-----------------|---------------|---------------|
|Insinyur Jaringan|Panduan Desain Cisco, Praktik Terbaik MikroTik, Fortinet Hardening, BGP, MPLS, IPv6, Zero Trust|RFC-0004|
|Insinyur Kode|Arsitektur Bersih, DDD, SOLID, CQRS, Sumber Acara, Pengodean Aman|RFC-0006|
|Analis Perdagangan|Wyckoff, ICT, SMC, Elliott Wave, Profil Volume, Makro, Opsi, Futures, Psikologi|RFC-0005|
|Asisten Peneliti|Peringkat bukti, deteksi fosil, kualitas sitasi, estimasi keyakinan| — |
|Asisten DevOps|Multi-cloud, GitOps, Rekayasa platform, Kebijakan sebagai kode, Rekayasa kekacauan| — |
|Pengembangan Diri|Pembelajaran pola lintas proyek, prediksi dampak, bau arsitektur taksonomi| — |

Untuk rincian topik yang lebih detail, lihat `docs/CAPABILITY_STRATEGY.md` (bagian Ekspansi Pengetahuan).

---

## Dokumen Terkait

|Dokumen|Tujuan|
|----------|---------|
|`docs/GOVERNANCE_CHARTER.md`|Visi, prinsip inti, filosofi, aturan konstitusional|
|`docs/GOVERNANCE.md`|Aturan operasional — ADR, Capability First, Architecture Freeze, penegakan hukum|
|`docs/RELEASE_CRITERIA.md`|Syarat rilis — gerbang kualitas, Definisi Selesai, Benchmark target|
|`docs/CAPABILITY_STRATEGY.md`|Strategi Capability Pack — model kedewasaan, siklus hidup, paket profil|
|`docs/DOCUMENT_STRUCTURE.md`|Fungsi dan SSOT setiap dokumen dalam strategi dokumentasi|
|`docs/v1_roadmap.md`|Kompatibilitas halaman arahan — menunjuk ke dokumen-dokumen di atas|
|`docs/rfcs/README.md`|Proses RFC dan daftar RFC aktif|
|`ARCHITECTURE_DECISIONS.md`|ADR yang sudah disetujui dan dibekukan|
