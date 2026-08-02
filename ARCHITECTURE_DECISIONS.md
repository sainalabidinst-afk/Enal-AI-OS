## Bahasa Indonesia/Bahasa Inggris

### Ringkas / Ringkas

Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.


### Informasi Dokumen / Info Dokumen
- Berkas: `ARCHITECTURE_DECISIONS.md`
- Judul: Keputusan Arsitektur
- Status: editor bilingual ditambahkan


<!-- DOCUMENT_METADATA_START -->
**Pemilik:** Tim Dokumentasi
**Pemilik Canonical:** Pimpinan Tata Kelola Dokumentasi
**Diverifikasi Terakhir:** 08-02-2026
**Versi:** 1.0.0
**Status:** Aktif
**SSOT:** Catatan Keputusan Arsitektur (ADR) dan tata kelola arsitektur
<!-- DOCUMENT_METADATA_END -->

# Keputusan Arsitektur

Dokumen ini mencatat keputusan arsitektur yang dianggap stabil dan tidak boleh diubah tanpa pengamatan formal.
Setiap keputusan diidentifikasi oleh Architecture Decision Record (ADR) dan diperlakukan sebagai bagian dari konstitusi teknis Enal Cognitive Platform.

Kontributor tidak boleh mengabaikan keputusan ini melalui stres, ketergantungan baru, atau pelanggaran lapisan.
Jika suatu keputusan harus berubah, pengusul harus mengajukan ADR baru dengan analisis dampak dan persetujuan dari otoritas arsitektur proyek.

---

## Prinsip Tata Kelola: Dua Arsitektur yang Setara

Enal AI OS diatur oleh dua arsitektur yang sama pentingnya:

1. **Arsitektur Teknis** — diperiksa oleh ADR-001 hingga ADR-008
2. **Arsitektur Pengalaman** — disimpan oleh ADR-009 hingga ADR-012 dan `docs/UX_DESIGN.md`

Keduanya membeku. Keduanya mengikat. Keduanya tidak boleh dilanggar tanpa ADR yang disetujui.

Arsitektur Teknis memastikan platform tetap stabil, dapat dipertahankan, dan dipertahankan.
Arsitektur Pengalaman memastikan pengguna berinteraksi dengan satu AI melalui satu percakapan, tanpa paparan mekanisme internal.

Perubahan yang melanggar salah satu arsitektur merupakan suatu cacat, terlepas dari manfaat teknisnya.

---

## Aturan Penerimaan Fitur

Setiap fitur baru harus menjawab tiga pertanyaan berikut sebelum diterapkan:

1. Kemampuan mana yang ditingkatkan?
   - Jika tidak ada kemampuan yang meningkat: jangan membangun.

2. Perjalanan mana yang lebih baik?
   - Jika tidak ada Perjalanan yang menjadi lebih baik: jangan membangun.

3. Benchmark yang mana yang meningkat?
   - Jika tidak ada Benchmark yang bertambah: jangan membangun.

Jika jawaban ketiga tersebut adalah “ya”, implementasi dapat dilanjutkan.
Aturan ini mencegah fitur menambahkan dan menjaga pengembangan selaras dengan nilai produk, bukan kebaruan arsitektur.

---

## ADR-001: Pembekuan Pipa Inti

**Status:** Beku
**Berlaku:** 07-10-2026

Core Pipeline harus tetap kecil, stabil, dan dapat diprediksi.

- Inti harus tetap berada di bawah 5.000 baris kode.
- Inti tidak boleh memiliki ketergantungan eksternal selain stdlib + pydantic.
- Kontrak inti memiliki versi dan kompatibel dengan versi utama.
- Perubahan yang dapat menyebabkan gangguan memerlukan masa tenggang 2 rilis dengan panduan migrasi.

**Alasan:**
Core yang berkembang menjadi pemeliharaan dan mengurangi kemampuan ECP untuk mengembangkan Paket kemampuan secara mandiri.
Membekukan ukuran dan kemandirian Inti memaksa pekerjaan baru ke dalam Paket Kemampuan, menjaga stabilitas Inti.

---

## ADR-002: Capability Pack Kemerdekaan

**Status:** Beku
**Berlaku:** 07-10-2026

Paket kemampuan tidak dapat mengimpor Paket kemampuan lain secara langsung.

