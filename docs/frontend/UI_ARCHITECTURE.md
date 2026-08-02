<!-- BILINGUAL_DOCS_START -->
## Bahasa Indonesia / English

### Ringkasan / Summary
Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.
> Terjemahan Indonesia: Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.

- Bahasa Indonesia: konten utama tetap dipertahankan dalam dokumen asli, dan bagian ini memberi konteks ringkas dalam bahasa Indonesia.
- English: the main content remains in the original document, and this section provides a concise bilingual context for international readers.

### Informasi Dokumen / Document Info
- File: `docs/frontend/UI_ARCHITECTURE.md`
- Judul: Ui Architecture
- Status: bilingual header added

<!-- BILINGUAL_DOCS_END -->

# Frontend UI Architecture

<!-- DOCUMENT_METADATA_START -->
**Owner:** Documentation Team
**Canonical Owner:** Documentation Governance Lead
**Last Verified:** 2026-08-02
**Version:** 1.0.0
**Status:** Active
**SSOT:** Frontend documentation for UI_ARCHITECTURE
<!-- DOCUMENT_METADATA_END -->

**Status:** Frozen  
**Effective:** 2026-07-11  
**Owner:** Chief Product Officer  
**Purpose:** Defines the non-negotiable architectural rules and flows for frontend implementation. No React code may be written before this document is approved.

---

## 1. Frontend Architecture Rules

These rules are non-negotiable. Any code that violates them is a defect.
> Terjemahan Indonesia: These rules adalah non-negotiable. Any code itu violates them adalah sebuah defect.

### Rule 1 â€” Frontend Never Thinks

The frontend must never make a decision that belongs to the backend.
> Terjemahan Indonesia: Frontend must never make sebuah decision itu belongs untuk backend.

**Wrong:**
```typescript
if (message.includes("mikrotik")) {
  capability = "network";
}
```

**Right:**
```typescript
POST /api/v1/chat
// Backend determines everything
Frontend only renders.
```

The frontend is a rendering layer. It does not interpret, classify, or route.
> Terjemahan Indonesia: Frontend adalah sebuah rendering layer. It does not interpret, classify, or route.

### Rule 2 â€” Frontend Never Plans

The frontend must never create:
> Terjemahan Indonesia: Frontend must never membuat:
- tasks
- execution graphs
- schedulers
- capability assignments
- plans of any kind

All of these originate from the backend.
> Terjemahan Indonesia: All dari these originate dari backend.

### Rule 3 â€” Backend is Source of Truth

For every piece of application state, there is one source of truth â€” the backend.
> Terjemahan Indonesia: Untuk every piece dari application state, there adalah one source dari truth â€” backend.

The frontend must never compute derived state that the backend already sends.
> Terjemahan Indonesia: Frontend must never compute derived state itu backend already sends.

Example â€” progress:
> Terjemahan Indonesia: Contoh - kemajuan:
```json
{
  "phase": "Security Analysis",
  "progress": 65
}
```

Backend sends this. Frontend displays this. No local computation.
> Terjemahan Indonesia: Backend sends ini. Frontend displays ini. No local computation.

### Rule 4 â€” UI = Projection

The frontend is a projection of backend state. All state originates from backend mutations.
> Terjemahan Indonesia: Frontend adalah sebuah projection dari backend state. All state originates dari backend mutations.

| State Concept | Source |
|---------------|--------|
| Workspace | Backend |
| Conversation | Backend |
| Execution | Backend |
| Artifacts | Backend |
| Progress | Backend |
| Notifications | Backend |
| Theme | Frontend |
| Sidebar | Frontend |

The frontend is permitted to cache temporarily for UX performance, but never as a source of truth.
> Terjemahan Indonesia: Frontend adalah permitted untuk cache temporarily untuk UX performance, but never as sebuah source dari truth.

### Rule 5 â€” Zero Mock Logic

Mock data is not allowed in any production screen once the backend is connected.
> Terjemahan Indonesia: Mock data adalah not allowed dalam any production screen once backend adalah connected.

