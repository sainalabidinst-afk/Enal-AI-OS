<!-- BILINGUAL_DOCS_START -->
## Bahasa Indonesia / English

### Ringkasan / Summary
Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.
> Terjemahan Indonesia: Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.

- Bahasa Indonesia: konten utama tetap dipertahankan dalam dokumen asli, dan bagian ini memberi konteks ringkas dalam bahasa Indonesia.
- English: the main content remains in the original document, and this section provides a concise bilingual context for international readers.

### Informasi Dokumen / Document Info
- File: `real_cases/FINAL_DATASET_AUDIT.md`
- Judul: Final Dataset Audit
- Status: bilingual header added

<!-- BILINGUAL_DOCS_END -->

# Final Dataset Audit - Sprint 5A.5

<!-- DOCUMENT_METADATA_START -->
**Owner:** Documentation Team
**Canonical Owner:** Documentation Governance Lead
**Last Verified:** 2026-08-02
**Version:** 1.0.0
**Status:** Active
**SSOT:** Real case study documentation
<!-- DOCUMENT_METADATA_END -->

## Audit Date: 2026-07-24

---

## Dataset Summary

| Metric | Value |
|--------|-------|
| Total Real Cases | 30 |
| MikroTik Cases | 10 |
| Cisco Cases | 10 |
| Fortinet Cases | 10 |

---

## Metadata Validation

All 30 cases have valid `expected.json` with:
> Terjemahan Indonesia: All 30 cases memiliki valid expected.json dengan:
- `vendor` field
- `expected` object with severity counts (critical, high, medium, low)
- `metadata` object with `description` and `tags`

---

## Configuration File Validation

All config files are readable text files in supported formats:
> Terjemahan Indonesia: All config files adalah readable text files dalam supported formats:
- MikroTik: `config.rsc` (RouterOS format)
- Cisco: `config.txt`
- Fortinet: `config.txt`

---

## Expected Findings Validation

Expected findings are derived from `metadata.tags` in `expected.json`:
> Terjemahan Indonesia: Expected findings adalah derived dari metadata.tags dalam expected.json:
- Tags map to expected finding strings via `_derive_expected_findings()`
- Tag-to-finding mapping includes: security, telnet, ssh, vpn, firewall, vlan, bgp, ospf, qos, nat, wireless, ha

---

## Structure Consistency

All cases follow consistent structure:
> Terjemahan Indonesia: Semua kasus mengikuti struktur yang konsisten:
```
real_cases/{vendor}/{case_name}/
â”œâ”€â”€ config.rsc OR config.txt
â””â”€â”€ expected.json
```

---

## Validation Status

| Status | Count |
|--------|-------|
| Valid | 30 |
| Invalid | 0 |

Ready for Gold Standard validation.
> Terjemahan Indonesia: Ready untuk Gold Standard validation.