Komunikasi antar Paket Kemampuan harus mengalir melalui:

1. Definisi Tugas / Maksud
2. Execution Runtime
3. Hanya kontrak bersama

Contoh pola terlarang:

```python
# FORBIDDEN
from apps.trading_analyst import engine as trading_engine
trading_engine.analyze(...)
```

Contoh pola yang diperbolehkan:

```python
# ALLOWED
task = {
    "domain": "research",
    "intent": "Analyze market sentiment for AAPL",
}
result = await execution_runtime.execute(task)
```

**Alasan:**
Impor langsung menciptakan hubungan yang erat, ketergantungan yang tersembunyi, dan risiko impor yang sirkular.
Kemandirian memungkinkan Paket kemampuan untuk dikembangkan, diuji, dan diterapkan tanpa mengoordinasikan perubahan di seluruh paket.

---

## ADR-003: Pekerja = Hanya Adaptor

**Status:** Beku
**Berlaku:** 07-10-2026

Pekerja adalah adaptor. Seorang Pekerja tidak memiliki logika bisnis.

Logika bisnis milik Mesin Domain di dalam Capability Pack.

Tanggung jawab:
- Pekerja: menerjemahkan subtugas menjadi panggilan Capability Pack, mengembalikan hasil
- Mesin Domain: memiliki analisis, pembuatan, validasi, dan logika khusus domain

Pola terlarang:

```python
# FORBIDDEN - Worker owning business logic
class NetworkWorker:
    def analyze_firewall(self, config):
        # 200 lines of firewall analysis logic here
        ...
```

Pola yang diperlukan:

```python
# ALLOWED - Worker delegates to Domain Engine
class NetworkWorker:
    async def execute(self, subtask, context):
        return await self._app.engine.analyze(config)
```

**Alasan:**
Mempertahankan logika bisnis di Mesin Domain akan menjaga kemampuan pengujian, penggunaan kembali, dan pemisahan masalah.
Pekerja tetap menjadi adaptor tipis yang dapat diganti atau tidak berfungsi tanpa mengubah domain logika.

---

## ADR-004: Mesin Domain Memiliki Logika Bisnis

**Status:** Beku
**Berlaku:** 07-10-2026

Semua logika bisnis untuk Capability Pack berada di Mesin Domainnya.

- Mesin Domain: analisis, pembuatan, validasi, simulasi, rekomendasi
- Pekerja: hanya adaptor (lihat ADR-003)
- Lapisan Percakapan: konteks, riwayat, streaming saja

Mesin Domain tidak boleh:
- Impor mesin Capability Pack lainnya secara langsung
- Ubah kontrak Inti
- Lewati Execution Runtime untuk komunikasi lintas paket

**Alasan:**
Memusatkan logika bisnis di Mesin Domain membuat setiap Capability Pack mandiri dan dapat diuji secara independen.
Ini adalah batasan arsitektur yang melindungi Core dari perubahan domain spesifik.

---

## ADR-005: Diperlukan Persetujuan Manusia

**Status:** Beku
**Berlaku:** 07-10-2026

Tidak ada perubahan kode, konfigurasi, atau arsitektur yang dapat diterapkan tanpa persetujuan pengguna secara eksplisit.

- Kemampuan otonom dapat menganalisis, merencanakan, dan mempersiapkan perubahan.
- Eksekusi perubahan memerlukan persetujuan pengguna secara eksplisit.
- Semua proposal, perbedaan, hasil pengujian, dan catatan persetujuan disimpan sebagai artefak.
- Platform tidak pernah memodifikasi dirinya sendiri tanpa adanya keputusan manusia.

Penerapan aturan:
- Langkah persetujuan harus dilakukan sebelum langkah Terapkan dalam alur kerja perubahan apa pun.
- Catatan persetujuan tidak dapat diubah setelah dibuat.

**Alasan:**
Prinsip ini tidak dapat dinegosiasikan demi kepercayaan pengguna, kemampuan audit, dan pengoperasian AI yang aman.
Mekanisme tata kelola inilah yang memungkinkan ECP memiliki kemampuan otonom tanpa menjadi otonom dalam keputusan pengambilan.

---

## ADR-006: Kontrak Kemampuan v1 Dibekukan

**Status:** Beku
**Berlaku:** 07-10-2026

