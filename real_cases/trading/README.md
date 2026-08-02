# Kasus Nyata Trading

<!-- DOCUMENT_METADATA_START -->
**Owner:** Documentation Team
**Canonical Owner:** Documentation Governance Lead
**Last Verified:** 2026-08-02
**Version:** 1.0.0
**Status:** Active
**SSOT:** Real case study documentation
<!-- DOCUMENT_METADATA_END -->

Skenario analisis pasar nyata yang ditemui saat menggunakan ECP.

## Template Kasus

Buat folder untuk setiap kasus:

```
<case_name>/
├── input/
│   ├── market_data.csv
│   ├── chart_screenshot.png
│   └── context.md
├── output/
│   ├── analysis.md
│   ├── recommendation.md
│   └── risk_assessment.md
└── evaluation.md
```

## Contoh Kasus

- `btc_breakout/` — Identifikasi dan analisis breakout Bitcoin
- `gold_news/` — Reaksi harga emas terhadap peristiwa berita
- `eurusd_nfp/` — Analisis EUR/USD seputar rilis NFP
- `portfolio_rebalance/` — Skenario rebalancing portofolio

## Template Evaluasi

```markdown
# Evaluation: <case_name>

Date: YYYY-MM-DD

## Ringkasan
Deskripsi singkat skenario pasar.

## Apa yang Dijawab Benar oleh ECP
- Temuan 1
- Temuan 2

## Apa yang Dijawab Salah oleh ECP
- Temuan 1
- Temuan 2

## Apa yang Dilewatkan oleh ECP
- Faktor yang kurang 1
- Faktor risiko yang kurang 2

## Aksi Perbaikan
- [ ] Tingkatkan penalaran untuk X
- [ ] Penjelasan risiko yang lebih baik untuk Y
- [ ] Tambahkan pola pengetahuan untuk Z

Referensi Benchmark: ________
```
