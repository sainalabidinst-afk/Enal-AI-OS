# Perjalanan Pengguna

<!-- DOCUMENT_METADATA_START -->
**Pemilik:** Tim Dokumentasi
**Pemilik Canonical:** Pimpinan Tata Kelola Dokumentasi
**Diverifikasi Terakhir:** 02-08-2026
**Versi:** 1.0.0
**Status:** Aktif
**SSOT:** Dokumentasi untuk USER_JOURNEYS
<!-- DOCUMENT_METADATA_END -->

Perjalanan pengguna kanonikal untuk Enal AI OS.
Semua pekerjaan desain dan implementasi harus mempertahankan perjalanan ini.

Untuk spesifikasi UX lengkap, lihat `docs/UX_DESIGN.md`.

---

## Perjalanan 1 - Insinyur Jaringan

**Tujuan:** Mengaudit konfigurasi MikroTik dan mendapatkan proposal perbaikan.

**Langkah:**
1. Buka Ruang Kerja
2. Unggah file `.rsc`
3. AI menganalisis konfigurasi
4. AI menyajikan temuan: Kritis, Peringatan, Saran
5. Pengguna menyetujui proposal perbaikan
6. AI menghasilkan konfigurasi yang diperbaiki
7. AI menjalankan tes
8. AI menyajikan uji perbedaan dan hasil
9. Pengguna menyetujui penerapan
10. AI men-deploy dengan rencana rollback

**Yang dilihat pengguna:** Indikasi kemajuan, temuan terstruktur, proposal, perbedaan, hasil pengujian, konfirmasi penerapan.
**Yang TIDAK dilihat pengguna:** Pemilihan Capability Pack, routing Worker, tahapan Execution Runtime, perencanaan tugas internal.

---

## Perjalanan 2 - Insinyur Kode

**Tujuan:** Me-review sebuah proyek dan mendapatkan perbaikan patch.

**Langkah:**
1. Buka Ruang Kerja
2. Unggah proyek ZIP atau berikan repositori
3. AI menganalisis basis kode
4. AI menyajikan temuan: Keamanan, Arsitektur, Kode Mati
5. Pengguna menyetujui generasi patch
6. AI menghasilkan tambalan
7. AI menjalankan tes
8. AI menyajikan patch dan hasil test
9. Pengguna menyetujui penerapan
10. AI menerapkan patch

**Yang dilihat pengguna:** Indikasi kemajuan, temuan terstruktur, patch, hasil pengujian, konfirmasi penerapan.
**Yang TIDAK dilihat pengguna:** Detail parsing AST, pemilihan mesin analisis statis, konfigurasi test runner.

---

## Perjalanan 3 — Analis Perdagangan

**Tujuan:** Menganalisis skenario pasar dan mendapatkan rekomendasi trading.

**Langkah:**
1. Buka Ruang Kerja
2. Berikan data pasar atau instrumen
3. AI menganalisis struktur pasar
4. AI menyajikan bias, support/resistance, risiko
5. AI memberikan rekomendasi dengan penalaran
6. Pengguna dapat meminta skenario alternatif
7. AI menjelaskan risiko dan kasus kegagalan

**Yang dilihat pengguna:** Bias pasar, level kunci, penilaian risiko, rekomendasi dengan penalaran.
**Yang TIDAK dilihat pengguna:** Indikator perhitungan, perpustakaan strategi pemilihan, mesin debat internal.

---

## Perjalanan 4 - Asisten Peneliti

**Tujuan:** Meneliti sebuah topik dan mendapatkan ringkasan dengan sitasi.

**Langkah:**
1. Buka Ruang Kerja
2. Ajukan pertanyaan penelitian
3. AI mengambil sumber yang relevan
4. AI memberikan bukti kualitas
5. AI mendeteksi keberadaan antar sumber
6. Temuan AI menyintesis
7. AI menyajikan ringkasan dengan sitasi
8. Pengguna dapat meminta analisis lebih dalam

**Yang dilihat pengguna:** Ringkas penelitian, sitasi dengan asal usul, estimasi keyakinan, catatan sepanjang masa.
**Yang TIDAK dilihat pengguna:** Detail retrieval RAG, skor kesamaan embedding, algoritma peringkat sumber.

---

## Perjalanan 5 - Pengembangan Diri

