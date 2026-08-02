# Tata Letak Seluler

<!-- DOCUMENT_METADATA_START -->
**Pemilik:** Tim Dokumentasi
**Pemilik Canonical:** Pimpinan Tata Kelola Dokumentasi
**Diverifikasi Terakhir:** 08-02-2026
**Versi:** 1.0.0
**Status:** Aktif
**SSOT:** Dokumentasi frontend untuk MOBILE_LAYOUT
<!-- DOCUMENT_METADATA_END -->

Dokumen ini mendefinisikan perilaku responsif untuk layar v1. Mobile adalah target kelas utama, bukan pemikiran kedua.

---

## Titik henti sementara

|Nama|Lebaran|Tata Letak|
|------|-------|--------|
|Seluler|<640 piksel|Panel layar penuh, navigasi bawah|
|Tablet|640 piksel - 1024 piksel|Sidebar yang dapat dilipat, panel lebih lebar|
|Desktop|> 1024 piksel|Memperbaiki sidebar, tata letak multi-panel|

---

## Layar Perilaku

### Mengobrol

|Perilaku|Seluler|Tablet|Desktop|
|----------|--------|--------|---------|
|Bila samping|Tersembunyi (lembar bawah)|Kiri yang bisa dilipat|Perbaiki ke kiri|
|pesan lebaran|Lebaran penuh|90%|70%|
|Kotak Prompt|Lebar penuh, tetap di bawah|Tengah, bawah|Tengah, bawah|
|Kartu Kemajuan|Lebar penuh, kompak|Lebaran penuh|Sejalan dengan pesan|
|Kartu Artefak|Lebaran penuh|Lebaran penuh|Sebaris, maks 60%|

### Ruang kerja

|Perilaku|Seluler|Tablet|Desktop|
|----------|--------|--------|---------|
|Bila samping|Lembaran bawah|Kiri yang bisa dilipat|Perbaiki ke kiri|
|tab|Gulir mendatar|Gulir mendatar|Tab penuh|
|Daftar berkas|Kartu lebar penuh|Daftar + mengecewakan|Daftar + mengecewakan|
|Jaringan artefak|1 kolom|2 kolom|3 kolom|

### Penampil Artefak

|Perilaku|Seluler|Tablet|Desktop|
|----------|--------|--------|---------|
|Tata Letak|Hamparan layar penuh|Tampilan terpisah|Tampilan terpisah|
|Pemilih versi|Lembaran bawah|Tarik-turun sebaris|Tarik-turun sebaris|
|Tombol tindakan|Bila bawah|Bila atas|Bila atas|

### Dialog Persetujuan

|Perilaku|Seluler|Tablet|Desktop|
|----------|--------|--------|---------|
|Posisi|Lembaran bawah|Modal tengah|Modal tengah|
|Tata letak tombol|Ditumpuk|Berdampingan|Berdampingan|
|Indikator risiko|Bila berwarna|Lencana berwarna|Lencana berwarna|

### Sejarah Eksekusi

|Perilaku|Seluler|Tablet|Desktop|
|----------|--------|--------|---------|
|Daftar|Kartu lebar penuh|Daftar ringkas|Daftar ringkas|
|Detil|Geser layar penuh|Panel geser|Perluasan sebaris|
|Garis Waktu|Vertikal|Vertikal|Horisontal atau vertikal|

---

## Sentuh Target

Semua elemen interaktif harus memiliki target sentuhan minimum 44x44px di seluler.

|Elemen|Ukuran|
|---------|------|
|Tombol kirim|44x44 piksel|
|Tombol persetujuan|Tinggi 44px, lebar penuh|
|Kartu artefak|Target ketuk lebar penuh|
|tab online|Memperbaiki bagian bawah, tinggi 48px|
|Pengalih sisi online|44x44 piksel|

---

## Penskalaan Tipografi

|Token|Seluler|Tablet|Desktop|
|-------|--------|--------|---------|
|`--font-size-md`|14 piksel|15 piksel|16 piksel|
|`--font-size-lg`|16 piksel|18 piksel|20 piksel|
|`--font-size-xl`|20 piksel|22 piksel|24 piksel|

---

## Pertunjukan

|Metrik|Target|
|--------|--------|
|Kucing Puas Pertama|< 1,5 detik pada 3G|
|Saatnya Interaktif|< 3s di 3G|
|Ukuran bundel|< 200KB di-gzip|
|Gambar|Pemuatan lambat, WebP, srcset responsif|

---

## Perilaku Offline

|Negara|Perilaku UI|
|-------|-------------|
|Memikat|Tampilkan spanduk secara offline. Antrean pesan untuk dicoba lagi.|
|memikat kembali|Tampilkan spanduk "Menghubungkan kembali...".|
|Sinkronisasi gagal|Tampilkan kesalahan dengan tombol coba lagi.|
