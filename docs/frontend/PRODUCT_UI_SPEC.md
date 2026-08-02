# Spesifikasi UI Produk

<!-- DOCUMENT_METADATA_START -->
**Pemilik:** Tim Dokumentasi
**Pemilik Canonical:** Pimpinan Tata Kelola Dokumentasi
**Diverifikasi Terakhir:** 08-02-2026
**Versi:** 1.0.0
**Status:** Aktif
**SSOT:** Dokumentasi frontend untuk PRODUCT_UI_SPEC
<!-- DOCUMENT_METADATA_END -->

**Status:** Beku
**Efektif:** 07-11-2026
**Pemilik:** Kepala Bagian Produk
**Tujuan:** Sumber kebenaran tunggal untuk semua pekerjaan frontend. Tidak ada kode UI yang boleh ditulis sebelum dokumen ini disetujui.

---

## 1. Posisi Produk

AI OS terakhir adalah **Platform Eksekusi AI**.

Pengguna mendeskripsikan hasil yang mereka inginkan. ECP memahami tujuan, merencanakan eksekusi, mengoordinasikan tugas, memverifikasi hasil, dan memberikan hasil lengkap—semua melalui satu percakapan.

Pengguna melihat satu AI. Pengguna tidak pernah melihat mesin di baliknya.

**Motto:** Inti yang stabil. Kapabilitas ahli. Satu percakapan.

---

## 2. Prinsip Desain

Prinsip-prinsip ini tidak dapat dinegosiasikan. Setiap elemen UI yang melanggarnya adalah cacat.

### Prinsip 1: Satu Percakapan

antarmuka pengguna adalah satu percakapan. Tidak ada menu untuk memilih Capability Pack. Tidak ada dropdown untuk memilih Worker. Tidak ada panel konfigurasi untuk memilih Model.

AI melakukannya secara internal.

### Prinsip 2: Hasil di atas Mekanisme

Pengguna mendeskripsikan hasil, bukan mekanisme.

Pengguna berkata: "Audit jaringan kantor saya."
Pengguna TIDAK berkata: "Jalankan Network Capability."

UI tidak boleh mengekspos konsep internal seperti Capability Pack, Worker, Execution Runtime, Task Planner, atau Execution Graph kepada pengguna.

### Prinsip 3: Transparansi Kemajuan

Selama tugas berjalan lama, sistem harus menampilkan kemajuan. Indikasi kemajuan harus berskala kasar dan mudah dibaca manusia.

Dapat diterima:
- "Menganalisis konfigurasi..."
- "Menghasilkan dokumentasi..."
- "Menjalankan tes..."

Tidak dapat diterima:
- "Memuat..." yang umum
- Nama langkah internal seperti "Stage 3: Execute Subtask 7"

### Prinsip 4: Persetujuan Sebelum Tindakan

Untuk tindakan yang tidak dapat dibatalkan, UI harus menampilkan dialog persetujuan eksplisit. AI tidak pernah menerapkan perubahan tanpa persetujuan pengguna.

### Prinsip 5: Artefak Didahulukan

Setiap keluaran penting adalah Artefak. Artefak selalu terlihat, berversi, dan dapat diambil kembali.

### Prinsip 6: Isolasi Ruang Kerja

Setiap proyek diisolasi dalam Ruang Kerja. Percakapan, file, memori, tugas, artefak, dan riwayat eksekusi dibatasi per Ruang Kerja.

### Prinsip 7: Tanpa Data Palsu

Frontend harus menggunakan API backend. Data palsu tidak diizinkan di layar produksi mana pun.

---

## 3. Inventaris Layar

Frontend v1 memiliki tepat 7 layar.

| # |Layar|Tujuan|
|---|--------|---------|
|1|Mengobrol|antarmuka utama. Pengguna mengetik tujuan, melihat respon AI, kemajuan, dan artefak.|
|2|Ruang kerja|Ikhtisar proyek: percakapan, file, memori, tugas, artefak, linimasa.|
|3|Penampil Artefak|Melihat, membandingkan, dan memulihkan versi artefak.|
|4|Dialog Persetujuan|Mengonfirmasi atau menolak tindakan yang tidak dapat dibatalkan.|
|5|Pengaturan|Model pemilihan, tema, notifikasi, API kunci.|
|6|Penemuan Kemampuan|Daftar kapabilitas dinamis dari backend.|
|7|Sejarah Eksekusi|Daftar eksekusi dengan status, kemajuan, dan artefak.|

