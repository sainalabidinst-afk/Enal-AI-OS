# Definisi Frontend Selesai

<!-- DOCUMENT_METADATA_START -->
**Pemilik:** Tim Dokumentasi
**Pemilik Canonical:** Pimpinan Tata Kelola Dokumentasi
**Diverifikasi Terakhir:** 08-02-2026
**Versi:** 1.0.0
**Status:** Aktif
**SSOT:** Dokumentasi frontend untuk FRONTEND_DEFINITION_OF_DONE
<!-- DOCUMENT_METADATA_END -->

**Status:** Beku
**Efektif:** 07-11-2026
**Pemilik:** Kepala Bagian Produk
**Tujuan:** Daftar periksa tingkat fitur untuk memverifikasi pekerjaan frontend telah selesai. Sebuah fitur tidak akan selesai sampai setiap kotak centang dicentang.

---

## Persyaratan Global (berlaku untuk semua fitur)

- [ ] Semua UI menggunakan desain token (`--color-*`, `--font-size-*`, `--space-*`, `--radius-*`, `--shadow-*`). Tidak ada warna, ukuran, atau tipografi hardcode.
- [ ] Tidak ada `switch(capability)`, `switch(domain)`, atau `switch(capabilityId)` di mana pun dalam perbedaan.
- [ ] Tidak ada `if (message.includes(...))` atau deteksi niat serupa diff.
- [ ] Tidak ada file data tiruan yang diimpor oleh komponen produksi.
- [ ] Tidak ada impor komponen dari `services/`.
- [ ] Semua panggilan API melalui `src/services/`.
- [ ] Semua mutasi negara melalui tindakan penyimpanan eksplisit.
- [ ] Komponen maksimal 300 baris (dengan komentar pembenaran jika terlampaui).
- [ ] Status kesalahan dapat ditindaklanjuti (tidak ada "Ada yang tidak beres" tanpa tindakan pemulihan).
- [ ] Tata letak seluler diuji pada lebar 320 piksel.
- [ ] Aksesibilitas: keyboard navigasi, cincin fokus, label ARIA.
- [ ] Unit pengujian untuk setiap komponen (uji snapshot atau interaksi).
- [ ] Uji integrasi untuk setiap fitur (setidaknya satu jalur bahagia).
- [ ] Serat lolos (`npm run lint`).
- [ ] Pemeriksaan pengetikan lolos (`npm run typecheck`).
- [ ] Tidak ada console.error, console.warn, atau console.log dalam kode yang ditentukan.

---

## Fitur Obrolan

### Tampilan Pesan
- [ ] Pesan dirender hanya dari status backend.
- [ ] Pesan pengguna dan pesan AI berbeda secara visual.
- [ ] Penurunan harga yang diberikan (judul, daftar, tebal, miring, tautan).
- [ ] Blok kode dirender dengan penyorotan sintaksis.
- [ ] Blok kode memiliki tombol salin.
- [ ] Gambar dirender sebaris saat backend mengembalikannya.
- [ ] Lampiran file ditampilkan sebagai kartu dengan nama file dan ukuran.
- [ ] Stempel waktu ditampilkan dalam urutan percakapan.
- [ ] Keadaan kosong menunjukkan prompt sebelum pesan pertama.

### Mengirim Pesan
- [ ] Pengguna mengetikkan tujuan di kotak prompt.
- [ ] Tombol Enter atau Kirim mengirimkan pesan ke backend (POST `/api/v1/chat`).
- [ ] Mengirim pesan akan mengosongkan kotak prompt.
- [ ] Pengiriman dihentikan selama streaming.
- [ ] Kesalahan jaringan menampilkan pesan kesalahan sebaris dengan tindakan coba lagi.
- [ ] 429 kesalahan menunjukkan hitungan mundur dan coba lagi secara otomatis.

