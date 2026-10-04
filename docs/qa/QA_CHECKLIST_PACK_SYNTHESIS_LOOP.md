# QA Checklist — Pack Synthesis Loop (RFC-0055)

<!-- DOCUMENT_METADATA_START -->
**Pemilik:** Tim Platform
**Canonical Owner:** Lead Platform Engineer
**Terakhir Diverifikasi:** 2026-10-04
**Versi:** 1.0.0
**Status:** Accepted
**SSOT:** QA checklist untuk Pilar 4 pack synthesis loop
<!-- DOCUMENT_METADATA_END -->

## Scope

Checklist ini mencakup siklus synthesis pack dari gap detection hingga registered pack.

## Checklist

### Gap Detection
- [ ] `CapabilityGapDetector.detect()` mengembalikan `GapDetectionResult` untuk query di luar domain eksisting.
- [ ] Threshold confidence `0.55` berfungsi: query dengan confidence >= threshold dianggap covered.
- [ ] Topic keyword matching mendeteksi minimal 2 keyword untuk menentukan partial coverage.
- [ ] Query "Apa yang bisa kamu lakukan?" diklasifikasikan sebagai `unknown` gap.

### Proposal
- [ ] `CapabilityProposal` dihasilkan dengan `status=draft` untuk setiap gap baru.
- [ ] Field `tier`, `estimated_effort`, `risk`, `confidence` terisi sesuai heuristik.
- [ ] Proposals disimpan ke `proposal_repository`.

### Sandbox Isolation
- [ ] `GovernanceSandbox` dibuat untuk setiap pack baru sebelum benchmark.
- [ ] `allowed_operations` hanya berisi `read`, `execute`, `benchmark`.
- [ ] `blocked_operations` berisi `write`, `network`, `delete`, `register`.
- [ ] Pack di sandbox tidak bisa mengakses registry tanpa promosi status.

### Benchmark & Quality Gate
- [ ] Benchmark score dihitung sebelum evaluasi gate.
- [ ] Quality gate berhasil jika:
  - `benchmark_score >= 0.8`
  - `coverage >= 0.8`
  - `test_pass_rate >= 0.95`
- [ ] Pack gagal gate jika salah satu threshold tidak terpenuhi → status `rejected`.

### Registration
- [ ] Pack dengan status `approved` bisa dipromosikan ke `registered`.
- [ ] Pack `registered` muncul di `/api/v1/governance/packs`.
- [ ] Pack terdeprecated bisa di-set status `deprecated`.

### Audit Trail
- [ ] Setiap perubahan status pack tercatat di `GovernanceEngine.get_audit_trail()`.
- [ ] Audit trail mencakup: `pack_registered`, `sandbox_created`, `pack_status_updated`, `quality_gate_evaluated`.
- [ ] Timestamp audit menggunakan UTC.

### API Endpoints
- [ ] `POST /api/v1/governance/packs` — register pack baru.
- [ ] `GET /api/v1/governance/packs` — list packs dengan filter opsional.
- [ ] `GET /api/v1/governance/packs/{pack_id}` — detail pack.
- [ ] `POST /api/v1/governance/packs/{pack_id}/sandbox` — buat sandbox.
- [ ] `POST /api/v1/governance/packs/{pack_id}/evaluate` — evaluasi quality gate.
- [ ] `GET /api/v1/governance/audit` — lihat audit trail.

## Acceptance Criteria

- Semua endpoint `/api/v1/governance/*` returning HTTP 200 untuk valid request.
- Pack synthesis loop dari draft → testing → approved → registered tercapai tanpa manual intervention (selama quality gate lolos).
- Audit trail lengkap untuk setiap transisi status.
