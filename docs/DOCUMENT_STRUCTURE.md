# Struktur Dokumen — Dokumentasi Strategis ECP

<!-- DOCUMENT_METADATA_START -->
**Pemilik:** Tim Dokumentasi
**Pemilik Canonical:** Pimpinan Tata Kelola Dokumentasi
**Diverifikasi Terakhir:** 08-02-2026
**Versi:** 1.0.0
**Status:** Aktif
**SSOT:** Dokumentasi untuk DOCUMENT_STRUCTURE
<!-- DOCUMENT_METADATA_END -->

**Tujuan:** Memetakan fungsi, kepemilikan, dan tingkat stabilitas setiap dokumen strategis. Membantu kontributor mengetahui di mana menemukan informasi dan di mana harus melakukan pembaruan.

---

## Prinsip

1. **Single Source of Truth (SSOT)** — Setiap informasi berada di tepat satu dokumen. Dokumen lain boleh merujuknya tetapi tidak boleh menduplikasinya.
2. **Tingkat Stabilitas** — Dokumen diklasifikasikan sebagai `Frozen`, `Stable`, `Active`, atau `Ephemeral` untuk menunjukkan seberapa sering dokumen berubah.
3. **Kepemilikan yang Jelas** — Setiap dokumen memiliki pemilik yang bertanggung jawab menjaga keakuratannya.

---

## Inventarisasi Dokumen

|Dokumen|SSOT Untuk|Stabilitas|Pemilik|Frekuensi Pembaruan|
|----------|----------|-----------|-------|------------------|
|`GOVERNANCE_CHARTER.md`|Visi, filosofi, aturan konstitusional|**Beku**|Kepala Arsitek|Hanya amandemen tingkat konstitusi|
|`GOVERNANCE.md`|Aturan operasional (ADR, Capability First, Architecture Freeze)|**Stabil**|Kepala Arsitek|Ketika aturan berubah (melalui ADR)|
|`RELEASE_CRITERIA.md`|Kondisi rilis, Definisi Selesai, gerbang kualitas|**Stabil**|Manajer Rilis|Per siklus rilis|
|`CAPABILITY_STRATEGY.md`|Profil Capability Pack, model kedewasaan, siklus hidup, perluasan pengetahuan|**Aktif**|Kemampuan pemimpin|Per siklus peningkatan kemampuan|
|`ROADMAP.md`|Linimasa, target rilis, visi jangka panjang|**Aktif**|Kepala Bagian Produk|Per kuartal atau ketika roadmap berubah|
|`DOCUMENT_STRUCTURE.md`|Tabel ini — pemetaan dokumen|**Stabil**|Kepala Arsitek|Ketika dokumen strategi baru ditambahkan|
|`v1_roadmap.md`|(Halaman Arahan warisan)|**Beku**| — |Tidak diperbarui lagi; mengarahkan ke dokumen baru|
|`ARCHITECTURE_DECISIONS.md`|Catatan ADR|**Beku**|Kepala Arsitek|Hanya ketika ADR baru disetujui|
|`PRODUCT_CONTRACT.md`|Definisi produk, kontrak UI/API|**Beku**|Kepala Bagian Produk|Permintaan Perubahan Produk saja|
|`CAPABILITY_GUIDE.md`|Spesifikasi kemampuan terperinci (pelengkap CAPABILITY_STRATEGY)|**Aktif**|Kemampuan pemimpin|Per paket peningkatan|
|`QUALITY_GATE.md`|Status gerbang kualitas|**Tdk kekal**|Pimpinan QA|Diperbarui per build/validasi|

---

## Di Mana Menemukan Apa

|Jika Anda membutuhkan...|Buka...|
|----------------|----------|
|Visi dan filosofi proyek|`GOVERNANCE_CHARTER.md`|
|Aturan untuk melakukan perubahan (ADR, tata kelola)|`GOVERNANCE.md`|
|Arti "selesai" untuk sebuah rilis|`RELEASE_CRITERIA.md`|
|Detail Capability Pack, kedewasaan, siklus hidup|`CAPABILITY_STRATEGY.md`|
|Linimasa dan jadwal rilis|`ROADMAP.md`|
|Keputusan ADR|`ARCHITECTURE_DECISIONS.md`|
|Kontrak produk (frontend-backend)|`PRODUCT_CONTRACT.md`|
|Status gerbang kualitas|`QUALITY_GATE.md`|
|Proses RFC|`docs/rfcs/README.md`|

---

## Definisi Tingkat Stabilitas

|Tingkat|Deskripsi|Dapat Berubah...|
|-------|-------------|---------------|
|**Beku**|Tidak dapat diubah tanpa proses amandemen formal|Hanya melalui ADR atau amandemen konstitusi|
|**Stabil**|Jarang berubah; perubahan memerlukan wawasan|Melalui PR dengan pengamatan arsitektur|
|**Aktif**|Berubah secara teratur sebagai bagian dari siklus pengembangan|Melalui proses PR normal|
|**Tdk kekal**|Cuplikan dari keadaan saat ini; dapat dibuat ulang|Kapan saja, dapat ditimpa|
