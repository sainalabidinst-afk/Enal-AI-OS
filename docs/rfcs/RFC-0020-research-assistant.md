# RFC-0020: Sertifikasi Research Assistant — Level 4 Domain Expert

<!-- DOCUMENT_METADATA_START -->
**Pemilik:** Tim Dokumentasi
**Pemilik Canonical:** Pimpinan Tata Kelola Dokumentasi
**Diverifikasi Terakhir:** 2026-08-05
**Versi:** 1.0.0
**Status:** Aktif
<!-- DOCUMENT_METADATA_END -->

|Bidang|Nilai|
|-------|-------|
|**ID RFC**|RFC-0020|
|**Status**|Draf|
|**Versi**|0.1.0|
|**Penulis**|Tim Inti AI OS Akhir|
|**Target Rilis**|v1.3.0 (fase Keunggulan Kemampuan)|
|**Capability Pack**|Asisten Peneliti|
|**ID Kemampuan**|`research-assistant`|
|**Kategori**|Penelitian|
|**Target Kualitas**|A+ (≥95)|
|**Target Kematangan**|Level 4 — Pakar Domain|
|**Referensi RFC**|RFC-0020|

---

## Motivasi

Capability Pack Research Assistant saat ini memiliki fondasi penelitian yang solid tetapi kedalaman domainnya masih terbatas pada sintesis dasar dan penilaian kualitas sitasi. Saat ini:

1. **Peringkat bukti terbatas** — Evidence Ranker menggunakan composite scoring sederhana tanpa mempertimbangkan metodologi penelitian secara mendalam.
2. **Deteksi kontradiksi terbatas** — Hanya mendeteksi konflik faktual, bukan metodologis atau interpretatif.
3. **Sintesis multi-sumber terbatas** — Tidak ada identifikasi area konsensus dan konflik secara eksplisit.
4. **Estimasi keyakinan terbatas** — Tidak ada kuantifikasi ketidakpastian yang komprehensif.
5. **Kepatuhan riset tidak diimplementasikan** — Tidak ada penilaian etik atau bias dalam penelitian.

RFC-0020 mengangkat Research Assistant ke Level 4 — Pakar Domain dengan fondasi metodologi penelitian yang lebih dalam, deteksi kontradiksi yang lebih canggih, dan estimasi keyakinan yang lebih akurat.

---

## Pernyataan Masalah

Tanpa sertifikasi Level 4:

- **Sintesis penelitian tidak dapat diandalkan** — Research Assistant hanya menggabungkan temuan tanpa menilai kualitas metodologi.
- **Kontradiksi tidak terdeteksi dengan baik** — Konflik metodologis dan interpretatif terlewatkan.
- **Keyakinan tidak terkuantifikasi** — Tidak ada ukuran ketidakpastian dalam temuan.
- **Bias penelitian tidak terdeteksi** — Tidak ada mekanisme untuk mengidentifikasi bias dalam sumber.
- **Kualitas sitasi tidak dinilai** — Tidak ada penilaian kualitas sitasi berdasarkan standar akademis.

---

## Tujuan

### 1. Peringkat Bukti Lanjutan
- **Metodologi penelitian** — Penilaian desain studi, sample size, kontrol
- **Kualitas jurnal** — Impact factor, peer review status
- **Kebaruan** — Weight berdasarkan tahun publikasi
- **Reproducibility** — Penilaian ketersediaan data dan kode

### 2. Deteksi Kontradiksi Lanjutan
- **Kontradiksi faktual** — Klaim yang bertentangan secara langsung
- **Kontradiksi metodologis** — Metode yang tidak sebanding
- **Kontradiksi interpretatif** — Interpretasi berbeda dari data yang sama
- **Kontradiksi temporal** — Temuan yang berubah seiring waktu

### 3. Estimasi Keyakinan Lanjutan
- **Kuantifikasi ketidakpastian** — Confidence intervals, standard error
- **Konsensus lintas sumber** — Agreement level antar sumber
- **Kualitas bukti** — Hierarchy of evidence (RCT > cohort > case control > case series)

### 4. Sintesis Lanjutan
- **Identifikasi area konsensus** — Temuan yang dikonfirmasi multi-sumber
- **Identifikasi area konflik** — Temuan yang bertentangan atau tidak konsisten
- **Gap Analysis** — Area yang belum diteliti secara memadai

### 5. Audit Keamanan
- **Bias detection** — Publication bias, selection bias, confirmation bias
- **PII redaction** — Deteksi dan redaksi informasi pribadi dalam sumber
- **Source verification** — Verifikasi kredibilitas sumber

---

## Dependensi

- RFC-0007 (Decision Intelligence) — Pipeline penalaran lintas domain
- RFC-0003 (Decorator SDK) — Plugin pattern untuk modul penelitian

---

## Kriteria Penerimaan

- Golden Test Suite: 10 skenario (sudah dibuat)
- Real Cases: 150 kasus di `real_cases/research/`
- Benchmark: ≥95% akurasi pada semua 6 dimensi
- Security Audit: OWASP Top 10, bias detection, PII redaction
- Performance: < 2s per query penelitian

---

## Referensi

- RFC-0003: Decorator SDK
- RFC-0007: Decision Intelligence
- CAPABILITY_GUIDE.md: Spesifikasi Capability Pack
