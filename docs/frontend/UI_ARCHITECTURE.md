# Frontend UI Architecture

**Status:** Frozen  
**Effective:** 2026-07-11  
**Owner:** Chief Product Officer  
**Purpose:** Defines the non-negotiable architectural rules and flows for frontend implementation. No React code may be written before this document is approved.

---

## 1. Frontend Architecture Rules

These rules are non-negotiable. Any code that violates them is a defect.

### Rule 1 — Frontend Never Thinks

The frontend must never make a decision that belongs to the backend.

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

### Rule 2 — Frontend Never Plans

The frontend must never create:
- tasks
- execution graphs
- schedulers
- capability assignments
- plans of any kind

All of these originate from the backend.

### Rule 3 — Backend is Source of Truth

For every piece of application state, there is one source of truth — the backend.

The frontend must never compute derived state that the backend already sends.

Example — progress:
```json
{
  "phase": "Security Analysis",
  "progress": 65
}
```

Backend sends this. Frontend displays this. No local computation.

### Rule 4 — UI = Projection

The frontend is a projection of backend state. All state originates from backend mutations.

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

### Rule 5 — Zero Mock Logic

Mock data is not allowed in any production screen once the backend is connected.

Forbidden:
- `fakeExecution()`
- `fakeArtifact()`
- `dummyHistory()`
- Any hardcoded fixtures in screens or features

The Developer Preview must use real backend APIs. Mock data is only acceptable in isolated local development contexts that are never shipped.

### Rule 6 — Stateless Components

Components should be as stateless as possible.

```typescript
// Correct
<ProgressCard phase="Security Analysis" progress={65} />

// Incorrect (contains business logic)
<ProgressCard data={execution} onPhaseUpdate={...} />
```

Components receive data via props and emit events via callbacks. They do not own business logic.

### Rule 7 — UI Does Not Know Capability

The frontend must not have domain-specific logic such as:

```typescript
switch (domain) {
  case "network":
  case "trading":
  case "research":
}
```

The frontend only knows these concepts:
- Execution
- Artifact
- Conversation
- Notification

Domains and Capability Packs are backend concepts and are never exposed to the UI layer.

---

## 2. Data Flow

The canonical path for all data in the frontend:

```
Backend
  ↓
API (REST / WebSocket / SSE)
  ↓
Service Layer (services/)
  ↓
Store (Zustand slices)
  ↓
Selector (derive UI data)
  ↓
Component (dumb, props-only)
  ↓
User
```

Rules:
- Components never call the API directly.
- Components never call services directly.
- Components subscribe to store selectors only.
- Services normalize and validate API responses before storing.
- The store is the single gateway between services and components.

---

## 3. Event Flow

The canonical path for all user-triggered events:

```
User
  ↓
UI (click, input, gesture)
  ↓
API call (via service)
  ↓
Backend
  ↓
Streaming response (SSE / WebSocket)
  ↓
Store update (via stream handler)
  ↓
UI re-render
```

Rules:
- API calls happen immediately — no intermediate "waiting" states before the first API call.
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

---

## 5. Streaming Contract

Backend uses Server-Sent Events (SSE) or WebSocket for all real-time updates.

All stream events must be handled by a single stream middleware that updates the store.

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

---

## 6. Service Layer Contract

All backend communication happens through `src/services/`.

```typescript
// services/api.ts — all HTTP calls
// services/chat.ts — chat-specific API functions
// services/execution.ts — execution-specific API functions
// services/workspace.ts — workspace-specific API functions
// services/artifact.ts — artifact-specific API functions
// services/notification.ts — notification-specific API functions
// services/stream.ts — WebSocket/SSE stream handler
```

Rules:
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
- Features own the logic for their domain.
- Features compose components.
- Features call services.
- Features dispatch store actions.
- Features may contain orchestration logic but never backend decision logic.

---

## 10. What Is Prohibited

The following patterns are explicitly prohibited:

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

Checklist for PR review:
- [ ] No `switch(capability)` or `switch(domain)` in diff
- [ ] No `if (message.includes(...))` in diff
- [ ] No mock imports in production files
- [ ] No component imports from `services/`
- [ ] No progress calculation outside backend data
- [ ] All API calls go through `services/`
- [ ] All state mutations go through explicit store actions
- [ ] All new components are under 300 lines
