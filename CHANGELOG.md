## Bahasa Indonesia/Bahasa Inggris


### Ringkas / Ringkas
Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.


### Informasi Dokumen / Info Dokumen
- Berkas: `CHANGELOG.md`
- Judul: Changelog
- Status: editor bilingual ditambahkan


# mencatat perubahan

Semua perubahan penting pada Enal Cognitive Platform (ECP) akan didokumentasikan dalam file ini.

Formatnya didasarkan pada [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
dan proyek ini menganut [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0-dasar-rekayasa] - 2024


### Dasar Teknik - Dibekukan 🧊


Tag ini menandai **Dasar Teknik** resmi dari Platform Kognitif Enal.

**Status:** 🟢 Dasar Teknik Stabil

#### Apa yang telah dicapai


- **Keamanan Tipe (MyPy):** 0 kesalahan di seluruh basis kode (27+ file diperbaiki)
- **Kompatibilitas Python 3.11:** Diverifikasi dengan `compile()` — 0 masalah dalam kode produksi
- **Pylance Severity 8:** 0 diagnostik tersisa
- **Masalah Kode VS:** 0 masalah tersisa
- **Rangkaian Tes:** 426 tes lulus
- **Konsistensi Arsitektur:** Semua kontrak struktural divalidasi
- **API Konsistensi Kontrak:** Semua tanda tangan penambangan

#### Rumah tangga

- Skrip utilitas (`_audit_hygiene.py`, `_fix_*.py`, `_run_*.py`) dipindahkan ke `tools/audit/`
- Repositori root dibersihkan dari file pembantu/perkakas
- `tools/audit/__init__.py` dibuat dengan dokumentasi tujuan yang jelas

#### Aturan Pasca-Dasar

- Tidak ada pemfaktoran ulang skala besar baru tanpa kebutuhan lintas domain yang terdokumentasi
- Tidak ada desain ulang arsitektur
- Fokus beralih ke:
  1. Dokumentasi (arsitektur, independen modul, aliran Runtime, API, gerbang kualitas)
  2. Pengembangan produk dengan landasan yang stabil

#### Penilaian Akhir Teknik


|Daerah|Status|
|------|--------|
|Konsistensi Arsitektur| ✅ |
|API Konsistensi Kontrak| ✅ |
|Jenis Keamanan (MyPy)|✅ 0 Kesalahan|
|Kompatibilitas Python 3.11| ✅ |
|Pilance Keparahan 8|✅ 0|
|Masalah Kode VS|✅ 0|
|Rangkaian Tes|✅ 426 Lulus|
|Pengerasan Teknik|✅ Lengkap|
|Dasar Teknik|✅ **Stabil**|

---

## [kandidat rilis 1.0.0] - 27-07-2026


### Ditambahkan
- Fase Pengerasan Rekayasa selesai - Semua masalah tipe Severity 8+ terselesaikan
- Saluran kognitif terintegrasi penuh (Persepsi → Perencana → Memori → Pelaksana)
- Dukungan Pos Pemeriksaan/Lanjutkan/Coba lagi di WorkflowExecutor
- SessionMemory dan ProjectMemory untuk konteks lintas eksekusi

### Tetap
- Impor melingkar: `knowledge/__init__.py`, `task_planner.py`, `meeting.py`
- Vendor model impor tidak ada: `UniversalBGP`, `UniversalMPLS`, `UniversalCAPsMAN`, `UniversalWireGuard` di cisco_ios.py, mikrotik.py
- `Team` kelas data tidak memiliki kolom `team_id`
- `create_checkpoint`, `resume_from_checkpoint`, `execute_with_retry` dipindahkan ke dalam kelas `WorkflowExecutor`
- Duplikat `PerceptionInput` dihapus, sekarang diimpor dari `perception_engine.py`
- CodeEngineerApp `generate_patch()` ditulis ulang dengan tanda tangan yang benar
- Fungsi kunci IntentRouter `max()` diperbaiki
- API pola akses diperkuat dengan pembantu `_safe_get`

### Status
- Runtime tes: 426 pelamar
- Analisis statistik: 0 masalah Tingkat Keparahan 8+ (turun dari 366)
- Arsitektur: 92/100 - Kandidat Rilis Platform

---

## [1.1.0] - 2026-08-04

### Ditambahkan
- Audit komprehensif dan remediasi Phase 1-3 selesai
- Real JWT authentication (PyJWT) dengan signature, expiry, algorithm enforcement
- Blocking LLM calls diperbaiki: `complete()` → `acomplete()` di jalur async
- Docker hardening: volume mounts, pinned ollama (`0.1.26`), `read_only` aman
- `redis.keys()` diganti `scan_iter()` di memory layer
- 122 integration tests baru (`test_api_comprehensive.py`) covering 130 endpoints
- Complexity reduction: max complexity 272 → 211, top 10 files di-split
- Trading Analyst certification: A+ (100%), Level 4 Domain Expert
- Benchmark dashboard: `benchmarks/reports/trading_dashboard.html`
- Capability contract: `docs/capabilities/trading-analyst.md`
- Size limits untuk unbounded structures (audit log, plugin registry)
- `TESTING` flag untuk disable rate limit selama test
- Debug scripts dipindah ke `tools/debug/`
- SWC minify diaktifkan kembali di frontend
- Makefile dimodernisasi ke `docker compose` v2 syntax
- Security Engineer Capability Pack (RFC-0008): OWASP Top 10 analyzer, secret detection, vulnerability scanner, threat modeler, hardening reviewer, compliance mapper
- Security Engineer benchmark: 9 dimensi, 90% overall score, 100% pass rate
- 103 security real cases di `real_cases/security/`
- Security Engineer benchmark dashboard: `benchmarks/dashboards/security_engineer_dashboard.html`
- Security Engineer capability guide: `docs/CAPABILITY_GUIDE.md`
- Security Engineer contract schemas: `apps/security_engineer/schemas.py`

### Diperbaiki
- Test count inkonsisten: standarkan ke 166 collected tests
- Dokumentasi inkonsisten: test count, version tags, capability grades
- Vendor detection bug: Cisco `detect()` salah klasifikasi Fortinet config
- Un-awaited coroutine di `model_gateway.py`
- `memory_episodic.py` import error untuk `EpisodicMemoryEntry`

### Berkontribusi
- 231 files changed, 14072 insertions(+), 7715 deletions(-)
- 22 new modules dari splitting top 10 complex files
- 100+ real cases baru (Cisco, Fortinet, MikroTik)
- Commit: `4aead78` — refactor: reduce complexity, add tests, commit artifacts

---

## [1.0.0-dev] - 07-08-2026


### Ditambahkan
- Perubahan merek yang strategi dari "Enal AI OS" menjadi "Enal Cognitive Platform (ECP)"
- peta jalan v1.0.0-dev dengan 6 Paket Kemampuan Resmi
- Pipeline CI/CD dengan 8 pemeriksaan otomatis (lint, pemeriksaan tipe, unit pengujian, arsitektur, tolok ukur, kompatibilitas SDK, kompatibilitas Plugin, pengujian emas)
- Golden Test Suite dengan 200 kasus uji dalam 4 kategori
- 13 Paket kemampuan perancah:
  - Insinyur Jaringan
  - Kode Insinyur
  - Asisten Peneliti
  - Asisten DevOps
  - Analis Perdagangan
  - Pengembangan Diri
- Manajemen versi (file VERSION, pyproject.toml diperbarui ke 1.0.0-dev)
- dokumen peta jalan v1 dengan kriteria dan metrik keberhasilan

### Ditambahkan (Upgrade Kapabilitas)
- Asisten DevOps ditingkatkan dari B+ (≥80) ke A+ (≥90), Level 4 — Pakar Domain
  - Modul baru: `schemas.py`, `smell_taxonomy.py`, `risk_modeler.py`, `suggestion_generator.py`, `project_scanner.py`, `pipeline_generator.py`, `infrastructure_designer.py`, `deployment_planner.py`, `monitoring_configurator.py`, `worker.py`
  - Benchmark: `benchmarks/devops_assistant_benchmark.py` dengan 10 skenario, hasil 100% (A+)
  - Deteksi 10 tipe masalah DevOps dengan rekomendasi perbaikan
- Pengembangan Diri ditingkatkan dari A (≥90) ke A+ (≥95), Level 4 — Pakar Domain
  - Modul baru: `schemas.py`, `smell_taxonomy.py`, `risk_modeler.py`, `suggestion_generator.py`, `project_scanner.py`, `worker.py`
  - Benchmark: `benchmarks/self_development_benchmark.py` dengan 10 skenario, hasil 100% (A+)
- Analis Perdagangan ditingkatkan ke A+ (≥95), Level 4 — Pakar Domain
  - 7 domain pengetahuan: Wyckoff, SMC/ICT, Elliott Wave, Volume Profile, Psychology, Macro, Derivatives
  - Benchmark: `benchmarks/trading_analyst_benchmark.py` dengan 100 skenario, hasil 100% (A+)
  - Konsistensi: 100% across repeated analysis
  - Risk-adjusted return quality: verified via reasoning + coverage + safety scoring
  - Real cases: 5+ scenarios in `real_cases/trading/`
  - Contract documentation: `docs/capabilities/trading-analyst.md`
  - Benchmark dashboard: `benchmarks/reports/trading_dashboard.html`

### Berubah
- Repositori direkonsiliasi untuk ekosistem (kernel, Runtime, SDK, studio, pasar, ability_packs, aplikasi, Plugin, contoh, dokumen, tolok ukur)
- Semua komponen Fase 1-6 terintegrasi ke dalam platform yang kohesif
- Dokumentasi diperbarui untuk mencerminkan positioning produk

### Tata Kelola
- Tidak ada mesin baru tanpa kasus penggunaan nyata
- Kernel harus tetap berada di bawah 5000 baris
- Semua Plugin memerlukan manifestasi validasi dan keamanan
- Tes emas harus lulus dengan tingkat ≥80%.

---

## [0.1.0] - 07-08-2026

### Ditambahkan
- Fase 1: AI Core (model router, memori, perencana, panggilan alat, RAG)
- Fase 2: Insinyur Perangkat Lunak AI (agen pengkodean, QA, DevOps)
- Fase 3: AI Enterprise Platform (organisasi, reputasi, pengalaman, observabilitas)
- Fase 4: Arsitektur Kognitif (penalaran, debat, simulasi, verifikasi)
- Fase 5: OS Kognitif Adaptif (adaptif Runtime, mesin keputusan, meta-kognisi)
- Fase 6: Ekosistem (SDK, kontrak, pasar, studio, didistribusikan Runtime)
- Kontrak stabil untuk semua antarmuka inti
- Manifestasi Plugin dan model keamanan
- Penegakan batas paket
- Benchmark suite
- Dokumentasi yang komprehensif
