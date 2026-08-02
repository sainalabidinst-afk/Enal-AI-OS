<!-- BILINGUAL_DOCS_START -->
## Bahasa Indonesia / English

### Ringkasan / Summary
Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.
> Terjemahan Indonesia: Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.

- Bahasa Indonesia: konten utama tetap dipertahankan dalam dokumen asli, dan bagian ini memberi konteks ringkas dalam bahasa Indonesia.
- English: the main content remains in the original document, and this section provides a concise bilingual context for international readers.

### Informasi Dokumen / Document Info
- File: `real_cases/self_development/README.md`
- Judul: Readme
- Status: bilingual header added

<!-- BILINGUAL_DOCS_END -->

# Self Development Real Cases

<!-- DOCUMENT_METADATA_START -->
**Owner:** Documentation Team
**Canonical Owner:** Documentation Governance Lead
**Last Verified:** 2026-08-02
**Version:** 1.0.0
**Status:** Active
**SSOT:** Real case study documentation
<!-- DOCUMENT_METADATA_END -->

Real project improvement scenarios encountered while using ECP.
> Terjemahan Indonesia: Real proyek improvement scenarios encountered while using ECP.

## Case Template

Create a folder for each case:
> Terjemahan Indonesia: Membuat sebuah folder untuk each case:

```
<case_name>/
â”œâ”€â”€ input/
â”‚   â”œâ”€â”€ project_snapshot/
â”‚   â””â”€â”€ problem_description.md
â”œâ”€â”€ output/
â”‚   â”œâ”€â”€ analysis.md
â”‚   â”œâ”€â”€ proposal.md
â”‚   â””â”€â”€ patch.diff
â””â”€â”€ evaluation.md
```

## Example Cases

- `dead_code_removal/` â€” Dead code detection and removal
- `architecture_improvement/` â€” Architecture refactoring proposal
- `test_coverage/` â€” Test coverage improvement
- `performance_bottleneck/` â€” Performance bottleneck analysis

## Evaluation Template

```markdown
# Evaluation: <case_name>

Date: YYYY-MM-DD

## Summary
Brief description of the project and problem.

## What ECP Got Right
- Finding 1
- Finding 2

## What ECP Got Wrong
- Finding 1
- Finding 2

## What ECP Missed
- Missing problem 1
- Missing solution 2

## Improvement Actions
- [ ] Improve detection for X
- [ ] Better proposal quality for Y
- [ ] Enhance impact prediction for Z

Benchmark Reference: ________
```
