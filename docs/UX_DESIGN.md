# Spesifikasi Desain UX

<!-- DOCUMENT_METADATA_START -->
**Pemilik:** Tim Dokumentasi
**Pemilik Canonical:** Pimpinan Tata Kelola Dokumentasi
**Diverifikasi Terakhir:** 02-08-2026
**Versi:** 1.0.0
**Status:** Aktif
<!-- DOCUMENT_METADATA_END -->

Dokumen ini mendefinisikan pengalaman yang dilihat pengguna (user-facing experience) dari Enal AI OS. Ini adalah sumber kebenaran untuk cara pengguna berinteraksi dengan platform.

---

## Prinsip Inti

Satu percakapan. Satu AI. Satu tujuan. Banyak tugas. Satu hasil.

Pengguna tidak perlu tahu tentang Capability Packs, Workers, Execution Runtime, Task Planners, Execution Graphs, atau mekanisme internal lainnya.
Semua itu diungkapkan di balik percakapan antar muka yang alami.

---

## Penentuan posisi

Terakhir AI OS adalah **Platform Eksekusi AI**.

Pengguna mendeskripsikan hasil yang mereka inginkan.
ECP memahami tujuan, merencanakan eksekusi, mengoordinasikan tugas, memverifikasi hasil, dan mengirimkan hasil yang lengkap — semuanya melalui satu percakapan.

Bukan:
- "AI dengan 300 agen mikro"
- "Tenaga Kerja AI"
- "Kerangka Kerja Multi-Agen"

Tetapi:
- "Satu AI yang menyelesaikan pekerjaan"

---

## Antarmuka

Antarmuka pengguna adalah satu jendela percakapan:

```
┌─────────────────────────────────────┐
│         Enal AI OS                   │
├─────────────────────────────────────┤
│                                      │
│  Describe the outcome you want.      │
│                                      │
│  ________________________________    │
│ | Ketik perintah...              |   │
│ |________________________________|   │
│                                      │
└─────────────────────────────────────┘
```

Tidak ada menu untuk memilih Capability Packs.
Tidak ada panel konfigurasi untuk memilih Pekerja.
Tidak ada dropdown untuk memilih Execution Runtime.
Tidak ada indikator "Agent Swarm".

AI melakukan semuanya secara internal.

---

## Model Eksekusi

```
One Conversation
        ↓
    One Goal
        ↓
  Goal Understanding
        ↓
 Execution Planning
        ↓
    Many Tasks
        ↓
   Execution Graph
        ↓
    Scheduler
        ↓
   Many Workers
        ↓
    Verification
        ↓
     Artifacts
        ↓
   One Result
```

Pengguna melihat: Satu Percakapan → Satu Tujuan → Satu Hasil.
Secara internal: Pemahaman Sasaran → Perencanaan Eksekusi → DAG Tugas → Penjadwal → Pekerja → Verifikasi → Artefak.

Goal Understanding adalah langkah paling kritis. AI harus memahami maksud, konteks, batasan, dan hasil yang diinginkan sebelum mengeksekusi apa pun.

---

## Alur Kerja Pengguna

### 1. Pengguna Menyatakan Tujuan

Pengguna mendeskripsikan hasil yang diinginkan dalam bahasa alami atau mengunggah file.

Contoh:
- "Bangun aplikasi Inventaris."
- "Analisa konfigurasi MikroTik ini."
- "Audit proyek FastAPI saya."
- "Saya ingin membuat ISP."

### 2. AI Memahami Tujuan

Di balik layar, ECP:
1. Memahami tujuan secara mendalam
2. Mengidentifikasi kemampuan yang dibutuhkan
3. Memecah tujuan menjadi fase dan tugas
4. Mengidentifikasi dependensi dan paralelisme
5. Memperkirakan usaha, artefak, dan risiko
6. Membangun Grafik Eksekusi

Ini adalah **Pemahaman Tujuan**. Ini adalah bagian yang paling sulit dan paling penting.

### 3. AI Menyajikan Rencana

AI merespons dengan rencana yang jelas dan dapat ditindaklanjuti:

```
Saya memahami tujuan Anda.

Saya membaginya menjadi:
Phase 1: Business Analysis
Phase 2: Architecture Design
Phase 3: Backend Implementation
Phase 4: Frontend Implementation
Phase 5: Testing
Phase 6: Documentation

Estimasi: 187 subtasks, 38 artifacts, existing packs

Mulai?
```

### 4. Pengguna Menyetujui atau Menyempurnakan

- Pengguna dapat menyetujui, menyempurnakan, atau membatalkan
- Tidak diperlukan konfigurasi tersembunyi
- Pengguna melihat satu rencana yang koheren, bukan daftar tugas internal

### 5. AI Mengeksekusi

AI menampilkan kemajuan secara real-time:

```
✓ Tujuan dipahami
✓ Plan dibuat
✓ Menjalankan Phase 1: Business Analysis
⏳ Menjalankan Phase 2: Architecture Design...
```

### 6. AI Mengirimkan Hasil

