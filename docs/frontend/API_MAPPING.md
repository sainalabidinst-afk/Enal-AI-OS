<!-- BILINGUAL_DOCS_START -->
## Bahasa Indonesia / English

### Ringkasan / Summary
Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.
> Terjemahan Indonesia: Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.

- Bahasa Indonesia: konten utama tetap dipertahankan dalam dokumen asli, dan bagian ini memberi konteks ringkas dalam bahasa Indonesia.
- English: the main content remains in the original document, and this section provides a concise bilingual context for international readers.

### Informasi Dokumen / Document Info
- File: `docs/frontend/API_MAPPING.md`
- Judul: Api Mapping
- Status: bilingual header added

<!-- BILINGUAL_DOCS_END -->

# API Mapping

<!-- DOCUMENT_METADATA_START -->
**Owner:** Documentation Team
**Canonical Owner:** Documentation Governance Lead
**Last Verified:** 2026-08-02
**Version:** 1.0.0
**Status:** Active
**SSOT:** Frontend documentation for API_MAPPING
<!-- DOCUMENT_METADATA_END -->

This document maps every frontend action to a backend API call. No undocumented API calls are allowed.
> Terjemahan Indonesia: Ini dokumen maps every frontend action untuk sebuah backend API call. No undocumented API calls adalah allowed.

---

## Chat

| Action | Method | Endpoint | Request | Response |
|--------|--------|----------|---------|----------|
| Send message | POST | `/api/v1/chat` | `{ message, conversationId?, workspaceId? }` | `ChatResponse` |
| Stream message | POST | `/api/v1/chat/stream` | `{ message, conversationId?, workspaceId? }` | `Stream<ChatEvent>` |
| Get history | GET | `/api/v1/conversations/{conversationId}` | â€” | `{ messages }` |
| Delete conversation | DELETE | `/api/v1/conversations/{conversationId}` | â€” | `{ deleted }` |

---

## Workspace

| Action | Method | Endpoint | Request | Response |
|--------|--------|----------|---------|----------|
| List workspaces | GET | `/api/v1/workspaces` | â€” | `Workspace[]` |
| Create workspace | POST | `/api/v1/workspaces` | `{ name, description? }` | `Workspace` |
| Get workspace | GET | `/api/v1/workspaces/{workspaceId}` | â€” | `Workspace` |
| List files | GET | `/api/v1/workspaces/{workspaceId}/files` | â€” | `{ workspaceId, files[] }` |
| Get file metadata | GET | `/api/v1/workspaces/{workspaceId}/files/{filename}` | â€” | `{ workspaceId, filename, path, size, uploadedAt, metadata }` |
| Add file | POST | `/api/v1/workspaces/{workspaceId}/files` | `{ filename, path, size, metadata? }` | `{ workspaceId, filename, path }` |
| Delete file | DELETE | `/api/v1/workspaces/{workspaceId}/files/{filename}` | â€” | `{ workspaceId, filename, deleted }` |
| Set memory | POST | `/api/v1/workspaces/{workspaceId}/memory` | `{ key, value }` | `{ workspaceId, key }` |
| Get memory | GET | `/api/v1/workspaces/{workspaceId}/memory/{key}` | â€” | `{ workspaceId, key, value }` |
| Delete workspace | DELETE | `/api/v1/workspaces/{workspaceId}` | â€” | `{ deleted }` |

---

## Execution

