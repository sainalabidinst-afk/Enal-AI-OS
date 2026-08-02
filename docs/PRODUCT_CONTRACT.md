# Kontrak Produk v1.0

<!-- DOCUMENT_METADATA_START -->
**Pemilik:** Tim Dokumentasi
**Pemilik Canonical:** Pimpinan Tata Kelola Dokumentasi
**Diverifikasi Terakhir:** 08-02-2026
**Versi:** 1.0.0
**Status:** Aktif
**SSOT:** Kontrak produk, janji pengguna, dan kemampuan komitmen
<!-- DOCUMENT_METADATA_END -->

**Status:** Beku
**Efektif:** 07-11-2026
**Pemilik:** Chief Product Officer
**Tujuan:** Mendefinisikan kontrak tingkat produk antara baseline backend dan implementasi frontend. Tidak ada kode frontend yang boleh ditulis sebelum dokumen ini disetujui dan semua pemeriksaan Product Gate lulus.

---

## 1. Penentuan Posisi Produk

AI OS terakhir adalah **Platform Eksekusi AI**.

Pengguna mendeskripsikan hasil yang mereka inginkan. ECP memahami tujuan, merencanakan eksekusi, mengoordinasikan tugas, memverifikasi hasil, dan mengirimkan hasil yang lengkap — semuanya melalui satu percakapan.

Pengguna hanya melihat satu AI. Pengguna tidak pernah melihat mesin di balik layar.

**Motto:** Inti yang stabil. Kemampuan yang ahli. Satu percakapan.

**Target pengguna:** Pengembang, operator, dan pekerja pengetahuan yang membutuhkan bantuan AI untuk tugas kompleks multi-langkah.

**Value proposition inti:** Satu percakapan → hasil yang lengkap.

---

## 2. Kunci Kontrak Produk

Dokumen ini mengunci resolusi produk untuk fase Product MVP.

### Artefak yang Dikunci

|Dokumen|Status|Efektif|
|----------|--------|-----------|
|`docs/frontend/PRODUCT_UI_SPEC.md`|Beku|07-11-2026|
|`docs/frontend/UI_ARCHITECTURE.md`|Beku|07-11-2026|
|`docs/frontend/SCREEN_FLOW.md`|Beku|07-11-2026|
|`docs/frontend/COMPONENT_LIBRARY.md`|Beku|07-11-2026|
|`docs/frontend/STATE_MANAGEMENT.md`|Beku|07-11-2026|
|`docs/frontend/API_MAPPING.md`|Beku|07-11-2026|
|`docs/frontend/ERROR_STATES.md`|Beku|07-11-2026|
|`docs/frontend/MOBILE_LAYOUT.md`|Beku|07-11-2026|
|`docs/frontend/DESIGN_TOKENS.md`|Beku|07-11-2026|
|`docs/frontend/FRONTEND_DEFINITION_OF_DONE.md`|Beku|07-11-2026|

Tidak ada perubahan lebih lanjut pada dokumen-dokumen ini yang diizinkan selama implementasi Product MVP tanpa Product Change Request.

---

## 3. MVP Produk Ruang Lingkup

### Dalam Ruang Lingkup

|Layar|Tujuan|Harus Dimiliki untuk MVP|
|--------|---------|-------------------|
|Mengobrol|antarmuka utama. Satu percakapan dengan AI.|Ya|
|Ruang kerja|Ringkas proyek dengan percakapan, file, memori, artefak, eksekusi.|Ya|
|Penampil Artefak|Melihat, membandingkan, memulihkan versi artefak.|Ya|
|Dialog Persetujuan|Mengonfirmasi atau menolak tindakan yang tidak dapat diubah.|Ya|
|Pengaturan|Tema, preferensi model, notifikasi.|Ya|
|Penemuan Kemampuan|Daftar kemampuan dinamis dari backend.|Ya|
|Sejarah Eksekusi|Daftar eksekusi dengan status, kemajuan, artefak.|Ya|

### Di Luar Ruang Lingkup (Pasca-MVP)

