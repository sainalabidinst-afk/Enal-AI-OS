# Trading Real Cases

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

## Summary
Deskripsi singkat skenario pasar.

## What ECP Got Right
- Temuan 1
- Temuan 2

## What ECP Got Wrong
- Temuan 1
- Temuan 2

## What ECP Missed
- Faktor yang kurang 1
- Faktor risiko yang kurang 2

## Improvement Actions
- [ ] Tingkatkan penalaran untuk X
- [ ] Penjelasan risiko yang lebih baik untuk Y
- [ ] Tambahkan pola pengetahuan untuk Z

Benchmark Reference: ________
```
