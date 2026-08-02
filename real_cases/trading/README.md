<!-- BILINGUAL_DOCS_START -->
## Bahasa Indonesia / English

### Ringkasan / Summary
Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.
> Terjemahan Indonesia: Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.

- Bahasa Indonesia: konten utama tetap dipertahankan dalam dokumen asli, dan bagian ini memberi konteks ringkas dalam bahasa Indonesia.
- English: the main content remains in the original document, and this section provides a concise bilingual context for international readers.

### Informasi Dokumen / Document Info
- File: `real_cases/trading/README.md`
- Judul: Readme
- Status: bilingual header added

<!-- BILINGUAL_DOCS_END -->

# Trading Real Cases

<!-- DOCUMENT_METADATA_START -->
**Owner:** Documentation Team
**Canonical Owner:** Documentation Governance Lead
**Last Verified:** 2026-08-02
**Version:** 1.0.0
**Status:** Active
**SSOT:** Real case study documentation
<!-- DOCUMENT_METADATA_END -->

Real market analysis scenarios encountered while using ECP.
> Terjemahan Indonesia: Skenario analisis pasar nyata ditemui saat menggunakan ECP.

## Case Template

Create a folder for each case:
> Terjemahan Indonesia: Membuat sebuah folder untuk each case:

```
<case_name>/
â”œâ”€â”€ input/
â”‚   â”œâ”€â”€ market_data.csv
â”‚   â”œâ”€â”€ chart_screenshot.png
â”‚   â””â”€â”€ context.md
â”œâ”€â”€ output/
â”‚   â”œâ”€â”€ analysis.md
â”‚   â”œâ”€â”€ recommendation.md
â”‚   â””â”€â”€ risk_assessment.md
â””â”€â”€ evaluation.md
```

## Example Cases

- `btc_breakout/` â€” Bitcoin breakout identification and analysis
- `gold_news/` â€” Gold price reaction to news event
- `eurusd_nfp/` â€” EUR/USD analysis around NFP release
- `portfolio_rebalance/` â€” Portfolio rebalancing scenario

## Evaluation Template

```markdown
# Evaluation: <case_name>

Date: YYYY-MM-DD

## Summary
Brief description of the market scenario.

## What ECP Got Right
- Finding 1
- Finding 2

## What ECP Got Wrong
- Finding 1
- Finding 2

## What ECP Missed
- Missing factor 1
- Missing risk factor 2

## Improvement Actions
- [ ] Improve reasoning for X
- [ ] Better risk explanation for Y
- [ ] Add knowledge pattern for Z

Benchmark Reference: ________
```