Forbidden:
> Terjemahan Indonesia: Terlarang:
- `fakeExecution()`
- `fakeArtifact()`
- `dummyHistory()`
- Any hardcoded fixtures in screens or features

The Developer Preview must use real backend APIs. Mock data is only acceptable in isolated local development contexts that are never shipped.
> Terjemahan Indonesia: Developer Preview must use real backend APIs. Mock data adalah only acceptable dalam isolated local development contexts itu adalah never shipped.

### Rule 6 â€” Stateless Components

Components should be as stateless as possible.
> Terjemahan Indonesia: Components should menjadi as stateless as possible.

```typescript
// Correct
<ProgressCard phase="Security Analysis" progress={65} />

// Incorrect (contains business logic)
<ProgressCard data={execution} onPhaseUpdate={...} />
```

Components receive data via props and emit events via callbacks. They do not own business logic.
> Terjemahan Indonesia: Components receive data via props dan emit events via callbacks. They do not own business logic.

### Rule 7 â€” UI Does Not Know Capability

The frontend must not have domain-specific logic such as:
> Terjemahan Indonesia: Frontend must not memiliki domain-specific logic such as:

```typescript
switch (domain) {
  case "network":
  case "trading":
  case "research":
}
```

The frontend only knows these concepts:
> Terjemahan Indonesia: Frontend only knows these concepts:
- Execution
- Artifact
- Conversation
- Notification

Domains and Capability Packs are backend concepts and are never exposed to the UI layer.
> Terjemahan Indonesia: Domains dan kapabilitas Packs adalah backend concepts dan adalah never exposed untuk UI layer.

---

## 2. Data Flow

The canonical path for all data in the frontend:
> Terjemahan Indonesia: Canonical path untuk all data dalam frontend:

```
Backend
  â†“
API (REST / WebSocket / SSE)
  â†“
Service Layer (services/)
  â†“
Store (Zustand slices)
  â†“
Selector (derive UI data)
  â†“
Component (dumb, props-only)
  â†“
User
```

Rules:
> Terjemahan Indonesia: Aturan:
- Components never call the API directly.
- Components never call services directly.
- Components subscribe to store selectors only.
- Services normalize and validate API responses before storing.
- The store is the single gateway between services and components.

---

## 3. Event Flow

The canonical path for all user-triggered events:
> Terjemahan Indonesia: Canonical path untuk all user-triggered events:

```
User
  â†“
UI (click, input, gesture)
  â†“
API call (via service)
  â†“
Backend
  â†“
Streaming response (SSE / WebSocket)
  â†“
Store update (via stream handler)
  â†“
UI re-render
```

Rules:
> Terjemahan Indonesia: Aturan:
- API calls happen immediately â€” no intermediate "waiting" states before the first API call.
- Streaming updates go directly to the store.
- The store emits changes; components re-render automatically.
- No local setTimeout polling.

---

## 4. State Ownership

| State | Owner | Persists | Notes |
|-------|-------|----------|-------|
| Conversation | Backend | Yes | Messages, streaming state |
| Workspace | Backend | Yes | Files, memory, context |
| Execution | Backend | Yes | Status, phases, logs, progress |
| Artifact | Backend | Yes | Versions, content |
| Notification | Backend | Yes | Unread count, history |
| Model Selection | Backend | Yes | Route via `/api/v1/models/route` |
| Theme | Frontend | localStorage | UI preference only |
| Sidebar state | Frontend | localStorage | Open/closed, width |
| Draft message | Frontend | Memory only | Cleared on send |

No state slice may exist in multiple places. If the backend owns it, the frontend never stores a copy as the source of truth.
> Terjemahan Indonesia: No state slice may exist dalam multiple places. If backend owns it, frontend never stores sebuah copy as source dari truth.

---

## 5. Streaming Contract

Backend uses Server-Sent Events (SSE) or WebSocket for all real-time updates.
> Terjemahan Indonesia: Backend uses Server-Sent Events (SSE) or WebSocket untuk all real-time updates.

All stream events must be handled by a single stream middleware that updates the store.
> Terjemahan Indonesia: All stream events must menjadi handled oleh sebuah single stream middleware itu updates store.