- Agen pemilihan UI
- Konfigurasi Capability Pack
- Konfigurasi Pekerja
- Model pemilihan UI (kecuali pada Pengaturan)
- Visualisasi Grafik Eksekusi
- Admin berlari
- Analitik dasbor
- Manajemen UI Plugin
- Tema lanjutan

---

## 4. Prinsip Produk yang Tidak Dapat Ditawar

Prinsip-prinsip ini terkunci. Elemen UI apa pun yang melanggarnya adalah cacat.

### Prinsip 1: Satu Percakapan

antarmuka pengguna adalah satu percakapan. Tidak ada menu untuk memilih Capability Pack. Tidak ada dropdown untuk memilih Worker. Tidak ada panel konfigurasi untuk memilih Model.

AI melakukannya secara internal.

### Prinsip 2: Hasil di Atas Mekanisme

Pengguna mendeskripsikan hasil, bukan mekanisme.

Pengguna berkata: "Audit jaringan kantor saya."
Pengguna TIDAK berkata: "Jalankan Network Capability."

UI tidak boleh mengekspos konsep internal seperti Capability Pack, Worker, Execution Runtime, Task Planner, atau Execution Graph kepada pengguna.

### Prinsip 3: Transparansi Kemajuan

Selama tugas berdurasi panjang, sistem harus menampilkan kemajuan. Indikasi kemajuan harus terperinci dan mudah dibaca manusia.

Dapat diterima:
- "Menganalisis konfigurasi..."
- "Membuat dokumentasi..."
- "Menjalankan tes..."

Tidak dapat diterima:
- "Memuat..." yang umum
- Nama langkah internal seperti "Stage 3: Execute Subtask 7"

### Prinsip 4: Persetujuan Sebelum Tindakan

Untuk tindakan yang tidak dapat diubah, UI harus menampilkan dialog persetujuan eksplisit. AI tidak pernah menerapkan perubahan tanpa persetujuan pengguna.

### Prinsip 5: Artefak Pertama

Setiap keluaran penting adalah Artefak. Artefak selalu terlihat, memiliki versi, dan dapat diambil kembali.

### Prinsip 6: Isolasi Ruang Kerja

Setiap proyek diisolasi dalam Ruang Kerja. Percakapan, file, memori, tugas, artefak, dan riwayat eksekusi dibatasi per Ruang Kerja.

### Prinsip 7: Tanpa Data Palsu

Frontend harus menggunakan backend API. Data palsu tidak diizinkan di layar produksi mana pun.

---

## 5. Kunci Ketergantungan Backend

Frontend tidak terkunci ke **Backend Baseline v1.0.0-dev** (11-07-2026).

Baseline tersebut stabil. Perubahan berikut diizinkan tanpa permintaan Perubahan Produk:

- Perbaikan bug
- Perbaikan keamanan
- Peningkatan kinerja
- Integrasi kecil yang dibutuhkan frontend
- Perubahan kemampuan lintas yang disetujui ADR

Perubahan berikut memerlukan Permintaan Perubahan Produk:

- Runtime v2
- Perencana v2
- Kernel v2
- Percakapan v2
- Pekerja v2
- Lapisan baru apa pun
- Refactor besar tanpa kebutuhan lintas domain
- Perubahan jalur pada endpoint API yang tidak terkunci

### Backend API yang diperlukan untuk MVP

Backend API berikut harus stabil dan tersedia sebelum pengembangan frontend dimulai:

#### Mengobrol
- [x] POSTING `/api/v1/chat`
- [x] POSTING `/api/v1/chat/stream`
- [x] DAPATKAN `/api/v1/conversations/{conversationId}`
- [x] HAPUS `/api/v1/conversations/{conversationId}`

#### Ruang kerja
- [x] DAPATKAN `/api/v1/workspaces`
- [x] POSTING `/api/v1/workspaces`
- [x] DAPATKAN `/api/v1/workspaces/{workspaceId}`
- [x] HAPUS `/api/v1/workspaces/{workspaceId}`
- [x] POSTING `/api/v1/workspaces/{workspaceId}/files`
- [x] POSTING `/api/v1/workspaces/{workspaceId}/memory`
- [x] DAPATKAN `/api/v1/workspaces/{workspaceId}/memory/{key}`

