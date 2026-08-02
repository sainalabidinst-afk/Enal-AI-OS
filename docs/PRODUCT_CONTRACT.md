<!-- BILINGUAL_DOCS_START -->
## Bahasa Indonesia / English

### Ringkasan / Summary
Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.
> Terjemahan Indonesia: Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.

- Bahasa Indonesia: konten utama tetap dipertahankan dalam dokumen asli, dan bagian ini memberi konteks ringkas dalam bahasa Indonesia.
- English: the main content remains in the original document, and this section provides a concise bilingual context for international readers.

### Informasi Dokumen / Document Info
- File: `docs/PRODUCT_CONTRACT.md`
- Judul: Product Contract
- Status: bilingual header added

<!-- BILINGUAL_DOCS_END -->

<!-- DOCUMENT_METADATA_START -->
**Owner:** Documentation Team
**Canonical Owner:** Documentation Governance Lead
**Last Verified:** 2026-08-02
**Version:** 1.0.0
**Status:** Active
**SSOT:** Product contract, user promises, and capability commitments
<!-- DOCUMENT_METADATA_END -->

# Product Contract v1.0

**Status:** Frozen  
**Effective:** 2026-07-11  
**Owner:** Chief Product Officer  
**Purpose:** Defines the product-level contract between backend baseline and frontend implementation. No frontend code may be written before this document is approved and all Product Gate checks pass.

---

## 1. Product Positioning

Enal AI OS is an **AI Execution Platform**.
> Terjemahan Indonesia: Enal AI OS adalah sebuah AI Execution platform.

Users describe the outcome they want. ECP understands the goal, plans execution, coordinates tasks, verifies results, and delivers a complete outcomeâ€”all through a single conversation.
> Terjemahan Indonesia: Users describe outcome they want. ECP understands goal, plans execution, coordinates tasks, verifies results, dan delivers sebuah complete outcomeâ€”all through sebuah single conversation.

The user sees one AI. The user never sees the machinery underneath.
> Terjemahan Indonesia: User sees one AI. user never sees machinery underneath.

**Motto:** A stable core. Expert capabilities. One conversation.

**Target user:** Developers, operators, and knowledge workers who need AI assistance for complex, multi-step tasks.

**Core value proposition:** One conversation â†’ complete outcome.

---

## 2. Product Contract Lock

This document locks the product definition for the Product MVP phase.
> Terjemahan Indonesia: Ini dokumen locks product definition untuk Product MVP phase.

### Locked Artifacts

| Document | Status | Effective |
|----------|--------|-----------|
| `docs/frontend/PRODUCT_UI_SPEC.md` | Frozen | 2026-07-11 |
| `docs/frontend/UI_ARCHITECTURE.md` | Frozen | 2026-07-11 |
| `docs/frontend/SCREEN_FLOW.md` | Frozen | 2026-07-11 |
| `docs/frontend/COMPONENT_LIBRARY.md` | Frozen | 2026-07-11 |
| `docs/frontend/STATE_MANAGEMENT.md` | Frozen | 2026-07-11 |
| `docs/frontend/API_MAPPING.md` | Frozen | 2026-07-11 |
| `docs/frontend/ERROR_STATES.md` | Frozen | 2026-07-11 |
| `docs/frontend/MOBILE_LAYOUT.md` | Frozen | 2026-07-11 |
| `docs/frontend/DESIGN_TOKENS.md` | Frozen | 2026-07-11 |
| `docs/frontend/FRONTEND_DEFINITION_OF_DONE.md` | Frozen | 2026-07-11 |

No further changes to these documents are allowed during Product MVP implementation without a Product Change Request.
> Terjemahan Indonesia: No further changes untuk these documents adalah allowed during Product MVP implementation without sebuah Product Change Request.

---

## 3. Product MVP Scope

### In Scope

