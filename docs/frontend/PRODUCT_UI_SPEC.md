# Product UI Specification

**Status:** Frozen  
**Effective:** 2026-07-11  
**Owner:** Chief Product Officer  
**Purpose:** Single source of truth for all frontend work. No UI code may be written before this document is approved.

---

## 1. Product Positioning

Enal AI OS is an **AI Execution Platform**.

Users describe the outcome they want. ECP understands the goal, plans execution, coordinates tasks, verifies results, and delivers a complete outcome—all through a single conversation.

The user sees one AI. The user never sees the machinery underneath.

**Motto:** A stable core. Expert capabilities. One conversation.

---

## 2. Design Principles

These principles are non-negotiable. Any UI element that violates them is a defect.

### Principle 1: One Conversation

The user interface is a single conversation. There is no menu for selecting Capability Pack. There is no dropdown for selecting a Worker. There is no configuration panel for choosing a Model.

The AI does that internally.

### Principle 2: Outcome Over Mechanism

Users describe outcomes, not mechanisms.

User says: "Audit jaringan kantor saya."
User does NOT say: "Jalankan Network Capability."

The UI must never expose internal concepts such as Capability Pack, Worker, Execution Runtime, Task Planner, or Execution Graph to the user.

### Principle 3: Progress Transparency

During long-running tasks, the system must show progress. Progress indication must be coarse-grained and human-readable.

Acceptable:
- "Analyzing configuration..."
- "Generating documentation..."
- "Running tests..."

Not acceptable:
- Generic "Loading..."
- Internal step names like "Stage 3: Execute Subtask 7"

### Principle 4: Approval Before Action

For irreversible actions, the UI must show an explicit approval dialog. AI never applies changes without user approval.

### Principle 5: Artifact First

Every significant output is an Artifact. Artifacts are always visible, versioned, and retrievable.

### Principle 6: Workspace Isolation

Each project is isolated in a Workspace. Conversation, files, memory, tasks, artifacts, and execution history are scoped per Workspace.

### Principle 7: No Mock Data

The frontend must consume backend APIs. Mock data is not allowed in any production screen.

---

## 3. Screen Inventory

The v1 frontend has exactly 7 screens.

| # | Screen | Purpose |
|---|--------|---------|
| 1 | Chat | Primary interface. User types goals, sees AI responses, progress, and artifacts. |
| 2 | Workspace | Project overview: conversation, files, memory, tasks, artifacts, timeline. |
| 3 | Artifact Viewer | View, compare, and restore artifact versions. |
| 4 | Approval Dialog | Confirm or reject irreversible actions. |
| 5 | Settings | Model selection, theme, notifications, API keys. |
| 6 | Capability Discovery | Dynamic list of capabilities from backend. |
| 7 | Execution History | List of executions with status, progress, and artifacts. |

No other screens are allowed in v1.

---

## 4. Component Inventory

These are the only allowed UI components in v1.

| Component | Purpose | Screen(s) |
|-----------|---------|-----------|
| ChatWindow | Main conversation container | Chat |
| ChatBubble | User or AI message bubble | Chat |
| PromptBox | Text input for user goals | Chat |
| ProgressCard | Real-time execution progress | Chat, Workspace |
| ArtifactCard | Single artifact preview | Chat, Workspace, Artifact Viewer |
| ApprovalDialog | Approve/reject action | Chat, Workspace |
| ExecutionTimeline | Visual timeline of execution phases | Workspace, Execution History |
| WorkspaceSidebar | Workspace switcher and navigation | All |
| LoadingIndicator | Loading state | All |
| NotificationToast | Non-blocking notifications | All |

No other components are allowed in v1.

---

## 5. State Management

All application state must flow through these slices:

```
Conversation
  - messages[]
  - conversationId
  - streaming state

Workspace
  - currentWorkspaceId
  - workspaces[]
  - files[]
  - memory{}

Execution
  - executions[]
  - currentExecutionId
  - status: idle | running | paused | completed | failed
  - progress: 0-100
  - phases[]
  - logs[]

Artifact
  - artifacts[]
  - currentArtifactId
  - versions[]

Notification
  - notifications[]
  - unreadCount

Settings
  - modelPreference
  - theme
  - notificationsEnabled
  - apiKeys{}
```

Rules:
- State is normalized.
- No derived state stored.
- All state mutations go through defined actions.
- State persists to backend via APIs.
- State survives browser refresh via backend + localStorage for UI preferences only.

---

## 6. API Mapping

Every screen and component must consume these backend APIs.

| Screen | API | Method | Purpose |
|--------|-----|--------|---------|
| Chat | POST /api/v1/chat | POST | Send message, get response |
| Chat | POST /api/v1/chat/stream | POST | Stream conversation events |
| Workspace | GET /api/v1/workspaces | GET | List workspaces |
| Workspace | POST /api/v1/workspaces | POST | Create workspace |
| Workspace | GET /api/v1/workspaces/{id} | GET | Get workspace detail |
| Workspace | POST /api/v1/workspaces/{id}/files | POST | Upload file |
| Workspace | POST /api/v1/workspaces/{id}/memory | POST | Set memory |
| Workspace | GET /api/v1/workspaces/{id}/memory/{key} | GET | Get memory |
| Artifact | GET /api/v1/artifacts | GET | List artifacts |
| Artifact | POST /api/v1/artifacts | POST | Create artifact |
| Artifact | GET /api/v1/artifacts/{id} | GET | Get artifact |
| Artifact | GET /api/v1/artifacts/{id}/versions/{version} | GET | Get artifact version |
| Artifact | POST /api/v1/artifacts/{id}/restore/{version} | POST | Restore artifact version |
| Execution | POST /api/v1/executions | POST | Create execution |
| Execution | GET /api/v1/executions/{id} | GET | Get execution |
| Execution | POST /api/v1/executions/{id}/progress | POST | Update progress |
| Execution | POST /api/v1/executions/{id}/cancel | POST | Cancel execution |
| Execution | POST /api/v1/executions/run | POST | Run execution end-to-end |
| Execution | GET /api/v1/executions/{id}/logs | GET | Get execution logs |
| Execution | GET /api/v1/executions/{id}/artifacts | GET | Get execution artifacts |
| Settings | GET /api/v1/models/providers | GET | List model providers |
| Settings | POST /api/v1/models/route | POST | Route model |
| Notifications | GET /api/v1/notifications/{recipient} | GET | Get notifications |
| Capability | GET /api/v1/capabilities | GET | List capabilities |
| Capability | GET /api/v1/capabilities/{id} | GET | Get capability detail |

