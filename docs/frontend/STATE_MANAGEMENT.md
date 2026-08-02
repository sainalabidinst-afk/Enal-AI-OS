<!-- BILINGUAL_DOCS_START -->
## Bahasa Indonesia / English

### Ringkasan / Summary
Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.
> Terjemahan Indonesia: Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.

- Bahasa Indonesia: konten utama tetap dipertahankan dalam dokumen asli, dan bagian ini memberi konteks ringkas dalam bahasa Indonesia.
- English: the main content remains in the original document, and this section provides a concise bilingual context for international readers.

### Informasi Dokumen / Document Info
- File: `docs/frontend/STATE_MANAGEMENT.md`
- Judul: State Management
- Status: bilingual header added

<!-- BILINGUAL_DOCS_END -->

# State Management

<!-- DOCUMENT_METADATA_START -->
**Owner:** Documentation Team
**Canonical Owner:** Documentation Governance Lead
**Last Verified:** 2026-08-02
**Version:** 1.0.0
**Status:** Active
**SSOT:** Frontend documentation for STATE_MANAGEMENT
<!-- DOCUMENT_METADATA_END -->

This document defines the v1 frontend state architecture. No other state management patterns are allowed.
> Terjemahan Indonesia: Ini dokumen defines v1 frontend state arsitektur. No other state management patterns adalah allowed.

---

## State Slices

### 1. Conversation Slice

```typescript
interface ConversationState {
  messages: Message[];
  conversationId: string | null;
  streaming: boolean;
  error: string | null;
}

// Actions
- setMessages(messages: Message[])
- addMessage(message: Message)
- setStreaming(streaming: boolean)
- setError(error: string | null)
- clearConversation()
```

### 2. Workspace Slice

```typescript
interface WorkspaceState {
  currentWorkspaceId: string | null;
  workspaces: Workspace[];
  files: File[];
  memory: Record<string, any>;
}

// Actions
- setCurrentWorkspace(id: string)
- setWorkspaces(workspaces: Workspace[])
- addFile(file: File)
- setMemory(key: string, value: any)
- removeMemory(key: string)
```

### 3. Execution Slice

```typescript
type ExecutionStatus = 'idle' | 'running' | 'paused' | 'completed' | 'failed';

interface ExecutionState {
  executions: Execution[];
  currentExecutionId: string | null;
  status: ExecutionStatus;
  progress: number;
  phases: ExecutionPhase[];
  logs: LogEntry[];
}

// Actions
- setExecutions(executions: Execution[])
- setCurrentExecution(id: string)
- setStatus(status: ExecutionStatus)
- setProgress(progress: number)
- addPhase(phase: ExecutionPhase)
- updatePhase(phaseId: string, updates: Partial<ExecutionPhase>)
- addLog(log: LogEntry)
- clearExecution()
```

### 4. Artifact Slice

```typescript
interface ArtifactState {
  artifacts: Artifact[];
  currentArtifactId: string | null;
  versions: ArtifactVersion[];
}

// Actions
- setArtifacts(artifacts: Artifact[])
- setCurrentArtifact(id: string)
- setVersions(versions: ArtifactVersion[])
```

### 5. Notification Slice

```typescript
interface NotificationState {
  notifications: Notification[];
  unreadCount: number;
}

// Actions
- addNotification(notification: Notification)
- markAsRead(notificationId: string)
- clearNotifications()
```

### 6. Settings Slice

```typescript
interface SettingsState {
  modelPreference: string;
  theme: 'light' | 'dark' | 'system';
  notificationsEnabled: boolean;
  apiKeys: Record<string, string>;
}

// Actions
- setModelPreference(model: string)
- setTheme(theme: 'light' | 'dark' | 'system')
- setNotificationsEnabled(enabled: boolean)
- setApiKey(provider: string, key: string)
```

---

## State Rules

1. All state slices are normalized. No nested arrays of objects by ID.
2. All state mutations go through defined actions.
3. No derived state is stored. Derive data in selectors.
4. State persists to backend via API calls on every mutation.
5. State survives browser refresh by hydrating from backend APIs.
6. UI preferences (theme, model) may persist to localStorage.
7. No local component state for shared data. Use Zustand/Context.

---

## Selectors

```typescript
// Conversation
const getCurrentMessage = (state) => state.conversation.messages[state.conversation.messages.length - 1];
const isStreaming = (state) => state.conversation.streaming;

// Workspace
const getCurrentWorkspace = (state) => state.workspace.workspaces.find(w => w.id === state.workspace.currentWorkspaceId);

// Execution
const getCurrentExecution = (state) => state.execution.executions.find(e => e.id === state.execution.currentExecutionId);
const getExecutionProgress = (state) => state.execution.progress;

// Artifacts
const getCurrentArtifact = (state) => state.artifact.artifacts.find(a => a.id === state.artifact.currentArtifactId);
```
