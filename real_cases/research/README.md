# Kasus Nyata Penelitian

<!-- DOCUMENT_METADATA_START -->
**Owner:** Documentation Team
**Canonical Owner:** Documentation Governance Lead
**Last Verified:** 2026-08-02
**Version:** 1.0.0
**Status:** Active
**SSOT:** Real case study documentation
<!-- DOCUMENT_METADATA_END -->

Pertanyaan penelitian nyata dan analisis sumber yang ditemui saat menggunakan ECP.

## Template Kasus

Buat folder untuk setiap kasus:

```
<case_name>/
├── input/
│   ├── question.md
│   └── sources/
├── output/
│   ├── literature_review.md
│   ├── synthesis.md
│   └── citations.md
└── evaluation.md
```

## Contoh Kasus

- `ai_security_survey/` — Survei makalah keamanan AI
- `market_efficiency/` — Riset hipotesis efisiensi pasar
- `protocol_comparison/` — Studi perbandingan protokol jaringan

## Template Evaluasi

```markdown
# Evaluation: <case_name>

Date: YYYY-MM-DD

## Ringkasan
Deskripsi singkat pertanyaan penelitian.

## Apa yang Dijawab Benar oleh ECP
- Temuan 1
- Temuan 2

## Apa yang Dijawab Salah oleh ECP
- Temuan 1
- Temuan 2

## Apa yang Dilewatkan oleh ECP
- Sumber yang kurang 1
- Kontradiksi yang kurang 2

## Aksi Perbaikan
- [ ] Tingkatkan peringkat bukti untuk X
- [ ] Deteksi kontradiksi yang lebih baik untuk Y
- [ ] Tingkatkan kualitas sitasi untuk Z

Referensi Benchmark: ________
```
