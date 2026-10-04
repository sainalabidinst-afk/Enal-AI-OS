# ADR-036: Consent Gating for High-Risk Remediation

<!-- DOCUMENT_METADATA_START -->
**Pemilik:** Tim Platform
**Canonical Owner:** Lead Platform Engineer
**Terakhir Diverifikasi:** 2026-10-04
**Versi:** 1.0.0
**Status:** Accepted
**SSOT:** Konsentrasi consent gate untuk remediation high-risk di Pilar 4
<!-- DOCUMENT_METADATA_END -->

## Abstrak

ADR ini menetapkan bahwa remediation high-risk di Pilar 4 harus melewati `ConsentGate` sebelum dieksekusi, menggunakan kontrak yang selaras dengan ADR-025.

## Konteks

Remediation layer Pilar 4 dapat mengeksekusi playbook yang berdampak ke infrastruktur atau operasional. High-risk remediation harus memerlukan approval eksplisit dari manusia sebelum dijalankan.

## Keputusan

Semua remediation dengan severity `high` atau `critical` wajib melalui `ConsentGate` sebelum dieksekusi.

- Severity mapping:
  - `low` — auto-approve, dijalankan langsung.
  - `medium` — memerlukan konfirmasi user.
  - `high` / `critical` — memerlukan persetujuan eksplisit + timeout.
- `ConsentGate` menggunakan `consent_manager` dari `backend.app.core.consent` (ADR-025).
- Setiap remediation request menciptakan consent request dengan:
  - `action_type`: `remediation.<playbook_id>`
  - `description`: deskripsi playbook + dampak yang diharapkan
  - `risk_level`: disesuaikan dengan severity remediation
- Remediation hanya dijalankan setelah `consent_manager.approve(request_id)` berhasil.
- Semua decision dicatat ke audit trail di `GovernanceEngine`.

## Konsekuensi

- **Positif:** Menghindari eksekusi sembarang remediation berisiko tinggi.
- **Positif:** Konsisten dengan mekanisme consent yang sudah ada di ECP.
- **Negatif:** Menambah langkah approval untuk remediation high-risk, yang bisa menambah latency.

## Referensi

- RFC-0055: Pilar 4 — Enterprise Autonomy & Self-Evolving Platform
- ADR-025: Consent & Permission Architecture
- `backend/app/core/consent.py`
