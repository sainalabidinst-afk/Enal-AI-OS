# API Mapping

This document maps every frontend action to a backend API call. No undocumented API calls are allowed.

---

## Chat

| Action | Method | Endpoint | Request | Response |
|--------|--------|----------|---------|----------|
| Send message | POST | `/api/v1/chat` | `{ message, conversationId?, workspaceId? }` | `ChatResponse` |
| Stream message | POST | `/api/v1/chat/stream` | `{ message, conversationId?, workspaceId? }` | `Stream<ChatEvent>` |
| Get history | GET | `/api/v1/conversations/{conversationId}` | — | `{ messages }` |
| Delete conversation | DELETE | `/api/v1/conversations/{conversationId}` | — | `{ deleted }` |

---

## Workspace

| Action | Method | Endpoint | Request | Response |
|--------|--------|----------|---------|----------|
| List workspaces | GET | `/api/v1/workspaces` | — | `Workspace[]` |
| Create workspace | POST | `/api/v1/workspaces` | `{ name, description? }` | `Workspace` |
| Get workspace | GET | `/api/v1/workspaces/{workspaceId}` | — | `Workspace` |
| List files | GET | `/api/v1/workspaces/{workspaceId}/files` | — | `{ workspaceId, files[] }` |
| Get file metadata | GET | `/api/v1/workspaces/{workspaceId}/files/{filename}` | — | `{ workspaceId, filename, path, size, uploadedAt, metadata }` |
| Add file | POST | `/api/v1/workspaces/{workspaceId}/files` | `{ filename, path, size, metadata? }` | `{ workspaceId, filename, path }` |
| Delete file | DELETE | `/api/v1/workspaces/{workspaceId}/files/{filename}` | — | `{ workspaceId, filename, deleted }` |
| Set memory | POST | `/api/v1/workspaces/{workspaceId}/memory` | `{ key, value }` | `{ workspaceId, key }` |
| Get memory | GET | `/api/v1/workspaces/{workspaceId}/memory/{key}` | — | `{ workspaceId, key, value }` |
| Delete workspace | DELETE | `/api/v1/workspaces/{workspaceId}` | — | `{ deleted }` |

---

## Execution

| Action | Method | Endpoint | Request | Response |
|--------|--------|----------|---------|----------|
| Create execution | POST | `/api/v1/executions` | `{ goal, conversationId?, workspaceId? }` | `ExecutionSession` |
| Get execution | GET | `/api/v1/executions/{executionId}` | — | `ExecutionSession` |
| List executions | GET | `/api/v1/executions` | `workspaceId?` | `ExecutionSession[]` |
| Add phase | POST | `/api/v1/executions/{executionId}/phases` | `{ name }` | `ExecutionPhase` |
| Update phase | PATCH | `/api/v1/executions/{executionId}/phases/{phaseId}` | `{ status, progress? }` | `ExecutionPhase` |
| Update progress | POST | `/api/v1/executions/{executionId}/progress` | `{ progress, etaSeconds? }` | `{ progress, etaSeconds }` |
| Add log | POST | `/api/v1/executions/{executionId}/logs` | `{ message, level?, metadata? }` | `LogEntry` |
| Get logs | GET | `/api/v1/executions/{executionId}/logs` | — | `{ logs }` |
| Cancel execution | POST | `/api/v1/executions/{executionId}/cancel` | — | `{ status, executionId }` |
| Delete execution | DELETE | `/api/v1/executions/{executionId}` | — | `{ deleted }` |
| Run execution | POST | `/api/v1/executions/run` | `{ goal, workspaceId, conversationId? }` | `{ execution, artifacts }` |

---

## Artifact

| Action | Method | Endpoint | Request | Response |
|--------|--------|----------|---------|----------|
| List artifacts | GET | `/api/v1/artifacts` | `workspaceId?`, `artifactType?` | `Artifact[]` |
| Create artifact | POST | `/api/v1/artifacts` | `{ workspaceId, name, type, description?, content?, path?, metadata? }` | `Artifact` |
| Get artifact | GET | `/api/v1/artifacts/{artifactId}` | — | `Artifact` |
| Get version | GET | `/api/v1/artifacts/{artifactId}/versions/{version}` | — | `ArtifactVersion` |
| Add version | POST | `/api/v1/artifacts/{artifactId}/versions` | `{ content?, path?, metadata? }` | `Artifact` |
| Restore version | POST | `/api/v1/artifacts/{artifactId}/restore/{version}` | — | `Artifact` |
| Get execution artifacts | GET | `/api/v1/executions/{executionId}/artifacts` | — | `ExecutionArtifact[]` |
| Delete artifact | DELETE | `/api/v1/artifacts/{artifactId}` | — | `{ deleted }` |

---

## Capability

| Action | Method | Endpoint | Request | Response |
|--------|--------|----------|---------|----------|
| List capabilities | GET | `/api/v1/capabilities` | — | `{ capabilities, domains }` |
| Get capability | GET | `/api/v1/capabilities/{capabilityId}` | — | `CapabilityDetail` |

---

## Model

| Action | Method | Endpoint | Request | Response |
|--------|--------|----------|---------|----------|
| List providers | GET | `/api/v1/models/providers` | — | `ModelProviders` |
| Health check | GET | `/api/v1/models/health` | `provider?` | `ProviderHealth` |
| Route model | POST | `/api/v1/models/route` | `{ taskType, capability, context? }` | `ModelRoute` |

---

## Notification

| Action | Method | Endpoint | Request | Response |
|--------|--------|----------|---------|----------|
| Get notifications | GET | `/api/v1/notifications/{recipient}` | `limit?` | `{ notifications }` |
| Mark as read | PATCH | `/api/v1/notifications/{recipient}/read/{notificationId}` | — | `{ read }` |

---

## Streaming Events

WebSocket/SSE stream from `/api/v1/chat/stream`:

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
