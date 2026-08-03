<!-- DOCUMENT_METADATA_START -->
**Pemilik:** Tim Dokumentasi
**Pemilik Canonical:** Pimpinan Tata Kelola Dokumentasi
**Diverifikasi Terakhir:** 08-02-2026
**Versi:** 1.0.0
**Status:** Aktif
**SSOT:** Kondisi rilis, gerbang kualitas, Definisi Selesai, dan target Benchmark
<!-- DOCUMENT_METADATA_END -->

# Kriteria Rilis ECP

**Versi:** 1.0.0
**Berlaku:** 02-08-2026
**Induk:** `GOVERNANCE_CHARTER.md`
**Tujuan:** Mendefinisikan kondisi rilis, quality gate, dan Definition of Done untuk rilis ECP dan Capability Pack.

---

## 1. Kriteria Keberhasilan — v1.0.0-dev

ECP v1.0.0-dev dinyatakan berhasil jika dan hanya jika:

1. ✅ **13 Capability Pack** ada dan terdaftar di Capability Graph
2. ✅ **Golden Test Suite** lulus dengan tingkat kelulusan ≥80%
3. ✅ **CI/CD Pipeline** penyumbatan pada setiap kegagalan
4. ✅ **Dokumentasi** mencakup permulaan, SDK, kontrak, dan Arsitektur
5. ✅ **Tanpa Kerangka Perangkap** — Inti tetap stabil sementara Capability Pack berevolusi
6. ✅ **Architecture Governance** aktif: Core terhenti, Capability First Rule ditegakkan, semua perubahan memerlukan ADR ketika berdampak pada banyak paket

---

## 2. Golden Test Set

Golden Test Suite (`benchmarks/golden_test_set.py`) berisi:

- 50 tugas sederhana (penalaran dasar, coding, penjelasan)
- 50 tugas menengah (desain API, skema database, konfigurasi)
- 50 tugas kompleks (aplikasi full-stack, sistem terdistribusi)
- 50 tugas spesifik-domain (jaringan, perdagangan, DevOps, penelitian, pengembangan diri)

**Ambang Lulus:** ≥80% (tes 160/200)

---

## 3. Pipa CI/CD

Setiap PR harus lulus:

1. **Serat & Format** — ruff + hitam
2. **Type Check** — mypy dengan mode ketat
3. **Unit Tests** — pytest dengan cakupan ≥80%
4. **Uji Arsitektur** — penegakan batasan paket
5. **Benchmark** — Benchmark kinerja dan kualitas
6. **SDK Kompatibilitas** — impor dan fungsionalitas dasar
7. **Plugin Kompatibilitas** — semua Plugin dimuat dengan benar
8. **Tes Emas** — Golden Test Suite lengkap
9. **Pemeriksaan Tata Kelola** — Penjaga perubahan inti, referensi ADR, Capability First (lihat `GOVERNANCE.md`)

**Kebijakan Penggabungan:** Semua pemeriksaan harus lulus. Tanpa mengungkapkan.

---

## 4. Metrik yang Dilacak

|Metrik|Target|pengukuran|
|--------|--------|-------------|
|Golden Test Tingkat Kelulusan|≥80%|Benchmark/golden_test_set.py|
|Cakupan Tes|≥80%|pytest-cov|
|Ketik Keamanan|0 kesalahan|mypy --ketat|
|Pelanggaran Arsitektur|0|Benchmark/package_boundaries.py|
|SDK Waktu Impor|<100 md|SDK/tolok ukur|
|Angka Mutu kemampuan|≥85%|Benchmark/capability_benchmark.py|
|Kecepatan Peningkatan|>0 kasus nyata/minggu per bungkus|kasus_nyata/<capability_id>/|
|Cakupan Dokumentasi|100%|dokumen/|

---

## 5. Pratinjau Pengembang Target Kualitas

Sertifikasi mewajibkan setiap Capability Pack mencapai atau melampaui skor Benchmark berikut:

