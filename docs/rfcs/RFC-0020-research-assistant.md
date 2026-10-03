# RFC-0020: Sertifikasi Research Assistant — Level 4 Domain Expert

<!-- DOCUMENT_METADATA_START -->
**Pemilik:** Tim Dokumentasi
**Pemilik Canonical:** Pimpinan Tata Kelola Dokumentasi
**Diverifikasi Terakhir:** 2026-10-02
**Versi:** 1.1.0
**Status:** Aktif
<!-- DOCUMENT_METADATA_END -->

|Bidang|Nilai|
|-------|-------|
|**ID RFC**|RFC-0020|
|**Status**|Diterima — Level 4 Domain Expert (A+)|
|**Versi**|1.1.0|
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

Capability Pack Research Assistant memiliki fondasi penelitian yang solid dengan kedalaman domain yang telah ditingkatkan ke Level 4. RFC-0020 mengangkat Research Assistant ke Level 4 — Pakar Domain dengan fondasi metodologi penelitian yang lebih dalam, deteksi kontradiksi yang lebih canggih, dan estimasi keyakinan yang lebih akurat.

Saat ini:
1. **Peringkat bukti lanjutan** — Evidence Ranker menggunakan composite scoring dengan mempertimbangkan metodologi penelitian.
2. **Deteksi kontradiksi lanjutan** — Mendeteksi konflik faktual, metodologis, dan interpretatif.
3. **Sintesis multi-sumber** — Identifikasi area konsensus dan konflik secara eksplisit.
4. **Estimasi keyakinan** — Kuantifikasi ketidakpastian secara komprehensif.
5. **Kepatuhan riset** — Penilaian etik, bias, dan PII redaction.

---

## Pernyataan Masalah

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

- Golden Test Suite: 10 skenario
- Real Cases: 150 kasus di `real_cases/research/`
- Benchmark: `benchmarks/research_assistant_benchmark.py` — ≥95% akurasi pada semua 6 dimensi (A+ certifikat)
- Security Audit: OWASP Top 10, bias detection, PII redaction
- Performance: < 2s per query penelitian

---

## Definisi Selesai

```text
Definition of Done — Research Assistant Certification RFC

Functional
- [x] Evidence Ranker with methodology assessment
- [x] Contradiction detection (factual, methodological, interpretative)
- [x] Multi-source synthesis with consensus/conflict identification
- [x] Confidence estimation with uncertainty quantification
- [x] Security audit: bias detection, PII redaction, source verification
- [x] RAG-powered research with citation quality scoring

Benchmark
- [x] ≥95% accuracy on all 6 dimensions (A+)
- [x] 150+ real cases in real_cases/research/
- [x] Golden test suite: 10 scenarios passing
- [x] Performance: < 2s per query

Documentation
- [x] Capability guide: docs/capabilities/research-assistant.md
- [x] Benchmark dashboard: benchmarks/dashboards/research_assistant_dashboard.html
- [x] Contract schemas: apps/research_assistant/schemas.py

Regression
- [x] No regression in existing capability pack dimensions
- [x] Benchmark reproducible (documented command + persisted result)

Release Notes
- [x] Capability Changelog updated
```

---

## Referensi

- RFC-0003: Decorator SDK
- RFC-0007: Decision Intelligence
- CAPABILITY_GUIDE.md: Spesifikasi Capability Pack
