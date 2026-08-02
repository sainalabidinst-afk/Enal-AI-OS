# User Journeys

<!-- DOCUMENT_METADATA_START -->
**Pemilik:** Tim Dokumentasi
**Pemilik Canonical:** Pimpinan Tata Kelola Dokumentasi
**Terakhir Diverifikasi:** 2026-08-02
**Versi:** 1.0.0
**Status:** Aktif
**SSOT:** Dokumentasi untuk USER_JOURNEYS
<!-- DOCUMENT_METADATA_END -->

User journeys kanonikal untuk Enal AI OS.
Semua pekerjaan desain dan implementasi harus mempertahankan journeys ini.

Untuk spesifikasi UX lengkap, lihat `docs/UX_DESIGN.md`.

---

## Journey 1 — Network Engineer

**Tujuan:** Mengaudit konfigurasi MikroTik dan mendapatkan proposal perbaikan.

**Langkah:**
1. Buka Workspace
2. Unggah file `.rsc`
3. AI menganalisis konfigurasi
4. AI menyajikan findings: Critical, Warning, Suggestion
5. Pengguna menyetujui proposal perbaikan
6. AI menghasilkan konfigurasi yang diperbaiki
7. AI menjalankan test
8. AI menyajikan diff dan hasil test
9. Pengguna menyetujui deployment
10. AI men-deploy dengan rollback plan

**Yang dilihat pengguna:** Indikasi progress, findings terstruktur, proposal, diff, hasil test, konfirmasi deployment.
**Yang TIDAK dilihat pengguna:** Pemilihan Capability Pack, routing Worker, tahapan Execution Runtime, perencanaan task internal.

---

## Journey 2 — Code Engineer

**Tujuan:** Me-review sebuah proyek dan mendapatkan patch perbaikan.

**Langkah:**
1. Buka Workspace
2. Unggah ZIP proyek atau berikan repositori
3. AI menganalisis codebase
4. AI menyajikan findings: Security, Architecture, Dead Code
5. Pengguna menyetujui generasi patch
6. AI menghasilkan patch
7. AI menjalankan test
8. AI menyajikan patch dan hasil test
9. Pengguna menyetujui penerapan
10. AI menerapkan patch

**Yang dilihat pengguna:** Indikasi progress, findings terstruktur, patch, hasil test, konfirmasi penerapan.
**Yang TIDAK dilihat pengguna:** Detail parsing AST, pemilihan engine static analysis, konfigurasi test runner.

---

## Journey 3 — Trading Analyst

**Tujuan:** Menganalisis skenario pasar dan mendapatkan rekomendasi trading.

**Langkah:**
1. Buka Workspace
2. Berikan data pasar atau instrument
3. AI menganalisis struktur pasar
4. AI menyajikan bias, support/resistance, risiko
5. AI memberikan rekomendasi dengan reasoning
6. Pengguna dapat meminta skenario alternatif
7. AI menjelaskan risiko dan kasus kegagalan

**Yang dilihat pengguna:** Market bias, level kunci, penilaian risiko, rekomendasi dengan reasoning.
**Yang TIDAK dilihat pengguna:** Perhitungan indikator, pemilihan strategy library, internal debate engine.

---

## Journey 4 — Research Assistant

**Tujuan:** Meneliti sebuah topik dan mendapatkan ringkasan dengan sitasi.

**Langkah:**
1. Buka Workspace
2. Ajukan pertanyaan riset
3. AI mengambil sumber yang relevan
4. AI memeringkat kualitas evidence
5. AI mendeteksi kontradiksi antar sumber
6. AI menyintesis findings
7. AI menyajikan ringkasan dengan sitasi
8. Pengguna dapat meminta analisis lebih dalam

**Yang dilihat pengguna:** Ringkasan riset, sitasi dengan provenance, estimasi confidence, catatan kontradiksi.
**Yang TIDAK dilihat pengguna:** Detail retrieval RAG, skor similarity embedding, algoritma peringkat sumber.

---

