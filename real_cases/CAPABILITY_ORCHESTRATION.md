<!-- BILINGUAL_DOCS_START -->
## Bahasa Indonesia / English

### Ringkasan / Summary
Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.
> Terjemahan Indonesia: Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.

- Bahasa Indonesia: konten utama tetap dipertahankan dalam dokumen asli, dan bagian ini memberi konteks ringkas dalam bahasa Indonesia.
- English: the main content remains in the original document, and this section provides a concise bilingual context for international readers.

### Informasi Dokumen / Document Info
- File: `real_cases/CAPABILITY_ORCHESTRATION.md`
- Judul: Capability Orchestration
- Status: bilingual header added

<!-- BILINGUAL_DOCS_END -->

# CAPABILITY ORCHESTRATION

<!-- DOCUMENT_METADATA_START -->
**Owner:** Documentation Team
**Canonical Owner:** Documentation Governance Lead
**Last Verified:** 2026-08-02
**Version:** 1.0.0
**Status:** Active
**SSOT:** Real case study documentation
<!-- DOCUMENT_METADATA_END -->

## Lifecycle

Each capability follows:
> Terjemahan Indonesia: Each kapabilitas follows:
1. **Init** - App instantiated via `get_app()`
2. **Register** - Available in registry
3. **Execute** - Called via worker or direct invocation
4. **Monitor** - Telemetry records events
5. **Complete** - Results returned

---

## Execution Flow

```
User Request
    â†“
Adaptive Runtime (perception/memory/reasoning/decision/action)
    â†“
Capability App (NetworkEngineerApp)
    â†“
Worker (NetworkWorker)
    â†“
Result
    â†“
Telemetry (record_analysis_event)
```

---

## Registry

Registered in `apps.society.agent.Agent` base class:
> Terjemahan Indonesia: Registered dalam apps.society.agen.agen base class:
- `agent_registry` maintains agent records
- Each agent has `agent_id`, `name`, `role`, `department`, `skills`

---

## Telemetry Integration

Every capability execution triggers:
> Terjemahan Indonesia: Every kapabilitas execution triggers:
- `record_analysis_event()` for attachment analysis
- `record_execution_event()` for execution sessions
- `record_chat_event()` for chat interactions

---

## Error Handling

Standard contract:
> Terjemahan Indonesia: Kontrak standar:
```python
{
    "status": "success" | "failed",
    "result": {...} | None,
    "error": str | None
}
```

All workers return this format consistently.
> Terjemahan Indonesia: All workers return ini format consistently.
