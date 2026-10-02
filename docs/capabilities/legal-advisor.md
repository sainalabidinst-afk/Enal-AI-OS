# Legal Advisor Capability Pack

**Version:** 1.0.0
**Target Grade:** A (≥90%)
**Status:** Implemented
**Category:** Vertical Industry

## Ringkasan

Legal Advisor Capability Pack menyediakan analisis dokumen hukum, ekstraksi klausal, pencocokan playbook, pendaftaran kewajiban, dan deteksi konflik antar sumber. Semua output didasarkan pada sumber yang disetujui dan mensyaratkan hak istimewa yurisdi yang tepat.

## Kemampuan Inti

1. **Clause Extraction** — Ekstrak klausal dari dokumen dengan lokasi sumber (halaman)
2. **Clause Deviation Check** — Bandingkan klausal dengan playbook yang disetujui
3. **Obligation Registration** — Ekstrak pihak, aksi, trigger, deadline, dan sumber
4. **Conflict Detection** — Identifikasi ketidakkonsistenan antar sumber yang berbeda
5. **Source Summarization** — Buat ringkasan dari dokumen hukum dengan referensi sumber

## Input Schema

- `operation`: document_extract | clause_check | source_register | conflict_check | source_summarize
- `document_id`, `text`, `page`
- `playbook_id`, `playbook_rule`
- `source_document`, `source_id`, `jurisdiction`, `effective_date`
- `approved_sources[]`: Daftar sumber yang dipercaya

## Batasan Keamanan

- **Tidak mengeluarkan nasihat hukum** — Semua output bersifat assistif, bukan pengganti kuasa hukum
- **Hanya mengandalkan sumber yang disetujui** — Tolak sumber di luar registry yang dikonfigurasi
- **Menyurfatkan abstain** — Jika tidak ada sumber yang disetujui yang mendukung, jangan ambil kesimpulan hukum
- **Meminta yurisdi** — Untuk analisis yang bergantung pada yurisdi, minta input sebelum memproses

## Integration

- **Konsumsi dari**: Compliance Officer (daftar kontrol), Knowledge Engineer (ontologi hukum)
- **Digunakan oleh**: Compliance Officer (evidence), Data Engineer (pipeline governance)

## Benchmark

- 10 skenario dalam 6 dimensi
- Overall score: A (90.3%)
- Dimensi: clause_extraction, deviation_check, obligation_registration, conflict_detection, compliance_boundary, explainability
- Dashboard: `benchmarks/dashboards/legal_advisor_dashboard.html`

## Real Cases

10 real cases di `real_cases/legal_advisor/`

## Changelog

- **2026-10-02**: Initial implementation (RFC-0031, ADR-011)