## Journey 5 — Self Development

**Tujuan:** Mengaudit sebuah proyek dan menerapkan perbaikan.

**Langkah:**
1. Buka Workspace
2. Minta audit proyek
3. AI menganalisis struktur proyek
4. AI mengidentifikasi bottleneck dan isu
5. AI menyajikan findings dengan severity
6. Pengguna menyetujui proposal
7. AI menghasilkan patch
8. AI menjalankan test
9. AI menyajikan proposal, patch, dan hasil test
10. Pengguna menyetujui penerapan
11. AI menerapkan perubahan

**Yang dilihat pengguna:** Analisis proyek, daftar isu, proposal, patch diff, hasil test, konfirmasi penerapan.
**Yang TIDAK dilihat pengguna:** Internal analisis arsitektur, algoritma deteksi code smell, logika generasi patch.

---

## Journey 6 — Multi-Capability

**Tujuan:** Membangun ISP dari konsep hingga rencana deployment.

**Langkah:**
1. Pengguna mendeskripsikan tujuan dalam bahasa alami
2. AI mengklasifikasikan intent dan memilih beberapa Capability Pack
3. AI membuat rencana eksekusi
4. AI mengeksekusi setiap tahap:
   - Research: market dan best practices
   - Network: desain topologi
   - DevOps: rencana infrastruktur
   - Code: desain sistem billing
   - Self Development: proposal deployment
5. AI menyajikan rencana terintegrasi
6. Pengguna dapat menelusuri setiap section
7. Pengguna menyetujui rencana keseluruhan
8. AI mengeksekusi dengan indikasi progress

**Yang dilihat pengguna:** Satu rencana yang koheren, progress per tahap, hasil per capability, dokumentasi terintegrasi.
**Yang TIDAK dilihat pengguna:** Routing Capability Pack, komunikasi antar pack, logika dekomposisi task.

---

## Journey 7 — Goal Execution

**Tujuan:** Eksekusi end-to-end yang kompleks dari satu pernyataan tujuan.

**Langkah:**
1. Pengguna menyatakan tujuan: "Bangun aplikasi Inventory."
2. AI memahami tujuan dan memecahnya menjadi phase
3. AI menyajikan rencana eksekusi dengan estimasi
4. Pengguna menyetujui
5. AI mengeksekusi:
   - Requirement gathering
   - Architecture design
   - Database design
   - Backend implementation
   - Frontend implementation
   - Testing
   - Documentation
6. AI menampilkan progress real-time
7. AI mengirimkan hasil yang lengkap dan terverifikasi

**Yang dilihat pengguna:** Satu tujuan, satu rencana, satu hasil.
**Yang TIDAK dilihat pengguna:** Dekomposisi task, pemilihan worker, penjadwalan, retry, verification loop.

---

## Prinsip Desain

Semua journeys harus mengikuti prinsip-prinsip berikut:

1. **Satu percakapan:** Pengguna tidak pernah memilih Capability Pack secara manual.
2. **Tanpa eksposur internal:** Pengguna tidak pernah melihat Workers, Runtimes, Planners, atau struktur data internal.
3. **Transparansi progress:** Tugas berdurasi panjang menampilkan progress yang dapat dibaca manusia.
4. **Persetujuan sebelum tindakan:** Tindakan ireversibel memerlukan persetujuan eksplisit pengguna.
5. **Persistensi artifact:** Semua output signifikan disimpan dan dapat diambil kembali.
6. **Explainability sesuai permintaan:** Pengguna dapat bertanya "mengapa" kapan saja.

---

## Validasi

Setiap fitur atau perubahan baru harus divalidasi terhadap:
1. Apakah mempertahankan pengalaman satu percakapan?
2. Apakah menyembunyikan mekanisme internal dari pengguna?
3. Apakah menjaga transparansi progress?
4. Apakah menghormati workflow persetujuan?
5. Apakah mempersist artifacts?

Jika ada jawaban "tidak", fitur harus didesain ulang sebelum rilis.