No other API calls are allowed in v1.

---

## 7. Error States

Every API call must handle these error states.

| Error | HTTP Status | UI Behavior |
|-------|-------------|-------------|
| Network error | N/A | Show "Connection lost. Retrying..." |
| 400 Bad Request | 400 | Show inline validation error |
| 401 Unauthorized | 401 | Redirect to settings |
| 403 Forbidden | 403 | Show "Permission denied" |
| 404 Not Found | 404 | Show "Not found" with recovery action |
| 429 Rate Limited | 429 | Show "Too many requests. Retrying in..." |
| 500 Internal Error | 500 | Show "Something went wrong. Please try again." |
| Execution failed | N/A | Show error with retry option |
| Workspace not found | 404 | Create new workspace or allow user to pick existing |
| Artifact not found | 404 | Show placeholder with "Artifact no longer available" |

All errors must be actionable. No generic "Error occurred" messages.

---

## 8. Mobile Layout

The UI must be responsive and work on mobile devices (320px width minimum).

| Breakpoint | Layout |
|------------|--------|
| Desktop (>1024px) | Sidebar + main content + optional artifact panel |
| Tablet (768-1024px) | Collapsible sidebar + main content |
| Mobile (<768px) | Full-screen chat, bottom navigation, slide-out panels |

Mobile rules:
- Chat is always full-screen on mobile.
- Workspace sidebar is a bottom sheet.
- Artifact viewer is a full-screen overlay.
- Approval dialog is a bottom sheet.
- Progress card collapses to a compact bar on mobile.

---

## 9. Design Tokens

All visual values must use these tokens. No hardcoded colors, spacing, or typography.

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

## 10. Frontend Architecture

```
frontend/
src/
├── app/
│   ├── providers/
│   └── router/
├── pages/
│   ├── Chat/
│   ├── Workspace/
│   ├── ArtifactViewer/
│   ├── ApprovalDialog/
│   ├── Settings/
│   ├── CapabilityDiscovery/
│   └── ExecutionHistory/
├── features/
│   ├── chat/
│   ├── workspace/
│   ├── execution/
│   ├── artifact/
│   ├── settings/
│   └── notifications/
├── components/
│   ├── ChatWindow/
│   ├── ChatBubble/
│   ├── PromptBox/
│   ├── ProgressCard/
│   ├── ArtifactCard/
│   ├── ApprovalDialog/
│   ├── ExecutionTimeline/
│   ├── WorkspaceSidebar/
│   ├── LoadingIndicator/
│   └── NotificationToast/
├── layouts/
│   ├── MainLayout/
│   └── MobileLayout/
├── hooks/
├── services/
│   ├── api.ts
│   ├── chat.ts
│   ├── execution.ts
│   ├── workspace.ts
│   ├── artifact.ts
│   └── notification.ts
├── store/
│   ├── conversationSlice.ts
│   ├── workspaceSlice.ts
│   ├── executionSlice.ts
│   ├── artifactSlice.ts
│   ├── notificationSlice.ts
│   └── settingsSlice.ts
├── types/
│   ├── chat.ts
│   ├── execution.ts
│   ├── workspace.ts
│   ├── artifact.ts
│   └── api.ts
└── utils/
```

Principles:
- Feature-based organization, not type-based.
- All API calls go through `services/`.
- All state lives in `store/`.
- Components are dumb. Features own logic.
- No business logic in components.

---

## 11. Definition of Done

Frontend v1 is complete when:

- [ ] User opens app and sees a single chat window.
- [ ] User types a goal and gets a response.
- [ ] Progress is visible during long-running tasks.
- [ ] Artifacts appear automatically.
- [ ] Approval dialog works for irreversible actions.
- [ ] Workspace is created automatically.
- [ ] Execution history is available.
- [ ] Capability Discovery works from the chat.
- [ ] All screens consume real backend APIs.
- [ ] No mock data in production screens.
- [ ] Mobile layout works at 320px width.
- [ ] All components use design tokens.
- [ ] Errors are actionable and user-friendly.
- [ ] No internal architecture terms exposed to user.

---

## 12. What Is Out of Scope

The following are explicitly out of scope for v1 frontend:

- Agent selection UI
- Capability Pack configuration
- Worker configuration
- Model selection UI (except in Settings)
- Execution Graph visualization
- Admin dashboard
- Analytics dashboard
- Plugin management UI
- Advanced theming

These may be added in future versions if validated by real user needs.

---

## 13. Success Criteria

The frontend is successful when a new user can:

1. Open the app and understand what to do without reading documentation.
2. Type a goal in plain language and get a result.
3. See progress while waiting.
4. Find artifacts after execution completes.
5. Approve or reject changes when asked.
6. Return to a previous workspace and continue where they left off.

If any of these fail, the frontend is not ready for Developer Preview.
