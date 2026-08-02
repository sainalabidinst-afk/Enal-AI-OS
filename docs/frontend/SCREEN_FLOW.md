<!-- BILINGUAL_DOCS_START -->
## Bahasa Indonesia / English

### Ringkasan / Summary
Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.
> Terjemahan Indonesia: Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.

- Bahasa Indonesia: konten utama tetap dipertahankan dalam dokumen asli, dan bagian ini memberi konteks ringkas dalam bahasa Indonesia.
- English: the main content remains in the original document, and this section provides a concise bilingual context for international readers.

### Informasi Dokumen / Document Info
- File: `docs/frontend/SCREEN_FLOW.md`
- Judul: Screen Flow
- Status: bilingual header added

<!-- BILINGUAL_DOCS_END -->

# Screen Flow

<!-- DOCUMENT_METADATA_START -->
**Owner:** Documentation Team
**Canonical Owner:** Documentation Governance Lead
**Last Verified:** 2026-08-02
**Version:** 1.0.0
**Status:** Active
**SSOT:** Frontend documentation for SCREEN_FLOW
<!-- DOCUMENT_METADATA_END -->

This document defines the user flow across all v1 screens. It is the reference for navigation, routing, and screen transitions.
> Terjemahan Indonesia: Ini dokumen defines user flow across all v1 screens. It adalah reference untuk navigation, routing, dan screen transitions.

---

## Screen Map

```
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚  WorkspaceSidebar (collapsible)         â”‚
â”‚  - Workspace list                       â”‚
â”‚  - Execution history link               â”‚
â”‚  - Settings link                        â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                    â”‚
                    â–¼
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚  Main Layout                            â”‚
â”‚  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”    â”‚
â”‚  â”‚                                  â”‚    â”‚
â”‚  â”‚  Screen Content                  â”‚    â”‚
â”‚  â”‚                                  â”‚    â”‚
â”‚  â”‚                                  â”‚    â”‚
â”‚  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜    â”‚
â”‚                                          â”‚
â”‚  [persistent: NotificationToast]       â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
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
- User switches Workspace â†’ Workspace screen.
- User clicks Execution History â†’ Execution History screen.
- User clicks Settings â†’ Settings screen.

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
- User clicks artifact â†’ Artifact Viewer.
- User clicks execution â†’ Execution History detail.
- User clicks back â†’ Chat.

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
- User clicks back â†’ previous screen.
- User closes viewer â†’ back to Chat or Workspace.

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
> Terjemahan Indonesia: What akan change. Risk level. Rollback availability. Test results (if applicable).
3. User clicks Approve or Reject.
4. If approved, execution continues.
5. If rejected, execution stops or asks for refinement.

**Exit points:**
- Approve â†’ execution continues.
- Reject â†’ execution stops, returns to Chat.

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
- User clicks back or close â†’ returns to previous screen.

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
- User clicks back â†’ Chat.
- User starts conversation â†’ Chat.

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
> Terjemahan Indonesia: Goal status Progress Duration Artifact count
3. User clicks execution â†’ detail view.
4. Detail view shows:
   - Full execution timeline
   - Phase breakdown
   - Logs
   - Artifacts
   - Retry/re-run option
> Terjemahan Indonesia: Timeline eksekusi penuh Perincian fase Log Artefak Opsi coba lagi/jalankan ulang

**Exit points:**
- User clicks back â†’ previous screen.
- User clicks execution â†’ Execution detail.

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
| Chat â†’ Workspace | User clicks workspace | Slide |
| Chat â†’ Execution History | User clicks history | Slide |
| Chat â†’ Artifact Viewer | User clicks artifact | Slide |
| Any â†’ Approval Dialog | Execution needs approval | Fade |
| Any â†’ Settings | User clicks settings | Slide |
| Any â†’ Chat | User clicks back | Slide reverse |

Animations must be subtle and fast (150-200ms). No elaborate transitions.
> Terjemahan Indonesia: Animations must menjadi subtle dan fast (150-200ms). No elaborate transitions.