Tidak ada layar lain yang diizinkan di v1.

---

## 4. Komponen Inventarisasi

Ini adalah satu-satunya komponen UI yang diizinkan di v1.

|Komponen|Tujuan|Layar|
|-----------|---------|-----------|
|Jendela Obrolan|Wadah percakapan utama|Mengobrol|
|menghasilkan Obrolan|Mengirim pesan pengguna atau AI|Mengobrol|
|Kotak Prompt|Masukkan teks untuk tujuan pengguna|Mengobrol|
|Kartu Kemajuan|Kemajuan eksekusi secara real-time|Obrolan, Ruang Kerja|
|Kartu Artefak|Artefak Pratinjau tunggal|Obrolan, Ruang Kerja, Penampil Artefak|
|Dialog Persetujuan|Menyetujui/menolak tindakan|Obrolan, Ruang Kerja|
|Garis Waktu Eksekusi|Linimasa visual fase eksekusi|Ruang Kerja, Riwayat Eksekusi|
|Bilah Sisi Ruang Kerja|Pengalih ruang kerja dan navigasi|Semua|
|Memuat Indikator|Negara sedang mencari|Semua|
|NotifikasiToast|Notifikasi non-blokir|Semua|

Tidak ada komponen lain yang diizinkan di v1.

---

## 5. Manajemen Negara

Semua state aplikasi harus mengalir melalui irisan berikut:

```
Conversation
  - messages[]
  - conversationId
  - streaming state

Workspace
  - currentWorkspaceId
  - workspaces[]
  - files[]
  - memory{}

Execution
  - executions[]
  - currentExecutionId
  - status: idle | running | paused | completed | failed
  - progress: 0-100
  - phases[]
  - logs[]

Artifact
  - artifacts[]
  - currentArtifactId
  - versions[]

Notification
  - notifications[]
  - unreadCount

Settings
  - modelPreference
  - theme
  - notificationsEnabled
  - apiKeys{}
```

Aturan:
- Keadaan dinormalisasi.
- Tidak ada status turunan yang disimpan.
- Semua penyembuhan keadaan melalui aksi yang terdefinisi.
- Status disimpan ke backend melalui API.
- Status bertahan setelah refresh browser melalui backend + localStorage hanya untuk preferensi UI.

---

## 6. Pemetaan API

Setiap layar dan komponen harus menggunakan API backend ini.

|Layar|API|Metode|Tujuan|
|--------|-----|--------|---------|
|Mengobrol|POSTING /API/v1/chat|POS|Kirim pesan, dapatkan tanggapan|
|Mengobrol|POST /API/v1/chat/stream|POS|Streaming acara percakapan|
|Ruang kerja|DAPATKAN /API/v1/workspaces|MENDAPATKAN|Daftar ruang kerja|
|Ruang kerja|POST /API/v1/workspaces|POS|Buat ruang kerja|
|Ruang kerja|DAPATKAN /API/v1/workspaces/{id}|MENDAPATKAN|Ambil detail ruang kerja|
|Ruang kerja|POST /API/v1/workspaces/{id}/files|POS|Unggah file|
|Ruang kerja|POST /API/v1/workspaces/{id}/memory|POS|Atur memori|
|Ruang kerja|DAPATKAN /API/v1/workspaces/{id}/memory/{key}|MENDAPATKAN|Ambil kenangan|
|Artefak|DAPATKAN /API/v1/artifacts|MENDAPATKAN|Daftar artefak|
|Artefak|POST /API/v1/artefak|POS|Buat artefak|
|Artefak|DAPATKAN /API/v1/artifacts/{id}|MENDAPATKAN|Ambil artefak|
|Artefak|DAPATKAN /API/v1/artifacts/{id}/versions/{version}|MENDAPATKAN|Ambil versi artefak|
|Artefak|POST /API/v1/artifacts/{id}/restore/{version}|POS|Artefak versi Pulikan|
|Eksekusi|POST /API/v1/executions|POS|Buat eksekusi|
|Eksekusi|DAPATKAN /API/v1/executions/{id}|MENDAPATKAN|Ambil eksekusi|
|Eksekusi|POST /API/v1/executions/{id}/progress|POS|memperbarui kemajuan|
|Eksekusi|POST /API/v1/executions/{id}/batal|POS|Eksekusi Batalkan|
|Eksekusi|POST /API/v1/executions/run|POS|Eksekusi dijalankan secara end-to-end|
|Eksekusi|DAPATKAN /API/v1/executions/{id}/logs|MENDAPATKAN|Ambil log eksekusi|
|Eksekusi|DAPATKAN /API/v1/executions/{id}/artifacts|MENDAPATKAN|Ambil eksekusi artefak|
|Pengaturan|DAPATKAN /API/v1/models/providers|MENDAPATKAN|Daftar penyedia model|
|Pengaturan|POST /API/v1/models/route|POS|Rute model|
|Pemberitahuan|DAPATKAN /API/v1/notifications/{penerima}|MENDAPATKAN|Ambil notifikasi|
|Kemampuan|DAPATKAN /API/v1/capability|MENDAPATKAN|Kemampuan mendaftar|
|Kemampuan|DAPATKAN /API/v1/capabilities/{id}|MENDAPATKAN|Ambil detail kemampuan|

