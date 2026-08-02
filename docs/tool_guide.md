# Panduan Pengembangan Alat

<!-- DOCUMENT_METADATA_START -->
**Pemilik:** Tim Dokumentasi
**Pemilik Canonical:** Pimpinan Tata Kelola Dokumentasi
**Diverifikasi Terakhir:** 02-08-2026
**Versi:** 1.0.0
**Status:** Aktif
**SSOT:** Dokumentasi untuk tool_guide
<!-- DOCUMENT_METADATA_END -->

## Alat Pembuatan

```python
from enal_ai import Tool, EnalAI

enal = EnalAI()

@enal.tool(
    name="my_tool",
    description="Description of what this tool does",
    parameters={
        "type": "object",
        "properties": {
            "param1": {"type": "string", "description": "Parameter description"},
            "param2": {"type": "integer", "description": "Another parameter"},
        },
        "required": ["param1"],
    },
    sandbox=True,
    permissions=["read", "write"],
)
async def my_tool(param1: str, param2: int = 0):
    # Your tool logic here
    return {"result": f"Processed {param1}"}
```

## Alat Kontrak

Semua alat harus mengimplementasikan:
- `invoke(parameters)` — Mengeksekusi alat dengan parameter
- `get_schema()` — Mengembalikan skema yang kompatibel dengan OpenAI

## Kotak pasir

Alat yang ditandai dengan `sandbox=True` berjalan di lingkungan terlindungi:
- Tidak ada akses filesystem secara langsung
- Tidak ada akses jaringan (kecuali secara eksplisit)
- Batasan sumber daya yang ditegakkan

## Izin

Alat memerlukan izin eksplisit:
- `read` — Membaca data
- `write` — Menulis data
- `execute` — Mengeksekusi kode/perintah
- `deploy` — Melakukan penerapan ke produksi
- `admin` — Operasi administratif

## Praktik Terbaik

- Jaga tool agar bersifat tujuan tunggal
- Validasi semua masukan
- Kembalikan keluaran yang terstruktur
- Dokumentasikan parameter secara menyeluruh
- Gunakan izin yang sesuai