#### Eksekusi
- [x] POSTING `/api/v1/executions`
- [x] DAPATKAN `/api/v1/executions/{executionId}`
- [x] DAPATKAN `/api/v1/executions`
- [x] POSTING `/api/v1/executions/{executionId}/phases`
- [x] PATCH `/api/v1/executions/{executionId}/phases/{phaseId}`
- [x] POSTING `/api/v1/executions/{executionId}/progress`
- [x] POSTING `/api/v1/executions/{executionId}/logs`
- [x] DAPATKAN `/api/v1/executions/{executionId}/logs`
- [x] POSTING `/api/v1/executions/{executionId}/cancel`
- [x] HAPUS `/api/v1/executions/{executionId}`
- [x] POSTING `/api/v1/executions/run`

#### Artefak
- [x] DAPATKAN `/api/v1/artifacts`
- [x] POSTING `/api/v1/artifacts`
- [x] DAPATKAN `/api/v1/artifacts/{artifactId}`
- [x] DAPATKAN `/api/v1/artifacts/{artifactId}/versions/{version}`
- [x] POSTING `/api/v1/artifacts/{artifactId}/versions`
- [x] POSTING `/api/v1/artifacts/{artifactId}/restore/{version}`
- [x] DAPATKAN `/api/v1/executions/{executionId}/artifacts`
- [x] HAPUS `/api/v1/artifacts/{artifactId}`

#### Kemampuan
- [x] DAPATKAN `/api/v1/capabilities`
- [x] DAPATKAN `/api/v1/capabilities/{capabilityId}`

#### Model
- [x] DAPATKAN `/api/v1/models/providers`
- [x] DAPATKAN `/api/v1/models/health`
- [x] POSTING `/api/v1/models/route`

#### Pemberitahuan
- [x] DAPATKAN `/api/v1/notifications/{recipient}`
- [x] PATCH `/api/v1/notifications/{recipient}/read/{notificationId}`

#### Acara Streaming
- [x] SSE dari `/api/v1/chat/stream` dengan acara: `final`, `execution_started`, `phase`, `task`, `log`, `artifact`, `progress`, `execution_complete`, `error`

---

## 6. Desain Kunci Token

Semua nilai visual harus menggunakan token ini. Tidak ada warna, spasi, atau tipografi yang di-hardcode.

### Warna

|Token|Nilai|Penggunaan|
|-------|-------|-------|
|`--color-bg-primary`|#0f1117|Latar belakang utama|
|`--color-bg-secondary`|#1a1d27|Kartu, panel|
|`--color-bg-tertiary`|#252830|Permukaannya ditinggikan|
|`--color-text-primary`|#e4e6eb|Teks utama|
|`--color-text-secondary`|#9ca3af|Teks sekunder|
|`--color-accent`|#3b82f6|Aksi utama|
|`--color-success`|#22c55e|Status sukses|
|`--color-warning`|#f59e0b|Status peringatan|
|`--color-danger`|#ef4444|Status kesalahan/bahaya|
|`--color-border`|#374151|Berbatasan|

### Tipografi

|Token|Nilai|Penggunaan|
|-------|-------|-------|
|`--font-family`|Antar, sistem-ui, sans-serif|Semua teks|
|`--font-size-xs`|0,75rem|Label, petunjuk|
|`--font-size-sm`|0,875rem|Teks sekunder|
|`--font-size-md`|1rem|Tubuh teks|
|`--font-size-lg`|1.125rem|Teks yang ditekankan|
|`--font-size-xl`|1,25rem|Menuju|
|`--font-size-2xl`|1,5rem|halaman judul|

### Jarak