Tidak ada panggilan API lain yang diizinkan di v1.

---

## 7. Kesalahan Negara

Setiap panggilan API harus menangani state error ini.

|Salah|Status HTTP|Perilaku UI|
|-------|-------------|-------------|
|jaringan salah|T/A|Tampilkan "Koneksi terputus. Mencoba lagi..."|
|400 Permintaan Buruk|400|Tampilkan kesalahan validasi sebaris|
|401 Tidak Sah|401|Arahkan ke pengaturan|
|403 Dilarang|403|Tampilkan "Izin ditolak"|
|404 Tidak Ditemukan|404|Tampilkan "Tidak ditemukan" dengan tindakan pemulihan|
|429 Tarif Terbatas|429|Tampilkan "Terlalu banyak permintaan. Mencoba lagi di..."|
|500 Kesalahan Internal|500|Tampilkan "Ada yang tidak beres. Silakan coba lagi."|
|Eksekusi gagal|T/A|Tampilkan kesalahan dengan opsi coba lagi|
|Ruang kerja tidak ditemukan|404|Buat ruang kerja baru atau izinkan pengguna memilih yang ada|
|Artefak tidak ditemukan|404|Tampilkan placeholder dengan "Artefak tidak lagi tersedia"|

Semua error harus dapat ditindaklanjuti. Tidak ada pesan "Terjadi kesalahan" yang umum.

---

## 8. Tata Letak Ponsel

UI harus responsif dan bekerja di perangkat seluler (lebar minimal 320px).

|Titik putus|Tata Letak|
|------------|--------|
|Desktop (>1024 piksel)|Sidebar + konten utama + panel artefak opsional|
|Tablet (768-1024 piksel)|Sidebar dapat dilipat + konten utama|
|Seluler (<768 piksel)|Obrolan layar penuh, navigasi bawah, panel geser keluar|

Aturan seluler:
- Chat selalu layar penuh di ponsel.
- Ruang kerja sidebar adalah lembar paling bawah.
- Artifact viewer adalah overlay layar penuh.
- Dialog persetujuan ada di lembar paling bawah.
- Kartu kemajuan menciut menjadi bar kompak di ponsel.

---

## 9. Desain Token

Semua nilai visual harus menggunakan token ini. Tidak ada warna, spasi, atau tipografi yang di-hardcode.

### Warna

|Token|Nilai|Penggunaan|
|-------|-------|-------|
|`--color-bg-primary`|#0f1117|Latar belakang utama|
|`--color-bg-secondary`|#1a1d27|Kartu, panel|
|`--color-bg-tertiary`|#252830|Permukaannya terangkat|
|`--color-text-primary`|#e4e6eb|Teks utama|
|`--color-text-secondary`|#9ca3af|Teks sekunder|
|`--color-accent`|#3b82f6|Aksi utama|
|`--color-success`|#22c55e|sukses negara|
|`--color-warning`|#f59e0b|peringatan|
|`--color-danger`|#ef4444|Kesalahan menyatakan/bahaya|
|`--color-border`|#374151|Batas|

### Tipografi

|Token|Nilai|Penggunaan|
|-------|-------|-------|
|`--font-family`|Antar, sistem-ui, sans-serif|Semua teks|
|`--font-size-xs`|0,75rem|Label, petunjuk|
|`--font-size-sm`|0,875rem|Teks sekunder|
|`--font-size-md`|1rem|Teks isi|
|`--font-size-lg`|1.125rem|Teks ditekankan|
|`--font-size-xl`|1,25rem|Menuju|
|`--font-size-2xl`|1,5rem|halaman judul|

### Spasi