**Tujuan:** Mengaudit sebuah proyek dan menerapkan perbaikan.

**Langkah:**
1. Buka Ruang Kerja
2. Minta audit proyek
3. AI menganalisis struktur proyek
4. AI mengidentifikasi kemacetan dan isu
5. AI menyajikan temuan dengan tingkat keparahan
6. Pengguna menyetujui usulan
7. AI menghasilkan tambalan
8. AI menjalankan tes
9. AI menyajikan proposal, patch, dan hasil test
10. Pengguna menyetujui penerapan
11. AI menerapkan perubahan

**Yang dilihat pengguna:** Analisis proyek, daftar isu, proposal, patch diff, hasil test, konfirmasi penerapan.
**Yang TIDAK dilihat pengguna:** Arsitektur analisis internal, algoritma deteksi bau kode, logika generasi patch.

---

## Perjalanan 6 — Multi-Kapabilitas

**Tujuan:** Membangun ISP dari konsep hingga rencana penerapan.

**Langkah:**
1. Pengguna mendeskripsikan tujuan dalam bahasa alami
2. AI mengklasifikasikan niat dan memilih beberapa Capability Pack
3. AI membuat rencana eksekusi
4. AI mengeksekusi setiap tahap:
   - Riset: pasar dan praktik terbaik
   - Jaringan: desain topologi
   - DevOps: rencana infrastruktur
   - Kode : desain sistem billing
   - Pengembangan Diri: penyebaran proposal
5. AI menyajikan rencana terintegrasi
6. Pengguna dapat menelusuri setiap bagian
7. Pengguna menyetujui rencana keseluruhan
8. AI menandai dengan indikasi kemajuan

**Yang dilihat pengguna:** Satu rencana yang koheren, kemajuan per tahap, hasil per kemampuan, dokumentasi terintegrasi.
**Yang TIDAK dilihat pengguna:** Routing Capability Pack, komunikasi antar pack, logika dekomposisi tugas.

---

## Perjalanan 7 - Eksekusi Sasaran

**Tujuan:** Eksekusi end-to-end yang kompleks dari satu pernyataan tujuan.

**Langkah:**
1. Pengguna menyatakan tujuan: "Bangun aplikasi Inventory."
2. AI memahami tujuan dan memecahnya menjadi fase
3. AI menyajikan rencana eksekusi dengan estimasi
4. Pengguna menyetujui
5. AI mengakhiri:
   - Pengumpulan kebutuhan
   - Desain arsitektur
   - Desain basis data
   - Implementasi ujung belakang
   - Implementasi ujung depan
   - Pengujian
   - Dokumentasi
6. AI menampilkan kemajuan secara real-time
7. AI mengirimkan hasil yang lengkap dan terverifikasi

**Yang dilihat pengguna:** Satu tujuan, satu rencana, satu hasil.
**Yang TIDAK dilihat pengguna:** Tugas dekomposisi, pemilihan pekerja, penjadwalan, coba lagi, putaran verifikasi.

---

## Prinsip Desain

Semua perjalanan harus mengikuti prinsip-prinsip berikut:

1. **Satu percakapan:** Pengguna tidak pernah memilih Capability Pack secara manual.
2. **Tanpa eksposur internal:** Pengguna tidak pernah melihat Workers, Runtimes, Planners, atau struktur data internal.
3. **Transparansi kemajuan:** Tugas berdurasi panjang menampilkan kemajuan yang dapat dibaca manusia.
4. **Persetujuan sebelum tindakan:** Tindakan ireversibel memerlukan persetujuan eksplisit pengguna.
5. **Pertahanan artefak:** Semua keluaran signifikan disimpan dan dapat diambil kembali.
6. **Penjelasan sesuai permintaan:** Pengguna dapat bertanya "mengapa" kapan saja.

---

## Validasi

Setiap fitur atau perubahan baru harus divalidasi terhadap:
1. Apakah mempertahankan pengalaman satu percakapan?
2. Apakah tersembunyi mekanisme internal dari pengguna?
3. Apakah menjaga transparansi mengalami kemajuan?
4. Apakah menghormati alur kerja persetujuan?
5. Apakah mempersist artefak?

Jika ada jawaban "tidak", fitur harus didesain ulang sebelum rilis.