| Screen | Purpose | Must-Have for MVP |
|--------|---------|-------------------|
| Chat | Primary interface. Single conversation with AI. | Yes |
| Workspace | Project overview with conversation, files, memory, artifacts, execution history. | Yes |
| Artifact Viewer | View, compare, restore artifact versions. | Yes |
| Approval Dialog | Confirm or reject irreversible actions. | Yes |
| Settings | Theme, model preference, notifications. | Yes |
| Capability Discovery | Dynamic list of capabilities from backend. | Yes |
| Execution History | List of executions with status, progress, artifacts. | Yes |

### Out of Scope (Post-MVP)

- Agent selection UI
- Capability Pack configuration
- Worker configuration
- Model selection UI (except in Settings)
- Execution Graph visualization
- Admin dashboard
- Analytics dashboard
- Plugin management UI
- Advanced theming

---

## 4. Non-Negotiable Product Principles

These principles are locked. Any UI element that violates them is a defect.
> Terjemahan Indonesia: These principles adalah locked. Any UI element itu violates them adalah sebuah defect.

### Principle 1: One Conversation

The user interface is a single conversation. There is no menu for selecting Capability Pack. There is no dropdown for selecting a Worker. There is no configuration panel for choosing a Model.
> Terjemahan Indonesia: User interface adalah sebuah single conversation. There adalah no menu untuk selecting kapabilitas Pack. There adalah no dropdown untuk selecting sebuah Worker. There adalah no konfigurasi panel untuk choosing sebuah Model.

The AI does that internally.
> Terjemahan Indonesia: AI does itu internally.

### Principle 2: Outcome Over Mechanism

Users describe outcomes, not mechanisms.
> Terjemahan Indonesia: Pengguna menggambarkan hasil, bukan mekanisme.

User says: "Audit jaringan kantor saya."
User does NOT say: "Jalankan Network Capability."
> Terjemahan Indonesia: User says: "Audit jaringan kantor saya." User does NOT say: "Jalankan Network kapabilitas."

The UI must never expose internal concepts such as Capability Pack, Worker, Execution Runtime, Task Planner, or Execution Graph to the user.
> Terjemahan Indonesia: UI must never expose internal concepts such as kapabilitas Pack, Worker, Execution Runtime, Task Planner, or Execution Graph untuk user.

### Principle 3: Progress Transparency

During long-running tasks, the system must show progress. Progress indication must be coarse-grained and human-readable.
> Terjemahan Indonesia: During long-running tasks, sistem must show progress. Progress indication must menjadi coarse-grained dan human-readable.

Acceptable:
> Terjemahan Indonesia: Dapat diterima:
- "Analyzing configuration..."
- "Generating documentation..."
- "Running tests..."

Not acceptable:
> Terjemahan Indonesia: Tidak dapat diterima:
- Generic "Loading..."
- Internal step names like "Stage 3: Execute Subtask 7"

### Principle 4: Approval Before Action

For irreversible actions, the UI must show an explicit approval dialog. AI never applies changes without user approval.
> Terjemahan Indonesia: Untuk irreversible actions, UI must show sebuah explicit approval dialog. AI never applies changes without user approval.

### Principle 5: Artifact First

Every significant output is an Artifact. Artifacts are always visible, versioned, and retrievable.
> Terjemahan Indonesia: Every significant output adalah sebuah Artifact. Artifacts adalah always visible, versioned, dan retrievable.

### Principle 6: Workspace Isolation

Each project is isolated in a Workspace. Conversation, files, memory, tasks, artifacts, and execution history are scoped per Workspace.
> Terjemahan Indonesia: Each proyek adalah isolated dalam sebuah Workspace. Conversation, files, memory, tasks, artifacts, dan execution history adalah scoped per Workspace.

### Principle 7: No Mock Data

The frontend must consume backend APIs. Mock data is not allowed in any production screen.
> Terjemahan Indonesia: Frontend must consume backend APIs. Mock data adalah not allowed dalam any production screen.

---

## 5. Backend Dependency Lock

