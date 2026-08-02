<!-- BILINGUAL_DOCS_START -->
## Bahasa Indonesia / English

### Ringkasan / Summary
Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.
> Terjemahan Indonesia: Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.

- Bahasa Indonesia: konten utama tetap dipertahankan dalam dokumen asli, dan bagian ini memberi konteks ringkas dalam bahasa Indonesia.
- English: the main content remains in the original document, and this section provides a concise bilingual context for international readers.

### Informasi Dokumen / Document Info
- File: `docs/USER_JOURNEYS.md`
- Judul: User Journeys
- Status: bilingual header added

<!-- BILINGUAL_DOCS_END -->

# User Journeys

<!-- DOCUMENT_METADATA_START -->
**Owner:** Documentation Team
**Canonical Owner:** Documentation Governance Lead
**Last Verified:** 2026-08-02
**Version:** 1.0.0
**Status:** Active
**SSOT:** Documentation for USER_JOURNEYS
<!-- DOCUMENT_METADATA_END -->

Canonical user journeys for Enal AI OS.
All design and implementation work must preserve these journeys.
> Terjemahan Indonesia: Canonical user journeys untuk Enal AI OS. All design dan implementation work must preserve these journeys.

For full UX specifications, see `docs/UX_DESIGN.md`.
> Terjemahan Indonesia: Untuk full UX specifications, see docs/UX_DESIGN.MD.

---

## Journey 1 â€” Network Engineer

**Goal:** Audit a MikroTik configuration and get a fix proposal.

**Steps:**
1. Open Workspace
2. Upload `.rsc` file
3. AI analyzes configuration
4. AI presents findings: Critical, Warning, Suggestion
5. User approves fix proposal
6. AI generates improved configuration
7. AI runs tests
8. AI presents diff and test results
9. User approves deployment
10. AI deploys with rollback plan

**User sees:** Progress indication, structured findings, proposal, diff, test results, deployment confirmation.
**User does NOT see:** Capability Pack selection, Worker routing, Execution Runtime stages, internal task planning.

---

## Journey 2 â€” Code Engineer

**Goal:** Review a project and get a fix patch.

**Steps:**
1. Open Workspace
2. Upload project ZIP or provide repository
3. AI analyzes codebase
4. AI presents findings: Security, Architecture, Dead Code
5. User approves patch generation
6. AI generates patch
7. AI runs tests
8. AI presents patch and test results
9. User approves application
10. AI applies patch

**User sees:** Progress indication, structured findings, patch, test results, application confirmation.
**User does NOT see:** AST parsing details, static analysis engine selection, test runner configuration.

---

## Journey 3 â€” Trading Analyst

**Goal:** Analyze a market scenario and get a trading recommendation.

**Steps:**
1. Open Workspace
2. Provide market data or instrument
3. AI analyzes market structure
4. AI presents bias, support/resistance, risk
5. AI gives recommendation with reasoning
6. User can ask for alternative scenarios
7. AI explains risk and failure case

**User sees:** Market bias, key levels, risk assessment, recommendation with reasoning.
**User does NOT see:** Indicator calculations, strategy library selection, debate engine internals.

---

## Journey 4 â€” Research Assistant

**Goal:** Research a topic and get a cited summary.

**Steps:**
1. Open Workspace
2. Ask a research question
3. AI retrieves relevant sources
4. AI ranks evidence quality
5. AI detects contradictions between sources
6. AI synthesizes findings
7. AI presents summary with citations
8. User can ask for deeper analysis

**User sees:** Research summary, citations with provenance, confidence estimate, contradiction notes.
**User does NOT see:** RAG retrieval details, embedding similarity scores, source ranking algorithms.

---

## Journey 5 â€” Self Development

**Goal:** Audit a project and apply improvements.

**Steps:**
1. Open Workspace
2. Request project audit
3. AI analyzes project structure
4. AI identifies bottlenecks and issues
5. AI presents findings with severity
6. User approves proposal
7. AI generates patch
8. AI runs tests
9. AI presents proposal, patch, and test results
10. User approves application
11. AI applies changes

**User sees:** Project analysis, issues list, proposal, patch diff, test results, application confirmation.
**User does NOT see:** Architecture analysis internals, code smell detection algorithms, patch generation logic.

---

## Journey 6 â€” Multi-Capability

**Goal:** Build an ISP from concept to deployment plan.

**Steps:**
1. User describes goal in natural language
2. AI classifies intent and selects multiple Capability Packs
3. AI creates execution plan
4. AI executes each stage:
   - Research: market and best practices
   - Network: design topology
   - DevOps: infrastructure plan
   - Code: billing system design
   - Self Development: deployment proposal
> Terjemahan Indonesia: Research: market dan best practices Network: design topology DevOps: infrastructure plan Code: billing sistem design Self Development: penyebaran proposal
5. AI presents integrated plan
6. User can drill into each section
7. User approves overall plan
8. AI executes with progress indication

**User sees:** Single coherent plan, progress per stage, results per capability, integrated documentation.
**User does NOT see:** Capability Pack routing, cross-pack communication, task decomposition logic.

---

## Journey 7 â€” Goal Execution

**Goal:** Complex end-to-end execution from a single goal statement.

**Steps:**
1. User states a goal: "Bangun aplikasi Inventory."
2. AI understands the goal and breaks it into phases
3. AI presents execution plan with estimates
4. User approves
5. AI executes:
   - Requirement gathering
   - Architecture design
   - Database design
   - Backend implementation
   - Frontend implementation
   - Testing
   - Documentation
> Terjemahan Indonesia: Requirement gathering arsitektur design Database design Backend implementation Frontend implementation Testing dokumentasi
6. AI shows real-time progress
7. AI delivers complete, verified result

**User sees:** One goal, one plan, one result.
**User does NOT see:** Task decomposition, worker selection, scheduling, retries, verification loops.

---

## Design Principles

All journeys must follow these principles:
> Terjemahan Indonesia: Semua perjalanan harus mengikuti prinsip-prinsip berikut:

1. **One conversation:** User never selects a Capability Pack manually.
2. **No internal exposure:** Users never see Workers, Runtimes, Planners, or internal data structures.
3. **Progress transparency:** Long-running tasks show human-readable progress.
4. **Approval before action:** Irreversible actions require explicit user approval.
5. **Artifact persistence:** All significant outputs are saved and retrievable.
6. **Explainability on demand:** User can ask "why" at any time.

---

## Validation

Every new feature or change must be validated against:
> Terjemahan Indonesia: Every new feature or change must menjadi validated against:
1. Does it preserve the one-conversation experience?
2. Does it hide internal mechanisms from the user?
3. Does it maintain progress transparency?
4. Does it respect the approval workflow?
5. Does it persist artifacts?

If any answer is "no", the feature must be redesigned before release.
> Terjemahan Indonesia: If any answer adalah "no", feature must menjadi redesigned before rilis.
