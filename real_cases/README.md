# Kasus Nyata Dunia

<!-- DOCUMENT_METADATA_START -->
**Owner:** Documentation Team
**Canonical Owner:** Documentation Governance Lead
**Last Verified:** 2026-08-04
**Version:** 1.0.0
**Status:** Active
**SSOT:** Real case study documentation
<!-- DOCUMENT_METADATA_END -->

Direktori ini berisi kasus-kasus dunia nyata yang dikumpulkan selama penggunaan ECP dalam pekerjaan aktual.
Ini bukan golden test. Ini adalah artefak penggunaan harian yang mendorong peningkatan Capability Pack.

## Statistik

|Capability Pack|Total Kasus|Status|
|-----------------|----------|-------|
|Insinyur Jaringan|100|Siap Produksi|
|Kode Insinyur|100|Siap Produksi|
|Asisten Peneliti|150|Bersertifikat|
|Asisten DevOps|100|Bersertifikat|
|Analis Perdagangan|100|Bersertifikat|
|Pengembangan Diri|100|Bersertifikat|
|Decision Intelligence|100|Siap Produksi|
|Sistem Arsitek|100|Siap Produksi|
|Security Engineer|100|Siap Produksi|
|Data Engineer|100|Siap Produksi|
|Database Engineer|100|Siap Produksi|
|QA Engineer|100|Siap Produksi|
|Business Analyst|100|Siap Produksi|
|**Total**|**1,350**|**Fase 1 Complete**|

## Struktur

Setiap Capability Pack memiliki folder tersendiri:

```
real_cases/
├── network/           # Konfigurasi jaringan dan audit nyata
├── code/              # Basis kode yang ditinjau atau dibuat
├── research/          # Pertanyaan penelitian dan sumber nyata
├── trading/           # Skenario analisis pasar nyata
├── devops/            # Skenario infrastruktur nyata
├── self_development/  # Kasus perbaikan proyek nyata
├── decision/          # Kasus pengambilan keputusan
├── system/            # Desain arsitektur sistem
├── security/          # Audit keamanan
├── data/              # Pipeline data
├── database/          # Desain dan optimasi database
├── qa/                # Rencana dan eksekusi QA
└── business/          # Persyaratan bisnis
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

Kasus nyata digunakan untuk:
- Melatih dan mengevaluasi Capability Pack
- Mengidentifikasi area perbaikan
- Mendokumentasikan pola penggunaan
- Memberikan umpan balik untuk pengembangan

Setiap kasus dievaluasi berdasarkan:
- Akurasi temuan
- Kualitas rekomendasi
- Kebermanfaatan praktis
- Potensi untuk perbaikan
