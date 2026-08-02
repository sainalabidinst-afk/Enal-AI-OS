<!-- BILINGUAL_DOCS_START -->
## Bahasa Indonesia / English


### Ringkasan / Summary
Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.
> Terjemahan Indonesia: Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.

- Bahasa Indonesia: konten utama tetap dipertahankan dalam dokumen asli, dan bagian ini memberi konteks ringkas dalam bahasa Indonesia.
- English: the main content remains in the original document, and this section provides a concise bilingual context for international readers.

### Informasi Dokumen / Document Info
- File: `docs/api_reference.md`
- Judul: Api Reference
- Status: bilingual header added

<!-- BILINGUAL_DOCS_END -->

# ECP API Reference

**Status:** Platform RC (2026-07-27) - Runtime: 426 tests passing

## Base URL

```
http://localhost:8000/api/v1
```

## Authentication

All API endpoints require authentication via Bearer token:
> Terjemahan Indonesia: Semua titik akhir API memerlukan autentikasi melalui token Pembawa:

```bash
curl -H "Authorization: Bearer your-api-key" http://localhost:8000/api/v1/health
```

## Endpoints

### Chat

#### POST /chat

Send a message to the AI orchestrator.
> Terjemahan Indonesia: Send sebuah message untuk AI orchestrator.

**Request:**
```json
{
  "message": "Build me a full-stack todo app",
  "conversation_id": "optional-conversation-id",
  "stream": false
}
```

**Response:**
```json
{
  "reply": "I'll build a full-stack todo app for you...",
  "conversation_id": "conv-123",
  "session_id": "orch-1234",
  "artifacts": []
}
```

### Cognitive

#### POST /cognitive/process


Full cognitive pipeline processing.
> Terjemahan Indonesia: Full kognitif jalur processing.

**Request:**
```json
{
  "user_input": "Build an ERP system",
  "project_id": "erp-001"
}
```

**Response:**
```json
{
  "pipeline": ["perception", "memory", "planning", "reasoning", "decision", "reflection", "action"],
  "complexity": "complex",
  "model": "claude-3-5-sonnet-20240620",
  "decision": {...},
  "verification": {...},
  "reflection": {...}
}
```

#### POST /cognitive/decide


Make a decision using decision theory.
> Terjemahan Indonesia: Make sebuah decision using decision theory.

**Request:**
```json
{
  "options": [
    {"id": "opt-1", "description": "Use React", "utility": 0.9, "risk": 0.2, "cost": 0.3, "confidence": 0.8},
    {"id": "opt-2", "description": "Use Vue", "utility": 0.7, "risk": 0.3, "cost": 0.2, "confidence": 0.7}
  ]
}
```

**Response:**
```json
{
  "selected_id": "opt-1",
  "description": "Use React",
  "confidence": 0.8,
  "expected_value": 1.54,
  "reasoning": "Selected based on expected value: 1.54",
  "all_options": [...]
}
```

### Organization

#### POST /organization

Create an organization node.
> Terjemahan Indonesia: Membuat sebuah organization node.

**Request:**
```json
{
  "name": "Backend Team",
  "role": "lead",
  "agent_type": "backend-agent",
  "parent_id": "parent-node-id",
  "capabilities": ["python", "fastapi", "postgresql"]
}
```

#### GET /organization/{node_id}/subtree


Get organization subtree.
> Terjemahan Indonesia: Dapatkan subpohon organisasi.

### Marketplace

#### POST /marketplace/publish


Publish a plugin.
> Terjemahan Indonesia: Publish sebuah plugin.

**Request:**
```json
{
  "plugin_id": "my-plugin",
  "name": "My Plugin",
  "version": "1.0.0",
  "description": "Description",
  "author": "Author Name",
  "category": "tools",
  "tags": ["tool", "custom"]
}
```

#### GET /marketplace/plugins


List available plugins.
> Terjemahan Indonesia: Daftar plugin yang tersedia.

### Studio

#### GET /studio/traces/{trace_id}


