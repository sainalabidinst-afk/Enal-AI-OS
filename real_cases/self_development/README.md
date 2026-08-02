# Self Development Real Cases

<!-- DOCUMENT_METADATA_START -->
**Owner:** Documentation Team
**Canonical Owner:** Documentation Governance Lead
**Last Verified:** 2026-08-02
**Version:** 1.0.0
**Status:** Active
**SSOT:** Real case study documentation
<!-- DOCUMENT_METADATA_END -->

Skenario perbaikan proyek nyata yang ditemui saat menggunakan ECP.

## Template Kasus

Buat folder untuk setiap kasus:

```
<case_name>/
├── input/
│   ├── project_snapshot/
│   └── problem_description.md
├── output/
│   ├── analysis.md
│   ├── proposal.md
│   └── patch.diff
└── evaluation.md
```

## Contoh Kasus

- `dead_code_removal/` — Deteksi dan penghapusan kode mati
- `architecture_improvement/` — Proposal refactoring arsitektur
- `test_coverage/` — Peningkatan cakupan pengujian
- `performance_bottleneck/` — Analisis bottleneck performa

## Template Evaluasi

```markdown
# Evaluation: <case_name>

Date: YYYY-MM-DD

## Summary
Deskripsi singkat proyek dan masalahnya.

## What ECP Got Right
- Temuan 1
- Temuan 2

## What ECP Got Wrong
- Temuan 1
- Temuan 2

## What ECP Missed
- Masalah yang kurang 1
- Solusi yang kurang 2

## Improvement Actions
- [ ] Tingkatkan deteksi untuk X
- [ ] Kualitas proposal yang lebih baik untuk Y
- [ ] Tingkatkan prediksi dampak untuk Z

Benchmark Reference: ________
```