### Mengalir
- [ ] Koneksi SSE/WebSocket terbuka pada `POST /api/v1/chat/stream`.
- [ ] Token dialirkan ke dalam gelembung pesan secara progresif.
- [ ] Indikator streaming (animasi berdenyut) terlihat selama streaming.
- [ ] Peristiwa aliran memperbarui penyimpanan melalui satu pengontrol aliran.
- [ ] Tidak ada komponen yang berlangganan aliran mentah.
- [ ] Koneksi terputus memicu indikator "Menyambungkan kembali...".
- [ ] Penyelesaian streaming memicu tindakan `addMessage()` terakhir.
- [ ] Kesalahan aliran memicu status `setError()`.

### Visualisasi Eksekusi
- [ ] Acara `execution_started` segera merender ProgressCard.
- [ ] Acara `phase` memperbarui ProgressCard dengan nama fase saat ini.
- [ ] Acara `progress` memperbarui bilah teknologi (0-100).
- [ ] `log` acara dirender sebaris di ProgressCard (dapat dilipat).
- [ ] Acara `artifact` menampilkan ArtifactCards sebaris dalam percakapan.
- [ ] Acara `execution_complete` menandai ProgressCard telah selesai.
- [ ] Acara `error`menunjukkan status kesalahan dengan tindakan coba lagi.

### Coba Lagi dan Tindakan
- [ ] Pesan yang gagal menampilkan tombol coba lagi.
- [ ] Coba lagi mengirim ulang pesan yang sama melalui API.
- [ ] Tindakan yang memerlukan persetujuan menunjukkan ApprovalDialog sebelum dieksekusi.
- [ ] Status disetujui/ditolak dikirim ke backend.

---

## Fitur Ruang Kerja

### Pembuatan Otomatis
- [ ] Interaksi dialog pertama secara otomatis membuat ruang kerja (POST `/api/v1/workspaces`).
- [ ] Ruang kerja dibuat sebelum streaming dimulai.
- [ ] ID Ruang Kerja dikirim bersama setiap pesan dialog dan permintaan eksekusi.

### Bilah Sisi Ruang Kerja
- [ ] Sidebar menampilkan daftar ruang kerja (GET `/api/v1/workspaces`).
- [ ] Sidebar menunjukkan ruang kerja saat ini yang dikumpulkan.
- [ ] Peralihan ruang kerja mempertahankan status percakapan.
- [ ] Sidebar memiliki tombol "Ruang Kerja Baru" (POST `/api/v1/workspaces`).

### Detail Ruang Kerja
- [ ] Halaman ruang kerja menampilkan file (dari backend, bukan komputasi lokal).
- [ ] Halaman ruang kerja menampilkan kunci memori (dari backend).
- [ ] File dapat diunggah melalui POST `/api/v1/workspaces/{id}/files`.
- [ ] Memori dapat diatur melalui POST `/api/v1/workspaces/{id}/memory`.
- [ ] Ruang kerja dapat diganti namanya (PATCH `/api/v1/workspaces/{id}`).
- [ ] Ruang kerja dapat dihapus (HAPUS `/api/v1/workspaces/{id}`).

### Sejarah Ruang Kerja
- [ ] Ruang kerja menampilkan riwayat percakapan (GET `/api/v1/conversations/{id}`).
- [ ] Ruang kerja menampilkan riwayat eksekusi (GET `/api/v1/executions?workspaceId={id}`).
- [ ] Ruang kerja menampilkan daftar artefak (GET `/api/v1/artifacts?workspaceId={id}`).

---

## Fitur Eksekusi

### Daftar Eksekusi
- [ ] Eksekusi ditampilkan di layar Riwayat Eksekusi (GET `/api/v1/executions`).
- [ ] Setiap eksekusi menunjukkan status, sasaran, waktu mulai, dan jumlah artefak.
- [ ] Warna lencana status dipetakan ke status eksekusi (idle, berjalan, dijeda, selesai, gagal).
- [ ] Keadaan kosong muncul ketika tidak ada eksekusi.

