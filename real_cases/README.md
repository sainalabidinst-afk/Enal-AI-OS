<!-- BILINGUAL_DOCS_START -->
## Bahasa Indonesia / English

### Ringkasan / Summary
Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.
> Terjemahan Indonesia: Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.

- Bahasa Indonesia: konten utama tetap dipertahankan dalam dokumen asli, dan bagian ini memberi konteks ringkas dalam bahasa Indonesia.
- English: the main content remains in the original document, and this section provides a concise bilingual context for international readers.

### Informasi Dokumen / Document Info
- File: `real_cases/README.md`
- Judul: Readme
- Status: bilingual header added

<!-- BILINGUAL_DOCS_END -->

# Real-world Cases

<!-- DOCUMENT_METADATA_START -->
**Owner:** Documentation Team
**Canonical Owner:** Documentation Governance Lead
**Last Verified:** 2026-08-02
**Version:** 1.0.0
**Status:** Active
**SSOT:** Real case study documentation
<!-- DOCUMENT_METADATA_END -->

This directory contains real-world cases collected while using ECP in actual work.
These are not golden tests. These are daily usage artifacts that drive Capability Pack improvement.
> Terjemahan Indonesia: Ini directory contains real-world cases collected while using ECP dalam actual work. These adalah not golden tests. These adalah daily usage artifacts itu drive kapabilitas Pack improvement.

## Structure

Each Capability Pack has its own folder:
> Terjemahan Indonesia: Each kapabilitas Pack memiliki its own folder:

```
real_cases/
â”œâ”€â”€ network/           # Real network configurations and audits
â”œâ”€â”€ code/              # Real codebases reviewed or generated
â”œâ”€â”€ research/          # Real research questions and sources
â”œâ”€â”€ trading/           # Real market analysis scenarios
â”œâ”€â”€ devops/            # Real infrastructure scenarios
â””â”€â”€ self_development/  # Real project improvement cases
```

## What to Store

For each real-world case, create a folder with:
> Terjemahan Indonesia: Untuk each real-world case, membuat sebuah folder dengan:

1. **Input**: What the user provided
2. **Output**: What ECP produced
3. **Evaluation**: What was good, what was wrong, what was missing
4. **Benchmark ID**: Link to associated benchmark if updated

Example:
> Terjemahan Indonesia: Contoh:

```
network/isp_dual_wan_failover/
â”œâ”€â”€ input/
â”‚   â””â”€â”€ config.rsc
â”œâ”€â”€ output/
â”‚   â”œâ”€â”€ analysis.md
â”‚   â””â”€â”€ recommendations.md
â””â”€â”€ evaluation.md
```

## How to Use

1. Run ECP against a real case
2. Save input, output, and evaluation
3. If improvements are needed, update the Capability Pack
4. Reference this case in the Capability Benchmark

This is how Capability Packs become genuinely expert: through real-world iteration, not synthetic tests alone.
> Terjemahan Indonesia: Ini adalah how kapabilitas Packs become genuinely expert: through real-world iteration, not synthetic tests alone.
