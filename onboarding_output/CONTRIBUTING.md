## Bahasa Indonesia/Bahasa Inggris


### Ringkas / Ringkas
Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.


### Informasi Dokumen / Info Dokumen
- Berkas: `CONTRIBUTING.md`
- Judul: Berkontribusi
- Status: editor bilingual ditambahkan


# Berkontribusi pada Platform Kognitif Enal


Terima kasih atas minat Anda untuk berkontribusi pada ECP!

## Kode Etik

Proyek ini mematuhi Kode Etik. Dengan berpartisipasi, Anda diharapkan menjunjung tinggi kode ini.

## Bagaimana Berkontribusi

### Melaporkan Bug

Sebelum membuat laporan bug, harap periksa masalah yang ada. Saat membuat laporan bug, sertakan:
- Langkah-langkah untuk mereproduksi
- Perilaku yang diharapkan
- Perilaku sebenarnya
- Lingkungan (OS, versi Python, dll.)

### Fitur yang Disarankan

Permintaan fitur dipersilakan! Silakan:
- Periksa apakah fitur tersebut sudah diminta
- Uraikan masalah dan solusinya dengan jelas
- Menjelaskan mengapa fitur ini berguna

### Tarik Permintaan

1. Cabangkan repositori
2. Buat fitur cabang (`git checkout -b feature/amazing-feature`)
3. Buat perubahan pada Anda
4. Jalankan pengujian (`pytest`)
5. Jalankan tolok ukur (`python -m benchmarks`)
6. Komit perubahan Anda (`git commit -m 'Add amazing feature'`)
7. Dorong ke cabang (`git push origin feature/amazing-feature`)
8. Buka Permintaan Tarik

## Pengaturan Pengembangan

```bash
# Clone repository
git clone https://github.com/enal-ai-org/ecp.git
cd ecp

# Setup environment
cp .env.example .env
docker-compose up -d

# Install backend
cd backend
poetry install

# Install SDK
cd ../sdk
pip install -e .

# Run tests
cd backend
pytest
```

## Standar Pengkodean

- Python: Ikuti PEP 8, gunakan `black` untuk memformat, `ruff` untuk linting
- Ketik petunjuk yang diperlukan untuk semua API publik
- Dokumen diperlukan untuk semua kelas dan metode publik
- Pengujian diperlukan untuk semua fitur baru

## Proses RFC

Untuk perubahan signifikan, harap kirimkan RFC:
1. Buat file baru di `docs/rfcs/RFC-XXXX-title.md`
2. Ikuti templat RFC di `docs/rfcs/README.md`
3. Kirim PR untuk ditinjau

## Batasan Paket

Batasan hormati paket yang ditentukan di `benchmarks/package_boundaries.py`:
- `kernel` tidak boleh bergantung pada `runtime`, `sdk`, atau `apps`
- `runtime` tidak boleh bergantung pada `apps` atau `sdk`
- `sdk` tidak boleh bergantung pada `runtime`

## Lisensi

Dengan berkontribusi, Anda setuju bahwa kontribusi Anda akan dilisensikan berdasarkan Lisensi MIT.
