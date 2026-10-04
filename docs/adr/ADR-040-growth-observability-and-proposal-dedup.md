<!-- DOCUMENT_METADATA_START -->
**Pemilik:** Tim Platform
**Canonical Owner:** Lead Platform Engineer
**Terakhir Diverifikasi:** 2026-10-05
**Versi:** 1.0.0
**Status:** Accepted
**SSOT:** Proposal store dedup, export/report, dan growth alert observability
<!-- DOCUMENT_METADATA_END -->

# ADR-040: Proposal Dedup, Export/Report, dan Growth Alert Observability

## Abstrak

ADR ini menetapkan tiga perubahan strategis pada capability pack
`self_development` beserta integrasinya ke pipeline observability:

1. **Dedup proposal store** — `apps/self_development/proposals.json`
   tidak lagi tumbuh tak terkendali.
2. **Export/report** — ringkasan progres user diekspor sebagai JSON
   atau HTML.
3. **Growth alert observability** — alert habit dan goal-drift muncul
   di feed alert dashboard utama.

## Konteks

### 1. Proposal store tumbuh tak terkendali

`ECPAnalyzer.propose_capabilities()` dan `propose_improvements()`
menghasilkan id acak (`cap-{uuid4().hex[:8]}`) pada setiap eksekusi.
`ProposalRepository` men-key store dengan `proposal.id`, sehingga
analisis yang dijalankan berulang kali menambahkan entri baru untuk
kapabilitas yang sama. Store mencapai 1 MB (162 capability proposal,
2082 improvement proposal) dengan duplikat yang identik kecuali id-nya.

### 2. Tidak ada export progres

User tidak memiliki cara membawa ringkasan progres belajarnya
(aktivitas, skill, goal, habit) keluar dari aplikasi.

### 3. Growth alert terisolasi dari dashboard

`HabitTracker.dispatch_alerts()` mempublikasikan alert habit dan
goal-drift di event bus, tetapi alert tersebut tidak tercatat di
telemetry aggregator — satu-satunya sumber feed alert dashboard
utama (`/api/v1/metrics/alerts`). Dashboard observability juga
memanggil path telemetry yang salah (`/api/v1/telemetry/...`)
sehingga feed alert-nya 404.

## Keputusan

### 1. Dedup proposal store

- **Id deterministik.** `capability_proposal_id(domain)` menghasilkan
  `cap-{domain}`; `improvement_proposal_id(target_type, target_id,
  improvement_type)` menghasilkan `imp-{sha1(natural_key)[:8]}`.
  Id cross-pack pattern juga deterministik (`pattern-{type}`) karena
  menjadi `target_id` improvement.
- **Dedup natural key.** `ProposalRepository.add_capability()` menggabungkan
  proposal dengan `domain` yang sama ke entri yang sudah ada (update
  in-place, id lama dipertahankan). `add_improvement()` melakukan hal
  yang sama untuk `(target_type, target_id, improvement_type)`.
- **Store terbatas.** `MAX_CAPABILITIES = 100` dan
  `MAX_IMPROVEMENTS = 200`; overflow dipangkas mulai dari proposal
  rejected dengan confidence terendah.
- **Dedup saat load.** `_load()` mendedup file legacy berdasarkan
  natural key (last-wins), dan `dedupe()` membersihkan store yang
  sudah ada.

### 2. Export/report

- Modul baru `apps/self_development/export_service.py` dengan
  `ExportService` yang menggabungkan snapshot progres, goal, habit,
  alert, dan rekomendasi menjadi satu laporan.
- Format `json` (payload lengkap) dan `html` (halaman ringkasan
  bergaya). Output ditulis ke `artifacts/self_development/` dan
  dikembalikan in-memory.
- Dependency injection untuk `LearningAnalytics`, `GoalAligner`,
  `HabitTracker`, dan `RecommendationEngine` agar dapat diuji dengan
  repository terisolasi.
- Endpoint `GET /api/v1/self-development/export?format=json|html`.

### 3. Growth alert observability

- `Aggregator.record_growth_alert()` mencatat alert habit/goal-drift
  ke feed `_growth_alert_events` (dibatasi 500 entri) dengan KPI
  `growth_alert_kpis()` dan metrik Prometheus `ecp_growth_alerts_total`.
- `HabitTracker.dispatch_alerts()` memanggil `record_growth_alert()`
  untuk setiap alert dan mempublikasikan gauge
  `self_development.habit_reminders` / `self_development.goal_drift_alerts`
  ke `metrics_collector` (RFC-0001).
- Feed `/api/v1/metrics/alerts` sekarang mengembalikan kunci
  `growth_alerts`.
- Frontend: `AlertFeedResponse` menambahkan `growth_alerts`, dashboard
  observability merender bagian "Growth alerts (habit / goal drift)",
  dan path telemetry yang salah (`/api/v1/telemetry/...`) diperbaiki
  menjadi `/api/v1/metrics/...`.

## Konsekuensi

- Store proposal tetap stabil berapa pun frekuensi analisis dijalankan;
  file `proposals.json` yang sudah ada dibersihkan dari 2244 entri
  menjadi 134 entri unik.
- Alert habit/goal-drift terlihat di dashboard utama tanpa perlu
  berlangganan event bus secara terpisah.
- Perubahan pada `backend/app/core/telemetry/aggregator.py` adalah
  perubahan core file; ADR ini menjadi referensinya.

## Alternatif yang ditolak

- **UUID tetap per domain tanpa dedup repository:** tidak membersihkan
  duplikat legacy dan tetap bisa tumbuh jika id pernah berubah.
- **Alert growth di event bus saja:** dashboard utama tidak
  berlangganan event bus, sehingga alert tidak pernah terlihat.
- **Menambah prefix `/telemetry` pada router:** merubah semua path
  API yang sudah ada; lebih murah memperbaiki path frontend.
