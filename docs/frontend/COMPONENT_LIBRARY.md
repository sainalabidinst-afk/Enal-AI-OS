# Perpustakaan Komponen

<!-- DOCUMENT_METADATA_START -->
**Pemilik:** Tim Dokumentasi
**Pemilik Canonical:** Pimpinan Tata Kelola Dokumentasi
**Diverifikasi Terakhir:** 08-02-2026
**Versi:** 1.0.0
**Status:** Aktif
**SSOT:** Dokumentasi frontend untuk COMPONENT_LIBRARY
<!-- DOCUMENT_METADATA_END -->

Dokumen ini mendefinisikan inventaris komponen v1 yang diizinkan. Tidak ada komponen lain yang dapat dibuat tanpa Product Review.

---

## 1. Jendela Obrolan

**Tujuan:** Wadah percakapan utama.
**Alat Peraga:**
- `conversationId: string`
- `messages: Message[]`
- `onSend: (message: string) => void`
- `streaming: boolean`

**Perilaku:**
- Menampilkan riwayat percakapan.
- Gulir otomatis ke bawah pada pesan baru.
- Menampilkan kursor streaming saat `streaming=true`.
- Berisi PromptBox di bagian bawah.

---

## 2. membujuk Obrolan

**Tujuan:** Membujuk pesan tunggal.
**Alat Peraga:**
- `role: 'user' | 'assistant' | 'system'`
- `content: string`
- `timestamp: string`
- `artifacts?: Artifact[]`

**Perilaku:**
- Pesan pengguna disejajarkan dengan benar.
- Pesan Asisten rata kiri.
- Menampilkan batang waktu saat mengarahkan kursor.
- Merender artefak menjadi ArtifactCards jika ada.

---

## 3. Kotak Prompt

**Tujuan:** Masukkan teks untuk tujuan pengguna.
**Alat Peraga:**
- `onSubmit: (message: string) => void`
- `disabled: boolean`
- `placeholder: string`

**Perilaku:**
- Memperluas hingga 3 baris.
- Kirim saat Enter (Shift+Enter untuk baris baru).
- Diaktifkan selama pengiriman.
- Menampilkan tombol kirim.

---

## 4. Kartu Kemajuan

**Tujuan:** Kemajuan eksekusi secara real-time.
**Alat Peraga:**
- `executionId: string`
- `status: ExecutionStatus`
- `progress: number`
- `phases: ExecutionPhase[]`
- `currentPhase: string`

**Perilaku:**
- Menampilkan barbar kemajuan.
- Menampilkan nama fase saat ini.
- Menampilkan fase yang telah selesai sebagai tanda centang.
- Menampilkan fase yang tertunda sebagai kosong.
- Runtuh menjadi formulir ringkas di perangkat seluler.

---

## 5. Kartu Artefak

**Tujuan:** Pratinjau artefak tunggal.
**Alat Peraga:**
- `artifactId: string`
- `name: string`
- `type: string`
- `version: number`
- `onClick: () => void`

**Perilaku:**
- Menampilkan ikon jenis artefak.
- Menampilkan nama dan versi.
- Klik membuka Penampil Artefak.
- Arahkan kursor menunjukkan metadata.

---

## 6. Dialog Persetujuan

**Tujuan:** Mengonfirmasi atau menolak tindakan yang tidak dapat diubah.
**Alat Peraga:**
- `open: boolean`
- `title: string`
- `description: string`
- `risk: 'low' | 'medium' | 'high'`
- `rollbackAvailable: boolean`
- `testResults?: { passed: number; total: number }`
- `onApprove: () => void`
- `onReject: () => void`

**Perilaku:**
- Modal hamparan.
- Menunjukkan tingkat risiko dengan warna.
- Menampilkan status pengembalian.
- Menampilkan hasil tes jika tersedia.
- Tombol Setujui/Tolak selalu terlihat.
- Fokus berpindah ke tombol Setuju saat terbuka.

---

## 7. Garis Waktu Eksekusi

**Tujuan:** Garis waktu visual fase eksekusi.
**Alat Peraga:**
- `phases: ExecutionPhase[]`
- `currentPhaseId?: string`

**Perilaku:**
- Menampilkan fase secara berurutan.
- Fase yang selesai: tanda centang hijau.
- Fase berjalan: kemajuan animasi.
- Fase yang tertunda: abu-abu.
- Fase gagal: merah dengan kesalahan.
- Klik fase untuk melihat detailnya.

---

## 8. Bilah Sisi Ruang Kerja

**Tujuan:** Pengalih dan navigasi ruang kerja.
**Alat Peraga:**
- `workspaces: Workspace[]`
- `currentWorkspaceId: string`
- `onSelectWorkspace: (id: string) => void`
- `onNewWorkspace: () => void`

**Perilaku:**
- Desktop: memperbaiki sidebar kiri.
- Seluler: lembaran bawah dipicu oleh hamburger.
- Menampilkan nama ruang kerja dan jumlah artefak.
- Menampilkan tombol "Ruang Kerja Baru".
- Menampilkan Riwayat tautan Eksekusi.
- Menampilkan pengaturan.

---

## 9. Indikator Pemuatan

**Tujuan:** Status sedang memuat.
**Alat Peraga:**
- `size?: 'sm' | 'md' | 'lg'`
- `label?: string`

**Perilaku:**
- Menggunakan animasi spinner.
- Menampilkan label jika disediakan.
- TIDAK mencakup seluruh layar kecuali diminta secara eksplisit.
- Dapat diakses: `aria-label="Loading"`.

---

## 10. NotifikasiToast

**Tujuan:** Notifikasi non-pemblokiran.
**Alat Peraga:**
- `message: string`
- `type: 'info' | 'success' | 'warning' | 'error'`
- `duration?: number`
- `onDismiss: () => void`

**Perilaku:**
- Muncul di kanan atas (desktop) atau tengah atas (seluler).
- Menutup otomatis setelah `duration` (default 5 detik).
- Animasi slide-in.
- Tombol tutup selalu terlihat.
- Dapat ditumpuk.

---

## Aturan Komponen

1. Komponen menerima data melalui alat peran. Mereka tidak memanggil API secara langsung.
2. Komponen memancarkan peristiwa melalui panggilan balik. Mereka tidak mengubah keadaan secara langsung.
3. Komponen ditata hanya dengan desain token.
4. Komponen dapat diakses (keyboard navigasi, label ARIA).
5. Komponen secara responsif default.
