<!-- BILINGUAL_DOCS_START -->
## Bahasa Indonesia / English

### Ringkasan / Summary
Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.
> Terjemahan Indonesia: Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.

- Bahasa Indonesia: konten utama tetap dipertahankan dalam dokumen asli, dan bagian ini memberi konteks ringkas dalam bahasa Indonesia.
- English: the main content remains in the original document, and this section provides a concise bilingual context for international readers.

### Informasi Dokumen / Document Info
- File: `real_cases/code/README.md`
- Judul: Readme
- Status: bilingual header added

<!-- BILINGUAL_DOCS_END -->

# Code Real Cases

<!-- DOCUMENT_METADATA_START -->
**Owner:** Documentation Team
**Canonical Owner:** Documentation Governance Lead
**Last Verified:** 2026-08-02
**Version:** 1.0.0
**Status:** Active
**SSOT:** Real case study documentation
<!-- DOCUMENT_METADATA_END -->

Real codebases reviewed or generated while using ECP.
> Terjemahan Indonesia: Basis kode nyata ditinjau atau dibuat saat menggunakan ECP.

## Case Template

Create a folder for each case:
> Terjemahan Indonesia: Membuat sebuah folder untuk each case:

```
<case_name>/
â”œâ”€â”€ input/
â”‚   â””â”€â”€ <source_code_or_requirements>
â”œâ”€â”€ output/
â”‚   â”œâ”€â”€ review.md or generated_code/
â”‚   â””â”€â”€ recommendations.md
â””â”€â”€ evaluation.md
```

## Example Cases

- `legacy_php/` â€” Legacy PHP codebase review
- `fastapi_microservice/` â€” FastAPI microservice generation
- `react_dashboard/` â€” React dashboard from requirements
- `database_refactor/` â€” Database schema refactoring

## Evaluation Template

```markdown
# Evaluation: <case_name>

Date: YYYY-MM-DD

## Summary
Brief description of the case.

## What ECP Got Right
- Finding 1
- Finding 2

## What ECP Got Wrong
- Finding 1
- Finding 2

## What ECP Missed
- Missing finding 1
- Missing finding 2

## Improvement Actions
- [ ] Update architecture knowledge for X
- [ ] Improve code generation for Y
- [ ] Add new pattern detection for Z

Benchmark Reference: ________
```
