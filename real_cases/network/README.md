# Network Real Cases

<!-- DOCUMENT_METADATA_START -->
**Owner:** Documentation Team
**Canonical Owner:** Documentation Governance Lead
**Last Verified:** 2026-08-02
**Version:** 1.0.0
**Status:** Active
**SSOT:** Real case study documentation
<!-- DOCUMENT_METADATA_END -->

Konfigurasi jaringan dan skenario audit nyata yang ditemui saat menggunakan ECP.

## Template Kasus

Buat folder untuk setiap kasus:

```
<case_name>/
├── input/
│   └── config.rsc
├── output/
│   ├── analysis.md
│   └── recommendations.md
└── evaluation.md
```

## Contoh Kasus

- `isp_dual_wan_failover/` — Dual WAN dengan aturan failover
- `mikrotik_hotspot_school/` — Hotspot sekolah dengan VLAN dan manajemen pengguna
- `campus_vlan/` — Jaringan kampus dengan banyak VLAN dan routing antar-VLAN
- `enterprise_firewall/` — Tinjauan kebijakan firewall enterprise

## Template Evaluasi

```markdown
# Evaluation: <case_name>

Date: YYYY-MM-DD

## Summary
Deskripsi singkat kasus.

## What ECP Got Right
- Temuan 1
- Temuan 2

## What ECP Got Wrong
- Temuan 1
- Temuan 2

## What ECP Missed
- Temuan yang kurang 1
- Temuan yang kurang 2

## Improvement Actions
- [ ] Perbarui analyzer untuk X
- [ ] Tingkatkan rekomendasi untuk Y
- [ ] Tambahkan aturan baru untuk Z

Benchmark Reference: ________
```
