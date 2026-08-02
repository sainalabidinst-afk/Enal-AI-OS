# Panduan Pengembangan Tool

<!-- DOCUMENT_METADATA_START -->
**Pemilik:** Tim Dokumentasi
**Pemilik Canonical:** Pimpinan Tata Kelola Dokumentasi
**Terakhir Diverifikasi:** 2026-08-02
**Versi:** 1.0.0
**Status:** Aktif
**SSOT:** Dokumentasi untuk tool_guide
<!-- DOCUMENT_METADATA_END -->

## Membuat Tool

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

## Kontrak Tool

Semua tool harus mengimplementasikan:
- `invoke(parameters)` — Mengeksekusi tool dengan parameter
- `get_schema()` — Mengembalikan skema yang kompatibel dengan OpenAI

## Sandboxing

Tool yang ditandai dengan `sandbox=True` berjalan di lingkungan terisolasi:
- Tidak ada akses filesystem langsung
- Tidak ada akses jaringan (kecuali diizinkan secara eksplisit)
- Batasan resource ditegakkan

## Permissions

Tool memerlukan permission eksplisit:
- `read` — Membaca data
- `write` — Menulis data
- `execute` — Mengeksekusi kode/command
- `deploy` — Melakukan deployment ke produksi
- `admin` — Operasi administratif

## Best Practices

- Jaga tool agar bersifat single-purpose
- Validasi semua input
- Kembalikan output terstruktur
- Dokumentasikan parameter secara menyeluruh
- Gunakan permission yang sesuai

