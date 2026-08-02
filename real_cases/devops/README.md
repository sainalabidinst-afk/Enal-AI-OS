<!-- BILINGUAL_DOCS_START -->
## Bahasa Indonesia / English

### Ringkasan / Summary
Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.
> Terjemahan Indonesia: Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.

- Bahasa Indonesia: konten utama tetap dipertahankan dalam dokumen asli, dan bagian ini memberi konteks ringkas dalam bahasa Indonesia.
- English: the main content remains in the original document, and this section provides a concise bilingual context for international readers.

### Informasi Dokumen / Document Info
- File: `real_cases/devops/README.md`
- Judul: Readme
- Status: bilingual header added

<!-- BILINGUAL_DOCS_END -->

# DevOps Real Cases

<!-- DOCUMENT_METADATA_START -->
**Owner:** Documentation Team
**Canonical Owner:** Documentation Governance Lead
**Last Verified:** 2026-08-02
**Version:** 1.0.0
**Status:** Active
**SSOT:** Real case study documentation
<!-- DOCUMENT_METADATA_END -->

Real infrastructure scenarios encountered while using ECP.
> Terjemahan Indonesia: Skenario infrastruktur nyata yang ditemui saat menggunakan ECP.

## Case Template

Create a folder for each case:
> Terjemahan Indonesia: Membuat sebuah folder untuk each case:

```
<case_name>/
â”œâ”€â”€ input/
â”‚   â””â”€â”€ requirements.md or infra_spec/
â”œâ”€â”€ output/
â”‚   â”œâ”€â”€ dockerfile
â”‚   â”œâ”€â”€ ci_cd_config/
â”‚   â””â”€â”€ documentation.md
â””â”€â”€ evaluation.md
```

## Example Cases

- `microservice_deploy/` â€” Microservice deployment pipeline
- `monitoring_setup/` â€” Monitoring and alerting configuration
- `kubernetes_migration/` â€” Kubernetes migration plan
- `cost_optimization/` â€” Infrastructure cost optimization

## Evaluation Template

```markdown
# Evaluation: <case_name>

Date: YYYY-MM-DD

## Summary
Brief description of the infrastructure scenario.

## What ECP Got Right
- Finding 1
- Finding 2

## What ECP Got Wrong
- Finding 1
- Finding 2

## What ECP Missed
- Missing configuration 1
- Missing best practice 2

## Improvement Actions
- [ ] Update knowledge base for X
- [ ] Improve configuration generation for Y
- [ ] Add multi-cloud pattern for Z

Benchmark Reference: ________
```