The frontend is locked to **Backend Baseline v1.0.0-dev** (2026-07-11).
> Terjemahan Indonesia: Frontend adalah locked untuk Backend dasar v1.0.0-dev (2026-07-11).

The baseline is stable. The following changes are allowed without a Product Change Request:
> Terjemahan Indonesia: Dasar adalah stable. following changes adalah allowed without sebuah Product Change Request:

- Bug fix
- Security fix
- Performance improvement
- Small integration needed by frontend
- ADR-approved cross-capability changes

The following changes require a Product Change Request:
> Terjemahan Indonesia: Following changes require sebuah Product Change Request:

- Runtime v2
- Planner v2
- Kernel v2
- Conversation v2
- Worker v2
- Any new layer
- Large refactors without cross-domain need
- Breaking changes to locked API endpoints

### Required Backend APIs for MVP

The following backend APIs must be stable and available before frontend development begins:
> Terjemahan Indonesia: Following backend APIs must menjadi stable dan available before frontend development begins:

#### Chat
- [x] POST `/api/v1/chat`
- [x] POST `/api/v1/chat/stream`
- [x] GET `/api/v1/conversations/{conversationId}`
- [x] DELETE `/api/v1/conversations/{conversationId}`

#### Workspace
- [x] GET `/api/v1/workspaces`
- [x] POST `/api/v1/workspaces`
- [x] GET `/api/v1/workspaces/{workspaceId}`
- [x] DELETE `/api/v1/workspaces/{workspaceId}`
- [x] POST `/api/v1/workspaces/{workspaceId}/files`
- [x] POST `/api/v1/workspaces/{workspaceId}/memory`
- [x] GET `/api/v1/workspaces/{workspaceId}/memory/{key}`

#### Execution
- [x] POST `/api/v1/executions`
- [x] GET `/api/v1/executions/{executionId}`
- [x] GET `/api/v1/executions`
- [x] POST `/api/v1/executions/{executionId}/phases`
- [x] PATCH `/api/v1/executions/{executionId}/phases/{phaseId}`
- [x] POST `/api/v1/executions/{executionId}/progress`
- [x] POST `/api/v1/executions/{executionId}/logs`
- [x] GET `/api/v1/executions/{executionId}/logs`
- [x] POST `/api/v1/executions/{executionId}/cancel`
- [x] DELETE `/api/v1/executions/{executionId}`
- [x] POST `/api/v1/executions/run`

#### Artifact
- [x] GET `/api/v1/artifacts`
- [x] POST `/api/v1/artifacts`
- [x] GET `/api/v1/artifacts/{artifactId}`
- [x] GET `/api/v1/artifacts/{artifactId}/versions/{version}`
- [x] POST `/api/v1/artifacts/{artifactId}/versions`
- [x] POST `/api/v1/artifacts/{artifactId}/restore/{version}`
- [x] GET `/api/v1/executions/{executionId}/artifacts`
- [x] DELETE `/api/v1/artifacts/{artifactId}`

#### Capability
- [x] GET `/api/v1/capabilities`
- [x] GET `/api/v1/capabilities/{capabilityId}`

#### Model
- [x] GET `/api/v1/models/providers`
- [x] GET `/api/v1/models/health`
- [x] POST `/api/v1/models/route`

#### Notification
- [x] GET `/api/v1/notifications/{recipient}`
- [x] PATCH `/api/v1/notifications/{recipient}/read/{notificationId}`

#### Streaming Events
- [x] SSE from `/api/v1/chat/stream` with events: `final`, `execution_started`, `phase`, `task`, `log`, `artifact`, `progress`, `execution_complete`, `error`

---

## 6. Design Token Lock

All visual values must use these tokens. No hardcoded colors, spacing, or typography.
> Terjemahan Indonesia: Semua nilai visual harus menggunakan token ini. Tidak ada warna, spasi, atau tipografi hardcode.

### Colors

