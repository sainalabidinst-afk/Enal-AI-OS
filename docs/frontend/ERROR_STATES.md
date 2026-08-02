# Status Kesalahan

<!-- DOCUMENT_METADATA_START -->
**Pemilik:** Tim Dokumentasi
**Pemilik Canonical:** Pimpinan Tata Kelola Dokumentasi
**Diverifikasi Terakhir:** 08-02-2026
**Versi:** 1.0.0
**Status:** Aktif
**SSOT:** Dokumentasi frontend untuk ERROR_STATES
<!-- DOCUMENT_METADATA_END -->

Dokumen ini mendefinisikan setiap kesalahan status yang dapat ditemui pengguna di v1, dan bagaimana UI harus merespons.

---

## Kesalahan Jaringan

|Salah|Menyebabkan|Perilaku UI|
|-------|-------|-------------|
|Koneksi terputus|Bagian belakang tidak dapat dijangkau|Tampilkan spanduk: "Koneksi terputus. Menyambungkan kembali..."|
|Minta batas waktu|Bagian belakang lambat|Tampilkan percobaan ulang sebaris: "Waktu permintaan habis. Coba lagi?"|
|permintaan dibatalkan|Pengguna menavigasi keluar|Batalkan diam-diam. Tidak ada kesalahan yang ditampilkan.|

---

## API Kesalahan

|Status HTTP|Menyebabkan|Perilaku UI|
|-------------|-------|-------------|
|400|permintaan buruk (input tidak valid)|Tampilkan kesalahan sebaris di dekat kolom masukan.|
|401|Tidak sah (kunci API hilang/tidak valid)|Arahkan ulang ke Pengaturan â†’ API Kunci.|
|403|Dilarang (izin tidak mencukupi)|Tampilkan: "Izin ditolak. Hubungi admin."|
|404|Tidak ditemukan (sumber daya terhapus/hilang)|Tampilkan: "Tidak ditemukan. Mungkin sudah dihapus." dengan tindakan pemulihan.|
|429|Tarif terbatas|Tampilkan: "Terlalu banyak permintaan. Mencoba lagi dalam X detik."|
|500|Kesalahan server internal|Tampilkan: "Terjadi masalah. Silakan coba lagi." dengan tombol coba lagi.|
|503|Layanan tidak tersedia|Tampilkan: "Layanan untuk sementara tidak tersedia. Silakan coba lagi nanti."|

---

## Salah Eksekusi

|Negara|Menyebabkan|Perilaku UI|
|-------|-------|-------------|
|Eksekusi gagal|Pengecualian yang tidak tertangani dalam eksekusi|Tampilkan kesalahan di ProgressCard. Tawarkan percobaan ulang.|
|Eksekusi dibatalkan|Dibatalkan|Tampilkan "Eksekusi dibatalkan." di ProgressCard.|
|Fase gagal|Satu fase gagal|Tampilkan fase gagal dengan warna merah. Hentikan eksekusi.|
|Ruang kerja tidak ditemukan|Ruang kerja hilang|Buat ruang kerja baru secara otomatis atau minta pengguna untuk memilih.|
|Artefak tidak ditemukan|Artefak dihapus|Tampilkan placeholder: "Artefak tidak lagi tersedia."|
|Persetujuan ditolak|Pengguna menolak perubahan|Tampilkan "Perubahan ditolak". Lanjutkan keadaan sebelumnya.|

---

## Validasi Masukan

|Masukan|Validasi|Perilaku UI|
|-------|-----------|-------------|
|Masukan tujuan|Kosong|Nonaktifkan tombol Kirim. Penemuan petunjuk: "Jelaskan tujuan Anda."|
|Nama ruang kerja|Kosong|Nonaktifkan tombol Buat. Tampilkan petunjuk: "Nama wajib diisi."|
|Kunci API|Formatnya tidak valid|Tampilkan kesalahan sebaris: "Format kunci API tidak valid."|

---

## Negara Bagian Pengganti

|Skenario|Perilaku UI|
|----------|-------------|
|Belum ada percakapan|Tampilkan pesan selamat datang dengan contoh.|
|Belum ada ruang kerja|Tampilkan status kosong dengan CTA "Buat ruang kerja pertama Anda".|
|Belum ada artefak|Tampilkan status kosong: "Belum ada artefak. Mulai percakapan untuk membuatnya."|
|Belum ada eksekusi|Tampilkan status kosong: "Belum ada eksekusi."|
|Pemuatan kemampuan|Tidak adanya pemuat kerangka.|
|Streaming dihentikan|Tampilkan pemintal koneksi ulang. Lanjutkan dari pesan terakhir.|

---

## Aturan Pesan Kesalahan

1. **Dapat ditindaklanjuti:** Setiap kesalahan harus mencakup tindakan pemulihan (coba lagi, kembali, coba lagi).
2. **Dapat dibaca manusia:** Tidak ada jejak tumpukan, tidak ada kode internal.
3. **Khusus:** "Konfigurasi jaringan tidak valid" lebih baik daripada "Ada yang tidak beres".
4. **Kontekstual:** Tampilkan kesalahan di dekat elemen UI yang relevan, bukan sebagai spanduk global.
5. **Non-pemblokiran:** Kesalahan tidak dapat memanggil pengguna. Selalu berikan jalan keluar.

---

## Pencatatan Kesalahan

- Semua kesalahan dicatat ke backend dengan `conversationId`, `workspaceId`, `executionId`, `userId`.
- Kesalahan ditampilkan kepada pengguna dalam bentuk yang kokoh.
- Kesalahan disimpan dalam log eksekusi untuk debugging.