|Kemampuan|Skor Sasaran|Nilai|
|------------|--------------|-------|
|Insinyur Jaringan|≥90|A|
|Kode Insinyur|≥85|A-|
|Asisten Peneliti|≥85|A-|
|Asisten DevOps|≥90|A+|
|Analis Perdagangan|≥90|A (Bersertifikat)|
|Pengembangan Diri|≥90|A|
|Decision Intelligence|≥90|A (Benchmark 91,25% — RFC-0007)|
|Sistem Arsitek|≥90|A (RFC-0011)|
|Security Engineer|≥85|SEBUAH- (RFC-0008)|
|Data Engineer|≥85|SEBUAH- (RFC-0009)|
|Database Engineer|≥85|SEBUAH- (RFC-0010)|
|QA Engineer|≥90|A (RFC-0012)|
|Business Analyst|≥85|SEBUAH- (RFC-0013)|

Semua skor diukur oleh kerangka Kapabilitas Benchmark 6 dimensi (Akurasi, Kelengkapan, Penjelasan, Keamanan, Efisiensi, Konsistensi).

---

## 6. Definisi Selesai — Templat Standar

Definisi Selesai setiap Capability Pack menggunakan template standar ini. Sebuah paket berisi nilai spesifiknya.

```text
Definition of Done

Functional
- [ ] <persyaratan fungsional>

Benchmark
- [ ] Skor benchmark ≥ <ambang> (grade <grade>)

Golden Tests
- [ ] Semua skenario Golden Test pack lulus (100%)

Real Cases
- [ ] ≥ <N> kasus nyata dicatat di real_cases/<capability_id>/
- [ ] Catatan evaluasi direkam untuk setiap kasus

Documentation
- [ ] Capability Guide diperbarui
- [ ] Referensi API / kontrak diperbarui

SDK
- [ ] Pack dapat diakses melalui SDK tanpa perubahan Core

Performance
- [ ] Respons dalam anggaran latensi target

Security
- [ ] Tidak ada masalah keamanan P0/P1 yang diketahui

Regression
- [ ] Tidak ada regresi pada dimensi benchmark yang ada
- [ ] Benchmark reproducible (perintah terdokumentasi + hasil tersimpan)

Release Notes
- [ ] Capability Changelog diperbarui
```

---

## 7. Definisi Selesai per Capability Pack

### 7.1 Insinyur Jaringan

|Barang Departemen Pertahanan|Kriteria|
|----------|-----------|
|Emas Benchmark|akurasi ≥95% (kelas A)|
|Kasus Nyata|≥100 kasus nyata di `real_cases/network/`|
|regresi|Tidak ada regresi di seluruh 6 dimensi Benchmark|
|Dokumentasi|`CAPABILITY_GUIDE.md` dan kontrak diperbarui|
|Reproduksibilitas|Benchmark dapat diproduksi melalui perintah terdokumentasi; hasil tersimpan|
|mencatat perubahan|Kemampuan Changelog diperbarui|

### 7.2 Kode Insinyur

|Barang Departemen Pertahanan|Kriteria|
|----------|-----------|
|Emas Benchmark|≥90% skor kualitas kode|
|Kasus Nyata|≥100 repositori nyata di `real_cases/code/`|
|regresi|Tidak ada regresi di seluruh 6 dimensi Benchmark|
|Dokumentasi|`CAPABILITY_GUIDE.md` dan kontrak diperbarui|
|Reproduksibilitas|Benchmark dapat diproduksi; hasil tersimpan|
|mencatat perubahan|Kemampuan Changelog diperbarui|

### 7.3 Asisten Peneliti

|Barang Departemen Pertahanan|Kriteria|
|----------|-----------|
|Emas Benchmark|≥85% akurasi sitasi|
|Kasus Nyata|≥100 pertanyaan penelitian di `real_cases/research/`|
|regresi|Tidak ada regresi di seluruh 6 dimensi Benchmark|
|Dokumentasi|`CAPABILITY_GUIDE.md` dan kontrak diperbarui|
|Reproduksibilitas|Benchmark dapat diproduksi; hasil tersimpan|
|mencatat perubahan|Kemampuan Changelog diperbarui|

