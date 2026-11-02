# Reverse Engineer Capability Pack

## Ringkasan

Pack ini mengintegrasikan REA untuk inspeksi berbasis evidence pada binary
native, aplikasi Electron/JavaScript, assembly .NET, dan aplikasi web. Hasil
memisahkan observasi langsung, inferensi, hal yang belum diketahui, dan
referensi evidence.

## Penggunaan

`ReverseEngineerCapabilityPack.run` menerima permintaan serta konteks opsional
berisi `target_path` dan `deep_analysis`. Tanpa target, pack mengembalikan
respons informasi. Untuk target yang tersedia, REAService memilih alur
inspeksi berdasarkan jenis artefak dan memetakan keluaran ke
`REAAnalysisResult`.

## Ketersediaan dan keselamatan

REA CLI dan toolchain eksternal tidak selalu tersedia. Jika REA tidak
terpasang, service menghasilkan status keterbatasan yang eksplisit; hasil
tersebut tidak boleh diperlakukan sebagai analisis sukses. Jalankan inspeksi
hanya pada artefak yang pengguna berwenang untuk menganalisis.

Kontrak dan service berada di `apps/reverse_engineer/models.py` dan
`apps/reverse_engineer/rea_service.py`.
