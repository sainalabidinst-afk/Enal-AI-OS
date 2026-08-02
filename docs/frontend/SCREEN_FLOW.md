# Alur Layar

<!-- DOCUMENT_METADATA_START -->
**Pemilik:** Tim Dokumentasi
**Pemilik Canonical:** Pimpinan Tata Kelola Dokumentasi
**Diverifikasi Terakhir:** 08-02-2026
**Versi:** 1.0.0
**Status:** Aktif
**SSOT:** Dokumentasi frontend untuk SCREEN_FLOW
<!-- DOCUMENT_METADATA_END -->

Dokumen ini mendefinisikan alur pengguna di semua layar v1. Ini adalah referensi untuk navigasi, routing, dan transisi layar.

---

## Peta Layar

```
┌────────────────────────────────────────────────────────┐
│  WorkspaceSidebar (collapsible)                       │
│  - Workspace list                                     │
│  - Execution history link                             │
│  - Settings link                                      │
└────────────────────────────────────────────────────────┘
                    │
                    ▼
┌────────────────────────────────────────────────────────┐
│  Main Layout                                          │
│  ┌──────────────────────────────────────┐    │
│  │                                    │    │
│  │  Screen Content                    │    │
│  │                                    │    │
│  │                                    │    │
│  └──────────────────────────────────────┘    │
│                                          │
│  [persistent: NotificationToast]        │
└────────────────────────────────────────────────────────┘
```

---

## Layar 1: Obrolan

**Rute:** `/chat`
**Tujuan:** antarmuka utama. Pengguna mengetik tujuan, melihat respon AI, kemajuan, dan artefak.

**Titik masuk:**
- Rute default saat aplikasi dibuka.
- Pengguna mengklik "Obrolan Baru" atau memilih Workspace.

**Alur:**
1. Pengguna melihat ChatWindow dengan riwayat percakapan (jika ada).
2. Pengguna mengetik tujuan di PromptBox.
3. Pengguna menekan Kirim atau Enter.
4. Pesan pengguna muncul sebagai ChatBubble.
5. Respons AI mengalir sebagai ChatBubble.
6. Jika eksekusi dimulai, ProgressCard muncul inline.
7. Artifact muncul sebagai ArtifactCards inline.
8. Dialog persetujuan muncul jika tindakan memerlukan persetujuan.
9. Pengguna menyetujui atau menolak.
10. Eksekusi berlanjut atau berhenti.

**Titik keluar:**
- Pengguna berpindah Workspace → layar Workspace.
- Pengguna mengklik Riwayat Eksekusi → layar Riwayat Eksekusi.
- Pengguna mengklik Pengaturan → Pengaturan layar.

---

## Layar 2: Ruang Kerja

**Rute:** `/workspace/:workspaceId`
**Tujuan:** Ikhtisar proyek dengan percakapan, file, memori, artefak, linimasa.

**Titik masuk:**
- Pengguna mengklik Workspace di sidebar.
- Pengguna mengklik tautan artefak dari Chat.
- Ruang kerja dibuat otomatis saat Obrolan dibuka.

**Alur:**
1. Pengguna melihat header Workspace dengan nama.
2. Tab: Percakapan, File, Artefak, Eksekusi, Timeline.
3. Tab Percakapan menampilkan riwayat dialog untuk ruang kerja ini.
4. Tab Files menampilkan file yang diunggah.
5. Tab Artefak menampilkan semua artefak di ruang kerja ini.
6. Tab Execution menampilkan riwayat eksekusi untuk workspace ini.
7. Tab Timeline menampilkan acara proyek secara kronologis.

**Titik keluar:**
- Pengguna mengklik artefak → Penampil Artefak.
- Pengguna mengklik eksekusi → detail Riwayat Eksekusi.
- Pengguna mengklik kembali → Obrolan.

---

## Layar 3 : Penampil Artefak

**Rute:** `/artifact/:artifactId`
**Tujuan:** Melihat, membandingkan, dan memulihkan versi artefak.

**Titik masuk:**
- Pengguna mengklik ArtifactCard di Chat.
- Pengguna mengklik artefak di Workspace.
- Pengguna mengklik artefak di Riwayat Eksekusi.

**Alur:**
1. Pengguna melihat konten artefak.
2. Pemilih versi menampilkan versi yang tersedia.
3. Pengguna dapat membandingkan dua versi.
4. Pengguna dapat memulihkan versi sebelumnya.
5. Pengguna dapat mengunduh/mengekspor artefak.

**Titik keluar:**
- Pengguna mengklik kembali → layar sebelumnya.
- Pengguna menutup viewer → kembali ke Chat atau Workspace.

---

## Layar 4 : Dialog Persetujuan

**Rute:** Modal overlay (tanpa rute)
**Tujuan:** Mengonfirmasi atau menolak tindakan yang tidak dapat dibatalkan.

**Pemicu:**
- Eksekusi mencapai titik kesepakatan.
- AI menyajikan perubahan yang diusulkan dengan penilaian risiko.

**Alur:**
1. Modal muncul di atas layar saat ini.
2. Pengguna melihat:
   - Apa yang akan berubah.
   - Tingkat risiko.
   - Kembalikan ketersediaan.
   - Hasil tes (jika relevan).