### Kemajuan Eksekusi
- [ ] Eksekusi yang berjalan menunjukkan kemajuan internet waktu nyata.
- [ ] Persentase bisnis online berasal dari backend (bidang `progress`).
- [ ] Nama fase saat ini ditampilkan (bidang `phase`).
- [ ] ETA ditampilkan saat disediakan (`etaSeconds`).
- [ ] Log dapat dilipat dan diperbesar berdasarkan level (info, peringatan, kesalahan).

### Tindakan Eksekusi
- [ ] Tombol Batal terlihat untuk melakukan eksekusi.
- [ ] Batalkan panggilan POST `/api/v1/executions/{id}/cancel`.
- [ ] Batal memicu konfirmasi dialog (tindakan yang tidak dapat diubah).
- [ ] Eksekusi dilanjutkan secara otomatis setelah penyegaran halaman (dihidrasi dari backend).

### Detil Eksekusi
- [ ] Tampilan detail eksekusi menunjukkan garis waktu fase lengkap.
- [ ] Eksekusi Artefak ditautkan dari tampilan eksekusi.
- [ ] Kesalahan eksekusi ditampilkan dengan pelacakan tumpukan (jika backend menyediakannya).

---

## Fitur Artefak

### Daftar Artefak
- [ ] Artefak ditampilkan di Penampil Artefak (GET `/api/v1/artifacts`).
- [ ] Setiap artefak menunjukkan nama, jenis, deskripsi, dan tanggal pembuatan.
- [ ] Artefak mengumpulkan berdasarkan ruang kerja.
- [ ] Status kosong muncul ketika tidak ada artefak.

### Pratinjau Artefak
- [ ] Konten artefak dirender berdasarkan jenis (kode, konfigurasi, dokumen, gambar).
- [ ] Artefak kode dirender dengan penyorotan sintaksis.
- [ ] Artefak biner (gambar, PDF) ditampilkan pada penampil yang sesuai.
- [ ] Artefak besar menampilkan peringatan atau tampilan terpotong dengan opsi "Lihat penuh".

### Tindakan Artefak
- [ ] Tombol unduh memicu gumpalan artefak GET.
- [ ] Tombol Bandingkan membuka tampilan perbedaan antara versi saat ini dan sebelumnya.
- [ ] Tombol Pulihan (kembali ke versi sebelumnya) memanggil POST `/api/v1/artifacts/{id}/restore/{version}`.
- [ ] Pulihkan pemicu ApprovalDialog sebelum menerapkan.

### Versi Artefak
- [ ] Pemilih versi memungkinkan penelusuran riwayat artefak.
- [ ] Setiap versi menampilkan penulis, batang waktu, dan deskripsi.
- [ ] Perbedaan versi menyoroti perubahan.

---

## Dialog Persetujuan

- [ ] Komponen ApprovalDialog dirender untuk semua tindakan yang tidak dapat diubah.
- [ ] Tindakan yang tidak dapat diubah: penghapusan ruang kerja, pemulihan artefak, pembatalan eksekusi.
- [ ] Dialog menunjukkan apa yang akan terjadi.
- [ ] Tombol Batal menutup dialog tanpa efek samping.
- [ ] Tombol Setujui mengirimkan panggilan API yang sebenarnya (bukan tiruan).
- [ ] Tindakan yang ditolak dicatat (tidak dijalankan).
- [ ] Memuat status saat pesanan ditunda (jika API lambat).
- [ ] Status kesalahan jika panggilan API gagal setelah disetujui.

---

## Pengaturan Fitur

### Model Pemilihan
- [ ] Penyedia model memuat dari GET `/api/v1/models/providers`.
- [ ] Pembaruan preferensi model melalui PATCH `/api/v1/models/route`.
- [ ] Pemilihan model disimpan ke backend, bukan Penyimpanan lokal saja.
- [ ] Model preferensi dihormati dalam dialog permintaan berikutnya.

