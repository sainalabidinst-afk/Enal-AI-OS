<!-- DOCUMENT_METADATA_START -->
**Pemilik:** Tim Dokumentasi
**Pemilik Canonical:** Pimpinan Tata Kelola Dokumentasi
**Terakhir Diverifikasi:** 02-08-2026
**Versi:** 1.0.0
**Status:** Aktif
**SSOT:** Peta jalan strategis, siklus hidup Capability Pack, dan jadwal rilis
<!-- DOCUMENT_METADATA_END -->

# Piagam Tata Kelola ECP — v1.0.0-dev

> **Status:** Dokumen ini telah direstrukturisasi menjadi dokumen strategis yang terfokus.
> Sekarang berfungsi sebagai halaman arahan dan indeks ke rangkaian dokumentasi ECP.

**Target Rilis:** Q3 2026
**Status:** Dalam Pengembangan
**Sasaran:** Platform ECP selesai. Fase berikutnya adalah Keunggulan Kemampuan — menjadikan setiap Capability Pack benar-benar ahli dalam bidangnya.

---

## Filsafat Inti

> **Core tidak lagi menjadi tempat berkembangnya fitur; Core menjadi platform yang stabil, sedangkan Capability Pack menjadi tempat inovasi.**

Prinsip ini adalah fondasi arsitektur ECP:

- **Core** penahanan — stabil, kompatibel ke belakang, tidak ada ketergantungan eksternal selain stdlib + pydantic
- **Capability Pack** berkembang — tempat inovasi, perluasan pengetahuan, dan keahlian domain
- **Governance** aktif — semua perubahan diatur oleh ADR, Capability First Rule, dan Architecture Freeze Policy

---

## Piagam Pemerintahan

Dokumen ini adalah **dokumen konstitusi (governance charter)** proyek ECP. Artinya:

- Semua RFC harus konsisten dengan dokumen ini.
- Semua ADR harus Merujuk dokumen ini.
- Semua Capability Pack harus memenuhi aturan di dokumen ini sebelum dianggap siap rilis.
- CI/CD dapat menambahkan pemeriksaan agar perubahan yang melanggar aturan tata kelola (misalnya perubahan Core tanpa ADR) gagal sebelum penggabungan.

---

## Indeks Dokumen

Dokumen ini telah terpecah menjadi 5 dokumen strategi berikut:

|Dokumen|Tujuan|SSOT Untuk|
|----------|---------|----------|
|`docs/GOVERNANCE_CHARTER.md`|Visi, filosofi, aturan konstitusi|Visi, filosofi, aturan konstitusional|
|`docs/GOVERNANCE.md`|Aturan operasional — ADR, Capability First, Architecture Freeze, penegakan hukum|Aturan operasional|
|`docs/RELEASE_CRITERIA.md`|Kondisi pelepasan, Departemen Pertahanan, gerbang kualitas|Syarat rilis, DoD, gerbang kualitas|
|`docs/CAPABILITY_STRATEGY.md`|Capability Pack profil, kedewasaan, siklus hidup|Profil, kematangan, siklus hidup Capability Pack|
|`docs/ROADMAP.md`|Timeline, target rilis, visi jangka panjang|Timeline, target rilis, visi jangka panjang|
|`docs/DOCUMENT_STRUCTURE.md`|Fungsi dan SSOT setiap dokumen strategis|Pemetaan dokumen|

---

## Referensi Cepat

### Kriteria Keberhasilan (v1.0.0-dev)

1. ✅ **13 Paket Kemampuan** ada dan terdaftar di Grafik Kemampuan
2. ✅ **Golden Test Suite** tiket dengan tingkat kelulusan ≥80%.
3. ✅ Blok **CI/CD Pipeline** bergabung jika terjadi kegagalan
4. ✅ **Dokumentasi** mencakup permulaan, SDK, kontrak, dan Arsitektur
5. ✅ **Tanpa Jebakan Kerangka Kerja** — Inti tetap stabil saat Paket Kemampuan berevolusi
6. ✅ **Tata Kelola Arsitektur** aktif: Inti dibekukan, Aturan Kapabilitas Pertama diberlakukan, semua perubahan memerlukan ADR ketika memengaruhi beberapa paket

### Ikhtisar Paket Kemampuan

|Kemampuan|Kategori|Sasaran Mutu|
|------------|----------|----------------|
|Insinyur Jaringan|Jaringan|SEBUAH (≥90)|
|Insinyur Kode|Perkembangan|SEBUAH- (≥85)|
|Asisten Peneliti|Riset|SEBUAH- (≥85)|
|Asisten DevOps|DevOps|A+ (≥90) — Bersertifikat|
|Analis Perdagangan|Keuangan|A (≥90) — Bersertifikat|
|Pengembangan Diri|Platform|SEBUAH (≥90)|
|Decision Intelligence|Platform — Penalaran Bersama|A (91,25%) — RFC-0007|
|Arsitek Sistem|Arsitektur|SEBUAH (≥90) — RFC-0011|
|Security Engineer|Keamanan|SEBUAH- (≥85) — RFC-0008|
|Data Engineer|Data|A- (≥85) — RFC-0009|
|Database Engineer|Basis data|SEBUAH- (≥85) — RFC-0010|
|QA Engineer|Jaminan Kualitas|SEBUAH (≥90) — RFC-0012|
|Business Analyst|Analisis Bisnis|SEBUAH- (≥85) — RFC-0013|

### Model Kematangan Kemampuan

|Tingkat|Label|Keterangan|
|-------|-------|-------------|
|1|**Eksperimental**|Prototipe konsep, belum siap produksi|
|2|**Fungsional**|Berfungsi untuk skenario dasar, batasan yang diketahui|
|3|**Produksi Siap**|Lulus tolok ukur, terdokumentasi, stabil|
|4|**Pakar Domain**|Pengetahuan mendalam, multi-vendor, multi-domain|
|5|**Bersertifikat**|Implementasi referensi yang diaudit, dijadikan tolok ukur|
|6|**Kemampuan Referensi**|Industri Benchmark untuk domain|

### Siklus Hidup Kemampuan

```
Proposal → RFC → Prototype → Experimental → Stable → Certified → Maintenance → Deprecated
```

### Garis Waktu Rilis

|Melepaskan|Target|Fokus|
|---------|--------|-------|
|v1.0.0-pengembangan|Q3 2026|Platform selesai, Tata Kelola Arsitektur aktif|
|v1.0.0|Q4 2026|Pratinjau Pengembang: semua paket bersertifikat|
|v1.1.0|Q1 2027|Keunggulan Kemampuan: naikkan semua paket satu tingkat|
|v1.2.0|Q2 2027|Ekosistem Komunitas: Pasar|
|v1.3.0|Q3 2027|Perusahaan: tata kelola, multi-penyewa, SLA|

---

## Dokumen Terkait

|Dokumen|Lokasi|
|----------|----------|
|Keputusan Arsitektur (ADR)|`ARCHITECTURE_DECISIONS.md`|
|Kontrak Produk|`docs/PRODUCT_CONTRACT.md`|
|Panduan Kemampuan (spesifikasi detail)|`docs/CAPABILITY_GUIDE.md`|
|Status Gerbang Kualitas|`docs/QUALITY_GATE.md`|
|Proses RFC|`docs/rfcs/README.md`|
|Ikhtisar Arsitektur|`docs/architecture.md`|
|Pembekuan Dasar|`docs/baseline_freeze.md`|
