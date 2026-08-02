<!-- BILINGUAL_DOCS_START -->
## Bahasa Indonesia / English

### Ringkasan / Summary
Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.
> Terjemahan Indonesia: Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.

- Bahasa Indonesia: konten utama tetap dipertahankan dalam dokumen asli, dan bagian ini memberi konteks ringkas dalam bahasa Indonesia.
- English: the main content remains in the original document, and this section provides a concise bilingual context for international readers.

### Informasi Dokumen / Document Info
- File: `docs/frontend/COMPONENT_LIBRARY.md`
- Judul: Component Library
- Status: bilingual header added

<!-- BILINGUAL_DOCS_END -->

# Component Library

<!-- DOCUMENT_METADATA_START -->
**Owner:** Documentation Team
**Canonical Owner:** Documentation Governance Lead
**Last Verified:** 2026-08-02
**Version:** 1.0.0
**Status:** Active
**SSOT:** Frontend documentation for COMPONENT_LIBRARY
<!-- DOCUMENT_METADATA_END -->

This document defines the allowed v1 component inventory. No other components may be created without a Product Review.
> Terjemahan Indonesia: Ini dokumen defines allowed v1 component inventory. No other components may menjadi created without sebuah Product Review.

---

## 1. ChatWindow

**Purpose:** Main conversation container.  
**Props:**
- `conversationId: string`
- `messages: Message[]`
- `onSend: (message: string) => void`
- `streaming: boolean`

**Behavior:**
- Shows conversation history.
- Auto-scrolls to bottom on new message.
- Shows streaming cursor when `streaming=true`.
- Contains PromptBox at bottom.

---

## 2. ChatBubble

**Purpose:** Single message bubble.  
**Props:**
- `role: 'user' | 'assistant' | 'system'`
- `content: string`
- `timestamp: string`
- `artifacts?: Artifact[]`

**Behavior:**
- User messages aligned right.
- Assistant messages aligned left.
- Shows timestamp on hover.
- Renders artifacts as ArtifactCards if present.

---

## 3. PromptBox

**Purpose:** Text input for user goals.  
**Props:**
- `onSubmit: (message: string) => void`
- `disabled: boolean`
- `placeholder: string`

**Behavior:**
- Expands up to 3 lines.
- Submit on Enter (Shift+Enter for newline).
- Disabled during submission.
- Shows send button.

---

## 4. ProgressCard

**Purpose:** Real-time execution progress.  
**Props:**
- `executionId: string`
- `status: ExecutionStatus`
- `progress: number`
- `phases: ExecutionPhase[]`
- `currentPhase: string`

**Behavior:**
- Shows progress bar.
- Shows current phase name.
- Shows completed phases as checkmarks.
- Shows pending phases as empty.
- Collapses to compact bar on mobile.

---

## 5. ArtifactCard

**Purpose:** Single artifact preview.  
**Props:**
- `artifactId: string`
- `name: string`
- `type: string`
- `version: number`
- `onClick: () => void`

**Behavior:**
- Shows artifact type icon.
- Shows name and version.
- Click opens Artifact Viewer.
- Hover shows metadata.

---

## 6. ApprovalDialog

**Purpose:** Confirm or reject irreversible actions.  
**Props:**
- `open: boolean`
- `title: string`
- `description: string`
- `risk: 'low' | 'medium' | 'high'`
- `rollbackAvailable: boolean`
- `testResults?: { passed: number; total: number }`
- `onApprove: () => void`
- `onReject: () => void`

**Behavior:**
- Modal overlay.
- Shows risk level with color.
- Shows rollback status.
- Shows test results if available.
- Approve/Reject buttons are always visible.
- Focus moves to Approve button on open.

---

## 7. ExecutionTimeline

**Purpose:** Visual timeline of execution phases.  
**Props:**
- `phases: ExecutionPhase[]`
- `currentPhaseId?: string`

**Behavior:**
- Shows phases in order.
- Completed phases: green checkmark.
- Running phase: animated progress.
- Pending phases: gray.
- Failed phase: red with error.
- Click phase to see details.

---

## 8. WorkspaceSidebar

**Purpose:** Workspace switcher and navigation.  
**Props:**
- `workspaces: Workspace[]`
- `currentWorkspaceId: string`
- `onSelectWorkspace: (id: string) => void`
- `onNewWorkspace: () => void`

**Behavior:**
- Desktop: fixed left sidebar.
- Mobile: bottom sheet triggered by hamburger.
- Shows workspace name and artifact count.
- Shows "New Workspace" button.
- Shows Execution History link.
- Shows Settings link.

---

## 9. LoadingIndicator

**Purpose:** Loading state.  
**Props:**
- `size?: 'sm' | 'md' | 'lg'`
- `label?: string`

**Behavior:**
- Uses spinner animation.
- Shows label if provided.
- Does NOT cover entire screen unless explicitly requested.
- Accessible: `aria-label="Loading"`.

---

## 10. NotificationToast

**Purpose:** Non-blocking notification.  
**Props:**
- `message: string`
- `type: 'info' | 'success' | 'warning' | 'error'`
- `duration?: number`
- `onDismiss: () => void`

**Behavior:**
- Appears top-right (desktop) or top-center (mobile).
- Auto-dismisses after `duration` (default 5s).
- Slide-in animation.
- Dismiss button always visible.
- Stackable.

---

## Component Rules

1. Components receive data via props. They do not call APIs directly.
2. Components emit events via callbacks. They do not modify state directly.
3. Components are styled with design tokens only.
4. Components are accessible (keyboard navigation, ARIA labels).
5. Components are responsive by default.
