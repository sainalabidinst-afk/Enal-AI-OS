<!-- BILINGUAL_DOCS_START -->
## Bahasa Indonesia / English

### Ringkasan / Summary
Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.
> Terjemahan Indonesia: Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.

- Bahasa Indonesia: konten utama tetap dipertahankan dalam dokumen asli, dan bagian ini memberi konteks ringkas dalam bahasa Indonesia.
- English: the main content remains in the original document, and this section provides a concise bilingual context for international readers.

### Informasi Dokumen / Document Info
- File: `SPRINT_HARDENING_SUMMARY.md`
- Judul: Sprint Hardening Summary
- Status: bilingual header added

<!-- BILINGUAL_DOCS_END -->

# Sprint Hardening - P0 Fix Summary

<!-- DOCUMENT_METADATA_START -->
**Owner:** Documentation Team
**Canonical Owner:** Documentation Governance Lead
**Last Verified:** 2026-08-02
**Version:** 1.0.0
**Status:** Active
**SSOT:** Documentation for SPRINT_HARDENING_SUMMARY
<!-- DOCUMENT_METADATA_END -->

## P0 Type Error Fixed
- **apps/code_engineer/__init__.py**: `ArchitectureReader` constructor accepts `str | Path`, now passes `str(path)` instead of `self._repo_path` (which is `str | None`)

## P0 Mutable Defaults - TO SCAN
Need to run: `python -m ruff check --select RUF012 --no-cache apps/ backend/`
> Terjemahan Indonesia: Need untuk run: Python -m ruff check --select RUF012 --no-cache apps/ backend/

## P0 Async Blocking I/O - TO SCAN
Need to run: `python -m flake8 --select S108 apps/ backend/` or grep for `open(` in `async def`
> Terjemahan Indonesia: Need untuk run: Python -m flake8 --select S108 apps/ backend/ or grep untuk open( dalam async def

## All Previously Fixed (27 files)
| File | Fix |
|------|-----|
| adaptive_runtime.py | Rewritten with proper types |
| reflection.py | No await on sync calls |
| cognitive_kernel.py | DecisionService returns dict |
| unified_orchestrator.py | Budget estimate is sync |
| orchestrator_v2.py | Use orchestrate_goal instead of process_request |
| code_engineer/__init__.py | ArchitectureReader str|None fix |
| conversation_manager.py | Added _persist_artifact method |
| reasoning_engine.py | No await on sync calls |
| strategic_planner.py | No await on sync calls |
| world_model.py | No await on sync calls |
| decision_engine.py | Returns dict instead of DecisionResult |
| vendor/models.py | Added NATRule.in_interface, BridgeConfig.comment |
| routeros_parser.py | Added missing dataclass fields |
| profiles.py | Fixed vendor model checks |
| enricher.py | Fixed evidence building |
| attachments/pipeline.py | Fixed InfrastructureAST fields |
| attachments/models.py | Fixed type breaks |
| execution_session.py | Fixed constructor params |
| memory_layer.py | Fixed constructor issues |
| workspace_service.py | Fixed create_workspace signature |
| artifact_service.py | Fixed create_artifact signature |
| config.py | Fixed settings types |
| event_bus.py | Fixed Redis type annotations |
| detector.py | Fixed VendorFamily|None type |
| voice_vision_agent.py | Fixed None defaults |
