<!-- BILINGUAL_DOCS_START -->
## Bahasa Indonesia / English

### Ringkasan / Summary
Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.
> Terjemahan Indonesia: Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.

- Bahasa Indonesia: konten utama tetap dipertahankan dalam dokumen asli, dan bagian ini memberi konteks ringkas dalam bahasa Indonesia.
- English: the main content remains in the original document, and this section provides a concise bilingual context for international readers.

### Informasi Dokumen / Document Info
- File: `real_cases/MULTI_CAPABILITY_COORDINATION.md`
- Judul: Multi Capability Coordination
- Status: bilingual header added

<!-- BILINGUAL_DOCS_END -->

# MULTI_CAPABILITY_COORDINATION

<!-- DOCUMENT_METADATA_START -->
**Owner:** Documentation Team
**Canonical Owner:** Documentation Governance Lead
**Last Verified:** 2026-08-02
**Version:** 1.0.0
**Status:** Active
**SSOT:** Real case study documentation
<!-- DOCUMENT_METADATA_END -->

## Handoff Contract

Standard format between capabilities:
> Terjemahan Indonesia: Standard format between kapabilitas:
```json
{
    "input": {...},
    "output": {...},
    "metadata": {
        "source_capability": "string",
        "target_capability": "string",
        "timestamp": "ISO"
    },
    "status": "success|failed|pending",
    "error": null | "message"
}
```

---

## Execution Sequencing

Rules:
> Terjemahan Indonesia: Aturan:
1. Tasks defined in `ExecutionGraph`
2. Dependencies declared in `dependencies` array
3. Run sequentially in topological order
4. Failure stops downstream tasks
5. Completion requires all tasks to succeed

---

## Failure Propagation

If any task fails:
> Terjemahan Indonesia: Jika ada tugas yang gagal:
- Session status â†’ `failed`
- Downstream tasks not executed
- Error logged to telemetry
- Artifact created with error details

---

## Stop Conditions

- All tasks completed
- Any task failed
- Explicit cancellation called
- Timeout exceeded (future)
