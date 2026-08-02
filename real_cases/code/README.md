# Code Real Cases

<!-- DOCUMENT_METADATA_START -->
**Owner:** Documentation Team
**Canonical Owner:** Documentation Governance Lead
**Last Verified:** 2026-08-02
**Version:** 1.0.0
**Status:** Active
**SSOT:** Real case study documentation
<!-- DOCUMENT_METADATA_END -->

Basis kode nyata yang ditinjau atau dibuat saat menggunakan ECP.

## Template Kasus

Buat folder untuk setiap kasus:

```
<case_name>/
├── input/
│   └── <source_code_or_requirements>
├── output/
│   ├── review.md or generated_code/
│   └── recommendations.md
└── evaluation.md
```

## Contoh Kasus

- `legacy_php/` — Tinjauan basis kode PHP legacy
- `fastapi_microservice/` — Pembuatan microservice FastAPI
- `react_dashboard/` — Dashboard React dari kebutuhan
- `database_refactor/` — Refactoring skema basis data

## Template Evaluasi

```markdown
# Evaluation: <case_name>

Date: YYYY-MM-DD

## Summary
Deskripsi singkat kasus.

## What ECP Got Right
- Temuan 1
- Temuan 2

## What ECP Got Wrong
- Temuan 1
- Temuan 2

## What ECP Missed
- Temuan yang kurang 1
- Temuan yang kurang 2

## Improvement Actions
- [ ] Perbarui pengetahuan arsitektur untuk X
- [ ] Tingkatkan pembuatan kode untuk Y
- [ ] Tambahkan deteksi pola baru untuk Z

Benchmark Reference: ________
```