Kontrak Kemampuan v1 adalah skema stabil untuk semua Paket Kemampuan.

Elemen kontrak:
- CapabilityNode: ability_id, nama, deskripsi, diperlukan_skills, dependensi, estimasi_kompleksitas, tag
- SubtugasTemplate: subtugas_id, nama, deskripsi, keterampilan_yang diperlukan, artefak_produksi, perkiraan_durasi_menit, prioritas, can_parallelize
- Fungsi validasi: validasi_capability_node, validasi_subtask_template, validasi_capability_pack

Perubahan Kontrak Kemampuan memerlukan:
- Proses RFC dengan periode peninjauan 7 hari
- Kompatibilitas mundur untuk semua Paket kemampuan yang ada
- Panduan migrasi untuk semua template yang mempengaruhi
- Persetujuan oleh otoritas arsitektur proyek

**Alasan:**
Kontrak Kemampuan adalah antarmuka antara platform dan semua Paket Kemampuan.
Membekukannya memungkinkan pasar paket internal, komunitas, dan pihak ketiga untuk hidup berdampingan tanpa konflik versi.

---

## ADR-007: Batas Percakapan

**Status:** Beku
**Berlaku:** 07-10-2026

Manajer Percakapan bertanggung jawab untuk:
- Manajemen konteks
- Pelacakan sejarah
- Streaming acara
- Tanggapan penemuan kemampuan

Manajer Percakapan tidak boleh:
- Lakukan perencanaan
- Jalankan penalaran
- Jadwalkan tugas
- Panggil Mesin Domain secara langsung

Semua pelaksanaan tugas harus mengalir melalui Masyarakat Runtime → Execution Runtime.

**Alasan:**
Menjaga Conversation Manager tetap menjaga batas antara lapisan interaksi pengguna dan pelaksanaan tugas.
Jika Conversation Manager menyerap logika perencanaan atau eksekusi, sistem menjadi lebih sulit untuk di-debug, diuji, dan dibahas.

---

## ADR-008: Perubahan Inti Membutuhkan Bukti Lintas Kemampuan

**Status:** Beku
**Berlaku:** 07-10-2026

Tidak ada perubahan pada Inti yang dapat dilakukan kecuali terbukti diperlukan oleh setidaknya dua Paket Kemampuan.

Proses:
1. identifikasi perubahan Inti yang diperlukan
2. Dokumentasikan Paket kemampuan mana yang memerlukannya
3. Jika kurang dari 2 paket memerlukannya, perubahannya menjadi milik Capability Pack, bukan Inti
4. Jika 2 paket atau lebih memerlukannya, kirimkan RFC dengan kasus uji dari kedua paket
5. RFC harus diterima sebelum modifikasi Inti apa pun

**Alasan:**
Hal ini mencegah Core berkembang berdasarkan kasus penggunaan tunggal.
Hal ini memastikan evolusi Inti didorong oleh seluruh sektoral, bukan kebutuhan Capability Pack individu.

---

## Proses: Mengubah Keputusan Arsitektur

1. Usulkan ADR baru atau perbarui ADR yang sudah ada
2. Dokumentasikan alasan dan analisis dampak
3. Kirim ke pandangan arsitektur
4. Jika disetujui, perbarui dokumen ini dan beri tahu semua pengelola
5. Implementasi yang ada harus dimigrasikan sesuai dengan kebijakan yang ditetapkan

Perubahan pada ADR yang memerlukan:
- Proses RFC dengan periode peninjauan yang diperpanjang
- Rencana migrasi untuk semua komponen yang terkena dampak
- Persetujuan oleh otoritas arsitektur proyek

---

## Pengertian Arsitektur Lengkap

Arsitektur Enal AI OS dianggap selesai jika kedua kondisi terpenuhi:

1. Capability Pack baru dapat ditambahkan tanpa modifikasi apa pun pada Core.
2. Setiap perubahan yang berdampak pada beberapa Paket kemampuan memerlukan ADR yang disetujui dengan bukti lintas kemampuan.

Kedua kondisi tersebut terpenuhi pada 10-07-2026. Fokus pengembangan bergeser dari konstruksi platform ke keunggulan kemampuan.

---

## Daftar Pengecualian: Yang Membutuhkan ADR