### 7.4 Asisten DevOps

|Barang Departemen Pertahanan|Kriteria|
|----------|-----------|
|Emas Benchmark|≥85% kebenaran pada konfigurasi yang dihasilkan|
|Kasus Nyata|≥100 skenario infrastruktur di `real_cases/devops/`|
|regresi|Tidak ada regresi di seluruh 6 dimensi Benchmark|
|Dokumentasi|`CAPABILITY_GUIDE.md` dan kontrak diperbarui|
|Reproduksibilitas|Benchmark dapat diproduksi; hasil tersimpan|
|mencatat perubahan|Kemampuan Changelog diperbarui|

### 7.5 Analis Perdagangan

|Barang Departemen Pertahanan|Kriteria|
|----------|-----------|
|Emas Benchmark|≥80% (kelas B+) dan Sertifikasi lulus|
|Kasus Nyata|≥100 skenario pasar di `real_cases/trading/`|
|regresi|Tidak ada regresi di seluruh 6 dimensi Benchmark|
|Dokumentasi|`CAPABILITY_GUIDE.md` dan kontrak diperbarui|
|Reproduksibilitas|Benchmark dapat diproduksi; hasil tersimpan|
|mencatat perubahan|Kemampuan Changelog diperbarui|

### 7.6 Pengembangan Diri

|Barang Departemen Pertahanan|Kriteria|
|----------|-----------|
|Emas Benchmark|≥90% (kelas A)|
|Kasus Nyata|≥10 proyek nyata di `real_cases/self_development/`|
|regresi|Tidak ada regresi di seluruh 6 dimensi Benchmark|
|Dokumentasi|`CAPABILITY_GUIDE.md` dan kontrak diperbarui|
|Reproduksibilitas|Benchmark dapat diproduksi; hasil tersimpan|
|mencatat perubahan|Kemampuan Changelog diperbarui|

### 7.7 Decision Intelligence

|Barang Departemen Pertahanan|Kriteria|
|----------|-----------|
|Emas Benchmark|≥90% (kelas A — Benchmark total 91,25%)|
|Kasus Nyata|(Lapisan pemikiran bersama — kasus nyata dilacak per bungkus konsumen)|
|regresi|Tidak ada regresi di seluruh 8 dimensi Benchmark|
|Dokumentasi|`docs/capabilities/decision-intelligence.md` diperbarui|
|Reproduksibilitas|Benchmark dapat diproduksi melalui `benchmarks/decision_intelligence_benchmark.py`; hasil tersimpan|
|mencatat perubahan|Kemampuan Changelog diperbarui|

### 7.8 Sistem Arsitek

|Barang Departemen Pertahanan|Kriteria|
|----------|-----------|
|Emas Benchmark|≥90% (kelas A)|
|Kasus Nyata|Kasus nyata dilacak melalui riwayat arsitektur review di `real_cases/system_architect/`|
|regresi|Tidak ada regresi di seluruh 8 dimensi Benchmark|
|Dokumentasi|`docs/capabilities/system-architect.md` dan `docs/CAPABILITY_GUIDE.md` diperbarui|
|Reproduksibilitas|Benchmark dapat diproduksi melalui `benchmarks/system_architect_benchmark.py`; hasil tersimpan|
|mencatat perubahan|Kemampuan Changelog diperbarui|

### 7.9 Security Engineer

|Barang Departemen Pertahanan|Kriteria|
|----------|-----------|
|Emas Benchmark|≥85% (kelas A-)|
|Kasus Nyata|≥20 kasus analisis keamanan di `real_cases/security_engineer/`|
|regresi|Tidak ada regresi di seluruh 9 dimensi Benchmark|
|Dokumentasi|`docs/capabilities/security-engineer.md` dan `docs/CAPABILITY_GUIDE.md` diperbarui|
|Reproduksibilitas|Benchmark dapat diproduksi melalui `benchmarks/security_engineer_benchmark.py`; hasil tersimpan|
|mencatat perubahan|Kemampuan Changelog diperbarui|

