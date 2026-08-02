## Bahasa Indonesia/Bahasa Inggris

### Ringka / Ringka

Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.


### Informasi Dokumen / Info Dokumen
- Berkas: `agents/core/README.md`
- Judul: Readme
- Status: editor bilingual ditambahkan


# Agen Inti (Fase 1)

Berikut adalah 10 agen inti yang diterapkan pada Fase 1:

1. **Perencana** - Menganalisis permintaan dan membuat rencana terstruktur
2. **Agen Pengkodean** - Menulis dan meninjau kode dalam berbagai bahasa
3. **Agen Penelitian** - Mengumpulkan informasi dari web dan dokumen
4. **Agen Data** - mengoordinasikan database, analisis data, dan migrasi
5. **Agen UI** - Merancang dan membangun antarmuka pengguna
6. **Agen Perdagangan** - Menganalisis pasar dan mengeksekusi perdagangan
7. **Agen Jaringan** - Mengonfigurasi jaringan dan keamanan
8. **Agen Penulis** - Membuat dokumentasi dan konten
9. **Agen QA** - Menguji dan memvalidasi keluaran
10. **Agen Keamanan** - Mengaudit kode dan infrastruktur
11. **Reviewer** - Meninjau dan menggabungkan hasil

## Penggunaan

```python
from backend.app.agents.orchestrator import orchestrator

result = await orchestrator.run("Build me a full-stack todo app", "conv-123")
print(result["final_result"])
```
