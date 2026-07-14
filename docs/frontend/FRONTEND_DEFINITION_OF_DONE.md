# Frontend Definition of Done

**Status:** Frozen  
**Effective:** 2026-07-11  
**Owner:** Chief Product Officer  
**Purpose:** Feature-level checklist to verify frontend work is complete. A feature is not done until every checkbox is checked.

---

## Global Requirements (apply to all features)

- [ ] All UI uses design tokens (`--color-*`, `--font-size-*`, `--space-*`, `--radius-*`, `--shadow-*`). No hardcoded colors, sizes, or typography.
- [ ] No `switch(capability)`, `switch(domain)`, or `switch(capabilityId)` anywhere in the diff.
- [ ] No `if (message.includes(...))` or similar intent detection in the diff.
- [ ] No mock data files imported by production components.
- [ ] No component imports from `services/`.
- [ ] All API calls go through `src/services/`.
- [ ] All state mutations go through explicit store actions.
- [ ] Component max 300 lines (with justification comment if exceeded).
- [ ] Error states are actionable (no "Something went wrong" without recovery action).
- [ ] Mobile layout tested at 320px width.
- [ ] Accessibility: keyboard navigable, focus rings, ARIA labels.
- [ ] Unit test for each component (snapshot or interaction test).
- [ ] Integration test for each feature (at least one happy path).
- [ ] Lint passes (`npm run lint`).
- [ ] Typecheck passes (`npm run typecheck`).
- [ ] No console.error, console.warn, or console.log in committed code.

---

## Chat Feature

### Message Display
- [ ] Messages render from backend state only.
- [ ] User messages and AI messages are visually distinct.
- [ ] Markdown is rendered (headings, lists, bold, italic, links).
- [ ] Code blocks render with syntax highlighting.
- [ ] Code blocks have a copy button.
- [ ] Images render inline when the backend returns them.
- [ ] File attachments display as cards with filename and size.
- [ ] Timestamps display in conversation order.
- [ ] Empty state shows a prompt before the first message.

### Sending Messages
- [ ] User types a goal in the prompt box.
- [ ] Enter or Send button dispatches the message to backend (POST `/api/v1/chat`).
- [ ] Sending a message clears the prompt box.
- [ ] Sending is disabled during streaming.
- [ ] Network errors show an inline error message with retry action.
- [ ] 429 errors show a countdown and auto-retry.

### Streaming
- [ ] SSE/WebSocket connection opens on `POST /api/v1/chat/stream`.
- [ ] Tokens stream into the message bubble progressively.
- [ ] Streaming indicator (pulsing animation) is visible during stream.
- [ ] Stream events update the store via a single stream handler.
- [ ] No component subscribes to the raw stream.
- [ ] Connection drops trigger a "Reconnecting..." indicator.
- [ ] Stream completion triggers a final `addMessage()` action.
- [ ] Stream errors trigger `setError()` state.

### Execution Visualization
- [ ] `execution_started` event renders a ProgressCard immediately.
- [ ] `phase` events update the ProgressCard with current phase name.
- [ ] `progress` events update the progress bar (0-100).
- [ ] `log` events render inline in the ProgressCard (collapsible).
- [ ] `artifact` events render ArtifactCards inline in the conversation.
- [ ] `execution_complete` event marks the ProgressCard as completed.
- [ ] `error` event shows an error state with retry action.

### Retry and Actions
- [ ] Failed messages show a retry button.
- [ ] Retry re-sends the same message via the API.
- [ ] Approval-required actions show an ApprovalDialog before execution.
- [ ] Approved/rejected state is sent to backend.

---

## Workspace Feature

### Auto Creation
- [ ] First chat interaction automatically creates a workspace (POST `/api/v1/workspaces`).
- [ ] Workspace is created before the stream starts.
- [ ] Workspace ID is sent with every chat message and execution request.

### Workspace Sidebar
- [ ] Sidebar shows list of workspaces (GET `/api/v1/workspaces`).
- [ ] Sidebar shows current workspace highlighted.
- [ ] Switching workspaces persists conversation state.
- [ ] Sidebar has a "New Workspace" button (POST `/api/v1/workspaces`).

### Workspace Detail
- [ ] Workspace page shows files (from backend, not local computation).
- [ ] Workspace page shows memory keys (from backend).
- [ ] Files can be uploaded via POST `/api/v1/workspaces/{id}/files`.
- [ ] Memory can be set via POST `/api/v1/workspaces/{id}/memory`.
- [ ] Workspace can be renamed (PATCH `/api/v1/workspaces/{id}`).
- [ ] Workspace can be deleted (DELETE `/api/v1/workspaces/{id}`).

### Workspace History
- [ ] Workspace shows conversation history (GET `/api/v1/conversations/{id}`).
- [ ] Workspace shows execution history (GET `/api/v1/executions?workspaceId={id}`).
- [ ] Workspace shows artifact list (GET `/api/v1/artifacts?workspaceId={id}`).

---

## Execution Feature

### Execution List
- [ ] Executions display in Execution History screen (GET `/api/v1/executions`).
- [ ] Each execution shows status, goal, start time, and artifact count.
- [ ] Status badge color maps to execution status (idle, running, paused, completed, failed).
- [ ] Empty state shows when no executions exist.

