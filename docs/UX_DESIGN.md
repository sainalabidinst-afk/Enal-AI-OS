# Spesifikasi UX Design

<!-- DOCUMENT_METADATA_START -->
**Pemilik:** Tim Dokumentasi
**Pemilik Canonical:** Pimpinan Tata Kelola Dokumentasi
**Terakhir Diverifikasi:** 2026-08-02
**Versi:** 1.0.0
**Status:** Aktif
<!-- DOCUMENT_METADATA_END -->

Dokumen ini mendefinisikan pengalaman yang dilihat pengguna (user-facing experience) dari Enal AI OS. Ini adalah sumber kebenaran untuk cara pengguna berinteraksi dengan platform.

---

## Prinsip Inti

Satu percakapan. Satu AI. Satu tujuan. Banyak tugas. Satu hasil.

Pengguna tidak perlu tahu tentang Capability Packs, Workers, Execution Runtime, Task Planners, Execution Graphs, atau mekanisme internal lainnya.
Semua itu disembunyikan di balik antarmuka percakapan yang alami.

---

## Positioning

Enal AI OS adalah **AI Execution Platform**.

Pengguna mendeskripsikan outcome yang mereka inginkan.
ECP memahami tujuan, merencanakan eksekusi, mengoordinasikan tugas, memverifikasi hasil, dan mengirimkan outcome yang lengkap — semuanya melalui satu percakapan.

Bukan:
- "AI dengan 300 micro-agents"
- "AI Workforce"
- "Multi-Agent Framework"

Tetapi:
- "Satu AI yang menyelesaikan pekerjaan"

---

## Interface

User interface adalah satu window percakapan:

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
Tidak ada panel konfigurasi untuk memilih Workers.
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

Pengguna melihat: One Conversation → One Goal → One Result.
Secara internal: Goal Understanding → Execution Planning → Task DAG → Scheduler → Workers → Verification → Artifacts.

Goal Understanding adalah langkah paling kritis. AI harus memahami intent, konteks, batasan, dan outcome yang diinginkan sebelum mengeksekusi apa pun.

---

## Alur Kerja Pengguna

### 1. Pengguna Menyatakan Tujuan

Pengguna mendeskripsikan outcome yang diinginkan dalam bahasa alami atau mengunggah file.

Contoh:
- "Bangun aplikasi Inventory."
- "Analisa konfigurasi MikroTik ini."
- "Audit project FastAPI saya."
- "Saya ingin membuat ISP."

### 2. AI Memahami Tujuan

Di balik layar, ECP:
1. Memahami tujuan secara mendalam
2. Mengidentifikasi capability yang dibutuhkan
3. Memecah tujuan menjadi phase dan task
4. Mengidentifikasi dependensi dan paralelisme
5. Memperkirakan effort, artifacts, dan risiko
6. Membangun Execution Graph

Ini adalah **Goal Understanding**. Ini adalah bagian yang paling sulit dan paling penting.

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
- Pengguna melihat satu rencana yang koheren, bukan daftar task internal

### 5. AI Mengeksekusi

AI menampilkan progress real-time:

```
✓ Tujuan dipahami
✓ Plan dibuat
✓ Menjalankan Phase 1: Business Analysis
⏳ Menjalankan Phase 2: Architecture Design...
```

### 6. AI Mengirimkan Hasil

AI menyajikan outcome akhir:

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

## Workspace

Setiap proyek memiliki Workspace sendiri.

- Riwayat bertahan antar session
- Memory dibatasi per Workspace
- Artifacts diorganisasi per Workspace
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

## Transparansi Progress

Selama eksekusi, AI menampilkan progress yang dapat dibaca manusia:

```
✓ Memahami permintaan
✓ Memilih Capability
✓ Menyusun Task
⏳ Menganalisis konfigurasi...
⏳ Membuat dokumentasi...
```

Bukan:
- "Stage 3: Execute Subtask 7"
- Nama state internal
- Worker ID atau Execution Graph node ID

---

## Explainability

Pengguna dapat bertanya "mengapa" kapan saja:

> "Why did you choose that approach?"

AI merespons dengan:
- Ringkasan pemahaman tujuan
- Capability yang digunakan
- Reasoning di balik pilihan
- Tingkat confidence
- Langkah yang diambil

Tanpa istilah arsitektur internal. Hanya penjelasan yang ramah pengguna.

---

## Skill Discovery

Pengguna dapat bertanya:
- "Apa yang bisa kamu lakukan?"
- "What can you do?"

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

## Artifacts

Semua output signifikan dipersist sebagai Artifacts:
- Laporan analisis
- Rekomendasi
- Patch dan diff
- Laporan test
- Rencana deployment
- Dokumentasi

Artifacts bersifat:
- Versioned
- Dibatasi per Workspace
- Dapat diambil kembali
- Dapat dibandingkan
- Dapat dipulihkan

---

## Persetujuan Manusia

Untuk tindakan ireversibel, AI memerlukan persetujuan eksplisit:

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
- Muncul di skill discovery
- Mengikuti workflow yang sama
- Tidak diperlukan konfigurasi pengguna

---

## Apa yang Tidak Pernah Dilihat Pengguna

- Menu pemilihan Capability Pack
- Panel konfigurasi Worker
- Pengaturan Execution Runtime
- Output Task Planner
- Internal Execution Graph
- Worker ID atau nama
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
- AI semakin baik seiring waktu
- "Saya dapat mempercayai Enal AI OS untuk menyelesaikan pekerjaan"
- "AI ini memahami apa yang saya inginkan, bukan hanya apa yang saya ketik"

---

## Kriteria Keberhasilan

UX dianggap berhasil ketika:
1. Pengguna baru dapat menyelesaikan tugas nyata tanpa membaca dokumentasi
2. Pengguna tidak pernah perlu memilih Capability Pack secara manual
3. Pengguna tidak pernah perlu mengonfigurasi Workers, Runtimes, atau Planners
4. Semua alur explainability, progress, dan persetujuan terasa alami
5. Sistem terasa seperti satu AI, bukan kumpulan tool
6. Pengguna mendeskripsikan ECP sebagai "AI yang menyelesaikan pekerjaan" daripada "framework dengan banyak agent"
7. Pengguna dapat mendeskripsikan tujuannya dalam bahasa sederhana dan mendapatkan hasil yang lengkap dan terverifikasi

