# HSE Specialist Capability Pack

**Version:** 1.0.0
**Target Grade:** A (≥90%)
**Status:** Implemented
**Category:** Vertical Industry

## Ringkasan

HSE Specialist Capability Pack menyediakan identifikasi bahaya, penilaian risiko, review kontrol, analisis insiden, dan pemeriksaan kepatuhan untuk operasi keamanan dan kesehatan kerja. Semua output mengikuti hierarki kontrol dan membutuhkan verifikasi kualifikasi untuk kondisi kritis.

## Kemampuan Inti

1. **Hazard Identification** — Identifikasi bahaya dari deskripsi tugas dan konteks lokasi
2. **Risk Scoring** — Hitung skor risiko menggunakan matriks likelihood × severity
3. **Control Review** — Evaluasi efektivitas kontrol yang ada menggunakan hierarki kontrol
4. **Incident Analysis** — Organisir narratif insiden menjadi timeline dan faktor kontribusi
5. **Compliance Checking** — Periksa kesenjangan kepatuhan terhadap standar (ISO 45001, OSHA)

## Input Schema

- `operation`: hazard_analysis | risk_calculate | controls_review | incident_analyze | compliance_check
- `task`: Deskripsi tugas kerja yang akan dianalisis
- `site_context`: Konteks lokasi kerja
- `hazard`, `likelihood` (1-5), `severity` (1-5)
- `existing_controls[]`: Daftar kontrol yang sudah ada
- `standard`: Standar kepatuhan (ISO 45001, OSHA-1910, dll)

## Batasan Keamanan

- **Tidak mengeluarkan perintah operasional** — Tidak kontrol peralatan secara autonom
- **Tidak mengganti penilaian profesional HSE** — Semua output assistif, membutuhkan review manusia terkualifikasi
- **Mensyaratkan likelihood dan severity** — Jangan hitung risiko jika data tidak lengkap
- **Eskalasi bahaya mendadak** — Ikuti prosedur dan personil situs yang ditetapkan untuk bahaya kritis

## Integration

- **Konsumsi dari**: Safety database (industry incident data), Compliance Officer (regulasi standar)
- **Digunakan oleh**: Infrastructure Engineer (site design), DevOps Assistant (CI/CD safety gates)

## Benchmark

- 10 skenario dalam 6 dimensi
- Overall score: A (90.8%)
- Dimensi: hazard_analysis, risk_scoring, control_review, incident_analysis, compliance_boundary, explainability
- Dashboard: `benchmarks/dashboards/hse_specialist_dashboard.html`

## Real Cases

10 real cases di `real_cases/hse_specialist/`

## Changelog

- **2026-10-02**: Initial implementation (RFC-0032, ADR-012)
