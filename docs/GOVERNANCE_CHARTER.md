<!-- DOCUMENT_METADATA_START -->
**Pemilik:** Tim Dokumentasi
**Pemilik Canonical:** Pimpinan Tata Kelola Dokumentasi
**Diverifikasi Terakhir:** 08-02-2026
**Versi:** 1.0.0
**Status:** Aktif
**SSOT:** Visi proyek, prinsip, dan aturan konstitusional
<!-- DOCUMENT_METADATA_END -->

# Piagam Tata Kelola ECP

**Versi:** 1.0.0
**Status:** Diratifikasi
**Berlaku:** 08-01-2026
**Otoritas:** Kepala Arsitek + Chief Product Officer
**Jenis Dokumen:** Konstitusi / Piagam Tata Kelola

---

## Pembukaan

Piagam ini adalah dokumen tata kelola strategi dan teknis tertinggi dari Enal Cognitive Platform (ECP). Piagam ini mendefinisikan filosofi produk, prinsip fundamental, dan aturan pengambilan keputusan yang harus diikuti oleh semua RFC, ADR, Capability Pack, dan aktivitas rilis.

Dokumen, RFC, ADR, implementasi, atau rilis apa pun yang bertentangan dengan Piagam ini dianggap tidak sah hingga diubah melalui proses amendemen yang ditentukan.

---

## 1. Visi Bintang Utara

> **Platform adalah penggerak. Tujuan akhirnya adalah AI Trading yang membuat keputusan investasi cerdas secara otonom.**

ECP dibangun sebagai platform eksekusi AI yang stabil. **Trading Analyst** adalah Capability Pack utama yang menjadi tujuan akhir. Semua kemampuan lainnya — Network, Code, Research, DevOps, Self Development, Decision Intelligence, Security, Data, dan yang akan datang — adalah kekuatan yang memperkuat ekosistem menuju visi tersebut.

Prinsip ini memandu setiap keputusan strategi:
- Setiap Capability Pack baru harus dievaluasi: *"Apakah ini memperkuat Trading Analyst atau ekosistem yang mendukungnya?"*
- Kualitas Trading Analyst adalah prioritas tertinggi — paket ini harus menjadi yang paling matang, paling akurat, dan paling dapat diandalkan.
- Platform tidak akan melebar ke domain yang tidak relevan dengan visi ini.

---

## 2. Filosofi Produk

> **Core bukanlah tempat fitur bertumbuh. Core adalah platform yang stabil. Capability Pack adalah tempat terjadinya inovasi.**

Ini adalah prinsip arsitektur paling penting dari ECP.

- **Inti** berhenti, kecil, stabil, dan dapat diprediksi. Inti menyediakan kontrak, eksekusi, dan tata kelola.
- **Capability Pack** adalah kendaraan untuk semua evolusi domain, perluasan pengetahuan, dan pertumbuhan fitur.
- **Tidak ada perubahan Core** yang boleh dilakukan untuk melayani satu Capability Pack saja. Core hanya berevolusi ketika banyak pack membuktikan adanya kebutuhan bersama.

### Mengapa Ini Penting

- Menjaga arsitektur tetap stabil dan mencegah churn fondasi yang didorong oleh fitur.
- proyek marketplace pack internal, komunitas, dan pihak ketiga tanpa konflik versi.
- Film setiap Capability Pack diputar, diuji, dan dirilis secara independen.
- Menggeser fokus pengembangan dari konstruksi platform ke **Capability Excellence**.

---

## 3. Prinsip Inti

| # |Prinsip|Makna|
|---|-----------|---------|
|1|**Inti Dibekukan**|Kontrak Core, Kernel, dan Core Pipeline stabil. Perubahan memerlukan persetujuan Architecture Freeze Policy (lihat `GOVERNANCE.md`).|
|2|**Kemampuan Pertama**|Tidak ada perubahan Core yang diizinkan hanya untuk meningkatkan satu Capability Pack. Perubahan harus tetap berada di dalam paket.|
|3|**Kemampuan Bukti Lintas**|Perubahan Core memerlukan bukti dari setidaknya dua Capability Pack dan ADR yang disetujui.|
|4|**Use Case Sebelum Mesin**|Tidak ada mesin, modul, atau abstraksi baru tanpa setidaknya dua Capability Pack yang menarik, Golden Test case, dan dokumentasi arsitektur.|
|5|**Persetujuan Manusia**|Tidak ada perubahan kode, konfigurasi, atau arsitektur yang boleh diterapkan tanpa persetujuan eksplisit pengguna. (ADR-005)|
|6|**Hasil di Atas Mekanisme**|Pengguna meminta hasil, bukan mekanisme. Mesin internal tidak pernah diekspos. (ADR-009, ADR-013)|
|7|**Diukur dari Hasil**|Kemajuan diukur dari skor Benchmark, kecepatan kasus nyata, dan hasil pengguna — bukan dari jumlah artefak.|
|8|**Pembelajaran Berkelanjutan**|Kasus nyata → Review → Pembaruan → Benchmark. Peningkatan platform dari setiap eksekusi.|

