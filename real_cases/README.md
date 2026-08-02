# Kasus Nyata Dunia

<!-- DOCUMENT_METADATA_START -->
**Owner:** Documentation Team
**Canonical Owner:** Documentation Governance Lead
**Last Verified:** 2026-08-02
**Version:** 1.0.0
**Status:** Active
**SSOT:** Real case study documentation
<!-- DOCUMENT_METADATA_END -->

Direktori ini berisi kasus-kasus dunia nyata yang dikumpulkan selama penggunaan ECP dalam pekerjaan aktual.
Ini bukan golden test. Ini adalah artefak penggunaan harian yang mendorong peningkatan Capability Pack.

## Struktur

Setiap Capability Pack memiliki folder tersendiri:

```
real_cases/
├── network/           # Konfigurasi jaringan dan audit nyata
├── code/              # Basis kode yang ditinjau atau dibuat
├── research/          # Pertanyaan penelitian dan sumber nyata
├── trading/           # Skenario analisis pasar nyata
├── devops/            # Skenario infrastruktur nyata
└── self_development/  # Kasus perbaikan proyek nyata
```

## Apa yang Harus Disimpan

Untuk setiap kasus dunia nyata, buat folder dengan:

1. **Input**: Apa yang diberikan pengguna
2. **Output**: Apa yang dihasilkan ECP
3. **Evaluation**: Apa yang baik, apa yang salah, apa yang kurang
4. **Benchmark ID**: Tautan ke benchmark terkait jika diperbarui

Contoh:

```
network/isp_dual_wan_failover/
├── input/
│   └── config.rsc
├── output/
│   ├── analysis.md
│   └── recommendations.md
└── evaluation.md
```

## Cara Menggunakan

1. Jalankan ECP terhadap kasus nyata
2. Simpan input, output, dan evaluation
3. Jika diperlukan perbaikan, perbarui Capability Pack
4. Referensikan kasus ini dalam Capability Benchmark

Inilah cara Capability Pack menjadi benar-benar ahli: melalui iterasi dunia nyata, bukan hanya tes sintetis.
