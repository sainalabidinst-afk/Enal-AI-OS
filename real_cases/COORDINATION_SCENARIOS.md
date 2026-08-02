<!-- BILINGUAL_DOCS_START -->
## Bahasa Indonesia / English

### Ringkasan / Summary
Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.
> Terjemahan Indonesia: Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.

- Bahasa Indonesia: konten utama tetap dipertahankan dalam dokumen asli, dan bagian ini memberi konteks ringkas dalam bahasa Indonesia.
- English: the main content remains in the original document, and this section provides a concise bilingual context for international readers.

### Informasi Dokumen / Document Info
- File: `real_cases/COORDINATION_SCENARIOS.md`
- Judul: Coordination Scenarios
- Status: bilingual header added

<!-- BILINGUAL_DOCS_END -->

# COORDINATION SCENARIOS

<!-- DOCUMENT_METADATA_START -->
**Owner:** Documentation Team
**Canonical Owner:** Documentation Governance Lead
**Last Verified:** 2026-08-02
**Version:** 1.0.0
**Status:** Active
**SSOT:** Real case study documentation
<!-- DOCUMENT_METADATA_END -->

## Multi-Capability Workflows

### Scenario 1: Network Configuration Audit
```
NetworkEngineerApp (parse)
    â†“
NetworkEngineerApp (analyze)
    â†“
NetworkEngineerApp (compliance check)
    â†“
NetworkEngineerApp (generate documentation)
```

### Scenario 2: Code Development Workflow
```
CodeEngineerApp (generate)
    â†“
CodeEngineerApp (validate)
    â†“
DevOpsApp (deploy)
    â†“
NetworkEngineerApp (verify access)
```

### Scenario 3: Trading Risk Assessment
```
TradingAnalystApp (analyze market)
    â†“
ResearchAssistantApp (verify news)
    â†“
TradingAnalystApp (execute trade)
```

---

## Dependency Structure

Each capability can operate standalone. Coordination happens via:
> Terjemahan Indonesia: Each kapabilitas dapat operate standalone. Coordination happens via:
- Execution graph in `ExecutionIntegration`
- Phases in `ExecutionSession`
- Artifacts shared between capabilities

---

## Current Implementation

The `ExecutionIntegration` already supports:
> Terjemahan Indonesia: ExecutionIntegration already mendukung:
- Sequential task execution via graph
- Dependency tracking
- Progress updates
- Artifact creation
