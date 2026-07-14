# Error States

This document defines every error state the user can encounter in v1, and how the UI must respond.

---

## Network Errors

| Error | Cause | UI Behavior |
|-------|-------|-------------|
| Connection lost | Backend unreachable | Show banner: "Connection lost. Reconnecting..." |
| Request timeout | Backend slow | Show inline retry: "Request timed out. Retry?" |
| Aborted request | User navigated away | Silent abort. No error shown. |

---

## API Errors

| HTTP Status | Cause | UI Behavior |
|-------------|-------|-------------|
| 400 | Bad request (invalid input) | Show inline error near input field. |
| 401 | Unauthorized (missing/invalid API key) | Redirect to Settings → API Keys. |
| 403 | Forbidden (insufficient permissions) | Show: "Permission denied. Contact admin." |
| 404 | Not found (deleted/missing resource) | Show: "Not found. It may have been deleted." with recovery action. |
| 429 | Rate limited | Show: "Too many requests. Retrying in X seconds." |
| 500 | Internal server error | Show: "Something went wrong. Please try again." with retry button. |
| 503 | Service unavailable | Show: "Service temporarily unavailable. Please try again later." |

---

## Execution Errors

| State | Cause | UI Behavior |
|-------|-------|-------------|
| Execution failed | Unhandled exception in execution | Show error in ProgressCard. Offer retry. |
| Execution cancelled | User cancelled | Show "Execution cancelled." in ProgressCard. |
| Phase failed | One phase failed | Show failed phase in red. Stop execution. |
| Workspace not found | Workspace missing | Create new workspace automatically or prompt user to select. |
| Artifact not found | Artifact deleted | Show placeholder: "Artifact no longer available." |
| Approval rejected | User rejected changes | Show "Changes rejected." Resume previous state. |

---

## Input Validation

| Input | Validation | UI Behavior |
|-------|-----------|-------------|
| Goal input | Empty | Disable Send button. Show hint: "Describe your goal." |
| Workspace name | Empty | Disable Create button. Show hint: "Name is required." |
| API key | Invalid format | Show inline error: "Invalid API key format." |

---

## Fallback States

| Scenario | UI Behavior |
|----------|-------------|
| No conversations yet | Show welcome message with examples. |
| No workspaces yet | Show empty state with "Create your first workspace" CTA. |
| No artifacts yet | Show empty state: "No artifacts yet. Start a conversation to create some." |
| No executions yet | Show empty state: "No executions yet." |
| Capabilities loading | Show skeleton loaders. |
| Stream interrupted | Show reconnection spinner. Resume from last message. |

---

## Error Message Rules

1. **Actionable:** Every error must include a recovery action (retry, go back, try again).
2. **Human-readable:** No stack traces, no internal codes.
3. **Specific:** "Network config invalid" is better than "Something went wrong."
4. **Contextual:** Show error near the relevant UI element, not as a global banner.
5. **Non-blocking:** Errors must not trap the user. Always provide an exit.

---

## Error Logging

- All errors are logged to backend with `conversationId`, `workspaceId`, `executionId`, `userId`.
- Errors are shown to user in simplified form.
- Errors are stored in execution logs for debugging.