| Action | Method | Endpoint | Request | Response |
|--------|--------|----------|---------|----------|
| Create execution | POST | `/api/v1/executions` | `{ goal, conversationId?, workspaceId? }` | `ExecutionSession` |
| Get execution | GET | `/api/v1/executions/{executionId}` | â€” | `ExecutionSession` |
| List executions | GET | `/api/v1/executions` | `workspaceId?` | `ExecutionSession[]` |
| Add phase | POST | `/api/v1/executions/{executionId}/phases` | `{ name }` | `ExecutionPhase` |
| Update phase | PATCH | `/api/v1/executions/{executionId}/phases/{phaseId}` | `{ status, progress? }` | `ExecutionPhase` |
| Update progress | POST | `/api/v1/executions/{executionId}/progress` | `{ progress, etaSeconds? }` | `{ progress, etaSeconds }` |
| Add log | POST | `/api/v1/executions/{executionId}/logs` | `{ message, level?, metadata? }` | `LogEntry` |
| Get logs | GET | `/api/v1/executions/{executionId}/logs` | â€” | `{ logs }` |
| Cancel execution | POST | `/api/v1/executions/{executionId}/cancel` | â€” | `{ status, executionId }` |
| Delete execution | DELETE | `/api/v1/executions/{executionId}` | â€” | `{ deleted }` |
| Run execution | POST | `/api/v1/executions/run` | `{ goal, workspaceId, conversationId? }` | `{ execution, artifacts }` |

---

## Artifact

| Action | Method | Endpoint | Request | Response |
|--------|--------|----------|---------|----------|
| List artifacts | GET | `/api/v1/artifacts` | `workspaceId?`, `artifactType?` | `Artifact[]` |
| Create artifact | POST | `/api/v1/artifacts` | `{ workspaceId, name, type, description?, content?, path?, metadata? }` | `Artifact` |
| Get artifact | GET | `/api/v1/artifacts/{artifactId}` | â€” | `Artifact` |
| Get version | GET | `/api/v1/artifacts/{artifactId}/versions/{version}` | â€” | `ArtifactVersion` |
| Add version | POST | `/api/v1/artifacts/{artifactId}/versions` | `{ content?, path?, metadata? }` | `Artifact` |
| Restore version | POST | `/api/v1/artifacts/{artifactId}/restore/{version}` | â€” | `Artifact` |
| Get execution artifacts | GET | `/api/v1/executions/{executionId}/artifacts` | â€” | `ExecutionArtifact[]` |
| Delete artifact | DELETE | `/api/v1/artifacts/{artifactId}` | â€” | `{ deleted }` |

---

## Capability

| Action | Method | Endpoint | Request | Response |
|--------|--------|----------|---------|----------|
| List capabilities | GET | `/api/v1/capabilities` | â€” | `{ capabilities, domains }` |
| Get capability | GET | `/api/v1/capabilities/{capabilityId}` | â€” | `CapabilityDetail` |

---

## Model

| Action | Method | Endpoint | Request | Response |
|--------|--------|----------|---------|----------|
| List providers | GET | `/api/v1/models/providers` | â€” | `ModelProviders` |
| Health check | GET | `/api/v1/models/health` | `provider?` | `ProviderHealth` |
| Route model | POST | `/api/v1/models/route` | `{ taskType, capability, context? }` | `ModelRoute` |

---

## Notification

| Action | Method | Endpoint | Request | Response |
|--------|--------|----------|---------|----------|
| Get notifications | GET | `/api/v1/notifications/{recipient}` | `limit?` | `{ notifications }` |
| Mark as read | PATCH | `/api/v1/notifications/{recipient}/read/{notificationId}` | â€” | `{ read }` |

---

## Streaming Events

WebSocket/SSE stream from `/api/v1/chat/stream`:
> Terjemahan Indonesia: WebSocket/SSE stream dari /API/v1/chat/stream:

| Event Type | Payload |
|------------|---------|
| `final` | `{ type: 'final', message, conversationId, domain, intent }` |
| `execution_started` | `{ type: 'execution_started', executionId, goal }` |
| `phase` | `{ type: 'phase', phaseId, name, status }` |
| `task` | `{ type: 'task', taskId, name, status }` |
| `log` | `{ type: 'log', level, message }` |
| `artifact` | `{ type: 'artifact', artifactId, name, artifactType }` |
| `progress` | `{ type: 'progress', progress, etaSeconds? }` |
| `execution_complete` | `{ type: 'execution_complete', executionId, progress }` |
| `error` | `{ type: 'error', message }` |