| Event Type | Store Action |
|------------|--------------|
| `final` | `addMessage()` |
| `execution_started` | `addExecution()` |
| `phase` | `updatePhase()` / `addPhase()` |
| `task` | `addTask()` (if applicable slice) |
| `log` | `addLog()` |
| `artifact` | `addArtifact()` |
| `progress` | `setProgress()` |
| `execution_complete` | `setExecutionStatus('completed')` |
| `error` | `setError()` |

No component may consume the stream directly. Components use store selectors only.
> Terjemahan Indonesia: No component may consume stream directly. Components use store selectors only.

---

## 6. Service Layer Contract

All backend communication happens through `src/services/`.
> Terjemahan Indonesia: Semua komunikasi backend terjadi melalui src/services/.

```typescript
// services/api.ts â€” all HTTP calls
// services/chat.ts â€” chat-specific API functions
// services/execution.ts â€” execution-specific API functions
// services/workspace.ts â€” workspace-specific API functions
// services/artifact.ts â€” artifact-specific API functions
// services/notification.ts â€” notification-specific API functions
// services/stream.ts â€” WebSocket/SSE stream handler
```

Rules:
> Terjemahan Indonesia: Aturan:
- Services return promises or observables (for streams).
- Services never modify store directly. They dispatch actions.
- Services never contain UI logic.
- Services never mock. They call real APIs.
- Services normalize all API responses to match store types.

---

## 7. Store Contract

```typescript
// store/conversationSlice.ts
// store/workspaceSlice.ts
// store/executionSlice.ts
// store/artifactSlice.ts
// store/notificationSlice.ts
// store/settingsSlice.ts
```

Rules:
> Terjemahan Indonesia: Aturan:
- Each slice is a single Zustand store.
- State is normalized by ID.
- No nested arrays of full objects.
- No derived state stored.
- All mutations must have explicit actions.
- Selectors are the only public read interface.
- Slice state is hydrates from backend on app load.

---

## 8. Component Contract

```typescript
// components/ChatBubble/
// components/ProgressCard/
// components/ArtifactCard/
// components/ApprovalDialog/
// components/ExecutionTimeline/
```

Rules:
> Terjemahan Indonesia: Aturan:
- Components receive data via props.
- Components emit events via callbacks (void return).
- Components never import services.
- Components never import other components' internal state.
- Components never contain business logic.
- Components never decide what to render based on domain type.
- Components use design tokens for all visual values.

---

## 9. Feature Layer Contract

```typescript
// features/chat/
// features/workspace/
// features/execution/
// features/artifact/
// features/settings/
// features/notifications/
```

Rules:
> Terjemahan Indonesia: Aturan:
- Features own the logic for their domain.
- Features compose components.
- Features call services.
- Features dispatch store actions.
- Features may contain orchestration logic but never backend decision logic.

---

## 10. What Is Prohibited

The following patterns are explicitly prohibited:
> Terjemahan Indonesia: Following patterns adalah explicitly prohibited:

- Switches on `domain`, `capability`, or `capabilityId` in frontend code
- Inline `if (message.includes(...))` for intent detection
- Local computation of progress, status, or phase
- `setTimeout` / polling for state updates
- Any `mock` or `fake` directory in production source
- Components that import from services
- Store slices that bypass service normalization
- Hardcoded API URLs or env-variable leakage in components
- Any React component larger than 300 lines without a justification comment

---

## 11. Enforcement

Files violating these rules are blocked from merge.
> Terjemahan Indonesia: Files violating these rules adalah blocked dari merge.

Checklist for PR review:
> Terjemahan Indonesia: Checklist untuk PR review:
- [ ] No `switch(capability)` or `switch(domain)` in diff
- [ ] No `if (message.includes(...))` in diff
- [ ] No mock imports in production files
- [ ] No component imports from `services/`
- [ ] No progress calculation outside backend data
- [ ] All API calls go through `services/`
- [ ] All state mutations go through explicit store actions
- [ ] All new components are under 300 lines
