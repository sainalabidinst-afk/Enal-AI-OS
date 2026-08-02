# ADR-002: Capability Pack Arsitektur


**Status:** ✅ Diterima
**Tanggal:** 2024
**Pengambilan Keputusan:** Kepala Arsitek, Tim Teknik

---

## Konteks

Platform ini perlu mendukung berbagai kemampuan domain tertentu (jaringan, pengkodean, penelitian, dll.) sambil mempertahankan inti yang stabil. Kemampuan ini harus:

- Dapat dikembangkan secara mandiri
- Dapat diuji secara independen
- Dapat dicolokkan ke sistem orkestrasi
- Konsisten dalam kontrak antarmuka mereka

---

## Keputusan

Atur fungsionalitas khusus domain ke dalam **Paket Kemampuan** di bawah `apps/`.

### Struktur

```
apps/
├── __init__.py          # Dynamic loader
├── base.py              # BaseApp abstract class
├── code_engineer/
├── network_engineer/
├── research_assistant/
├── devops_assistant/
├── trading_analyst/
└── self_development/
```

### Capability Pack Kontrak


Setiap paket harus dipaparkan:
1. Kelas yang diwariskan dari `BaseApp`
2. Fungsi pabrik `get_app()` tingkat modul
3. Daftar `pipeline` yang mendefinisikan tahapan saluran kognitif
4. Kemampuan yang diperlukan terdaftar di `skills.yaml`

---

## Alternatif yang Dipertimbangkan


|Alternatif|Alasan Ditolak|
|-------------|-----------------|
|Aplikasi tunggal monolitik|Melanggar kekhawatiran, sulit dipertahankan|
|Layanan mikro untuk kemampuan|Prematur — menambah kompleksitas kepatuhan tanpa terbukti diperlukan|
|Plugin hanya sistem|Plugin menginstalnya, paket kemampuan adalah warga negara kelas satu|

---

## Lanjutnya

- **Positif:** Batasan domain yang jelas, pengujian independen
- **Positif:** Pemuatan dinamis melalui `apps/__init__.py` untuk penemuan
- **Positif:** antarmuka yang konsisten melalui kelas abstrak `BaseApp`
- **Negatif:** Membutuhkan disiplin untuk menghindari penggabungan lintas paket
- **Negatif:** Pendaftaran paket harus disimpan di `skills.yaml`

---

## Kepatuhan

Semua kemampuan domain baru HARUS diimplementasikan sebagai Capability Pack di bawah `apps/`. Tidak ada logika domain dalam modul inti.
