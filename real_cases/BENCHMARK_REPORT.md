# BENCHMARK REPORT
# Network Engineer Benchmark Stabilization

## 1. Jumlah Benchmark yang Dijalankan: 30

## 2. Jumlah Benchmark yang Lulus: 0
Note: Benchmark tidak menggunakan expected_findings untuk passing (semua kosong), scoring tidak dapat dihitung

## 3. Jumlah Benchmark yang Gagal: 0
Note: Tidak ada crash atau exception

## 4. Quality Metrics

### Findings Distribution
| Severity | Count | % |
|----------|-------|-----|
| CRITICAL | 65 | 23.3% |
| WARNING | 70 | 25.1% |
| INFO | 100 | 35.8% |
| SUGGESTION | 44 | 15.8% |

### Vendor Findings
| Vendor | Total Findings | Critical |
|--------|---------------|---------|
| mikrotik | 88 | 15 |
| cisco | 89 | 20 |
| fortinet | 102 | 30 |

## 5. Precision, Recall, Accuracy
Note: Tidak dapat dihitung karena expected_findings tidak diisi di schema

## 6. False Positive/Negative
- False Positive Rate: Tinggi (rules mendeteksi pola di semua vendor)
- False Negative Rate: Rendah (semua case menghasilkan findings)

## 7. Exact Match Rate
- N/A (expected_findings tidak diisi)

## Known Limitations
1. Schema tidak memuat expected_findings dari expected.json
2. Scoring berdasarkan findings match tidak berfungsi
3. Severity threshold di expected.json tidak dipakai

## Rekomendasi Sprint 5A.4
1. Isi expected_findings di expected.json
2. Perbaiki benchmark untuk membaca expected_findings
3. Tambah expected_severity per finding
4. Buat validator untuk menjamin expected.json konsisten