|Token|Nilai|Penggunaan|
|-------|-------|-------|
|`--space-1`|4 piksel|Jarak rapat|
|`--space-2`|8 piksel|Jarak tanamnya kompak|
|`--space-3`|12 piksel|Spasi bawaan|
|`--space-4`|16 piksel|Jarak tanamnya nyaman|
|`--space-5`|24 piksel|Bagian spasi|
|`--space-6`|32 piksel|Spasi halaman|

### Radius

|Token|Nilai|Penggunaan|
|-------|-------|-------|
|`--radius-sm`|4 piksel|Elemen kecil|
|`--radius-md`|8 piksel|Kartu, tombol|
|`--radius-lg`|12 piksel|Panel, modal|

### Bayangan

|Token|Nilai|Penggunaan|
|-------|-------|-------|
|`--shadow-sm`|0 1px 2px rgba(0,0,0,0.3)|Ketinggian halus|
|`--shadow-md`|0 4px 6px rgba(0,0,0,0.4)|Kartu|
|`--shadow-lg`|0 10px 15px rgba(0,0,0,0.5)|Modal, dialog|

---

## 7. Kontrak Aturan API

Aturan ini tidak dapat ditawar selama fase Product MVP.

- Frontend **tidak boleh** mendefinisikan endpoint backend baru.
- Frontend **tidak boleh** memanggil endpoint yang tidak tercantum di `docs/frontend/API_MAPPING.md`.
- Jika frontend membutuhkan endpoint, backend harus menambahkan endpoint kecil dan fokus mengikuti pola yang ada.
- Setelah endpoint baru ditambahkan, `API_MAPPING.md` dan `PRODUCT_CONTRACT.md` harus diperbarui sebelum frontend menggunakannya.
- `API_MAPPING.md` adalah single source of truth untuk semua kontrak API.

Ini mencegah memastikan drift frontend/backend dan Product Contract tetap menjadi kontrak yang dapat dieksekusi antara dua layer.

---

## 8. DaftarPeriksa Gerbang Produk

Semua item harus dicentang sebelum coding frontend dimulai.

### Gerbang Dokumentasi
- [x] product_ui_spec.md ada dan dibekukan
- [x] UI_ARCHITECTURE.md ada dan difreeze
- [x] SCREEN_FLOW.md ada dan difreeze
- [x] COMPONENT_LIBRARY.md ada dan difreeze
- [x] STATE_MANAGEMENT.md ada dan difreeze
- [x] API_MAPPING.md ada dan difreeze
- [x] ERROR_STATES.md ada dan difreeze
- [x] MOBILE_LAYOUT.md ada dan difreeze
- [x] DESIGN_TOKENS.md ada dan difreeze
- [x] FRONTEND_DEFINITION_OF_DONE.md ada dan difreeze

### Gerbang Belakang
- [x] Backend Baseline v1.0.0-dev aktif
- [x] Semua API yang dibutuhkan diimplementasikan dan didokumentasikan
- [x] Kontrak API stabil (tidak ada perubahan yang direncanakan)
- [x] Streaming SSE titik akhir berfungsi
- [x] Tidak ada perubahan arsitektur backend yang tertunda yang mempengaruhi frontend

### Gerbang Produk
- [x] Semua 7 layar memiliki tujuan dan kriteria penerimaan yang jelas
- [x] Semua perjalanan pengguna dapat diselesaikan dari satu percakapan
- [x] Aliran seluler halus dan memuaskan
- [x] Status kesalahan ditentukan untuk semua panggilan API
- [x] Alur persetujuan ditentukan untuk tindakan yang tidak dapat diubah
- [x] Siklus hidup artefak didefinisikan (buat, lihat, versi, pulihkan)
- [x] Siklus hidup ruang kerja didefinisikan (buat, alihkan, hapus)
- [x] Tidak ada Capability Pack atau Pekerja yang diekspos di UI
- [x] Tidak ada data asli yang diizinkan di layar produksi