| Token | Value | Usage |
|-------|-------|-------|
| `--color-bg-primary` | #0f1117 | Main background |
| `--color-bg-secondary` | #1a1d27 | Cards, panels |
| `--color-bg-tertiary` | #252830 | Elevated surfaces |
| `--color-text-primary` | #e4e6eb | Primary text |
| `--color-text-secondary` | #9ca3af | Secondary text |
| `--color-accent` | #3b82f6 | Primary action |
| `--color-success` | #22c55e | Success state |
| `--color-warning` | #f59e0b | Warning state |
| `--color-danger` | #ef4444 | Error/danger state |
| `--color-border` | #374151 | Borders |

### Typography

| Token | Value | Usage |
|-------|-------|-------|
| `--font-family` | Inter, system-ui, sans-serif | All text |
| `--font-size-xs` | 0.75rem | Labels, hints |
| `--font-size-sm` | 0.875rem | Secondary text |
| `--font-size-md` | 1rem | Body text |
| `--font-size-lg` | 1.125rem | Emphasized text |
| `--font-size-xl` | 1.25rem | Headings |
| `--font-size-2xl` | 1.5rem | Page titles |

### Spacing

| Token | Value | Usage |
|-------|-------|-------|
| `--space-1` | 4px | Tight spacing |
| `--space-2` | 8px | Compact spacing |
| `--space-3` | 12px | Default spacing |
| `--space-4` | 16px | Comfortable spacing |
| `--space-5` | 24px | Section spacing |
| `--space-6` | 32px | Page spacing |

### Radius

| Token | Value | Usage |
|-------|-------|-------|
| `--radius-sm` | 4px | Small elements |
| `--radius-md` | 8px | Cards, buttons |
| `--radius-lg` | 12px | Panels, modals |

### Shadows

| Token | Value | Usage |
|-------|-------|-------|
| `--shadow-sm` | 0 1px 2px rgba(0,0,0,0.3) | Subtle elevation |
| `--shadow-md` | 0 4px 6px rgba(0,0,0,0.4) | Cards |
| `--shadow-lg` | 0 10px 15px rgba(0,0,0,0.5) | Modals, dialogs |

---

## 7. API Contract Rule

This rule is non-negotiable during the Product MVP phase.
> Terjemahan Indonesia: Ini rule adalah non-negotiable during Product MVP phase.

- Frontend **must not** define new backend endpoints.
- Frontend **must not** call any endpoint not listed in `docs/frontend/API_MAPPING.md`.
- If the frontend needs an endpoint, the backend must add a small, focused endpoint following existing patterns.
- After any new endpoint is added, `API_MAPPING.md` and `PRODUCT_CONTRACT.md` must be updated before the frontend consumes it.
- `API_MAPPING.md` is the single source of truth for all API contracts.

This prevents frontend/backend drift and ensures the Product Contract remains the executable contract between the two layers.
> Terjemahan Indonesia: Ini prevents frontend/backend drift dan ensures Product Contract remains executable contract between two layers.

---

## 8. Product Gate Checklist

All items must be checked before frontend coding begins.
> Terjemahan Indonesia: All items must menjadi checked before frontend coding begins.

### Documentation Gate
- [x] PRODUCT_UI_SPEC.md exists and is frozen
- [x] UI_ARCHITECTURE.md exists and is frozen
- [x] SCREEN_FLOW.md exists and is frozen
- [x] COMPONENT_LIBRARY.md exists and is frozen
- [x] STATE_MANAGEMENT.md exists and is frozen
- [x] API_MAPPING.md exists and is frozen
- [x] ERROR_STATES.md exists and is frozen
- [x] MOBILE_LAYOUT.md exists and is frozen
- [x] DESIGN_TOKENS.md exists and is frozen
- [x] FRONTEND_DEFINITION_OF_DONE.md exists and is frozen