### Tema
- [ ] Pengalih tema beralih antara terang, gelap, dan sistem preferensi.
- [ ] Tema tetap ada di Penyimpanan lokal.
- [ ] Tema diterapkan secara instan tanpa memuat ulang halaman.

### Pemberitahuan
- [ ] Pengaturan notifikasi (aktifkan/ aktifkan) tetap ada di backend.
- [ ] Notifikasi dimuat dari GET `/api/v1/notifications/{recipient}`.
- [ ] Notifikasi ditampilkan sebagai toast di UI.

### API Kunci
- [ ] Bidang kunci API ditutupi.
- [ ] Kunci API disimpan ke backend melalui POST `/api/v1/models/route` (atau titik akhir yang sesuai).
- [ ] API kesalahan utama muncul sebagai pesan yang dapat dilanjutkan.

---

## Fitur Penemuan Kemampuan

- [ ] Daftar kemampuan dimuat dari GET `/api/v1/capabilities`.
- [ ] Backend mengembalikan kemampuan dan domain yang tersedia.
- [ ] Frontend menjadikan kemampuan sebagai daftar saja.
- [ ] Frontend tidak pernah memfilter atau menyusun ulang berdasarkan logika domain.
- [ ] Detail kemampuan dimuat dari GET `/api/v1/capabilities/{id}`.
- [ ] Pemilihan kemampuan mengirimkan tujuan ke wawancara (bukan eksekusi langsung).

---

## Penanganan Kesalahan (Global)

- [ ] Kesalahan jaringan: "Koneksi terputus. Mencoba lagi..." dengan coba lagi otomatis.
- [ ] 400: kesalahan validasi sebaris di dekat bidang.
- [ ] 401: alihkan ke Pengaturan atau alur login.
- [ ] 403: Pesan "Izin ditolak".
- [ ] 404: Pesan "Tidak ditemukan" dengan tindakan pemulihan.
- [ ] 429: "Terlalu banyak permintaan. Mencoba lagi dalam Xs" dengan hitung mundur.
- [ ] 500: "Ada yang tidak beres. Silakan coba lagi." dengan tombol coba lagi.
- [ ] Eksekusi gagal: pesan kesalahan dengan opsi coba lagi.
- [ ] Ruang kerja tidak ditemukan: tawaran untuk membuat ruang kerja baru.
- [ ] Artefak tidak ditemukan: tampilkan placeholder "Artefak tidak lagi tersedia."

---

## Persyaratan Non-Fungsional

- [ ] Cat bermakna pertama <3 detik di 3G.
- [ ] Pesan dialog ditampilkan <100 md setelah token streaming.
- [ ] Sambungan ulang streaming < 2 detik setelah pemulihan jaringan.
- [ ] Tidak ada jank saat menggulir percakapan dengan 1000+ pesan.
- [ ] Peralihan ruang kerja <500ms.
- [ ] Tidak ada kesalahan konsol dalam pembuatan produksi.
- [ ] Skor aksesibilitas mercusuar > 90.
- [ ] Tes E2E mencakup: mengirim pesan, menyimpan ruang kerja, mengunduh artefak, alur persetujuan.

---

## Definisi Ringkas Selesai

Sebuah fitur dinyatakan DONE ketika:
1. Semua kotak centang di dokumen ini tercentang.
2. Fitur ini berjalan pada API backend sebenarnya.
3. Tidak ada data tiruan yang digunakan dalam kode produksi.
4. Lint dan pass pemeriksaan ketik.
5. Tidak ada pola terlarang yang ditemukan di diff.
6. Fitur ini berfungsi di perangkat seluler (320 piksel).
7. Peninjauan dari tim frontend telah menandatangani.

Semua checkbox tidak tercentang di awal sprint. Semua kotak centang tercentang saat PR mengeras.
