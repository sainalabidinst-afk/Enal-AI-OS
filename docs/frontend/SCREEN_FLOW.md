# Screen Flow

This document defines the user flow across all v1 screens. It is the reference for navigation, routing, and screen transitions.

---

## Screen Map

```
┌─────────────────────────────────────────┐
│  WorkspaceSidebar (collapsible)         │
│  - Workspace list                       │
│  - Execution history link               │
│  - Settings link                        │
└─────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────┐
│  Main Layout                            │
│  ┌─────────────────────────────────┐    │
│  │                                  │    │
│  │  Screen Content                  │    │
│  │                                  │    │
│  │                                  │    │
│  └─────────────────────────────────┘    │
│                                          │
│  [persistent: NotificationToast]       │
└─────────────────────────────────────────┘
```

---

## Screen 1: Chat

**Route:** `/chat`  
**Purpose:** Primary interface. User types goals, sees AI responses, progress, and artifacts.

**Entry points:**
- Default route on app open.
- User clicks "New Chat" or selects a Workspace.

**Flow:**
1. User sees ChatWindow with conversation history (if any).
2. User types goal in PromptBox.
3. User presses Send or Enter.
4. User message appears as ChatBubble.
5. AI response streams in as ChatBubble.
6. If execution starts, ProgressCard appears inline.
7. Artifacts appear as ArtifactCards inline.
8. Approval dialog appears if action requires approval.
9. User approves or rejects.
10. Execution continues or stops.

**Exit points:**
- User switches Workspace → Workspace screen.
- User clicks Execution History → Execution History screen.
- User clicks Settings → Settings screen.

---

## Screen 2: Workspace

**Route:** `/workspace/:workspaceId`  
**Purpose:** Project overview with conversation, files, memory, artifacts, timeline.

**Entry points:**
- User clicks Workspace in sidebar.
- User clicks artifact link from Chat.
- Workspace is auto-created when Chat opens.

**Flow:**
1. User sees Workspace header with name.
2. Tabs: Conversation, Files, Artifacts, Execution, Timeline.
3. Conversation tab shows chat history for this workspace.
4. Files tab shows uploaded files.
5. Artifacts tab shows all artifacts in this workspace.
6. Execution tab shows execution history for this workspace.
7. Timeline tab shows chronological project events.

**Exit points:**
- User clicks artifact → Artifact Viewer.
- User clicks execution → Execution History detail.
- User clicks back → Chat.

---

## Screen 3: Artifact Viewer

**Route:** `/artifact/:artifactId`  
**Purpose:** View, compare, and restore artifact versions.

**Entry points:**
- User clicks ArtifactCard in Chat.
- User clicks artifact in Workspace.
- User clicks artifact in Execution History.

**Flow:**
1. User sees artifact content.
2. Version selector shows available versions.
3. User can compare two versions.
4. User can restore a previous version.
5. User can download/export artifact.

**Exit points:**
- User clicks back → previous screen.
- User closes viewer → back to Chat or Workspace.

---

## Screen 4: Approval Dialog

**Route:** Modal overlay (no route)  
**Purpose:** Confirm or reject irreversible actions.

**Trigger:**
- Execution reaches an approval point.
- AI presents proposed changes with risk assessment.

**Flow:**
1. Modal appears over current screen.
2. User sees:
   - What will change.
   - Risk level.
   - Rollback availability.
   - Test results (if applicable).
3. User clicks Approve or Reject.
4. If approved, execution continues.
5. If rejected, execution stops or asks for refinement.

**Exit points:**
- Approve → execution continues.
- Reject → execution stops, returns to Chat.

---

## Screen 5: Settings

**Route:** `/settings`  
**Purpose:** Configure model, theme, notifications, API keys.

**Entry points:**
- User clicks Settings in sidebar.
- User asks AI "Open settings".

**Flow:**
1. User sees settings form.
2. Sections: Model, Theme, Notifications, API Keys.
3. User changes settings.
4. Settings are saved immediately or on "Save" button.
5. Changes take effect immediately.

**Exit points:**
- User clicks back or close → returns to previous screen.

---

## Screen 6: Capability Discovery

**Route:** Accessible via `/capabilities` or triggered by user question in Chat.  
**Purpose:** Show user what ECP can do.

**Entry points:**
- User asks "Apa yang bisa kamu lakukan?" in Chat.
- User clicks "Discover" in sidebar.

**Flow:**
1. User sees list of Capability Packs.
2. User clicks a capability.
3. AI shows subtasks and examples for that capability.
4. User can click "Try it" to start a conversation with that capability.

**Exit points:**
- User clicks back → Chat.
- User starts conversation → Chat.

---

## Screen 7: Execution History

**Route:** `/executions`  
**Purpose:** List all executions with status, progress, and artifacts.

**Entry points:**
- User clicks Execution History in sidebar.
- User sees execution history in Workspace.

**Flow:**
1. User sees list of executions.
2. Each execution shows:
   - Goal
   - Status
   - Progress
   - Duration
   - Artifact count
3. User clicks execution → detail view.
4. Detail view shows:
   - Full execution timeline
   - Phase breakdown
   - Logs
   - Artifacts
   - Retry/re-run option

**Exit points:**
- User clicks back → previous screen.
- User clicks execution → Execution detail.

---

## Navigation Rules

1. **Primary navigation:** WorkspaceSidebar (desktop) / Bottom nav (mobile).
2. **Secondary navigation:** Breadcrumbs and back buttons.
3. **No deep linking to internal state:** URLs contain identifiers only (workspaceId, executionId, artifactId), not internal state.
4. **No browser back button traps:** Back button always returns to previous logical screen.
5. **No popup windows:** All navigation stays within the single-page app.

---

## Routing Table

| Route | Screen | Requires Auth | Requires Workspace |
|-------|--------|---------------|-------------------|
| `/` | Chat (redirect to `/chat`) | No | No |
| `/chat` | Chat | No | Auto-create |
| `/workspace/:workspaceId` | Workspace | No | Yes |
| `/artifact/:artifactId` | Artifact Viewer | No | No |
| `/executions` | Execution History | No | No |
| `/executions/:executionId` | Execution Detail | No | No |
| `/capabilities` | Capability Discovery | No | No |
| `/settings` | Settings | No | No |

---

## Transition Rules

| Transition | Trigger | Animation |
|------------|---------|-----------|
| Chat → Workspace | User clicks workspace | Slide |
| Chat → Execution History | User clicks history | Slide |
| Chat → Artifact Viewer | User clicks artifact | Slide |
| Any → Approval Dialog | Execution needs approval | Fade |
| Any → Settings | User clicks settings | Slide |
| Any → Chat | User clicks back | Slide reverse |

Animations must be subtle and fast (150-200ms). No elaborate transitions.