### Backend Gate
- [x] Backend Baseline v1.0.0-dev is active
- [x] All required APIs are implemented and documented
- [x] API contracts are stable (no breaking changes planned)
- [x] Streaming SSE endpoint is functional
- [x] No backend architecture changes pending that affect frontend

### Product Gate
- [x] All 7 screens have clear purpose and acceptance criteria
- [x] All user journeys can be completed from a single chat
- [x] Mobile flow is defined and approved
- [x] Error states are defined for all API calls
- [x] Approval flow is defined for irreversible actions
- [x] Artifact lifecycle is defined (create, view, version, restore)
- [x] Workspace lifecycle is defined (create, switch, delete)
- [x] No Capability Pack or Worker exposed in UI
- [x] No mock data allowed in production screens

### Technical Gate
- [x] Frontend framework chosen: Next.js 14 + React 18 + TypeScript
- [x] State management chosen: Zustand
- [x] Styling chosen: Tailwind CSS v3
- [x] API client chosen: fetch with custom service layer
- [x] Streaming client chosen: EventSource with custom hook
- [x] All design tokens are defined in DESIGN_TOKENS.md
- [x] Tech stack aligns with UI_ARCHITECTURE.md

### Gap Analysis

| Frontend Requirement | Backend Status | Action |
|---------------------|----------------|--------|
| POST /chat | Implemented | None |
| POST /chat/stream | Implemented | None |
| GET /conversations/{id} | Implemented | None |
| DELETE /conversations/{id} | Implemented | None |
| GET /workspaces | Implemented | None |
| POST /workspaces | Implemented | None |
| GET /workspaces/{id} | Implemented | None |
| DELETE /workspaces/{id} | Implemented | None |
| GET /workspaces/{id}/files | Implemented | None |
| POST /workspaces/{id}/files | Implemented | None |
| DELETE /workspaces/{id}/files/{filename} | Implemented | None |
| GET /workspaces/{id}/memory/{key} | Implemented | None |
| POST /workspaces/{id}/memory | Implemented | None |
| All execution APIs | Implemented | None |
| All artifact APIs | Implemented | None |
| GET /api/v1/capabilities | Implemented | None |
| GET /api/v1/capabilities/{id} | Implemented | None |
| GET /api/v1/models/providers | Implemented | None |
| GET /api/v1/models/health | Implemented | None |
| POST /api/v1/models/route | Implemented | None |
| GET /api/v1/notifications/{recipient} | Implemented | None |
| PATCH /api/v1/notifications/{recipient}/read/{id} | Implemented | None |
| SSE streaming events | Implemented | None |

**Blocker:** None. All 22 required backend APIs are implemented and available.

---

## 8. Frontend Implementation Plan

### Phase 1: Foundation (3â€“5 days)

Scaffold the project structure. Wire up all services to real backend APIs. Zero mock data.
> Terjemahan Indonesia: Scaffold proyek structure. Wire up all services untuk real backend APIs. Zero mock data.

Deliverables:
> Terjemahan Indonesia: Kiriman:
- Project structure matches `docs/frontend/PRODUCT_UI_SPEC.md` Section 10
- All services in `services/` call real backend APIs
- All types in `types/` match backend schemas
- Zustand stores in `store/` are wired to services
- `layout.tsx` renders without errors

### Phase 2: Chat MVP (1 week)

Build the single conversation interface. This is the heart of the product.
> Terjemahan Indonesia: Membangun single conversation interface. ini adalah heart dari product.

Deliverables:
> Terjemahan Indonesia: Kiriman:
- User can type a goal and send it
- AI response streams in via SSE
- Progress events render in real-time
- Artifact events render inline
- Error states are actionable
- Mobile responsive at 320px

### Phase 3: Workspace (3 days)

Build the workspace screen.
> Terjemahan Indonesia: Membangun workspace screen.

Deliverables:
> Terjemahan Indonesia: Kiriman:
- List workspaces
- Create new workspace
- Switch between workspaces
- View files, memory, artifacts, execution history
- Delete workspace with approval dialog

