# Rencana Milestone ECP v1.0-dev

<!-- DOCUMENT_METADATA_START -->
**Pemilik:** Tim Dokumentasi
**Pemilik Canonical:** Pimpinan Tata Kelola Dokumentasi
**Terakhir Diverifikasi:** 2026-08-02
**Versi:** 1.0.0
**Status:** Aktif
**SSOT:** Dokumentasi untuk v1_sprint_plan
<!-- DOCUMENT_METADATA_END -->

**Metodologi:** Berbasis milestone produk, bukan berbasis fitur.
**Definition of Done:** Milestone memenuhi semua kriteria pengiriman dan gate terpenuhi.

---

## Milestone 1 — Network Engineer MVP

**Status:** ✅ Accepted
**Baseline:** `v1.0.0-dev+network-sprint2`

**Tujuan:** Membuktikan ECP dapat menganalisis, menghasilkan, mensimulasikan, dan mendokumentasikan konfigurasi jaringan.

**Durasi:** 2–3 minggu

**Definition of Done:**
- [x] Mengunggah file `.rsc`
- [x] Mem-parsing konfigurasi RouterOS
- [x] Membangun topologi internal
- [x] Mendeteksi masalah konfigurasi
- [x] Menghasilkan rekomendasi
- [x] Menghasilkan konfigurasi yang diperbaiki
- [x] Menghasilkan dokumentasi deployment
- [x] Lolos semua Golden Test untuk domain networking (31/31 skenario)

**Deliverables:**
- Parser RouterOS (v6/v7)
- Network graph builder
- 45 analysis rules
- Recommendation engine (P0–P3)
- Documentation generator (Markdown)

---

## Milestone 1.5 — Hardening

**Status:** ✅ Accepted

**Tujuan:** Memperkuat Milestone 1 dengan regression suite, benchmarks, dan pelacakan coverage.

**Durasi:** 3–5 hari

**Definition of Done:**
- [x] 31 skenario golden test (7 original + 24 baru)
- [x] Dataset regresi (broken, invalid, partial, v6, v7)
- [x] Rule coverage tracker (hit count, precision, recall, F1)
- [x] Benchmark kinerja (500/5k/50k baris)
- [x] Kalibrasi confidence dari evidence
- [x] Semua test lulus

---

## Milestone 2 — Controlled Deployment

**Status:** ✅ Accepted

**Tujuan:** Membangun pipeline deployment dengan keamanan, audit, dan persetujuan manusia.

**Durasi:** 2–3 minggu

**Definition of Done:**
- [x] Semantic Configuration Diff Engine
- [x] Backup Manager (export → hash → timestamp → artifact store)
- [x] Risk Scoring Engine (config/rollback/security/downtime)
- [x] Verification Engine (interface, gateway, DNS, DHCP, routes)
- [x] Audit Trail (semua langkah dicatat sebagai artifacts)
- [x] Controlled Deployment Orchestrator
- [x] Deployment Runbook UX (Changes/Risk/Pre-Deployment/Deployment/Post-Deployment/Recovery)
- [x] Deployment Timeline (visual progres langkah)
- [x] Explain Before Deploy (bahasa berorientasi proses)
- [x] Rollback Status: Pending / Ready / Unavailable / Completed
- [x] Persetujuan manusia diperlukan di v1.0-dev
- [x] Semua test Milestone 2 lulus (7/7)

---

## Milestone 3 — Network Operations

**Status:** 📋 Planned

**Tujuan:** Workflow operasional yang digunakan network engineer setiap hari.

**Durasi:** 2–3 minggu

**Definition of Done:**
- [ ] Configuration Compare (semantic diff backup-to-backup + dampak)
- [ ] Compliance Audit (Pass/Fail berbasis kebijakan)
- [ ] Health Report (skor health/security/performance/maintainability)
- [ ] Change Impact Analysis (memprediksi dampak sebelum deployment)
- [ ] Explain Like Engineer (penjelasan bahasa sederhana untuk onboarding)
- [ ] Semua test Milestone 3 lulus (≥95%)
- [ ] Feedback dogfooding diintegrasikan

**Deliverables:**
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
- Orkestrasi multi-router

---

## Fase Dogfooding

**Status:** 🧪 In Progress (1–2 minggu)

**Tujuan:** Menggunakan Network Engineer pada config nyata sebelum membangun fitur baru.

**Aktivitas:**
- Mengaudit config MikroTik nyata (Sun Clint, lab, production)
- Membandingkan findings ECP dengan penilaian ahli
- Mencatat false positives, false negatives, isu UX
- Mengumpulkan data Time Saved

**Output:**
- `dogfooding/feedback_YYYY-MM-DD.md`
- Skenario golden test yang diperbarui
- 5 prioritas teratas untuk Milestone 3

**Lihat:** `docs/dogfooding_guide.md`

---

## Milestone 4 — Reasoning Excellence

**Status:** 🎯 Target: Rilis v1.0-dev