### 7.10 Data Engineer

|Barang Departemen Pertahanan|Kriteria|
|----------|-----------|
|Emas Benchmark|≥85% (kelas A-)|
|Kasus Nyata|≥20 kasus pipa data di `real_cases/data_engineer/`|
|regresi|Tidak ada regresi di seluruh 8 dimensi Benchmark|
|Dokumentasi|`docs/capabilities/data-engineer.md` dan `docs/CAPABILITY_GUIDE.md` diperbarui|
|Reproduksibilitas|Benchmark dapat diproduksi melalui `benchmarks/data_engineer_benchmark.py`; hasil tersimpan|
|mencatat perubahan|Kemampuan Changelog diperbarui|

### 7.11 Database Engineer

|Barang Departemen Pertahanan|Kriteria|
|----------|-----------|
|Emas Benchmark|≥85% (kelas A-)|
|Kasus Nyata|≥20 analisis database kasus di `real_cases/database_engineer/`|
|regresi|Tidak ada regresi di seluruh 8 dimensi Benchmark|
|Dokumentasi|`docs/capabilities/database-engineer.md` dan `docs/CAPABILITY_GUIDE.md` diperbarui|
|Reproduksibilitas|Benchmark dapat diproduksi melalui `benchmarks/database_engineer_benchmark.py`; hasil tersimpan|
|mencatat perubahan|Kemampuan Changelog diperbarui|

### 7.12 QA Engineer

|Barang Departemen Pertahanan|Kriteria|
|----------|-----------|
|Emas Benchmark|≥90% (kelas A)|
|Kasus Nyata|≥20 kasus analisis QA di `real_cases/qa_engineer/`|
|regresi|Tidak ada regresi di seluruh 9 dimensi Benchmark|
|Dokumentasi|`docs/capabilities/qa-engineer.md` dan `docs/CAPABILITY_GUIDE.md` diperbarui|
|Reproduksibilitas|Benchmark dapat diproduksi melalui `benchmarks/qa_engineer_benchmark.py`; hasil tersimpan|
|mencatat perubahan|Kemampuan Changelog diperbarui|

### 7.13 Business Analyst

|Barang Departemen Pertahanan|Kriteria|
|----------|-----------|
|Emas Benchmark|≥85% (kelas A-)|
|Kasus Nyata|≥20 analisis kasus bisnis di `real_cases/business_analyst/`|
|regresi|Tidak ada regresi di seluruh 9 dimensi Benchmark|
|Dokumentasi|`docs/capabilities/business-analyst.md` dan `docs/CAPABILITY_GUIDE.md` diperbarui|
|Reproduksibilitas|Benchmark dapat diproduksi melalui `benchmarks/business_analyst_benchmark.py`; hasil tersimpan|
|mencatat perubahan|Kemampuan Changelog diperbarui|

---

## 8. Pemahaman Selesai Rilis

Sebuah rilis dinyatakan selesai ketika:

- [ ] Semua Capability Pack target memenuhi Definisi Selesai mereka (Bagian 7)
- [ ] Golden Test Suite ≥80% (160/200)
- [ ] Tes Cakupan ≥80%
- [ ] mypy --strict: 0 kesalahan
- [ ] Pelanggaran arsitektur: 0
- [ ] Semua pemeriksaan tata kelola lulus (Core change guard, referensi ADR)
- [ ] Catatan rilis dan changelog diperbarui
- [ ] Metrik dicatat dan hasil Benchmark disimpan

---

## 9. Tinjauan Pasca-Rilis

Setelah setiap rilis:

1. Bandingkan skor Benchmark aktual vs target.
2. Katat pembelajaran ke dalam siklus Pembelajaran Berkelanjutan.
3. memperbarui tabel nilai `CAPABILITY_STRATEGY.md`.
4. perbarui `ROADMAP.md` berdasarkan kecepatan aktual.

---

## 10. Persetujuan

|Peran|Status|Tanggal|
|------|--------|------|
|Kepala Bagian Produk|Disetujui|08-02-2026|