**Blocker:** None. Semua endpoint yang dibutuhkan untuk Frontend MVP sudah tersedia di backend.

### Phase 4: Streaming UX (2 days)

Polish the streaming experience.
> Terjemahan Indonesia: Polish streaming experience.

Deliverables:
> Terjemahan Indonesia: Kiriman:
- Human-readable progress messages
- Phase transitions are smooth
- Logs are collapsible
- Artifact cards appear inline
- Connection drop shows reconnect indicator

### Phase 5: Approval UX (1 day)

Build the approval dialog.
> Terjemahan Indonesia: Membangun approval dialog.

Deliverables:
> Terjemahan Indonesia: Kiriman:
- Approval dialog renders for irreversible actions
- Cancel dismisses without side effects
- Approve sends the actual API call
- Loading state while pending
- Error state if API call fails

### Phase 6: Artifact Viewer (2 days)

Build the artifact viewer.
> Terjemahan Indonesia: Membangun artifact viewer.

Deliverables:
> Terjemahan Indonesia: Kiriman:
- View artifact content
- Compare versions
- Restore previous version
- Download artifact
- Type-specific rendering (code, markdown, config)

### Phase 7: Polish & Mobile (2 days)

Final polish before dogfooding.
> Terjemahan Indonesia: Poles terakhir sebelum dogfood.

Deliverables:
> Terjemahan Indonesia: Kiriman:
- Mobile layout at 320px
- Navigation works on mobile
- All screens responsive
- Design tokens used consistently
- Accessibility: keyboard navigation, ARIA labels, focus rings

### Phase 8: Dogfooding (30 days)

Use Enal AI OS to build and improve Enal AI OS.
> Terjemahan Indonesia: Use Enal AI OS untuk membangun dan improve Enal AI OS.

Deliverables:
> Terjemahan Indonesia: Kiriman:
- Daily usage by team
- Real cases logged in `real_cases/`
- Bugs and UX issues tracked
- Capability improvements measured via benchmarks

---

## 9. Definition of Done â€” Product MVP

Product MVP is complete when:
> Terjemahan Indonesia: Product MVP adalah complete when:

- [ ] All 7 screens are implemented and functional
- [ ] Chat works end-to-end: send message â†’ receive response â†’ see progress â†’ see artifacts
- [ ] Streaming renders real-time progress events
- [ ] Workspace is created automatically on first chat
- [ ] Approval dialog works for all irreversible actions
- [ ] Artifact viewer can display, compare, and restore versions
- [ ] Execution history shows all past executions
- [ ] Mobile layout works at 320px width
- [ ] All screens consume real backend APIs
- [ ] No mock data in production code
- [ ] All design tokens are used
- [ ] No internal architecture terms exposed to user
- [ ] 30-day dogfooding completed
- [ ] â‰¥100 real cases logged
- [ ] Capability benchmark score â‰¥85%

---

## 10. Post-MVP Roadmap

After Product MVP is complete:
> Terjemahan Indonesia: After Product MVP adalah complete:

1. **Dogfooding Insights** â†’ Capability improvements
2. **Real Cases** â†’ Benchmark-driven capability excellence
3. **User Feedback** â†’ UX refinements
4. **Performance** â†’ Optimization based on real usage
5. **v1.0.0 Stable** â†’ Production readiness

---

## 11. Approval

| Role | Name | Status | Date |
|------|------|--------|------|
| Chief Product Officer | | Approved | 2026-07-11 |
| Chief Architect | | Approved | 2026-07-11 |
| Frontend Lead | | Pending | |

This document is locked. No further changes to product scope, design principles, or backend dependencies are allowed without a Product Change Request signed by the Chief Product Officer and Chief Architect.
> Terjemahan Indonesia: Ini dokumen adalah locked. No further changes untuk product scope, design principles, or backend dependencies adalah allowed without sebuah Product Change Request signed oleh Chief Product Officer dan Chief Architect.
