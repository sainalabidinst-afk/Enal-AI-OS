<!-- BILINGUAL_DOCS_START -->
## Bahasa Indonesia / English

### Ringkasan / Summary
Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.
> Terjemahan Indonesia: Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.

- Bahasa Indonesia: konten utama tetap dipertahankan dalam dokumen asli, dan bagian ini memberi konteks ringkas dalam bahasa Indonesia.
- English: the main content remains in the original document, and this section provides a concise bilingual context for international readers.

### Informasi Dokumen / Document Info
- File: `docs/UX_DESIGN.md`
- Judul: Ux Design
- Status: bilingual header added

<!-- BILINGUAL_DOCS_END -->

<!-- DOCUMENT_METADATA_START -->
**Owner:** Documentation Team
**Canonical Owner:** Documentation Governance Lead
**Last Verified:** 2026-08-02
**Version:** 1.0.0
**Status:** Active
<!-- DOCUMENT_METADATA_END -->

# UX Design Specification

This document defines the user-facing experience of Enal AI OS.
It is the source of truth for how users interact with the platform.
> Terjemahan Indonesia: Ini dokumen defines user-facing experience dari Enal AI OS. It adalah source dari truth untuk how users interact dengan platform.

---

## Core Principle

One conversation. One AI. One goal. Many tasks. One result.
> Terjemahan Indonesia: Satu percakapan. Satu AI. Satu tujuan. Banyak tugas. Satu hasil.

Users do not need to know about Capability Packs, Workers, Execution Runtime, Task Planners, Execution Graphs, or any other internal mechanism.
All of that is hidden behind a natural conversational interface.
> Terjemahan Indonesia: Users do not need untuk know about kapabilitas Packs, Workers, Execution Runtime, Task Planners, Execution Graphs, or any other internal mechanism. All dari itu adalah hidden behind sebuah natural conversational interface.

---

## Positioning

Enal AI OS is an **AI Execution Platform**.
> Terjemahan Indonesia: Enal AI OS adalah sebuah AI Execution platform.

Users describe the outcome they want.
ECP understands the goal, plans execution, coordinates tasks, verifies results, and delivers a complete outcomeâ€”all through a single conversation.
> Terjemahan Indonesia: Users describe outcome they want. ECP understands goal, plans execution, coordinates tasks, verifies results, dan delivers sebuah complete outcomeâ€”all through sebuah single conversation.

Not:
- "AI with 300 micro-agents"
- "AI Workforce"
- "Multi-Agent Framework"

But:
- "One AI that gets things done"

---

## Interface

The user interface is a single conversational window:
> Terjemahan Indonesia: User interface adalah sebuah single conversational window:

```
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚         Enal AI OS                   â”‚
â”œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¤
â”‚                                      â”‚
â”‚  Describe the outcome you want.      â”‚
â”‚                                      â”‚
â”‚  ________________________________    â”‚
â”‚ | Ketik perintah...              |   â”‚
â”‚ |________________________________|   â”‚
â”‚                                      â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

There is no menu for selecting Capability Packs.
There is no configuration panel for choosing Workers.
There is no dropdown for selecting Execution Runtime.
There is no "Agent Swarm" indicator.
> Terjemahan Indonesia: There adalah no menu untuk selecting kapabilitas Packs. There adalah no konfigurasi panel untuk choosing Workers. There adalah no dropdown untuk selecting Execution Runtime. There adalah no "agen Swarm" indicator.

The AI does everything internally.
> Terjemahan Indonesia: AI does everything internally.

---

## Execution Model

```
One Conversation
        â†“
    One Goal
        â†“
  Goal Understanding
        â†“
 Execution Planning
        â†“
    Many Tasks
        â†“
   Execution Graph
        â†“
    Scheduler
        â†“
   Many Workers
        â†“
    Verification
        â†“
     Artifacts
        â†“
   One Result
```

The user sees: One Conversation â†’ One Goal â†’ One Result.
Internally: Goal Understanding â†’ Execution Planning â†’ Task DAG â†’ Scheduler â†’ Workers â†’ Verification â†’ Artifacts.
> Terjemahan Indonesia: User sees: One Conversation â†’ One Goal â†’ One Result. Internally: Goal Understanding â†’ Execution Planning â†’ Task DAG â†’ Scheduler â†’ Workers â†’ Verification â†’ Artifacts.

Goal Understanding is the most critical step. The AI must understand intent, context, constraints, and desired outcome before executing anything.
> Terjemahan Indonesia: Goal Understanding adalah most critical step. AI must understand intent, context, constraints, dan desired outcome before executing anything.

---

## User Workflow

### 1. User States a Goal

User describes the desired outcome in natural language or uploads a file.
> Terjemahan Indonesia: User describes desired outcome dalam natural language or uploads sebuah file.

Examples:
> Terjemahan Indonesia: Contoh:
- "Bangun aplikasi Inventory."
- "Analisa konfigurasi MikroTik ini."
- "Audit project FastAPI saya."
- "Saya ingin membuat ISP."

### 2. AI Understands the Goal

Behind the scenes, ECP:
> Terjemahan Indonesia: Behind scenes, ECP:
1. Understands the goal deeply
2. Identifies required capabilities
3. Breaks goal into phases and tasks
4. Identifies dependencies and parallelism
5. Estimates effort, artifacts, and risks
6. Builds Execution Graph

This is **Goal Understanding**. It is the hardest and most important part.
> Terjemahan Indonesia: Ini adalah Goal Understanding. It adalah hardest dan most important part.

### 3. AI Presents the Plan

AI responds with a clear, actionable plan:
> Terjemahan Indonesia: AI responds dengan sebuah clear, actionable plan:

```
Saya memahami tujuan Anda.