### Execution Progress
- [ ] Running execution shows a real-time progress bar.
- [ ] Progress bar percentage comes from backend (field `progress`).
- [ ] Current phase name is displayed (field `phase`).
- [ ] ETA is shown when provided (`etaSeconds`).
- [ ] Logs are collapsible and colored by level (info, warning, error).

### Execution Actions
- [ ] Cancel button is visible for running executions.
- [ ] Cancel calls POST `/api/v1/executions/{id}/cancel`.
- [ ] Cancel triggers a confirmation dialog (irreversible action).
- [ ] Execution resumes automatically after page refresh (hydrated from backend).

### Execution Detail
- [ ] Execution detail view shows complete phase timeline.
- [ ] Execution artifacts are linked from the execution view.
- [ ] Execution errors show with stack trace (if backend provides it).

---

## Artifact Feature

### Artifact List
- [ ] Artifacts display in Artifact Viewer (GET `/api/v1/artifacts`).
- [ ] Each artifact shows name, type, description, and creation date.
- [ ] Artifacts are grouped by workspace.
- [ ] Empty state shows when no artifacts exist.

### Artifact Preview
- [ ] Artifact content renders based on type (code, config, document, image).
- [ ] Code artifacts render with syntax highlighting.
- [ ] Binary artifacts (images, PDFs) render in an appropriate viewer.
- [ ] Large artifacts show a warning or truncated view with "View full" option.

### Artifact Actions
- [ ] Download button triggers GET artifact blob.
- [ ] Compare button opens a diff view between the current and previous version.
- [ ] Restore button (revert to previous version) calls POST `/api/v1/artifacts/{id}/restore/{version}`.
- [ ] Restore triggers ApprovalDialog before applying.

### Artifact Versions
- [ ] Version selector allows browsing artifact history.
- [ ] Each version shows author, timestamp, and description.
- [ ] Version diff highlights changes.

---

## Approval Dialog

- [ ] ApprovalDialog component renders for all irreversible actions.
- [ ] Irreversible actions: workspace delete, artifact restore, execution cancel.
- [ ] Dialog shows what will happen.
- [ ] Cancel button dismisses dialog without side effects.
- [ ] Approve button sends the actual API call (not a mock).
- [ ] Rejected actions are logged (not executed).
- [ ] Loading state while approval is pending (if API is slow).
- [ ] Error state if API call fails after approval.

---

## Settings Feature

### Model Selection
- [ ] Model providers load from GET `/api/v1/models/providers`.
- [ ] Model preference updates via PATCH `/api/v1/models/route`.
- [ ] Model selection is saved to backend, not localStorage alone.
- [ ] Model preference is respected in subsequent chat requests.

### Theme
- [ ] Theme toggle switches between light, dark, and system preference.
- [ ] Theme persists to localStorage.
- [ ] Theme applies instantly without page reload.

### Notifications
- [ ] Notification settings (enable/disable) persist to backend.
- [ ] Notifications load from GET `/api/v1/notifications/{recipient}`.
- [ ] Notifications render as toasts in the UI.

### API Keys
- [ ] API key fields are masked.
- [ ] API keys are saved to backend via POST `/api/v1/models/route` (or appropriate endpoint).
- [ ] API key errors surface as actionable messages.

---

## Capability Discovery Feature

- [ ] Capability list loads from GET `/api/v1/capabilities`.
- [ ] Backend returns available capabilities and domains.
- [ ] Frontend renders capabilities as a list only.
- [ ] Frontend never filters or reorders based on domain logic.
- [ ] Capability detail loads from GET `/api/v1/capabilities/{id}`.
- [ ] Selection of a capability sends a goal to the chat (not a direct execution).

---

## Error Handling (Global)

- [ ] Network error: "Connection lost. Retrying..." with auto-retry.
- [ ] 400: inline validation error near the field.
- [ ] 401: redirect to Settings or login flow.
- [ ] 403: "Permission denied" message.
- [ ] 404: "Not found" message with recovery action.
- [ ] 429: "Too many requests. Retrying in Xs" with countdown.
- [ ] 500: "Something went wrong. Please try again." with retry button.
- [ ] Execution failed: error message with retry option.
- [ ] Workspace not found: offer to create new workspace.
- [ ] Artifact not found: show placeholder "Artifact no longer available."

---

## Non-Functional Requirements

- [ ] First meaningful paint < 3s on 3G.
- [ ] Chat message render < 100ms after stream token.
- [ ] Stream reconnection < 2s after network recovery.
- [ ] No jank during scroll in conversation with 1000+ messages.
- [ ] Workspace switch < 500ms.
- [ ] No console errors in production build.
- [ ] Lighthouse accessibility score > 90.
- [ ] E2E tests cover: send message, workspace switch, artifact download, approval flow.

---

## Definition of Done Summary

A feature is DONE when:
1. All checkboxes in this document are checked.
2. The feature runs against real backend APIs.
3. No mock data is used in production code.
4. Lint and typecheck pass.
5. No prohibited patterns are found in the diff.
6. The feature works on mobile (320px).
7. A reviewer from the frontend team has signed off.

All checkboxes unchecked at start of sprint. All checkboxes checked at PR merge.
