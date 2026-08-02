# Pengetahuan K2 — Pengambilan Hibrid & Pembuat Konteks

<!-- DOCUMENT_METADATA_START -->
**Pemilik:** Tim Dokumentasi
**Pemilik Canonical:** Pimpinan Tata Kelola Dokumentasi
**Diverifikasi Terakhir:** 08-02-2026
**Versi:** 1.0.0
**Status:** Aktif
**SSOT:** Dokumentasi untuk KNOWLEDGE_RETRIEVAL
<!-- DOCUMENT_METADATA_END -->

## Status: Diimplementasikan

## Ikhtisar

K2 dibangun di atas K1 (Knowledge Graph + Registry + Evidence) untuk menyediakan hybrid retrieval yang menggabungkan kesamaan grafik, registri pencarian, dan pencarian bukti ke dalam satu konteks terintegrasi untuk AI.

## Komponen

### Pengambilan Hibrid

Menggabungkan tiga strategi pengambilan:
- **Kesamaan grafik** melalui `KnowledgeGraph.similarity()`
- **Pencarian registrasi** melalui `KnowledgeRegistry.find_by_name()` dan `find_by_domain()`
- **Pencarian bukti** melalui `EvidenceStore.get()`

### Pembuat Konteks

Menyusun `KnowledgeContext` terstruktur dari hasil pengambilan:
- Konsep primer
- Konsep terkait (melalui traversal grafik)
- Bukti pendukung
- Bukti yang berbeda
- Agregat kepercayaan diri
- Pelacakan sumber

### Konteks Pengetahuan

Kontrak keluaran standar:
```json
{
  "query": "string",
  "primary_concepts": [],
  "related_concepts": [],
  "supporting_evidence": [],
  "contradicting_evidence": [],
  "confidence": 0.0,
  "sources": [],
  "metadata": {}
}
```

## Penggunaan

```python
from apps.organization.knowledge_retrieval import create_context_builder

builder = create_context_builder()
context = builder.build("Clean Architecture", domain="code")
print(context.to_dict())
```

## Integrasi

- Digunakan oleh mesin penalaran untuk memperkaya prompt dengan pengetahuan yang relevan
- Digunakan oleh kemampuan pekerja untuk menambah konteks eksekusi
- Memberikan masukan ke K3 Evidence Intelligence untuk mendeteksi konflik
- Memberikan masukan ke K4 Experience Memory untuk ekstraksi pelajaran
