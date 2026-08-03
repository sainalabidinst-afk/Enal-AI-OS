# Kasus Nyata Kode

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

- `fastapi_microservice/` — Pembuatan dan review microservice FastAPI
- `ddd_order_management/` — Implementasi DDD untuk manajemen pesanan
- `security_audit/` — Audit keamanan kode dengan berbagai kerentanan
- `legacy_php/` — Tinjauan basis kode PHP legacy
- `react_dashboard/` — Dashboard React dari kebutuhan
- `database_refactor/` — Refactoring skema basis data

## Template Evaluasi

```markdown
# Evaluation: <case_name>

Date: YYYY-MM-DD

## Ringkasan
Deskripsi singkat kasus.

## Apa yang Dijawab Benar oleh ECP
- Temuan 1
- Temuan 2

## Apa yang Dijawab Salah oleh ECP
- Temuan 1
- Temuan 2

## Apa yang Dilewatkan oleh ECP
- Temuan yang kurang 1
- Temuan yang kurang 2

## Aksi Perbaikan
- [ ] Perbarui pengetahuan arsitektur untuk X
- [ ] Tingkatkan pembuatan kode untuk Y
- [ ] Tambahkan deteksi pola baru untuk Z

Referensi Benchmark: ________
```
