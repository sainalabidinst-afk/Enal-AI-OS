# Panduan Dogfooding — Insinyur Jaringan

<!-- DOCUMENT_METADATA_START -->
**Pemilik:** Tim Dokumentasi
**Pemilik Canonical:** Pimpinan Tata Kelola Dokumentasi
**Diverifikasi Terakhir:** 08-02-2026
**Versi:** 1.0.0
**Status:** Aktif
**SSOT:** Dokumentasi untuk dogfooding_guide
<!-- DOCUMENT_METADATA_END -->

**Durasi:** 1–2 minggu
**Tujuan:** Menggunakan Network Engineer pada konfigurasi dunia nyata untuk mengumpulkan umpan balik sebelum membangun fitur baru.

## Apa itu Dogfood?

Dogfooding = menggunakan produk Anda sendiri pada pekerjaan nyata, bukan hanya uji sintetis.

Untuk ECP, ini berarti:
1. Ambil konfigurasi MikroTik nyata dari produksi atau lab
2. Jalankan melalui Network Engineer
3. Bandingkan keluaran ECP dengan penilaian ahli Anda
4. Catat setiap ketidakcocokan, kesalahan, atau temuan yang hilang

## Apa yang Harus Dicatat

### A. Positif Palsu
ECP menandai sesuatu yang sebenarnya benar atau dapat diterima.

**Templat:**
```
Scenario: [deskripsi singkat]
Config: [nama file/skenario]
Finding: [apa yang dilaporkan ECP]
Why it's wrong: [kenapa ini sebenarnya OK]
Rule: [rule mana yang memicunya]
Suggested fix: [sesuaikan ambang rule, tambahkan exception, atau abaikan konteks]
```

### B. Negatif Palsu
Kekurangan ECP adalah sesuatu yang sebenarnya merupakan masalah.

**Templat:**
```
Scenario: [deskripsi singkat]
Config: [nama file/skenario]
Issue: [apa yang seharusnya ditandai]
Why it matters: [dampak keamanan/performa/operasional]
Suggested rule: [rule baru atau peningkatan]
```

### C.Rekomendasi Buruk
ECP menandai sesuatu dengan benar, tetapi perbaikannya salah atau tidak praktis.

**Templat:**
```
Scenario: [deskripsi singkat]
Config: [nama file/skenario]
Problem: [diidentifikasi dengan benar]
Current recommendation: [apa yang disarankan ECP]
Why it's wrong: [kenapa perbaikan ini buruk]
Better recommendation: [apa yang seharusnya disarankan]
```

### D.Kegagalan Parser
Konfigurasi tidak dijelaskan dengan benar.

**Templat:**
```
Config: [nama file/skenario]
Error: [apa yang salah]
Snippet: [baris RouterOS yang gagal]
Expected: [apa yang seharusnya diuraikan]
```

### E.Kebingungan UX
Sesuatu yang membingungkan, menakutkan, atau sulit dipahami.

**Templat:**
```
Feature: [bagian ECP mana]
Problem: [apa yang membingungkan]
Suggestion: [cara memperbaikinya]
```

## Cara Garis Dogfood

### Langkah 1: Kumpulkan Config
Gunakan config MikroTik nyata dari:
- Router produksi (disanitasi)
- Router laboratorium/lapangan
- Ekspor cadangan dari klien
- Konfigurasi proyek Sun Clint

**Minimum:** 10 konfigurasi berbeda
**Target:** 20–30 konfigurasi

### Langkah 2: Jalankan Analisis
```python
from apps.network_engineer import get_app

app = get_app()
with open("config.rsc") as f:
    config = f.read()

result = await app.analyze_config(config)
print(f"Findings: {len(result['issues'])}")
for issue in result["issues"]:
    print(f"[{issue['severity']}] {issue['category']}: {issue['description']}")
```

### Langkah 3: Tinjau Temuan
Untuk setiap temuan, tanyakan:
1. Apakah ini nyata? (Positif Benar / Positif Palsu)
2. Apakah tingkat keparahannya benar? (terlalu tinggi / terlalu rendah / benar)
3. Apakah rekomendasinya dapat dilanjutkan? (ya / tidak / perlu perbaikan)

### Langkah 4: Bandingkan dengan Penilaian Ahli
Tuliskan apa yang akan ANDA tandai vs apa yang ditandai ECP.

| # |Temuan ECP|Penilaian Anda|Cocok?|Catatan|
|---|-------------|---------------|--------|-------|
|1|[Temuan ECP]|[temuan Anda]|Ya/Tidak|[katatan]|
|2| ... | ... | ... | ... |

### Langkah 5: Uji Penerapan Terkontrol
Jika Anda memiliki lab MikroTik:
1. Jalankan penerapan pipa terkendali penuh
2. Coba disetujui = Benar
3. Coba disetujui = Salah
4. Periksa kembalikan
5. Tinjau jejak audit

Jika tidak ada perangkat lab, simulasikan dengan Golden Test config.

## Format Log Umpan Balik

Buat file: `dogfooding/feedback_YYYY-MM-DD.md`

```markdown
# Dogfooding Session — 2026-07-09

## Configs Reviewed
- `golden/mikrotik/home/config.rsc` — 11 findings
- `golden/mikrotik/office/config.rsc` — 13 findings
- [config nyata dari Sun Clint] — X findings

## False Positives
### FP-001: [judul]
- Config: [config mana]
- Rule: [rule mana]
- Why wrong: [penjelasan]
- Fix: [apa yang diubah]

## False Negatives
### FN-001: [judul]
- Config: [config mana]
- Missing: [apa yang seharusnya ditandai]
- Impact: [kenapa penting]
- Suggested rule: [deskripsi]

## Bad Recommendations
### BR-001: [judul]
...

## Parser Failures
### PF-001: [judul]
...

## UX Confusion
### UX-001: [judul]
...

## Summary
- Total configs reviewed: X
- Total findings reviewed: X
- False positives: X
- False negatives: X
- Parser failures: X
- UX issues: X

## Top 5 Priorities untuk Milestone Berikutnya
1. [prioritas 1]
2. [prioritas 2]
3. [prioritas 3]
4. [prioritas 4]
5. [prioritas 5]
```

## Kriteria Keberhasilan

Dogfooding berhasil ketika:
1. Minimal 10 config nyata direview
2. Minimal 5 teridentifikasi positif palsu
3. Minimal 5 teridentifikasi negatif palsu
4. Minimal 3 masalah UX teridentifikasi
5. 5 prioritas teratas untuk pencapaian berikutnya jelas

## Keluaran

Setelah dogfood, Anda harus memiliki:
1. `dogfooding/feedback_YYYY-MM-DD.md` — umpan balik secara konsisten
2. Skenario Golden Test yang diperbarui berdasarkan temuan nyata
3. Prioritas yang jelas untuk Milestone 3 (Network Operations)

## Aturan Penting

1. **Jangan perbaiki masalah selama dogfooding.** Kata saja.
2. **Jangan tambahkan rule baru selama dogfooding.** Catat saja apa yang hilang.
3. **Jangan ubah parser selama dogfooding.** Catat saja kegagalannya.
4. **Fokus pada kualitas, bukan kuantitas.** 10 config direview mendalam > 100 config di-skim.

Dogfooding adalah tentang belajar, bukan membangun.