Perubahan berikut tidak lagi rutin. Pengecualian apa pun harus disetujui melalui proses ADR:

- Menambahkan Runtime baru
- Menambahkan Perencana baru
- Menambahkan Kernel baru
- Menambahkan Layer arsitektur baru
- Memodifikasi Inti untuk meningkatkan satu Capability Pack

Semua hal di atas memerlukan:
1. Bukti kebutuhan lintas kemampuan (minimal 2 paket yang ada)
2. RFC dengan analisis dampak
3. Persetujuan oleh otoritas arsitektur proyek

---

## Penutupan Arsitektur v1

**Efektif:** 07-11-2026
**Status:** Ditutup

Arsitektur v1 resmi ditutup. Kondisi berikut terpenuhi:
- Pipa Inti Pembekuan
- Kontrak Kemampuan Pembekuan
- Pekerja API stabil
- Lapisan Percakapan stabil
- Kemampuan Penemuan stabil
- Tata Kelola Arsitektur aktif
- Proses ADR ditetapkan
- Kemampuan kerangka Benchmark aktif
- Benchmark di dunia nyata aktif
- Definisi Keunggulan Kemampuan diformalkan
- Dokumentasi disinkronkan

Mulai saat ini, fokus pengembangan sepenuhnya beralih dari konstruksi platform ke Keunggulan Kemampuan dan Penyempurnaan Produk.

Pekerjaan baru harus mengikuti siklus ini:
> Penggunaan Nyata → Pengukuran → Peningkatan Kemampuan → Benchmark → Rilis

Tidak ada perubahan arsitektur lebih lanjut yang diharapkan atau diizinkan kecuali perubahan tersebut memenuhi Daftar Pengecualian di atas.

Dokumen ini, bersama dengan ADR-001 hingga ADR-014, merupakan Tata Kelola Arsitektur Enal AI OS.

---

## ADR-009: Antarmuka Percakapan Tunggal

**Status:** Beku
**Efektif:** 07-11-2026

Pengguna berinteraksi dengan Enal AI OS melalui satu antarmuka percakapan.
Pengguna tidak boleh diharuskan memilih Paket kemampuan, mengonfigurasi Pekerja, memilih Waktu Proses Eksekusi, atau memahami mekanisme internal apa pun.

Semua hal berikut harus tetap bersifat internal:
- Capability Pack seleksi
- Pekerja Perutean
- Execution Runtime seleksi
- Detil Perencanaan Tugas
- Struktur data internal

Pengguna melihat satu AI. Secara internal, ECP mengarahkan ke Capability Pack yang sesuai, merencanakan tugas, dan mengeksekusi melalui Pekerja.

Pelanggaran terhadap prinsip ini merupakan cacat UX, bukan fitur.

**Alasan:**
Enal AI OS bersaing dengan ChatGPT, Claude, dan Kimi dalam hal pengalaman pengguna, bukan dalam kompleksitas arsitektur.
Proposisi nilainya adalah "satu AI yang memahami berbagai domain profesional melalui satu percakapan."
Mengekspos mekanisme internal mengingkari janji ini dan menciptakan beban kognitif bagi pengguna.

---

## ADR-010: Isolasi Ruang Kerja

**Status:** Beku
**Efektif:** 07-11-2026

Setiap proyek atau konteks pekerjaan diisolasi di Ruang Kerja.
Ruang Kerja berisi: Sejarah, Artefak, dan Memori.
Memori dicakup per Ruang Kerja. Berbagi memori melintasi Ruang Kerja memerlukan tindakan pengguna yang eksplisit.

**Alasan:**
Pengguna mengerjakan banyak proyek secara bersamaan.
Mencampur memori dan artefak antar proyek menimbulkan kebingungan dan risiko privasi.
Isolasi ruang kerja menjaga konteks tetap bersih dan dapat diprediksi.

---

## ADR-011: Kegigihan Artefak

**Status:** Beku
**Efektif:** 07-11-2026

Semua keluaran signifikan dari Paket Kemampuan harus dipertahankan sebagai Artefak.
Artefak diberi versi dan cakupannya per Ruang Kerja.
Pengguna dapat mengambil, membandingkan, dan memulihkan versi artefak sebelumnya.

