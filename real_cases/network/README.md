# Kasus Nyata Jaringan

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

## Ringkasan
Deskripsi singkat kasus.

## Apa yang Dijawab Benar oleh ECP
- Temuan 1
- Temuan 2

## Apa yang Dijawab Salah oleh ECP
- Temuan 1
- Temuan 2

## Apa yang Dilewatkan oleh ECP
- Temuan yang kurang 1
- Temuan yang kurang 2

## Aksi Perbaikan
- [ ] Perbarui analyzer untuk X
- [ ] Tingkatkan rekomendasi untuk Y
- [ ] Tambahkan aturan baru untuk Z

Referensi Benchmark: ________
```