**Tujuan:** Meningkatkan kualitas reasoning di semua Capability Pack tanpa mengubah Core.

**Durasi:** Berkelanjutan

**Area fokus:**
- Reasoning domain yang lebih dalam di Capability Packs
- Generasi penjelasan yang lebih baik
- Analisis risiko dan dampak yang lebih baik
- Rekomendasi yang sadar konteks

**Kriteria Keberhasilan:**
- Network: mendeteksi bukan hanya port terbuka, tetapi kemungkinan tujuan dan gap firewall terkait
- Trading: menjelaskan BUY/SELL dengan alternatif, risiko, dan skenario kegagalan
- Research: mengidentifikasi kontradiksi antar sumber dengan estimasi confidence
- Code: merekomendasikan pola arsitektur dengan rationale
- Semua Capability Pack mempertahankan skor Consistency ≥85%

---

## Milestone 5 — Developer Preview

**Status:** 🎯 Target: Rilis v1.0.0

**Tujuan:** Rilis siap produk dengan semua sertifikasi, dokumentasi, dan tooling lengkap.

**Definition of Done:**
- [ ] Semua Capability Pack memenuhi quality target
- [ ] Trading Analyst Certification lulus
- [ ] Artifact Store v1 diimplementasikan
- [ ] Website developer diluncurkan
- [ ] Dokumentasi SDK lengkap
- [ ] Video Tutorial dan Quick Start diterbitkan
- [ ] Marketplace berfungsi
- [ ] Capability Discovery API publik
- [ ] Capability Benchmark Dashboard operasional
- [ ] Studio trace viewer berfungsi

**Release Checklist:**
- [ ] Release notes disusun
- [ ] Panduan migrasi untuk penulis capability pack
- [ ] Contoh SDK diterbitkan
- [ ] Video/tutorial Quick Start disiapkan
- [ ] Pengumuman Public Developer Preview

---

## Ritme Pengembangan Mingguan

| Hari | Fokus |
|-----|-------|
| Senin | Ekspansi pengetahuan |
| Selasa | Peningkatan benchmark |
| Rabu | Peningkatan reasoning |
| Kamis | Peningkatan explainability |
| Jumat | Peningkatan skor benchmark |

Semua pekerjaan terjadi di dalam Capability Packs. Core tetap tidak tersentuh.

---

## Daftar "Jangan"

Berikut tidak lagi dapat diterima sebagai aktivitas pengembangan reguler:

- ❌ Menambahkan Runtime baru
- ❌ Menambahkan Planner baru
- ❌ Menambahkan Kernel baru
- ❌ Menambahkan Layer baru
- ❌ Memodifikasi Core untuk satu Capability Pack

Setiap pengecualian memerlukan ADR yang disetujui dengan bukti lintas capability.

---

## Target Capability Quality — v1.0 Developer Preview

| Capability | Target Score | Pengukuran |
|------------|--------------|-------------|
| Network | A (≥90) | benchmarks/capability_benchmark.py |
| Code | A- (≥85) | benchmarks/capability_benchmark.py |
| Research | A- (≥85) | benchmarks/capability_benchmark.py |
| DevOps | B+ (≥80) | benchmarks/capability_benchmark.py |
| Trading | B+ (≥80, lulus Certification) | benchmarks/capability_benchmark.py |
| Self Development | A (≥90) | benchmarks/capability_benchmark.py |

Skor harus berasal dari benchmark 6 dimensi, bukan penilaian subjektif.

---

## Peta Jalan Pasca Developer Preview

### v1.1 — Capability Excellence
- Network A+
- Trading B+
- Research A-
- Code A
- Semua pack naik satu grade melalui pengetahuan dan kerja benchmark

### v1.2 — Community Ecosystem
- Peluncuran Marketplace
- Mendukung Community Capability Packs
- Template SDK Capability Pack
- Proses sertifikasi pack pihak ketiga

### v1.3 — Enterprise
- Enterprise Capability Roadmap
- Fitur governance dan audit lanjutan
- Dukungan multi-tenant
- Tooling SLA dan compliance

---

## Peta Jalan Spesifik Capability

### Peta Jalan Capability Network

| Fase | Fokus | Target Grade |
|-------|-------|--------------|
| Audit | Analisis konfigurasi, keamanan, kepatuhan | A |
| Optimization | Performance tuning, best practices | A |
| Migration | Upgrade versi, migrasi vendor | A |
| Design | Desain jaringan greenfield | A+ |
| Automation | Controlled deployment, rollback | A+ |

### Peta Jalan Capability Code

| Fase | Fokus | Target Grade |
|-------|-------|--------------|
| Review | Kualitas kode, keamanan, maintainability | A- |
| Refactor | Memperbaiki struktur tanpa mengubah perilaku | A- |
| Generate | Full-stack dari requirements | A |
| Architecture | Clean Architecture, DDD, Hexagonal, CQRS | A |
| Modernization | Migrasi legacy, pengurangan tech debt | A |

### Peta Jalan Capability Trading

