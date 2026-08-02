# Kasus Nyata DevOps

<!-- DOCUMENT_METADATA_START -->
**Owner:** Documentation Team
**Canonical Owner:** Documentation Governance Lead
**Last Verified:** 2026-08-02
**Version:** 1.0.0
**Status:** Active
**SSOT:** Real case study documentation
<!-- DOCUMENT_METADATA_END -->

Skenario infrastruktur nyata yang ditemui saat menggunakan ECP.

## Template Kasus

Buat folder untuk setiap kasus:

```
<case_name>/
├── input/
│   └── requirements.md or infra_spec/
├── output/
│   ├── dockerfile
│   ├── ci_cd_config/
│   └── documentation.md
└── evaluation.md
```

## Contoh Kasus

- `microservice_deploy/` — Pipa deployment microservice
- `monitoring_setup/` — Konfigurasi monitoring dan alerting
- `kubernetes_migration/` — Rencana migrasi Kubernetes
- `cost_optimization/` — Optimasi biaya infrastruktur

## Template Evaluasi

```markdown
# Evaluation: <case_name>

Date: YYYY-MM-DD

## Ringkasan
Deskripsi singkat skenario infrastruktur.

## Apa yang Dijawab Benar oleh ECP
- Temuan 1
- Temuan 2

## Apa yang Dijawab Salah oleh ECP
- Temuan 1
- Temuan 2

## Apa yang Dilewatkan oleh ECP
- Konfigurasi yang kurang 1
- Best practice yang kurang 2

## Aksi Perbaikan
- [ ] Perbarui basis pengetahuan untuk X
- [ ] Tingkatkan pembuatan konfigurasi untuk Y
- [ ] Tambahkan pola multi-cloud untuk Z

Referensi Benchmark: ________
```
