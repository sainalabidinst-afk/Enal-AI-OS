# Arsitektur UI Frontend

<!-- DOCUMENT_METADATA_START -->
**Pemilik:** Tim Dokumentasi
**Pemilik Canonical:** Pimpinan Tata Kelola Dokumentasi
**Diverifikasi Terakhir:** 08-02-2026
**Versi:** 1.0.0
**Status:** Aktif
**SSOT:** Dokumentasi frontend untuk UI_ARCHITECTURE
<!-- DOCUMENT_METADATA_END -->

**Status:** Beku
**Efektif:** 07-11-2026
**Pemilik:** Kepala Bagian Produk
**Tujuan:** Mendefinisikan aturan dan alur arsitektur yang tidak dapat dinegosiasikan untuk implementasi frontend. Tidak ada kode React yang boleh ditulis sebelum dokumen ini disetujui.

---

## 1. Aturan Arsitektur Frontend

Aturan-aturan ini tidak dapat dinegosiasikan. Kode apa pun yang melanggarnya adalah cacat.

### Aturan 1 — Frontend Tidak Pernah Berpikir

Frontend tidak boleh membuat keputusan yang menjadi tanggung jawab backend.

**Salah:**
```typescript
if (message.includes("mikrotik")) {
  capability = "network";
}
```

**Benar:**
```typescript
POST /api/v1/chat
// Backend menentukan segalanya
Frontend hanya merender.
```

Frontend adalah lapisan rendering. Frontend tidak menginterpretasi, mengklasifikasi, atau melakukan routing.

### Aturan 2 — Frontend Tidak Pernah Merencanakan

Frontend tidak boleh membuat:
- tugas
- grafik eksekusi
- penjadwalan
- pengugasan kemampuan
- rencana dalam bentuk apa pun

Semua itu berasal dari backend.

### Aturan 3 — Backend adalah Sumber Kebenaran

Untuk setiap bagian aplikasi, hanya ada satu sumber kebenaran — backend.

Frontend tidak boleh menghitung state turunan yang sudah dikirim backend.

Contoh — kemajuan:
```json
{
  "phase": "Security Analysis",
  "progress": 65
}
```

Backend mengirim ini. Frontend menampilkan ini. Tanpa komputasi lokal.

### Aturan 4 — UI = Proyeksi

Frontend adalah proyeksi dari state backend. Semua state berasal dari mutasi backend.

|Konsep Negara|Sumber|
|---------------|--------|
|Ruang kerja|Bagian belakang|
|Percakapan|Bagian belakang|
|Eksekusi|Bagian belakang|
|Artefak|Bagian belakang|
|Kemajuan|Bagian belakang|
|Pemberitahuan|Bagian belakang|
|Tema|Bagian depan|
|Bila samping|Bagian depan|

Frontend diizinkan melakukan cache sementara untuk menjalankan UX, tetapi tidak pernah menjadi sumber kebenaran.

### Aturan 5 — Nol Logika Mock

Data palsu tidak diizinkan di layar produksi mana pun setelah backend terhubung.

Terlarang:
- `fakeExecution()`
- `fakeArtifact()`
- `dummyHistory()`
- Fixture hardcode apa pun di layar atau fitur

Pratinjau Pengembang harus menggunakan API backend nyata. Data tiruan hanya dapat diterima dalam konteks pengembangan lokal yang dilindungi dan tidak pernah dirilis.

### Aturan 6 — Komponen Stateless

Komponen harus se-stateless mungkin.

```typescript
// Benar
<ProgressCard phase="Security Analysis" progress={65} />

// Salah (mengandung logika bisnis)
<ProgressCard data={execution} onPhaseUpdate={...} />
```

Komponen menerima data melalui props dan memancarkan event melalui callback. Mereka tidak memiliki logika bisnis.

### Aturan 7 — UI Tidak Mengenal Kapabilitas

Frontend tidak boleh memiliki logika khusus domain seperti:

```typescript
switch (domain) {
  case "network":
  case "trading":
  case "research":
}
```

Frontend hanya mengenal konsep-konsep ini:
- Eksekusi
- Artefak
- Percakapan
- Pemberitahuan

Domain dan Capability Packs adalah konsep backend dan tidak pernah diekspos ke lapisan UI.

---

## 2. Data Alur

Jalur kanonik untuk semua data di frontend:

```
Backend
  ↓
API (REST / WebSocket / SSE)
  ↓
Service Layer (services/)
  ↓
Store (Zustand slices)
  ↓
Selector (derive UI data)
  ↓
Component (dumb, props-only)
  ↓
User
```

Aturan:
- Components tidak pernah memanggil API secara langsung.
- Komponen tidak pernah memanggil layanan secara langsung.
- Komponen hanya berlangganan penyeleksi toko.
- Layanan menormalkan dan memvalidasi respons API sebelum disimpan.
- Store adalah satu-satunya gerbang antara layanan dan komponen.

---

## 3. Acara Alur

Jalur kanonik untuk semua acara yang dipicu pengguna:

```
User
  ↓
UI (click, input, gesture)
  ↓
API call (via service)
  ↓
Backend
  ↓
Streaming response (SSE / WebSocket)
  ↓
Store update (via stream handler)
  ↓
UI re-render
```

Aturan:
- Panggilan API terjadi segera — tidak ada status "waiting" perantara sebelum panggilan API pertama.
- Update streaming langsung menuju toko.
- Toko memancarkan perubahan; komponen me-render ulang secara otomatis.
- Tidak ada polling `setTimeout` lokal.

---

## 4. Kepemilikan Negara

