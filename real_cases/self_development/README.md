# Kasus Nyata Pengembangan Diri

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

## Ringkasan
Deskripsi singkat proyek dan masalahnya.

## Apa yang Dijawab Benar oleh ECP
- Temuan 1
- Temuan 2

## Apa yang Dijawab Salah oleh ECP
- Temuan 1
- Temuan 2

## Apa yang Dilewatkan oleh ECP
- Masalah yang kurang 1
- Solusi yang kurang 2

## Aksi Perbaikan
- [ ] Tingkatkan deteksi untuk X
- [ ] Kualitas proposal yang lebih baik untuk Y
- [ ] Tingkatkan prediksi dampak untuk Z

Referensi Benchmark: ________
```