Jenis artefak termasuk, namun tidak terbatas pada:
- Analisis laporan
- Rekomendasi
- Tambalan dan perbedaan
- Laporan pengujian
- Rencana penerapan
- Dokumentasi

**Alasan:**
Keluaran AI sangat berharga dan tidak boleh bersifat sementara.
Artefak yang persisten dan berversi memungkinkan kemampuan audit, pengukuran, dan rollback.
Hal ini sangat penting untuk Pengembangan Diri dan alur kerja penerapan yang terkendali.

---

## ADR-012: Transparansi Kemajuan

**Status:** Beku
**Efektif:** 07-11-2026

Selama tugas yang berjalan lama, sistem harus menunjukkan kemajuan kepada pengguna.
Indikasi kemajuan harus terperinci dan dapat dibaca oleh manusia.
Pengguna tidak dapat melihat informasi rahasia tanpa.

Pola kemajuan yang dapat diterima:
- "Menganalisis konfigurasi..."
- "Membuat dokumentasi..."
- "Menjalankan tes..."

Tidak dapat diterima:
- Generik "Memuat..." tanpa konteks
- Nama langkah internal seperti "Tahap 3: Jalankan Subtugas 7"

**Alasan:**
Indikasi kemajuan membangun kepercayaan dan mengurangi waktu tunggu yang dirasakan.
Hal ini juga membantu pengguna memahami apa yang dilakukan AI, yang merupakan bagian dari kemampuan menjelaskan.

---

## ADR-013: Aturan Hasil Pertama

**Status:** Beku
**Efektif:** 07-11-2026

Pengguna meminta hasil, bukan mekanisme.

Seorang pengguna tidak pernah mengatakan:
- "Gunakan Kemampuan Jaringan."
- "Panggil Pekerja Jaringan Pekerja."
- "Jalankan Execution Runtime."

Seorang pengguna mengatakan:
- "Audit jaringan kantor saya."
- "Analisa BTCUSDT."
- "Bangun aplikasi Inventaris."

Semua mekanisme internal—Paket kemampuan, Pekerja, Grafik Eksekusi, Penjadwalan, Model Gateway—adalah sarana untuk mencapai tujuan. Ujungnya adalah hasil pengguna.

Fitur apa pun, elemen UI, atau API yang menampilkan mekanisme internal kepada pengguna merupakan cacat, bukan fitur.

**Alasan:**
Enal AI OS bersaing dalam hal hasil, bukan transparansi arsitektur. Pengguna tidak perlu mengetahui cara kerja AI; mereka perlu tahu bahwa itu berhasil. Mengekspos konsep internal seperti Paket Kemampuan, Pekerja, atau Grafik Eksekusi janji percakapan tunggal dan menciptakan beban kognitif yang tidak perlu. Produk dinilai dari apa yang dikirimkannya, bukan dari cara pengirimannya.

---

## ADR-014: Lapisan Produk Operasional

**Status:** Beku
**Efektif:** 07-11-2026

Lapisan Produk Operasional terdiri dari layanan yang membuat ECP terasa seperti produk nyata dan bukan kerangka AI. Layanan ini dibangun di atas Core yang stabil dan diperlukan untuk penggunaan produksi.

Layanan yang dibutuhkan:
- Layanan Eksekusi: mengelola siklus hidup penuh sesi eksekusi
- Layanan Ruang Kerja: mengisolasi proyek dengan percakapan, file, memori, artefak, garis waktu
- Layanan Artefak: penyimpanan berversi dengan perbandingan, pemulihan, ekspor
- Model Gateway: perutean terpadu ke OpenAI, Anthropic, Gemini, Qwen, DeepSeek, Llama, Ollama
- Layanan Pemberitahuan: pemberitahuan kemajuan dan penyelesaian waktu nyata

Layanan ini tidak dapat mengubah Core. Mereka adalah bagian dari lapisan produk, bukan lapisan platform.

**Alasan:**
Pengguna menilai ECP berdasarkan kegunaan sehari-hari, bukan berdasarkan arsitektur internal. Lapisan Produk Operasional inilah yang mengubah AI Runtime yang kuat menjadi produk yang dapat diandalkan pengguna untuk pekerjaan nyata. Tanpa layanan ini, ECP hanya akan menjadi sebuah kerangka kerja. Bersama mereka, ini menjadi Platform Eksekusi AI.
