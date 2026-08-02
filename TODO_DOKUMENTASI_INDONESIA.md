# TODO: Konversi Dokumentasi ke Bahasa Indonesia

**Tujuan:** Seluruh dokumentasi Markdown (*.md) menggunakan Bahasa Indonesia sebagai bahasa utama, tanpa format bilingual.

**Aturan:**
1. Terjemahkan heading, paragraf, tabel, daftar ke Bahasa Indonesia formal dan konsisten.
2. Hapus blok `BILINGUAL_DOCS`, baris `Terjemahan Indonesia:`, `Bahasa Indonesia:`, dan duplikasi bahasa.
3. Pertahankan istilah teknis dalam Bahasa Inggris (Capability Pack, Golden Test, Benchmark, API, SDK, Docker, FastAPI, Runtime, Plugin, Knowledge Graph, Execution Runtime, nama pack, class, function, file, folder, endpoint, blok kode, command terminal).
4. JANGAN terjemahkan: source code, prompt runtime (`backend/app/core/prompts/*.md`), sample output (`real_cases/**/output/*.md`), dataset benchmark (`real_cases/**/input/*.md` yang dipakai benchmark).
5. Jangan mengubah arsitektur, RFC/ADR content, jumlah pack, versi, roadmap, referensi silang.

---

## Fase 1 — Dokumentasi Strategis (Prioritas Tertinggi)

- [x] README.md
- [x] docs/GOVERNANCE_CHARTER.md
- [x] docs/GOVERNANCE.md
- [x] docs/CAPABILITY_STRATEGY.md
- [x] docs/RELEASE_CRITERIA.md
- [x] docs/ROADMAP.md
- [x] docs/DOCUMENT_STRUCTURE.md
- [x] docs/architecture.md
- [x] docs/ENGINEERING_BASELINE.md
- [x] docs/CAPABILITY_GUIDE.md

**Fase 1 SELESAI (10/10).**

## Fase 2 — RFC & ADR

- [x] docs/rfcs/README.md
- [x] docs/rfcs/RFC-0004-network-knowledge.md
- [x] docs/rfcs/RFC-0005-trading-knowledge.md
- [x] docs/rfcs/RFC-0006-code-knowledge.md
- [x] docs/rfcs/RFC-0007-decision-intelligence.md
- [x] docs/rfcs/RFC-0008-security-engineer.md
- [x] docs/rfcs/RFC-0009-data-engineer.md
- [x] docs/rfcs/RFC-0010-database-engineer.md
- [x] docs/rfcs/RFC-0011-system-architect.md
- [x] docs/rfcs/RFC-0012-qa-engineer.md
- [x] docs/rfcs/RFC-0013-business-analyst.md
- [x] docs/adr/ADR-001-event-bus-architecture.md
- [x] docs/adr/ADR-002-capability-pack-architecture.md
- [x] docs/adr/ADR-003-universal-ast-design.md
- [x] docs/adr/ADR-004-debate-engine-architecture.md

**Fase 2 SELESAI (15/15).**

## Fase 3 — Dokumentasi Teknis

- [x] docs/api_reference.md (bersih — tanpa marker)
- [x] docs/APP_DEV_GUIDE.md (bersih — tanpa marker)
- [x] docs/AES_ARCHITECTURE.md (bersih — tanpa marker)
- [x] docs/REFERENCE_ARCHITECTURE.md
- [x] docs/tool_guide.md
- [x] docs/testing_strategy.md
- [x] docs/agent_guide.md (bersih — tanpa marker)
- [x] docs/dogfooding_guide.md
- [x] docs/REASONING_ENGINE.md
- [x] docs/KNOWLEDGE_RETRIEVAL.md
- [x] docs/operational_metrics.md
- [x] docs/QUALITY_GATE.md
- [x] docs/quality/QUALITY_GATES.md
- [x] docs/ENGINEERING_BASELINE.md (bersih — tanpa marker)
- [x] docs/frontend/* (11 file) — API_MAPPING, COMPONENT_LIBRARY, DESIGN_TOKENS, ERROR_STATES, FRONTEND_DEFINITION_OF_DONE, MOBILE_LAYOUT, PRODUCT_UI_SPEC, SCREEN_FLOW, STATE_MANAGEMENT, UI_ARCHITECTURE
- [x] docs/FRONTEND_GAP_ANALYSIS.md
- [x] sdk/README.md
- [x] benchmarks/README.md

**Fase 3 SELESAI (18/18).**

## Fase 4 — Dokumentasi Pendukung

- [ ] docs/capabilities/* (9 file)
- [ ] docs/releases/2026-07-14-product-intelligence.md
- [ ] docs/baseline_freeze.md
- [ ] docs/PHASE_SUMMARY.md
- [ ] docs/PRODUCT_CONTRACT.md
- [ ] docs/USER_JOURNEYS.md
- [ ] docs/UX_DESIGN.md
- [ ] docs/WORKFLOW_CATALOG.md
- [ ] docs/workforce_constitution.md
- [ ] docs/SPRINT_5A_PLAN.md
- [ ] docs/SPRINT_T1_PLAN.md
- [ ] docs/sprint3_network_operations.md
- [ ] docs/v1_roadmap.md
- [ ] docs/v1_sprint_plan.md
- [ ] docs/CANONICAL_CONSOLIDATION.md
- [ ] docs/DEPENDENCY_AUDIT.md
- [ ] docs/getting_started.md
- [ ] docs/GOVERNANCE.md (pendukung)
- [ ] docs/AI_PLANNER.md
- [ ] Root-level: ARCHITECTURE_*, RELEASE_*, dll.
- [ ] real_cases/* (kecuali output benchmark)
- [ ] RELEASE/* (kecuali SBOM teknis)
- [ ] CONVERT: docs/BILINGUAL_DOCUMENTATION.md → panduan Bahasa Indonesia
- [ ] CONVERT: docs/BILINGUAL_STYLE_GUIDE.md → panduan gaya Bahasa Indonesia

## Audit Akhir

- [ ] Tidak ada format bilingual tersisa (findstr BILINGUAL_DOCS / Terjemahan Indonesia)
- [ ] Tidak ada tautan internal rusak
- [ ] Tidak ada inkonsistensi istilah
- [ ] Tidak ada perubahan contoh kode/kontrak API
- [ ] Jumlah Capability Pack = 13, versi & roadmap konsisten