AI menyajikan hasil akhir:

```
Selesai.

Hasil:
- requirements.md
- architecture.md
- database_schema.sql
- backend/ (complete)
- frontend/ (complete)
- tests/ (87% coverage)
- README.md

Apakah ada yang perlu diperbaiki?
```

---

## Ruang kerja

Setiap proyek memiliki Ruang Kerja sendiri.

- Kisah bertahan antar session
- Memori dibatasi per Ruang Kerja
- Artefak diorganisasi per Workspace
- Pengguna dapat berpindah antar Workspace

Contoh:
```
Workspace: Inventory System
├── History
├── Artifacts
│   ├── requirements.md
│   ├── schema.sql
│   └── backend/
└── Memory
```

---

## Kemajuan Transparansi

Selama eksekusi, AI menampilkan kemajuan yang dapat dibaca manusia:

```
✓ Memahami permintaan
✓ Memilih Capability
✓ Menyusun Task
⏳ Menganalisis konfigurasi...
⏳ Membuat dokumentasi...
```

Bukan:
- "Tahap 3: Jalankan Subtugas 7"
- Nama keadaan internal
- ID Pekerja atau ID node Grafik Eksekusi

---

## Penjelasan

Pengguna dapat bertanya "mengapa" kapan saja:

> “Mengapa kamu memilih pendekatan itu?”

AI merespons dengan:
- Ringkasan pemahaman tujuan
- Kemampuan yang digunakan
- Alasan di balik pilihan
- Tingkat kepercayaan diri
- Langkah yang diambil

Tanpa istilah arsitektur internal. Hanya penjelasan yang ramah pengguna.

---

## Penemuan Keterampilan

Pengguna dapat bertanya:
- "Apa yang bisa kamu lakukan?"
- "Apa yang bisa kamu lakukan?"

AI merespons dari Capability Graph secara dinamis:

```
Saya memiliki 13 Capability Pack:
✓ Network Engineering
  - Audit MikroTik
  - Audit Cisco
  - Audit Fortinet
  - Generate Documentation
  - Compliance Check
  - Security Review
✓ Code Engineering
  - Full-stack generation
  - Code review
  - Security review
  - Architecture analysis
...
Mau mulai dari mana?
```

---

## Artefak

Semua keluaran signifikan dipertahankan sebagai Artefak:
- Analisis laporan
- Rekomendasi
- Patch dan diff
- Laporan tes
- Rencana penerapan
- Dokumentasi

Artefak bersifat:
- Berversi
- Dibatasi per Ruang Kerja
- Dapat diambil kembali
- Dapat dibandingkan
- Dapat dijanjikan

---

## Persetujuan Manusia

Untuk tindakan yang tidak dapat diubah, AI memerlukan persetujuan eksplisit:

```
Saya akan menerapkan patch ini.

Files modified:
- src/auth/service.py
- src/auth/validator.py

Tests: 43/43 passed

[Ya, terapkan] [Tidak, batalkan]
```

---

## Ekosistem Plugin

Capability Pack baru yang diinstal melalui Marketplace secara otomatis terintegrasi:
- Muncul di penemuan keterampilan
- alur kerja berikutnya yang sama
- Tidak diperlukan konfigurasi pengguna

---

## Apa yang Tidak Pernah Dilihat Pengguna

- Menu pemilihan Capability Pack
- Panel konfigurasi Pekerja
- Pengaturan Execution Runtime
- Perencana Tugas Keluaran
- Grafik Eksekusi Internal
- ID Pekerja atau nama
- Struktur data internal
- Pesan error dari modul internal

Jika pengguna melihat salah satu dari ini, desain UX telah gagal.

---

## Apa yang Seharusnya Dirasakan Pengguna

- Satu asisten AI yang kompeten
- Tanpa perlu konfigurasi
- Hasil datang dari keahlian, bukan menu
- AI menjelaskan saat diminta
- AI tidak pernah bertindak tanpa persetujuan
- AI mengingat konteks antar percakapan
- AI semakin baik seiring berjalannya waktu
- "Saya dapat mempercayai Enal AI OS untuk menyelesaikan pekerjaan"
- "AI ini memahami apa yang saya inginkan, bukan hanya apa yang saya ketik"

---

## Kriteria Keberhasilan

UX dianggap berhasil ketika:
1. Pengguna baru dapat menyelesaikan tugas nyata tanpa membaca dokumentasi
2. Pengguna tidak perlu memilih Capability Pack secara manual
3. Pengguna tidak perlu mengonfigurasi Workers, Runtimes, atau Planners
4. Semua alur penjelasan, kemajuan, dan persetujuan terasa alami
5. Sistem terasa seperti satu AI, bukan kumpulan alat
6. Pengguna mendeskripsikan ECP sebagai "AI yang menyelesaikan pekerjaan" daripada "framework dengan banyak agen"
7. Pengguna dapat mendeskripsikan tujuannya dalam bahasa sederhana dan mendapatkan hasil yang lengkap dan terverifikasi