| Fase | Fokus | Target Grade |
|-------|-------|--------------|
| Analysis | Data pasar, tren, indikator | B+ |
| Strategy | Desain strategi dan backtesting | A- |
| Portfolio | Konstruksi portfolio dan rebalancing | A- |
| Risk | Model risiko, VaR, drawdown, korelasi | A |
| Execution Planning | Perencanaan trading dengan risiko dan alternatif | A |

### Peta Jalan Capability Research

| Fase | Fokus | Target Grade |
|-------|-------|--------------|
| Retrieval | RAG multi-sumber dengan sitasi | B |
| Evidence | Peringkat evidence, deteksi kontradiksi | A- |
| Synthesis | Sintesis multi-paper dengan confidence | A- |
| Experiment | Advisory desain eksperimen | A |
| Peer Review | Simulasi pengecekan kualitas peer review | A |

### Peta Jalan Capability DevOps

| Fase | Fokus | Target Grade |
|-------|-------|--------------|
| Generate | Dockerfiles, CI/CD, Kubernetes manifests | B+ |
| Verify | Kesehatan deployment, kebenaran konfigurasi | A- |
| Multi-cloud | Pola AWS, Azure, GCP | A |
| Platform | Observability, GitOps, policy-as-code | A |
| Resilience | Chaos engineering, persiapan insiden | A |

### Peta Jalan Capability Self Development

| Fase | Fokus | Target Grade |
|-------|-------|--------------|
| Analyze | Struktur proyek, deteksi bottleneck | A- |
| Propose | Refactoring, proposal perbaikan | A |
| Patch | Generasi patch dengan test coverage | A |
| Learn | Pembelajaran pola lintas proyek | A |
| Predict | Prediksi dampak sebelum perubahan | A+ |

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

Rencana sprint ini mengasumsikan disiplin vibe coding: AI menghasilkan, AI me-review, AI menguji, AI melakukan benchmark, manusia menyetujui.

### Minggu 1 — Chat UX

**Fokus:** Interface percakapan tunggal seperti Kimi/ChatGPT.
- Chat UI dengan streaming
- Rendering Markdown
- Upload file
- Workspace switcher
- Indikasi progress
- Artifact viewer

**Gate:** Pengguna dapat mengunggah config MikroTik dan melihat analisis streaming.

---

### Minggu 2 — Workspace

**Fokus:** Isolasi proyek dan memory.
- Workspace CRUD
- Riwayat percakapan per workspace
- Penyimpanan dan pengambilan artifact
- Pembatasan memory per workspace

**Gate:** Pengguna dapat berpindah antara dua workspace dan riwayat terisolasi.

---

### Minggu 3 — Streaming & Long Context

**Fokus:** Umpan balik eksekusi real-time.
- Event streaming dari Execution Runtime
- Pembaruan progress subtask
- Artifact streaming
- Pesan pemulihan error

**Gate:** Pengguna melihat progress real-time selama tugas 5+ langkah.

---

### Minggu 4 — Capability Excellence: Network

**Fokus:** Membuat Network Engineer benar-benar ahli.
- Menambahkan 20 real cases ke `real_cases/network/`
- Meningkatkan kedalaman analyzer
- Meningkatkan explainability
- Benchmark: 92%+

**Gate:** Skor benchmark Network ≥92%.

---

### Minggu 5 — Capability Excellence: Code, Research, DevOps

**Fokus:** Membawa pack lainnya ke kualitas minimum yang layak.
- Code: Review + Patch end-to-end
- Research: Peringkat evidence + sitasi
- DevOps: Generasi Docker + CI/CD

**Gate:** Ketiga pack lulus benchmark ≥80%.

---

### Minggu 6 — Dogfooding

**Fokus:** Menggunakan ECP untuk membangun ECP.
- Mengaudit dokumen ECP dengan Self Development
- Me-review kode ECP dengan Code Capability
- Mendokumentasikan findings di `real_cases/`

**Gate:** 50+ real cases dikumpulkan, semuanya diumpankan kembali ke capability packs.

---

### Minggu 7 — Benchmark & Polish

**Fokus:** Mengukur dan meningkatkan.
- Menjalankan semua capability benchmarks
- Memperbaiki regresi
- Polish alur UX terhadap USER_JOURNEYS.md
- Optimasi kinerja

**Gate:** Semua 6 pack memenuhi target kualitas Developer Preview.

---

### Minggu 8 — Developer Preview

**Fokus:** Rilis produk.
- Release notes
- Dokumentasi SDK
- Quick Start
- Pengumuman publik

**Gate:** ECP v1.0.0 dirilis dengan capability packs bersertifikat.

---

## Ritme Pengembangan

| Hari | Fokus |
|-----|-------|
| Senin | Ekspansi pengetahuan |
| Selasa | Peningkatan benchmark |
| Rabu | Peningkatan reasoning |
| Kamis | Explainability |
| Jumat | Peningkatan skor benchmark |

Semua perubahan terjadi di dalam Capability Packs. Core tetap tidak tersentuh.