Get trace details for debugging.
> Terjemahan Indonesia: Get trace details untuk debugging.

#### GET /studio/metrics

Get observability metrics.
> Terjemahan Indonesia: Dapatkan metrik observabilitas.

#### GET /studio/artifacts/{project_id}


Get artifacts for a project.
> Terjemahan Indonesia: Get artifacts untuk sebuah proyek.

#### GET /studio/graph

Get the knowledge graph.
> Terjemahan Indonesia: Get knowledge graph.

#### GET /studio/memory

Search memory by layer.
> Terjemahan Indonesia: Search memory oleh layer.

#### GET /studio/reputation


Get agent reputation leaderboard.
> Terjemahan Indonesia: Get agen reputation leaderboard.

#### GET /studio/cognitive-services


List available cognitive services.
> Terjemahan Indonesia: List available kognitif services.

#### GET /studio/pipeline-presets


List adaptive pipeline presets.
> Terjemahan Indonesia: List adaptive jalur presets.

#### GET /studio/meta/metrics


Get meta-cognition metrics.
> Terjemahan Indonesia: Dapatkan metrik meta-kognisi.

---

### Chat Streaming

#### POST /stream

Send a message and receive Server-Sent Events (SSE) stream via query parameter.
> Terjemahan Indonesia: Send sebuah message dan receive Server-Sent Events (SSE) stream via query parameter.

Use `POST /api/v1/chat` with `stream: true` or use SSE endpoint:
> Terjemahan Indonesia: Use POST /API/v1/chat dengan stream: true or use SSE endpoint:

```bash
GET /api/v1/chat/stream?message=Hello&conversation_id=conv-123
```

**Request:** Same as POST /chat.

**Response:** SSE stream with event types:
- `final` — Final response message
- `execution_started` — Execution began
- `phase` — Execution phase update
- `task` — Task update
- `log` — Execution log entry
- `artifact` — New artifact created
- `progress` — Progress update (0–100)
- `execution_complete` — Execution finished
- `error` — Error occurred

---

### Workspace

#### GET /workspaces

List all workspaces.
> Terjemahan Indonesia: Daftar semua ruang kerja.

#### POST /workspaces

Create a new workspace.
> Terjemahan Indonesia: Membuat sebuah new workspace.

**Request:**
```json
{
  "name": "My Project",
  "description": "Optional description"
}
```

#### GET /workspaces/{workspace_id}


Get workspace detail.
> Terjemahan Indonesia: Dapatkan detail ruang kerja.

#### DELETE /workspaces/{workspace_id}


Delete a workspace.
> Terjemahan Indonesia: Delete sebuah workspace.

#### POST /workspaces/{workspace_id}/files


Upload a file to workspace.
> Terjemahan Indonesia: Upload sebuah file untuk workspace.

#### POST /workspaces/{workspace_id}/memory


Set a memory key.
> Terjemahan Indonesia: Set sebuah memory key.

#### GET /workspaces/{workspace_id}/memory/{key}


Get a memory value.
> Terjemahan Indonesia: Get sebuah memory value.

---

### Execution

#### POST /executions/run


Run an execution end-to-end.
> Terjemahan Indonesia: Run sebuah execution end-untuk-end.

**Request:**
```json
{
  "goal": "Build a todo app",
  "workspace_id": "ws-123",
  "conversation_id": "conv-123"
}
```

**Response:**
```json
{
  "execution": { ... },
  "artifacts": [ ... ]
}
```

#### PATCH /executions/{execution_id}/phases/{phase_id}


Update a phase status.
> Terjemahan Indonesia: Update sebuah phase status.

**Request:**
```json
{
  "status": "running",
  "progress": 45.0
}
```

#### POST /executions/{execution_id}/cancel


Cancel a running execution.
> Terjemahan Indonesia: Cancel sebuah running execution.

#### POST /executions/{execution_id}/progress


Update execution progress.
> Terjemahan Indonesia: Perbarui kemajuan eksekusi.

**Request:**
```json
{
  "progress": 65.0,
  "eta_seconds": 120
}
```

