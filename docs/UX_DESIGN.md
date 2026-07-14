# UX Design Specification

This document defines the user-facing experience of Enal AI OS.
It is the source of truth for how users interact with the platform.

---

## Core Principle

One conversation. One AI. One goal. Many tasks. One result.

Users do not need to know about Capability Packs, Workers, Execution Runtime, Task Planners, Execution Graphs, or any other internal mechanism.
All of that is hidden behind a natural conversational interface.

---

## Positioning

Enal AI OS is an **AI Execution Platform**.

Users describe the outcome they want.
ECP understands the goal, plans execution, coordinates tasks, verifies results, and delivers a complete outcome—all through a single conversation.

Not:
- "AI with 300 micro-agents"
- "AI Workforce"
- "Multi-Agent Framework"

But:
- "One AI that gets things done"

---

## Interface

The user interface is a single conversational window:

```
┌──────────────────────────────────────┐
│         Enal AI OS                   │
├──────────────────────────────────────┤
│                                      │
│  Describe the outcome you want.      │
│                                      │
│  ________________________________    │
│ | Ketik perintah...              |   │
│ |________________________________|   │
│                                      │
└──────────────────────────────────────┘
```

There is no menu for selecting Capability Packs.
There is no configuration panel for choosing Workers.
There is no dropdown for selecting Execution Runtime.
There is no "Agent Swarm" indicator.

The AI does everything internally.

---

## Execution Model

```
One Conversation
        ↓
    One Goal
        ↓
  Goal Understanding
        ↓
 Execution Planning
        ↓
    Many Tasks
        ↓
   Execution Graph
        ↓
    Scheduler
        ↓
   Many Workers
        ↓
    Verification
        ↓
     Artifacts
        ↓
   One Result
```

The user sees: One Conversation → One Goal → One Result.
Internally: Goal Understanding → Execution Planning → Task DAG → Scheduler → Workers → Verification → Artifacts.

Goal Understanding is the most critical step. The AI must understand intent, context, constraints, and desired outcome before executing anything.

---

## User Workflow

### 1. User States a Goal

User describes the desired outcome in natural language or uploads a file.

Examples:
- "Bangun aplikasi Inventory."
- "Analisa konfigurasi MikroTik ini."
- "Audit project FastAPI saya."
- "Saya ingin membuat ISP."

### 2. AI Understands the Goal

Behind the scenes, ECP:
1. Understands the goal deeply
2. Identifies required capabilities
3. Breaks goal into phases and tasks
4. Identifies dependencies and parallelism
5. Estimates effort, artifacts, and risks
6. Builds Execution Graph

This is **Goal Understanding**. It is the hardest and most important part.

### 3. AI Presents the Plan

AI responds with a clear, actionable plan:

```
Saya memahami tujuan Anda.

Saya membaginya menjadi:
Phase 1: Business Analysis
Phase 2: Architecture Design
Phase 3: Backend Implementation
Phase 4: Frontend Implementation
Phase 5: Testing
Phase 6: Documentation

Estimasi: 187 subtasks, 38 artifacts, 4 capability packs

Mulai?
```

### 4. User Approves or Refines

- User can approve, refine, or cancel
- No hidden configuration required
- User sees one coherent plan, not internal task lists

### 5. AIExecutes

AI shows real-time progress:

```
✓ Tujuan dipahami
✓ Plan dibuat
✓ Menjalankan Phase 1: Business Analysis
⏳ Menjalankan Phase 2: Architecture Design...
```

### 6. AI Delivers Result

AI presents the final outcome:

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

- History persists across sessions
- Memory is scoped per Workspace
- Artifacts are organized per Workspace
- User can switch between Workspaces

Example:
```
Workspace: Inventory System
├── History
├── Artifacts
│   ├── requirements.md
│   ├── schema.sql
│   └── backend/
└── Memory
```

---

## Progress Transparency

During execution, AI shows human-readable progress:

```
✓ Memahami permintaan
✓ Memilih Capability
✓ Menyusun Task
⏳ Menganalisis konfigurasi...
⏳ Membuat dokumentasi...
```

Not:
- "Stage 3: Execute Subtask 7"
- Internal state names
- Worker IDs or Execution Graph node IDs

---

## Explainability

User can ask "why" at any time:

> "Why did you choose that approach?"

AI responds with:
- Goal understanding summary
- Capability used
- Reasoning behind the choice
- Confidence level
- Steps taken

No internal architecture terms. User-friendly explanations only.

---

## Skill Discovery

User can ask:
- "Apa yang bisa kamu lakukan?"
- "What can you do?"

AI responds from the Capability Graph, dynamically:

```
Saya memiliki 6 Capability utama:
✓ Network Engineering
  - Audit MikroTik
  - Audit Cisco
  - Audit Fortinet
  - Generate Documentation
  - Compliance Check
  - Security Review
✓ Code Engineering
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
- Analysis reports
- Recommendations
- Patches and diffs
- Test reports
- Deployment plans
- Documentation

Artifacts are:
- Versioned
- Scoped per Workspace
- Retrievable
- Comparable
- Restorable

---

## Human Approval

For irreversible actions, AI requires explicit approval:

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
1. A new user can accomplish a real task without reading documentation
2. User never needs to select a Capability Pack manually
3. User never needs to configure Workers, Runtimes, or Planners
4. All explainability, progress, and approval flows feel natural
5. The system feels like one AI, not a collection of tools
6. Users describe ECP as "an AI that gets things done" rather than "a framework with many agents"
7. Users can describe their goal in plain language and get a complete, verified result