Saya membaginya menjadi:
Phase 1: Business Analysis
Phase 2: Architecture Design
Phase 3: Backend Implementation
Phase 4: Frontend Implementation
Phase 5: Testing
Phase 6: Documentation

Estimasi: 187 subtasks, 38 artifacts, existing packs

Mulai?
```

### 4. User Approves or Refines

- User can approve, refine, or cancel
- No hidden configuration required
- User sees one coherent plan, not internal task lists

### 5. AIExecutes

AI shows real-time progress:
> Terjemahan Indonesia: AI menunjukkan kemajuan waktu nyata:

```
âœ“ Tujuan dipahami
âœ“ Plan dibuat
âœ“ Menjalankan Phase 1: Business Analysis
â³ Menjalankan Phase 2: Architecture Design...
```

### 6. AI Delivers Result

AI presents the final outcome:
> Terjemahan Indonesia: AI presents final outcome:

```
Selesai.

Hasil:
- requirements.md
- architecture.md
- database_schema.sql
- backend/ (complete)
- frontend/ (complete)
- tests/ (87% coverage)
- README.md

Apakah ada yang perlu diperbaiki?
```

---

## Workspace

Each project gets its own Workspace.
> Terjemahan Indonesia: Each proyek gets its own Workspace.

- History persists across sessions
- Memory is scoped per Workspace
- Artifacts are organized per Workspace
- User can switch between Workspaces

Example:
> Terjemahan Indonesia: Contoh:
```
Workspace: Inventory System
â”œâ”€â”€ History
â”œâ”€â”€ Artifacts
â”‚   â”œâ”€â”€ requirements.md
â”‚   â”œâ”€â”€ schema.sql
â”‚   â””â”€â”€ backend/
â””â”€â”€ Memory
```

---

## Progress Transparency

During execution, AI shows human-readable progress:
> Terjemahan Indonesia: Selama eksekusi, AI menunjukkan kemajuan yang dapat dibaca manusia:

```
âœ“ Memahami permintaan
âœ“ Memilih Capability
âœ“ Menyusun Task
â³ Menganalisis konfigurasi...
â³ Membuat dokumentasi...
```

Not:
- "Stage 3: Execute Subtask 7"
- Internal state names
- Worker IDs or Execution Graph node IDs

---

## Explainability

User can ask "why" at any time:
> Terjemahan Indonesia: User dapat ask "why" at any time:

> "Why did you choose that approach?"

AI responds with:
> Terjemahan Indonesia: AI responds dengan:
- Goal understanding summary
- Capability used
- Reasoning behind the choice
- Confidence level
- Steps taken

No internal architecture terms. User-friendly explanations only.
> Terjemahan Indonesia: No internal arsitektur terms. User-friendly explanations only.

---

## Skill Discovery

User can ask:
> Terjemahan Indonesia: User dapat ask:
- "Apa yang bisa kamu lakukan?"
- "What can you do?"

AI responds from the Capability Graph, dynamically:
> Terjemahan Indonesia: AI responds dari kapabilitas Graph, dynamically:

```
Saya memiliki 13 Capability Pack:
âœ“ Network Engineering
  - Audit MikroTik
  - Audit Cisco
  - Audit Fortinet
  - Generate Documentation
  - Compliance Check
  - Security Review
âœ“ Code Engineering
  - Full-stack generation
  - Code review
  - Security review
  - Architecture analysis
...
Mau mulai dari mana?
```

---

## Artifacts

All significant outputs are persisted as Artifacts:
> Terjemahan Indonesia: All significant outputs adalah persisted as Artifacts:
- Analysis reports
- Recommendations
- Patches and diffs
- Test reports
- Deployment plans
- Documentation

Artifacts are:
> Terjemahan Indonesia: Artifacts adalah:
- Versioned
- Scoped per Workspace
- Retrievable
- Comparable
- Restorable

---

## Human Approval

For irreversible actions, AI requires explicit approval:
> Terjemahan Indonesia: Untuk irreversible actions, AI requires explicit approval:

```
Saya akan menerapkan patch ini.

Files modified:
- src/auth/service.py
- src/auth/validator.py

Tests: 43/43 passed

[Ya, terapkan] [Tidak, batalkan]
```

---

## Plugin Ecosystem

New Capability Packs installed via Marketplace automatically integrate:
> Terjemahan Indonesia: New kapabilitas Packs installed via Marketplace automatically integrate:
- Appear in skill discovery
- Follow the same workflow
- No user configuration needed

---

## What Users Never See

- Capability Pack selection menus
- Worker configuration panels
- Execution Runtime settings
- Task Planner outputs
- Execution Graph internals
- Worker IDs or names
- Internal data structures
- Error messages from internal modules

If a user sees any of these, the UX design has failed.
> Terjemahan Indonesia: If sebuah user sees any dari these, UX design memiliki failed.

---

## What Users Should Feel

- One competent AI assistant
- No configuration needed
- Results come from expertise, not menus
- AI explains when asked
- AI never acts without approval
- AI remembers context across conversations
- AI gets better over time
- "I can trust Enal AI OS to finish the job"
- "This AI understands what I want, not just what I type"

---

## Success Criteria

The UX is successful when:
> Terjemahan Indonesia: UX adalah successful when:
1. A new user can accomplish a real task without reading documentation
2. User never needs to select a Capability Pack manually
3. User never needs to configure Workers, Runtimes, or Planners
4. All explainability, progress, and approval flows feel natural
5. The system feels like one AI, not a collection of tools
6. Users describe ECP as "an AI that gets things done" rather than "a framework with many agents"
7. Users can describe their goal in plain language and get a complete, verified result
