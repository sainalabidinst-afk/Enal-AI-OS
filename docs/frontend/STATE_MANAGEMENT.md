# Manajemen Negara

<!-- DOCUMENT_METADATA_START -->
**Pemilik:** Tim Dokumentasi
**Pemilik Canonical:** Pimpinan Tata Kelola Dokumentasi
**Diverifikasi Terakhir:** 08-02-2026
**Versi:** 1.0.0
**Status:** Aktif
**SSOT:** Dokumentasi frontend untuk STATE_MANAGEMENT
<!-- DOCUMENT_METADATA_END -->

Dokumen ini mendefinisikan arsitektur state frontend v1. Tidak ada pola manajemen negara bagian lain yang diizinkan.

---

## Irisan Negara

### 1. Sepotong Percakapan

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

### 2. Irisan Ruang Kerja

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

### 3. Irisan Eksekusi

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

### 4. Artefak Irisan

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

### 5. Pemberitahuan Irisan

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

### 6. Pengaturan Irisan

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

## Negara Bagian Aturan

1. Semua keadaan irisan dinormalisasi. Tidak ada susunan objek penempatannya berdasarkan ID.
2. Semua penyembuhan keadaan melalui aksi yang terdefinisi.
3. Tidak ada status turunan yang disimpan. Turunkan data di penyeleksi.
4. Status disimpan ke backend melalui panggilan API pada setiap pengobatan.
5. State bertahan setelah refresh browser dengan hydrating dari API backend.
6. Preferensi UI (tema, model) dapat disimpan ke localStorage.
7. Tidak ada komponen lokal untuk data bersama. Gunakan Zustand/Konteks.

---

## Penyeleksian

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