#### GET /executions/{execution_id}/logs


Get execution logs.
> Terjemahan Indonesia: Dapatkan log eksekusi.

#### GET /executions/{execution_id}/artifacts


List artifacts produced by an execution.
> Terjemahan Indonesia: List artifacts produced oleh sebuah execution.

---

### Artifact

#### GET /artifacts

List artifacts, optionally filtered.
> Terjemahan Indonesia: Daftar artefak, difilter secara opsional.

**Query params:** `workspace_id`, `artifact_type`

#### POST /artifacts

Create an artifact.
> Terjemahan Indonesia: Membuat sebuah artifact.

**Request:**
```json
{
  "workspace_id": "ws-123",
  "name": "todo-app",
  "artifact_type": "code",
  "description": "Full-stack todo app",
  "content": "...",
  "metadata": {}
}
```

#### GET /artifacts/{artifact_id}/versions/{version}


Get a specific version.
> Terjemahan Indonesia: Get sebuah specific versi.

#### POST /artifacts/{artifact_id}/versions


Add a new version.
> Terjemahan Indonesia: Add sebuah new versi.

#### POST /artifacts/{artifact_id}/restore/{version}


Restore to a previous version.
> Terjemahan Indonesia: Restore untuk sebuah previous versi.

#### DELETE /artifacts/{artifact_id}


Delete an artifact.
> Terjemahan Indonesia: Delete sebuah artifact.

---

### Capability Discovery

#### GET /capabilities

List all available capabilities.
> Terjemahan Indonesia: List all available kapabilitas.

**Response:**
```json
{
  "capabilities": [ ... ],
  "domains": [ ... ]
}
```

#### GET /capabilities/{capability_id}


Get capability detail.
> Terjemahan Indonesia: Get kapabilitas detail.

---

### Notifications

#### GET /notifications/{recipient}


Get notifications for a recipient.
> Terjemahan Indonesia: Get notifications untuk sebuah recipient.

**Query params:** `limit` (default 20)

#### PATCH /notifications/{recipient}/read/{notification_id}


Mark a notification as read.
> Terjemahan Indonesia: Mark sebuah notification as read.

---

### Model Routing

#### GET /models/providers


List available model providers.
> Terjemahan Indonesia: Daftar penyedia model yang tersedia.

#### GET /models/health

Health check for a specific provider.
> Terjemahan Indonesia: Health check untuk sebuah specific provider.

**Query params:** `provider`

---

### Long Tasks

#### POST /longtasks

Submit a long-running workflow.
> Terjemahan Indonesia: Submit sebuah long-running alur kerja.

**Request:**
```json
{
  "name": "my-workflow",
  "workflow": [ ... ]
}
```

#### POST /longtasks/{task_id}/start


Start a submitted workflow.
> Terjemahan Indonesia: Start sebuah submitted alur kerja.

#### POST /longtasks/{task_id}/pause


Pause a running workflow.
> Terjemahan Indonesia: Pause sebuah running alur kerja.

#### POST /longtasks/{task_id}/resume


Resume a paused workflow.
> Terjemahan Indonesia: Resume sebuah paused alur kerja.

---

### Phase3 (Experimental APIs)


#### POST /cognitive/process


Full cognitive pipeline processing.
> Terjemahan Indonesia: Full kognitif jalur processing.

#### POST /cognitive/reason


Generate hypotheses and reach a decision.
> Terjemahan Indonesia: Generate hypotheses dan reach sebuah decision.

#### POST /cognitive/debate


Run a debate between AI agents.
> Terjemahan Indonesia: Run sebuah debate between AI agen.

#### POST /cognitive/verify


Run self-verification pipeline.
> Terjemahan Indonesia: Run self-verification jalur.

#### POST /cognitive/simulate


Simulate a plan (dry-run).
> Terjemahan Indonesia: Simulate sebuah plan (dry-run).

#### GET /cognitive/world/query


Query the world model.
> Terjemahan Indonesia: Query world model.

#### POST /cognitive/strategy