3. Pengguna mengklik Setuju atau Tolak.
4. Jika selesai, eksekusi dilanjutkan.
5. Jika ditolak, eksekusi dihentikan atau meminta penyempurnaan.

**Titik keluar:**
- Setuju → eksekusi dilanjutkan.
- Tolak → eksekusi berhenti, kembali ke Chat.

---

## Layar 5: Pengaturan

**Rute:** `/settings`
**Tujuan:** Mengonfigurasi model, tema, notifikasi, kunci API.

**Titik masuk:**
- Pengguna mengklik Pengaturan di sidebar.
- Pengguna meminta AI "Buka pengaturan".

**Alur:**
1. Pengguna melihat pengaturan.
2. Bagian: Model, Tema, Notifikasi, API Kunci.
3. Pengguna mengubah pengaturan.
4. Pengaturan disimpan langsung atau saat tombol "Simpan".
5. Perubahan segera terjadi.

**Titik keluar:**
- Pengguna mengklik kembali atau menutup → kembali ke layar sebelumnya.

---

## Layar 6: Penemuan Kemampuan

**Rute:** Dapat diakses melalui `/capabilities` atau dipicu oleh pertanyaan pengguna di Chat.
**Tujuan:** Menunjukkan apa yang dapat dilakukan ECP.

**Titik masuk:**
- Pengguna bertanya "Apa yang bisa kamu lakukan?" di Obrolan.
- Pengguna mengklik "Temukan" di sidebar.

**Alur:**
1. Pengguna melihat daftar Capability Packs.
2. Pengguna mengklik suatu kemampuan.
3. AI menunjukkan subtugas dan contoh untuk kemampuan tersebut.
4. Pengguna dapat mengklik "Try it" untuk memulai percakapan dengan kemampuan tersebut.

**Titik keluar:**
- Pengguna mengklik kembali → Obrolan.
- Pengguna memulai percakapan → Obrolan.

---

## Layar 7: Riwayat Eksekusi

**Rute:** `/executions`
**Tujuan:** Mendaftar semua eksekusi dengan status, kemajuan, dan artefak.

**Titik masuk:**
- Pengguna Riwayat mengklik Eksekusi di sidebar.
- Pengguna melihat riwayat eksekusi di Workspace.

**Alur:**
1. Pengguna melihat daftar eksekusi.
2. Setiap eksekusi menampilkan:
   - Tujuan
   - Status
   - Kemajuan
   - Durasi
   - Jumlah artefak
3. Pengguna mengklik eksekusi → tampilan detail.
4. Tampilan detailnya menunjukkan:
   - Linimasa eksekusi penuh
   - Rincian fase
   - Catatan
   - Artefak
   - Opsi coba lagi/jalankan ulang

**Titik keluar:**
- Pengguna mengklik kembali → layar sebelumnya.
- Pengguna mengklik eksekusi → detail Eksekusi.

---

## Aturan Navigasi

1. **Navigasi primer:** WorkspaceSidebar (desktop) / Navigasi bawah (seluler).
2. **Navigasi sekunder:** Breadcrumbs dan tombol kembali.
3. **Tidak ada tautan dalam ke internal negara:** URL hanya berisi pengidentifikasi (workspaceId, eksekusiId, artefakId), bukan internal negara.
4. **Tidak ada jebakan tombol kembali browser:** Tombol kembali selalu kembali ke layar logistik sebelumnya.
5. **Tidak ada jendela popup:** Semua navigasi tetap di dalam aplikasi satu halaman.

---

## Tabel Perutean

|Rute|Layar|Membutuhkan Auth|Membutuhkan Ruang Kerja|
|-------|--------|---------------|-------------------|
|`/`|Obrolan (alihkan ke `/chat`)|Tidak|Tidak|
|`/chat`|Mengobrol|Tidak|Buat otomatis|
|`/workspace/:workspaceId`|Ruang kerja|Tidak|Ya|
|`/artifact/:artifactId`|Penampil Artefak|Tidak|Tidak|
|`/executions`|Sejarah Eksekusi|Tidak|Tidak|
|`/executions/:executionId`|Detil Eksekusi|Tidak|Tidak|
|`/capabilities`|Penemuan Kemampuan|Tidak|Tidak|
|`/settings`|Pengaturan|Tidak|Tidak|

---

## Aturan Transisi

|Transisi|Pemicu|Animasi|
|------------|---------|-----------|
|Obrolan → Ruang Kerja|Pengguna mengklik ruang kerja|Menggeser|
|Obrolan → Riwayat Eksekusi|Pengguna mengklik riwayat|Menggeser|
|Obrolan → Penampil Artefak|Pengguna mengklik artefak|Menggeser|
|Apa saja → Dialog Persetujuan|Eksekusi memerlukan persetujuan|Memudar|
|Apa saja → Pengaturan|Pengguna mengklik pengaturan|Menggeser|
|Apa saja → Obrolan|Pengguna mengklik kembali|Geser mundur|

Animasi harus halus dan cepat (150-200ms). Tidak ada transisi yang rumit.
