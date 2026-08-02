# ADR-004: Arsitektur Mesin Debat


**Status:** ✅ Diterima
**Tanggal:** 2024
**Pengambilan Keputusan:** Kepala Arsitek, Tim Teknik

---

## Konteks

Platform harus memverifikasi kebenaran keluarannya, terutama untuk operasi berisiko tinggi seperti perubahan konfigurasi jaringan, pembuatan kode, dan analisis keamanan.

Penilaian keyakinan yang sederhana saja tidak cukup – sistem memerlukan mekanisme untuk menantang dan memvalidasi kesimpulannya sendiri.

---

## Keputusan

Terapkan **Mesin Debat** yang menghasilkan berbagai perspektif dan menyelesaikannya melalui debat terstruktur.

### Arsitektur

```
┌─────────────────────────────────────────────┐
│              DebateOrchestrator             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐ │
│  │Debater A │  │Debater B │  │Debater C │ │
│  │ (Pro)    │  │ (Con)    │  │ (Judge)  │ │
│  └──────────┘  └──────────┘  └──────────┘ │
│         │            │             │        │
│         └────────────┴─────────────┘        │
│                      ▼                       │
│              Resolution Synthesis            │
└─────────────────────────────────────────────┘
```

### Desain Kunci

- **Debater** mengambil posisi berlawanan (pro/con) terhadap validitas keluaran
- **Hakim** memicu argumen dan menghasilkan resolusi akhir
- Berbagai argumentasi untuk kasus-kasus kompleks
- Putusan: DITERIMA, DITOLAK, atau KEBUTUHAN_REVISI

---

## Alternatif yang Dipertimbangkan


|Alternatif|Alasan Ditolak|
|-------------|-----------------|
|Verifikasi mandiri LLM tunggal|Rentan terhadap bias konfirmasi, kasus-kasus yang meleset|
|Validasi berdasarkan aturan|Tidak dapat menangani skenario baru atau kompleks|
|Peninjauan eksternal LLM|Latensi/biaya tambahan, masih perspektif tunggal|
|Ansambel pemungutan suara|Tidak ada mekanisme penyelesaian, mayoritas sederhana tidak mencukupi|

---

## Lanjutnya

- **Positif:** Verifikasi kualitas lebih tinggi melalui proses permusuhan
- **Positif:** Verifikasi mandiri tanpa campur tangan manusia untuk kasus rutin
- **Negatif:** 2-3x panggilan LLM per verifikasi (biaya + latensi)
- **Negatif:** Kompleksitas dalam mengatur putaran perdebatan
- **Negatif:** Kualitas debat bergantung pada rekayasa cepat debat

---

## Kepatuhan

Semua verifikasi otomatis terhadap konfigurasi yang dihasilkan, patch kode, dan analisis keamanan HARUS menggunakan Mesin Debat. Penilaian keyakinan yang sederhana tidak cukup untuk menghasilkan keluaran produksi.