Create a strategic roadmap.
> Terjemahan Indonesia: Membuat sebuah strategic roadmap.

#### POST /cognitive/learn


Run a benchmark and learn.
> Terjemahan Indonesia: Run sebuah benchmark dan learn.

#### POST /cognitive/adaptive


Run adaptive cognitive pipeline.
> Terjemahan Indonesia: Run adaptive kognitif jalur.

#### POST /cognitive/meta/optimize


Meta-cognition optimization.
> Terjemahan Indonesia: Optimalisasi meta-kognisi.

#### GET /cognitive/meta/metrics


Get meta-cognition metrics.
> Terjemahan Indonesia: Dapatkan metrik meta-kognisi.

#### POST /cognitive/meta/choose-pipeline


Select pipeline for a task.
> Terjemahan Indonesia: Select jalur untuk sebuah task.

#### POST /budget/estimate


Estimate cognitive budget for a task.
> Terjemahan Indonesia: Estimate kognitif budget untuk sebuah task.

#### POST /prompt/compile


Compile a prompt for an agent type.
> Terjemahan Indonesia: Compile sebuah prompt untuk sebuah agen type.

#### POST /goals

Create a goal.
> Terjemahan Indonesia: Membuat sebuah goal.

#### POST /goals/{goal_id}/execute


Execute a goal.
> Terjemahan Indonesia: Execute sebuah goal.

#### GET /goals/{goal_id}


Get a goal by ID.
> Terjemahan Indonesia: Get sebuah goal oleh ID.

#### POST /evaluation/benchmarks


Register a benchmark.
> Terjemahan Indonesia: Register sebuah benchmark.

#### GET /recovery/checkpoints


List recovery checkpoints.
> Terjemahan Indonesia: Daftar pos pemeriksaan pemulihan.

#### POST /graph/nodes

Create a graph node.
> Terjemahan Indonesia: Membuat sebuah graph node.

#### POST /graph/edges

Create a graph edge.
> Terjemahan Indonesia: Membuat sebuah graph edge.

#### GET /graph/nodes/{node_id}/related


Get related nodes.
> Terjemahan Indonesia: Dapatkan node terkait.

#### POST /mcp/tools

List MCP tools.
> Terjemahan Indonesia: List MCP alat.

**Query params:** `permissions` (comma-separated)

#### GET /mcp/plugins

List MCP plugins.
> Terjemahan Indonesia: Daftar plugin MCP.

#### POST /reputation/record


Record an agent reputation event.
> Terjemahan Indonesia: Record sebuah agen reputation event.

#### GET /reputation/leaderboard


Get agent leaderboard.
> Terjemahan Indonesia: Get agen leaderboard.

#### GET /experience/search


Search experience database.
> Terjemahan Indonesia: Basis data pengalaman pencarian.

#### POST /experience/record


Record a new experience.
> Terjemahan Indonesia: Record sebuah new experience.

#### GET /observability/traces/{trace_id}


Get trace details.
> Terjemahan Indonesia: Dapatkan detail jejak.

#### GET /observability/metrics


Get observability metrics.
> Terjemahan Indonesia: Dapatkan metrik observabilitas.

#### POST /governance/policies


Create a governance policy.
> Terjemahan Indonesia: Membuat sebuah tata kelola policy.

#### POST /artifacts (Phase3)


Create an artifact via Phase3 API.
> Terjemahan Indonesia: Membuat sebuah artifact via Phase3 API.

#### GET /artifacts/{artifact_id} (Phase3)


Get artifact via Phase3 API.
> Terjemahan Indonesia: Dapatkan artefak melalui API Phase3.

---

## Error Responses

All errors follow this format:
> Terjemahan Indonesia: All errors follow ini format:

```json
{
  "detail": "Error message"
}
```

Common HTTP status codes:
> Terjemahan Indonesia: Kode status HTTP umum:
- `400` — Bad request
- `401` — Unauthorized
- `403` — Forbidden
- `404` — Not found
- `422` — Validation error
- `500` — Internal server error