### Gerbang Teknis
- [x] Kerangka frontend dipilih: Next.js 14 + React 18 + TypeScript
- [x] Manajemen negara yang dipilih: Zustand
- [x] Gaya yang dipilih: Tailwind CSS v3
- [x] API klien dipilih: ambil dengan lapisan layanan khusus
- [x] Klien streaming dipilih: EventSource dengan kait khusus
- [x] Semua desain token didefinisikan di DESIGN_TOKENS.md
- [x] Tumpukan teknologi selaras dengan UI_ARCHITECTURE.md

### Analisis Kesenjangan

|Kebutuhan Frontend|Latar Belakang Status|Tindakan|
|---------------------|----------------|--------|
|POSTING/ngobrol|Diimplementasikan|Tidak ada|
|POSTING /obrolan/aliran|Diimplementasikan|Tidak ada|
|DAPATKAN /percakapan/{id}|Diimplementasikan|Tidak ada|
|HAPUS /percakapan/{id}|Diimplementasikan|Tidak ada|
|DAPATKAN /ruang kerja|Diimplementasikan|Tidak ada|
|POST /ruang kerja|Diimplementasikan|Tidak ada|
|DAPATKAN /ruang kerja/{id}|Diimplementasikan|Tidak ada|
|HAPUS /ruang kerja/{id}|Diimplementasikan|Tidak ada|
|DAPATKAN /workspaces/{id}/files|Diimplementasikan|Tidak ada|
|POST /ruang kerja/{id}/files|Diimplementasikan|Tidak ada|
|HAPUS /ruang kerja/{id}/files/{nama file}|Diimplementasikan|Tidak ada|
|DAPATKAN /ruang kerja/{id}/memori/{key}|Diimplementasikan|Tidak ada|
|POST /ruang kerja/{id}/memory|Diimplementasikan|Tidak ada|
|Semua API eksekusi|Diimplementasikan|Tidak ada|
|Semua API artefak|Diimplementasikan|Tidak ada|
|DAPATKAN /API/v1/capability|Diimplementasikan|Tidak ada|
|DAPATKAN /API/v1/capabilities/{id}|Diimplementasikan|Tidak ada|
|DAPATKAN /API/v1/models/providers|Diimplementasikan|Tidak ada|
|DAPATKAN /API/v1/models/health|Diimplementasikan|Tidak ada|
|POST /API/v1/models/route|Diimplementasikan|Tidak ada|
|DAPATKAN /API/v1/notifications/{penerima}|Diimplementasikan|Tidak ada|
|PATCH /API/v1/notifications/{penerima}/baca/{id}|Diimplementasikan|Tidak ada|
|Acara streaming SSE|Diimplementasikan|Tidak ada|

**Pemblokiran:** Tidak ada. Semua 22 backend API yang dibutuhkan telah diimplementasikan dan tersedia.

---

## 9. Rencana Implementasi Frontend

### Fase 1: Fondasi (3–5 hari)

Proyek struktur perancah. menghubungkan semua layanan ke backend API yang sebenarnya. Tidak ada data tiruan.

Kiriman:
- Struktur proyek sesuai `docs/frontend/PRODUCT_UI_SPEC.md` Bagian 10
- Semua layanan di `services/` memanggil backend API asli
- Semua tipe di `types/` sesuai skema backend
- Zustand store di `store/` terhubung ke layanan
- `layout.tsx` render tanpa kesalahan

### Fase 2: Chat MVP (1 minggu)

Bangun antarmuka percakapan tunggal. Ini adalah inti dari produk.

Kiriman:
- Pengguna dapat mengetik tujuan dan mengirimnya
- Tanggapan AI di-stream melalui SSE
- Kemajuan acara dirender secara real-time
- Peristiwa artefak dirender sebaris
- Status kesalahan dapat dilanjutkan
- Responsif seluler pada 320px

### Fase 3: Ruang Kerja (3 hari)

Ruang kerja layar Bangun.

Kiriman:
- Daftar ruang kerja
- Membuat ruang kerja baru
- Berpindah antar ruang kerja
- Melihat file, memori, artefak, riwayat eksekusi
- Menghapus ruang kerja dengan dialog persetujuan

