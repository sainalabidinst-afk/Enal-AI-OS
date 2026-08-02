# ECP Network Engineer — Baseline Freeze

<!-- DOCUMENT_METADATA_START -->
**Pemilik:** Tim Dokumentasi
**Pemilik Canonical:** Pimpinan Tata Kelola Dokumentasi
**Terakhir Diverifikasi:** 2026-08-02
**Versi:** 1.0.0
**Status:** Aktif
<!-- DOCUMENT_METADATA_END -->

**Tag Baseline:** `v1.0.0-dev+network-sprint2`
**Status:** Accepted
**Tanggal:** 2026-08-02
**Catatan:** Sprint historis dipertahankan untuk integritas baseline. Perkembangan saat ini menggunakan terminologi "Milestone".

## Definition of Done — Terpenuhi

### Capaian 1 — Network Engineer MVP (Sprint 1)
- [x] Upload file `.rsc`
- [x] Parse konfigurasi RouterOS
- [x] Bangun topologi internal
- [x] Deteksi masalah konfigurasi (45 aturan)
- [x] Hasilkan rekomendasi (P0–P3 dengan Nature/Impact/Confidence)
- [x] Hasilkan konfigurasi yang ditingkatkan
- [x] Pertahankan dokumentasi kebijakan (Markdown)
- [x] Lulus semua Golden Test (31/31 skenario)

### Capaian 1.5 — Hardening (Sprint 1.5)
- [x] 31 skenario Golden Test (7 asli + 24 baru)
- [x] Dataset regresi: konfigurasi rusak, sintaksis tidak valid, konfigurasi parsial, v6 lama, v7 baru
- [x] Rule coverage tracker (hit count, precision, recall, F1)
- [x] Benchmark kinerja (500/5k/50k baris)
- [x] Kalibrasi confidence dari evidence
- [x] Semua test lulus

### Milestone 2 — Controlled Deployment (Sprint 2)
- [x] Semantic Configuration Diff Engine
- [x] Backup Manager (export → hash → timestamp → artifact store)
- [x] Risk Scoring Engine (config/rollback/security/downtime)
- [x] Verification Engine (interface, gateway, DNS, DHCP, routes)
- [x] Audit Trail (semua langkah dicatat sebagai artifacts)
- [x] Controlled Deployment Orchestrator
- [x] Deployment Runbook UX (Changes/Risk/Pre-Deployment/Deployment/Post-Deployment/Recovery)
- [x] Deployment Timeline (progress visual per langkah)
- [x] Explain Before Deploy (berorientasi proses, bukan biner ya/tidak)
- [x] Rollback Status: Pending / Ready / Unavailable / Completed
- [x] Persetujuan manusia diperlukan di v1.0-dev
- [x] Semua test Milestone 2 lulus (7/7)

## Artifacts Baseline

- Golden Test Scenarios: `golden/mikrotik/` (31 skenario)
- Golden Test Runner: `tests/reference/test_network_engineer.py`
- Controlled Deployment Tests: `tests/reference/test_controlled_deployment.py`
- Performance Benchmark: `benchmarks/network_performance_benchmark.py`
- Rule Coverage Tracker: `apps/network_engineer/rule_coverage_tracker.py`
- Modul inti:
  - `apps/network_engineer/mikrotik/routeros_parser.py`
  - `apps/network_engineer/analyzer.py`
  - `apps/network_engineer/graph_builder.py`
  - `apps/network_engineer/recommendation_engine.py`
  - `apps/network_engineer/docs_generator.py`
  - `apps/network_engineer/diff_engine.py`
  - `apps/network_engineer/backup_manager.py`
  - `apps/network_engineer/risk_scorer.py`
  - `apps/network_engineer/verification_engine.py`
  - `apps/network_engineer/audit_trail.py`
  - `apps/network_engineer/controlled_deployment.py`

## Keterbatasan yang Diketahui

- Parser: hanya bagian dasar RouterOS v6/v7 (belum ada protokol routing lanjutan)
- Analyzer: 45 aturan, domain khusus untuk jaringan dasar
- Deployment: hanya simulasi (tidak ada SSH/API langsung ke perangkat MikroTik)
- Dokumentasi: hanya Markdown (belum ada HTML/PDF/Draw.io)
- Tidak ada orkestrasi multi-router
- Tidak ada deployment paralel

## Fase Berikutnya: Dogfooding → Network Operations

Lihat `docs/ROADMAP.md` untuk langkah selanjutnya.

