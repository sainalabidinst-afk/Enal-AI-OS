# Rangkaian Benchmark ECP

Direktori ini berisi tolok ukur untuk mengukur kinerja dan kualitas ECP.

## Tolok Ukur yang Berjalan

```bash
# Run all benchmarks
python -m benchmarks.performance_benchmark

# Run specific benchmark
python -m benchmarks.agent_quality
```

## Benchmark Kategori

### Tolok Ukur Kinerja

- `performance_benchmark.py` — Latensi, efisiensi token, determinisme, tingkat keberhasilan
- `package_boundaries.py` — Penegakan paket ketergantungan

### Tolok Ukur Kualitas

- `agent_quality.py` — Kualitas respons agen
- `capability_benchmark.py` — Capability Pack kualitas dalam 6 dimensi: Akurasi, Kelengkapan, Penjelasan, Keamanan, Efisiensi, Konsistensi
- Kasus dunia nyata dari `real_cases/<capability_id>/` dimasukkan ke dalam tolok ukur kemampuan

## Benchmark Jenis

### Sintetis Benchmark

Skenario disusun dengan keluaran yang diharapkan diketahui, ditentukan dalam `benchmarks/`.

### Benchmark di dunia nyata

Kasus dari penggunaan sebenarnya disimpan di `real_cases/<capability_id>/`.
Setiap kasus berisi masukan, keluaran, dan evaluasi.
Kasus-kasus di dunia nyata adalah sumber utama perbaikan Capability Pack.
Tolok ukur sintetis memvalidasi peningkatan; kasus-kasus dunia nyata mendorong mereka.

## Menambahkan Tolok Ukur Baru

1. Buat file Python baru di direktori ini
2. Gunakan kelas `Benchmark` dari `backend.app.core.evaluation`
3. Jalankan dengan `python -m benchmarks.your_benchmark`

## Integrasi CI

Tolok ukur dijalankan secara otomatis di setiap PR:
- Kinerja tolok ukur tidak boleh menurun > 10%
- Tolok ukur kualitas harus mempertahankan tingkat kelulusan > 80%.
- Batasan paket tidak boleh ada pelanggaran