**Pemblokiran:** Tidak ada. Semua endpoint yang dibutuhkan untuk Frontend MVP sudah tersedia di backend.

### Fase 4: Streaming UX (2 hari)

Sempurnakan pengalaman streaming.

Kiriman:
- Kemajuan pesan yang mudah dibaca manusia
- Fase transisi yang mulus
- Log dapat dilipat
- Artefak kartu muncul inline
- Koneksi putusnya menampilkan indikator reconnect

### Fase 5: Persetujuan UX (1 hari)

Bangun dialog persetujuan.

Kiriman:
- Dialog persetujuan diberikan untuk tindakan yang tidak dapat diubah
- Batal menutup tanpa efek samping
- Setujui pengiriman API panggilan yang sebenarnya
- Memuat status saat menunggu
- Status kesalahan jika panggilan API gagal

### Fase 6 : Penampil Artefak (2 hari)

Penampil artefak Bangun.

Kiriman:
- Melihat artefak konten
- Membandingkan versi
- Memulihkan versi sebelumnya
- Mengunduh artefak
- Merender tipe khusus (kode, penurunan harga, konfigurasi)

### Fase 7: Bahasa Polandia & Seluler (2 hari)

Polandia terakhir sebelum dogfood.

Kiriman:
- Tata letak seluler pada 320px
- Navigasi berfungsi di seluler
- Semua layar responsif
- Desain token digunakan secara konsisten
- Aksesibilitas: navigasi keyboard, label ARIA, cincin fokus

### Fase 8: Dogfood (30 hari)

Gunakan Enal AI OS untuk membangun dan meningkatkan Enal AI OS.

Kiriman:
- Penggunaan harian oleh tim
- Kasus nyata dicatat di `real_cases/`
- Bug dan isu UX dilacak
- Peningkatan kemampuan diukur melalui Benchmark

---

## 10. Definisi Selesai — Produk MVP

MVP Produk selesai ketika:

- [ ] Semua 7 layar diimplementasikan dan berfungsi
- [ ] Obrolan berfungsi end-to-end: kirim pesan → terima respons → lihat kemajuan → lihat artefak
- [ ] Streaming merender perkembangan peristiwa secara real-time
- [ ] Ruang kerja dibuat otomatis pada chat pertama
- [ ] Dialog persetujuan berfungsi untuk semua tindakan yang tidak dapat diubah
- [ ] Artifact viewer dapat menampilkan, membandingkan, dan memulihkan versi
- [ ] Riwayat Eksekusi menampilkan semua eksekusi sebelumnya
- [ ] Tata letak seluler berfungsi pada lebar 320px
- [ ] Semua layar menggunakan backend API asli
- [ ] Tidak ada data tiruan dalam kode produksi
- [ ] Semua token desain digunakan
- [ ] Tidak ada istilah arsitektur internal yang diekspos ke pengguna
- [ ] Dogfood 30 hari selesai
- [ ] ≥100 kasus nyata dicatat
- [ ] Skor kemampuan Benchmark ≥85%

---

## 11. Peta Jalan Pasca-MVP

Setelah MVP Produk selesai:

1. **Dogfooding Insights** → Peningkatan kemampuan
2. **Kasus Nyata** → Kemampuan unggul berbasis Benchmark
3. **Masukan Pengguna** → Penyempurnaan UX
4. **Kinerja** → Optimasi berdasarkan penggunaan nyata
5. **v1.0.0 Stable** → Kesiapan produksi

---

## 12. Persetujuan

|Peran|Nama|Status|Tanggal|
|------|------|--------|------|
|Kepala Bagian Produk| |Disetujui|07-11-2026|
|Kepala Arsitek| |Disetujui|07-11-2026|
|Pemimpin Bagian Depan| |Tertunda| |

Dokumen ini terkunci. Tidak ada perubahan lebih lanjut pada ruang lingkup produk, prinsip desain, atau dependensi backend yang diizinkan tanpa permintaan Perubahan Produk yang ditandatangani oleh Chief Product Officer dan Chief Architect.
