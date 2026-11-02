# Adversarial Testing Capability Pack

## Ringkasan

Pack ini menguji rencana, rekomendasi, arsitektur, keputusan, dan patch secara
adversarial. Tujuannya adalah menemukan asumsi rapuh dan risiko sebelum hasil
digunakan; pack ini tidak menjalankan eksploit terhadap sistem target.

## Alur kerja

1. Membuat skenario serangan dari kategori yang dipilih, seperti kegagalan
   dependensi, gangguan operasional, kerusakan data, atau perubahan regulasi.
2. Mengaudit asumsi yang mendasari subjek dan skenario.
3. Menilai kemungkinan dampak dan kerentanan yang teridentifikasi.
4. Menyusun tindakan hardening dan menjelaskan dasar penilaiannya.
5. Menghasilkan gate `pass`, `fail`, atau `review_required`.

## Kontrak

Input utama adalah `subject` dan `subject_type`. Konteks, evidence, batasan,
kategori serangan, mitigasi yang sudah ada, serta `attack_budget` (1–50)
bersifat opsional. Hasil memuat attack vectors, vulnerabilities, rekomendasi
hardening, skor, dan hasil gate.

Entry point pack adalah `AdversarialTestingApp.run`; engine dan kontraknya
berada di `apps/adversarial_testing/`.

## Batasan

Hasil adalah analisis skenario, bukan bukti bahwa serangan berhasil atau
kerentanan dapat dieksploitasi. Validasi manusia dan pemeriksaan terhadap
evidence tetap diperlukan sebelum mengambil tindakan.