|Token|Nilai|Penggunaan|
|-------|-------|-------|
|`--space-1`|4 piksel|Spasi rapat|
|`--space-2`|8 piksel|Spasi kompak|
|`--space-3`|12 piksel|Spasi bawaan|
|`--space-4`|16 piksel|Spasi nyaman|
|`--space-5`|24 piksel|Spasi bagian|
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

## 10. Arsitektur Frontend

```
frontend/
src/
├── app/
│   ├── providers/
│   └── router/
├── pages/
│   ├── Chat/
│   ├── Workspace/
│   ├── ArtifactViewer/
│   ├── ApprovalDialog/
│   ├── Settings/
│   ├── CapabilityDiscovery/
│   └── ExecutionHistory/
├── features/
│   ├── chat/
│   ├── workspace/
│   ├── execution/
│   ├── artifact/
│   ├── settings/
│   └── notifications/
├── components/
│   ├── ChatWindow/
│   ├── ChatBubble/
│   ├── PromptBox/
│   ├── ProgressCard/
│   ├── ArtifactCard/
│   ├── ApprovalDialog/
│   ├── ExecutionTimeline/
│   ├── WorkspaceSidebar/
│   ├── LoadingIndicator/
│   └── NotificationToast/
├── layouts/
│   ├── MainLayout/
│   └── MobileLayout/
├── hooks/
├── services/
│   ├── api.ts
│   ├── chat.ts
│   ├── execution.ts
│   ├── workspace.ts
│   ├── artifact.ts
│   └── notification.ts
├── store/
│   ├── conversationSlice.ts
│   ├── workspaceSlice.ts
│   ├── executionSlice.ts
│   ├── artifactSlice.ts
│   ├── notificationSlice.ts
│   └── settingsSlice.ts
├── types/
│   ├── chat.ts
│   ├── execution.ts
│   ├── workspace.ts
│   ├── artifact.ts
│   └── api.ts
└── utils/
```

Prinsip:
- Organisasi berbasis fitur, bukan berbasis tipe.
- Semua panggilan API melalui `services/`.
- Semua negara bagian berada di `store/`.
- Komponen bersifat bodoh. Fitur memiliki logika.
- Tidak ada logika bisnis di komponen.

---

## 11. Pemahaman Selesai

Frontend v1 selesai ketika:

- [ ] Pengguna membuka aplikasi dan melihat satu jendela dialog.
- [ ] Pengguna mengetik tujuan dan mendapatkan respons.
- [ ] Kemajuan terlihat selama tugas berjalan lama.
- [ ] Artefak muncul otomatis.
- [ ] Dialog persetujuan berfungsi untuk tindakan yang tidak dapat dibatalkan.
- [ ] Ruang kerja dibuat otomatis.
- [ ] Riwayat eksekusi tersedia.
- [ ] Capability Discovery bekerja dari dialog.
- [ ] Semua layar menggunakan API backend nyata.
- [ ] Tidak ada data tiruan di layar produksi.
- [ ] Tata letak seluler bekerja pada lebar 320px.
- [ ] Semua komponen menggunakan desain token.
- [ ] Error dapat ditindaklanjuti dan ramah pengguna.
- [ ] Tidak ada istilah arsitektur internal yang diekspos ke pengguna.

---

## 12. Ruang Lingkup Luar

Hal-hal berikut secara eksplisit di luar scope untuk frontend v1:

- Agen pemilihan UI
- Konfigurasi Capability Pack
- Konfigurasi Pekerja
- Pemilihan Model UI (kecuali di Pengaturan)
- Visualisasi Grafik Eksekusi
- Admin berlari
- Analitik dasbor
- Manajemen UI Plugin
- Tema lanjutan

Ini dapat ditambahkan di versi mendatang jika tervalidasi oleh kebutuhan pengguna nyata.

---

## 13. Kriteria Keberhasilan

Frontend berhasil ketika pengguna baru dapat:

1. Membuka aplikasi dan memahami apa yang harus dilakukan tanpa membaca dokumentasi.
2. Mengetik tujuan dalam bahasa sehari-hari dan mendapatkan hasil.
3. Melihat kemajuan sambil menunggu.
4. Menemukan artefak setelah eksekusi selesai.
5. Menyetujui atau menolak perubahan saat diminta.
6. Kembali ke ruang kerja sebelumnya dan melanjutkan dari posisi terakhir.

Jika salah satu dari ini gagal, frontend belum siap untuk Pratinjau Pengembang.