---

## 4. Dokumen yang Diatur oleh Piagam Ini

|Dokumen|Tujuan|Stabilitas|
|----------|---------|-----------|
|`GOVERNANCE.md`|Aturan operasional: Capability First, No New Engine, Architecture Freeze Policy, Kernel Stability, proses ADR, penegakan CI/CD, Capability Changelog|Stabil, berubah melalui amandemen|
|`RELEASE_CRITERIA.md`|Kondisi rilis, gerbang kualitas, Definisi Selesai, sertifikasi|Berubah per rilis|
|`CAPABILITY_STRATEGY.md`|Strategi Capability Pack, model kematangan, tingkat kualitas, siklus hidup, Benchmark, perluasan pengetahuan|Berevolusi seiring pengembangan paket|
|`ROADMAP.md`|Linimasa rilis, rencana 12 bulan, roadmap bebas 5 tahun, model strategi|Berubah seiring rencana berkembang|
|`DOCUMENT_STRUCTURE.md`|Peran setiap dokumen, single source of truth (SSOT), siapa memperbarui apa|Stabil|

---

## 5. Kematangan Kemampuan & Mutu Kelas

Kematangan dan kualitas adalah **dua konsep terpisah**:

- **Capability Maturity Model** menggambarkan siklus hidup kematangan sebuah Capability Pack (Level 1–6). Lihat `CAPABILITY_STRATEGY.md`.
- **Quality Grades** (A, A-, B+, …) menggambarkan **hasil Benchmark terkini** dari sebuah paket. Grade ini adalah hasil evaluasi, bukan level kematangan.

Sebuah paket mungkin matang (Stabil/Bersertifikat) tetapi tetap berupaya meningkatkan kualitas grade-nya.

---

## 6. Kewajiban Tata Kelola

Setiap RFC, ADR, Capability Pack, dan rilis harus:

1. **Konsisten dengan Piagam ini.** Kontradiksi = persetujuan.
2. **Menghormati Core Freeze.** Perubahan Core memerlukan persetujuan Architecture Freeze Policy.
3. **Memberikan bukti lintas-capability** untuk setiap perubahan Core atau shared-layer (minimal 2 pack).
4. **Mendefinisikan Benchmark** dan direktori kasus nyata sebelum dipertimbangkan untuk rilis.
5. **Lulus semua pemeriksaan tata kelola di CI/CD.** Perubahan yang melanggar tata kelola (misalnya, perubahan Core tanpa ADR) harus gagal sebelum penggabungan.

---

## 7. Proses Amandemen

Piagam ini adalah konstitusi. Amandemen bersifat luar biasa dan memerlukan:

1. **Proposal** oleh Chief Architect atau Chief Product Officer, dengan:
   - Dasar pemikiran
   - Analisis dampak
   - Rencana migrasi (jika ada)
2. **Periode peninjauan** minimal 7 hari untuk umpan balik komunitas/tim.
3. **Ratifikasi** oleh:
   - Persetujuan Kepala Arsitek
   - Persetujuan Chief Product Officer
4. **Publikasi** — versi Piagam yang diperbarui dicatat, versi yang diganti diarsipkan.

Jika terjadi konflik dengan dokumen lain, **Piagam ini yang berlaku**.

---

## 8. Definisi Arsitektur Tata Kelola Aktif

Tata Kelola Arsitektur dianggap **aktif** ketika semua hal berikut terpenuhi:

- [ ] Inti konservasi dan dilindungi oleh Kebijakan Pembekuan Arsitektur.
- [ ] Capability First Rule ditegakkan dalam code review dan CI/CD.
- [ ] Setiap perubahan Core memiliki ADR yang disetujui dengan bukti lintas-kemampuan.
- [ ] Setiap Capability Pack memiliki Benchmark dan direktori `real_cases/`.
- [ ] RFC dan ADR mereferensikan Piagam ini.
- [ ] CI/CD memblokir pelanggaran tata kelola sebelum penggabungan.

---

## 9. Persetujuan

|Peran|Status|Tanggal|
|------|--------|------|
|Kepala Arsitek|Disetujui|01-08-2026|
|Kepala Bagian Produk|Disetujui|01-08-2026|

**Review Berikutnya:** 11-01-2026 atau saat ada perubahan.
