# ADR-035: Governance Sandbox Isolation Architecture

<!-- DOCUMENT_METADATA_START -->
**Pemilik:** Tim Platform
**Canonical Owner:** Lead Platform Engineer
**Terakhir Diverifikasi:** 2026-10-04
**Versi:** 1.0.0
**Status:** Accepted
**SSOT:** Arsitektur isolasi sandbox untuk governance pack synthesis
<!-- DOCUMENT_METADATA_END -->

## Abstrak

ADR ini mendokumentasikan keputusan arsitektur untuk Governance Sandbox isolation pada Pilar 4, menjamin capability pack baru dijalankan terisolasi sebelum diregistrasi secara resmi.

## Konteks

Pilar 4 mensintesis capability pack baru secara otonom. Pack baru tidak boleh langsung mengakses sistem produksi atau memodifikasi registry tanpa validasi. Diperlukan lapisan isolasi yang konsisten dan dapat diaudit.

## Keputusan

Gunakan `GovernanceSandbox` contract di `backend/app/core/governance.py` sebagai lapisan isolasi untuk setiap pack baru.

- `isolated: bool = True` — default semua pack baru dijalankan terisolasi.
- `environment: str = "sandbox"` — env marker untuk routing dan logging.
- `allowed_operations: list[str]` — operasi yang diizinkan di sandbox: `read`, `execute`, `benchmark`.
- `blocked_operations: list[str]` — operasi yang diblokir: `write`, `network`, `delete`, `register`.
- Setiap pack synthesis wajib membuat `GovernanceSandbox` sebelum benchmark dijalankan.
- Setelah quality gate lolos, pack bisa dipromosikan ke status `approved` lalu `registered`.

## Konsekuensi

- **Positif:** Mencegah akses sembarang ke sistem produksi dari pack belum tervalidasi.
- **Positif:** Audit trail terpisah untuk setiap sandbox session.
- **Negatif:** Overhead maintenance untuk konfigurasi allowed/blocked operations per pack.

## Referensi

- RFC-0055: Pilar 4 — Enterprise Autonomy & Self-Evolving Platform
- ADR-025: Consent & Permission Architecture
