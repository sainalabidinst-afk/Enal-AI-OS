# Prinsip Arsitektur ECP

<!-- DOCUMENT_METADATA_START -->
**Pemilik:** Tim Dokumentasi
**Pemilik Canonical:** Pimpinan Tata Kelola Dokumentasi
**Diverifikasi Terakhir:** 08-02-2026
**Versi:** 1.0.0
**Status:** Aktif
**SSOT:** Dokumentasi untuk ARCHITECTURE_PRINCIPLES
<!-- DOCUMENT_METADATA_END -->


Ini adalah prinsip dasar yang mengatur semua keputusan desain dan implementasi di Enal Cognitive Platform (ECP).

## 1. Platform Ada untuk Melayani Aplikasi


> **Setiap perubahan pada Kernel, Runtime, SDK, Studio, atau Marketplace harus disesuaikan dengan kebutuhan aplikasi nyata.**

- Tidak ada mesin, abstraksi, atau modul yang ditambahkan kecuali aplikasi referensi memerlukannya.
- Jika tidak ada aplikasi yang memerlukan fitur, maka fitur tersebut tidak ada.
- Lamaran adalah warga negara kelas satu; komponen platform adalah infrastruktur.

## 2. Tidak Ada Jalan Pintas dalam Integrasi


> **Referensi aplikasi harus menggunakan tumpukan platform lengkap.**

Jika aplikasi referensi melewati SDK, Runtime, Kontrak, Marketplace, atau Studio, itu merupakan kerusakan platformâ€”bukan solusi aplikasi.

- SDK Agen â†’ Adaptif Runtime â†’ Saluran Kognitif â†’ Plugin â†’ Sistem Artefak â†’ Studio Trace
- Setiap komponen harus dijalankan setidaknya satu aplikasi referensi.

## 3. Stabilitas Kernel

> **Kernel harus tetap kecil, stabil, dan dapat diprediksi.**

- Kernel harus berada di bawah 5.000 baris kode.
- Kernel tidak boleh memiliki ketergantungan eksternal selain stdlib + pydantic.
- Kontrak kernel memiliki versi dan kompatibel dengan versi utama.
- Perubahan yang dapat menyebabkan gangguan memerlukan masa tenggang 2 rilis dengan panduan migrasi.

## 4. Pengembangan Kontrak-Pertama


> **Semua antarmuka publik adalah kontrak.**

- Setiap batas modul ditentukan oleh kontrak yang diketik.
- Kontrak didaftarkan, dibuat versinya, dan diuji kompatibilitasnya.
- SDK, Plugin, dan alat eksternal bergantung pada kontrak, bukan implementasi detail.

## 5. Dapat Diamati secara Default


> **Setiap eksekusi meninggalkan jejak.**

- Semua rangkaian kognitifnya memancarkan rentang jejak.
- Semua keputusan mencatat alasan, keyakinan, dan biaya.
- Semua artefak memiliki versi dan dapat diaudit.
- Studio menyediakan proses replay, diff, dan perbandingan.

## 6. Keamanan berdasarkan Desain

> **Plugin tidak dipercaya secara default.**

- Plugin mendeklarasikan izin yang diperlukan secara eksplisit.
- Plugin istimewa memerlukan persetujuan manual.
- Eksekusi sandbox untuk Plugin terbatas/istimewa.
- Tidak ada Plugin yang mendapat akses lebih dari yang dibutuhkan.

## 7. Pengalaman Pengembang adalah Produk


> **Jika pengembang tidak dapat membuat aplikasi dalam waktu kurang dari 1 jam, berarti platform belum siap.**

- SDK harus dapat diinstal dengan pip dengan dekorator yang jelas.
- Dokumentasi harus menyertakan contoh end-to-end.
- Pesan kesalahan harus dapat ditindaklanjuti.
- Debugging harus dapat dilakukan tanpa membaca kode sumber platform.

## 8. Pengujian adalah Gerbang Kualitas


> **Tidak ada PR yang digabung tanpa melewati gerbang kualitas penuh.**

Gerbang kualitas meliputi:
1. Serat & format
2. Ketik periksa
3. Tes satuan
4. Tes batas arsitektur
5. Tolok ukur kinerja
6. Kompatibilitas SDK
7. Kompatibilitas Plugin
8. Golden Test suite

Setiap blok kegagalan digabungkan.

## 9. Ukur Berdasarkan Hasil, Bukan Artefak


> **Kemajuan diukur berdasarkan apa yang dapat dicapai pengguna, bukan berdasarkan jumlah file yang ada.**

Metrik yang buruk:
- Jumlah file
- Jumlah agen
- Jumlah Plugin
- Jumlah komitmen

Metrik yang bagus:
- Referensi aplikasi yang berjalan end-to-end
- Golden Test tingkat kelulusan
- Waktu orientasi pengembang
- Tingkat keberhasilan penerapan produksi

## 10. Prinsip Tata Kelola Manusia


> **Tidak ada perubahan kode, konfigurasi, atau arsitektur yang dapat diterapkan tanpa persetujuan pengguna secara eksplisit.**

- Kemampuan otonom dapat menganalisis, merencanakan, dan mempersiapkan perubahan.
- Eksekusi perubahan memerlukan persetujuan pengguna secara eksplisit.
- Semua proposal, perbedaan, hasil pengujian, dan catatan persetujuan disimpan sebagai artefak.
- Platform tidak pernah memodifikasi dirinya sendiri tanpa adanya keputusan manusia.

## 11. Pembelajaran Berkelanjutan


> **Platform meningkat dari setiap eksekusi.**

- Setiap lari menghasilkan pelajaran.
- Tolok ukur berjalan pada setiap perubahan.
- Regresi terdeteksi dalam beberapa menit.
- Meta-kognisi mengoptimalkan pemilihan saluran pipa dari waktu ke waktu.

---

## Filter Keputusan

Gunakan filter ini untuk setiap keputusan penting:

```
1. Does a reference application need this?
   â†’ No: reject.
   â†’ Yes: continue.

2. Does it require kernel changes?
   â†’ Yes: propose an RFC.
   â†’ No: implement in runtime/plugin/apps.

3. Does it break any existing contract?
   â†’ Yes: deprecate first, migrate, then remove.
   â†’ No: proceed.

4. Does it respect Human Governance Principle?
   â†’ No: reject.
   â†’ Yes: continue.

5. Is it testable?
   â†’ No: refine until it is.
   â†’ Yes: add to golden test suite.

6. Can a developer discover and use it in <1 hour?
   â†’ No: improve DX before merging.
   â†’ Yes: merge.
```
