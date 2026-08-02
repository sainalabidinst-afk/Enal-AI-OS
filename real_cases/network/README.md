<!-- BILINGUAL_DOCS_START -->
## Bahasa Indonesia / English

### Ringkasan / Summary
Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.
> Terjemahan Indonesia: Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.

- Bahasa Indonesia: konten utama tetap dipertahankan dalam dokumen asli, dan bagian ini memberi konteks ringkas dalam bahasa Indonesia.
- English: the main content remains in the original document, and this section provides a concise bilingual context for international readers.

### Informasi Dokumen / Document Info
- File: `real_cases/network/README.md`
- Judul: Readme
- Status: bilingual header added

<!-- BILINGUAL_DOCS_END -->

# Network Real Cases

<!-- DOCUMENT_METADATA_START -->
**Owner:** Documentation Team
**Canonical Owner:** Documentation Governance Lead
**Last Verified:** 2026-08-02
**Version:** 1.0.0
**Status:** Active
**SSOT:** Real case study documentation
<!-- DOCUMENT_METADATA_END -->

Real network configurations and audit scenarios encountered while using ECP.
> Terjemahan Indonesia: Real network configurations dan audit scenarios encountered while using ECP.

## Case Template

Create a folder for each case:
> Terjemahan Indonesia: Membuat sebuah folder untuk each case:

```
<case_name>/
â”œâ”€â”€ input/
â”‚   â””â”€â”€ config.rsc
â”œâ”€â”€ output/
â”‚   â”œâ”€â”€ analysis.md
â”‚   â””â”€â”€ recommendations.md
â””â”€â”€ evaluation.md
```

## Example Cases

- `isp_dual_wan_failover/` â€” Dual WAN with failover rules
- `mikrotik_hotspot_school/` â€” School hotspot with VLANs and user management
- `campus_vlan/` â€” Campus network with multiple VLANs and inter-VLAN routing
- `enterprise_firewall/` â€” Enterprise firewall policy review

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
- [ ] Update analyzer for X
- [ ] Improve recommendation for Y
- [ ] Add new rule for Z

Benchmark Reference: ________
```