|Negara|Pemilik|Bertahan|Catatan|
|-------|-------|----------|-------|
|Percakapan|Bagian belakang|Ya|Pesan, streaming status|
|Ruang kerja|Bagian belakang|Ya|File, memori, konteks|
|Eksekusi|Bagian belakang|Ya|Status, fase, log, kemajuan|
|Artefak|Bagian belakang|Ya|Versi, konten|
|Pemberitahuan|Bagian belakang|Ya|Hitungan yang belum dibaca, sejarah|
|Model Pemilihan|Bagian belakang|Ya|Rute melalui `/api/v1/models/route`|
|Tema|Bagian depan|Penyimpanan lokal|Hanya preferensi UI|
|Status online sisi|Bagian depan|Penyimpanan lokal|Buka/tutup, lebar|
|Draf pesan|Bagian depan|Hanya kenangan|Dihapus saat dikirim|

Tidak ada potongan negara yang boleh ada di banyak tempat. Jika backend memilikinya, frontend tidak pernah menyimpan salinannya sebagai sumber kebenaran.

---

## 5. Kontrak Streaming

Backend menggunakan Server-Sent Events (SSE) atau WebSocket untuk semua pembaruan secara real-time.

Semua event stream harus ditangani oleh satu stream middleware yang memperbarui store.

|Tipe Acara|Toko Aksi|
|------------|--------------|
|`final`|`addMessage()`|
|`execution_started`|`addExecution()`|
|`phase`|`updatePhase()` / `addPhase()`|
|`task`|`addTask()` (jika potongan berlaku)|
|`log`|`addLog()`|
|`artifact`|`addArtifact()`|
|`progress`|`setProgress()`|
|`execution_complete`|`setExecutionStatus('completed')`|
|`error`|`setError()`|

Tidak ada komponen yang boleh mengonsumsi stream secara langsung. Komponen hanya menggunakan penyeleksi toko.

---

## 6. Lapisan Layanan Kontrak

Semua komunikasi backend terjadi melalui `src/services/`.

```typescript
// services/api.ts — semua panggilan HTTP
// services/chat.ts — fungsi API khusus chat
// services/execution.ts — fungsi API khusus execution
// services/workspace.ts — fungsi API khusus workspace
// services/artifact.ts — fungsi API khusus artifact
// services/notification.ts — fungsi API khusus notification
// services/stream.ts — WebSocket/SSE stream handler
```

Aturan:
- Layanan mengembalikan janji atau yang dapat diamati (untuk streaming).
- Layanan tidak pernah mengubah toko secara langsung. Mereka memancarkan aksi.
- Layanan tidak pernah mengandung logika UI.
- Layanan tidak pernah mengejek. Mereka memanggil API nyata.
- Layanan menormalkan semua respons API agar cocok dengan tipe toko.

---

## 7. Toko Kontrak

```typescript
// store/conversationSlice.ts
// store/workspaceSlice.ts
// store/executionSlice.ts
// store/artifactSlice.ts
// store/notificationSlice.ts
// store/settingsSlice.ts
```

Aturan:
- Setiap irisan adalah satu toko Zustand.
- Keadaan dinormalisasi berdasarkan ID.
- Tidak ada array yang berisi objek lengkap.
- Tidak ada status turunan yang disimpan.
- Semua pengobatan harus memiliki aksi eksplisit.
- Selectors adalah satu-satunya antarmuka baca publik.
- Statuskan irisan dihidrat dari backend saat aplikasi dimuat.

---

## 8. Kontrak Komponen

```typescript
// components/ChatBubble/
// components/ProgressCard/
// components/ArtifactCard/
// components/ApprovalDialog/
// components/ExecutionTimeline/
```

Aturan:
- Komponen menerima data melalui alat peraga.
- Komponen memancarkan acara melalui panggilan balik (void return).
- Komponen tidak pernah mengimpor layanan.
- Komponen tidak pernah mengimpor keadaan internal komponen lain.
- Komponen tidak pernah mengandung logika bisnis.
- Components tidak pernah memutuskan apa yang dirender berdasarkan tipe domain.
- Komponen menggunakan desain token untuk semua nilai visual.

---

## 9. Lapisan Fitur Kontrak

```typescript
// features/chat/
// features/workspace/
// features/execution/
// features/artifact/
// features/settings/
// features/notifications/
```

Aturan:
- Fitur memiliki logika untuk domain mereka.
- Fitur menyusun komponen.
- Fitur memanggil layanan.
- Fitur mencerminkan tindakan toko.
- Fiturnya dapat mengandung logika orkestrasi tetapi tidak pernah logika keputusan backend.

---

## 10. Yang Dilarang

Pola-pola berikut secara eksplisit dilarang:

- Beralih pada `domain`, `capability`, atau `capabilityId` ke kode frontend
- `if (message.includes(...))` sebaris untuk mendeteksi maksud
- Komputasi lokal untuk kemajuan, status, atau fase
- `setTimeout` / polling untuk memperbarui status
- Direktori `mock` atau `fake` apa pun di sumber produksi
- Komponen yang mengimpor dari layanan
- Simpan irisan yang melewati layanan normalisasi
- URL API hardcode atau kebocoran env-variable di komponen
- Komponen React apa pun lebih dari 300 baris tanpa komentar justifikasi

---

## 11. Penegakan

File yang melanggar aturan ini diblokir dari penggabungan.

Daftar periksa untuk melihat PR:
- [ ] Tidak ada `switch(capability)` atau `switch(domain)` di diff
- [ ] Tidak ada `if (message.includes(...))` berbeda
- [ ] Tidak ada mock imports di file produksi
- [ ] Tidak ada komponen yang diimpor dari `services/`
- [ ] Tidak ada perhitungan keuangan di luar data backend
- [ ] Semua panggilan API melalui `services/`
- [ ] Semua status penyembuhan melalui aksi store eksplisit
- [ ] Semua komponen baru di bawah 300 baris
