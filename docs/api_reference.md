# Referensi API ECP

**Status:** Platform RC (2026-07-27) — Runtime: 426 test lulus

## Base URL

```
http://localhost:8000/api/v1
```

## Autentikasi

Semua endpoint API memerlukan autentikasi melalui Bearer token:

```bash
curl -H "Authorization: Bearer your-api-key" http://localhost:8000/api/v1/health
```

## Endpoint

### Chat

#### POST /chat

Mengirim pesan ke AI orchestrator.

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

#### GET /chat/stream

Melakukan streaming pesan dan menerima aliran Server-Sent Events (SSE).

```bash
GET /api/v1/chat/stream?message=Hello&conversation_id=conv-123
```

**Response:** Aliran SSE dengan tipe event:
- `final` — Pesan respons terakhir
- `execution_started` — Eksekusi dimulai
- `phase` — Pembaruan fase eksekusi
- `task` — Pembaruan task
- `log` — Entri log eksekusi
- `artifact` — Artifact baru dibuat
- `progress` — Pembaruan progress (0–100)
- `execution_complete` — Eksekusi selesai
- `error` — Terjadi error

#### GET /conversations/{conversation_id}

Mendapatkan detail percakapan.

#### DELETE /conversations/{conversation_id}

Menghapus percakapan.

### Cognitive

#### POST /cognitive/process

Pemrosesan pipeline kognitif penuh.

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

Mengambil keputusan menggunakan decision theory.

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

#### POST /cognitive/reason

Menghasilkan hipotesis dan mengambil keputusan.

#### POST /cognitive/debate

Menjalankan debat antar agen AI.

#### POST /cognitive/verify

Menjalankan alur self-verification.

#### POST /cognitive/simulate

Mensimulasikan sebuah rencana (simulasi).

#### GET /cognitive/world/query

Proses query terhadap world model.

#### POST /cognitive/strategy

Membuat strategic roadmap.

#### POST /cognitive/learn

Menjalankan Benchmark dan pembelajaran.

#### GET /cognitive/services

Mendaftar semua layanan kognitif yang tersedia.

#### POST /cognitive/execute

Mengeksekusi pipeline kognitif.

#### POST /cognitive/adaptive

Menjalankan pipeline kognitif adaptif.

#### POST /cognitive/meta/optimize

Optimalisasi meta-cognition.

#### GET /cognitive/meta/metrics

Mendapatkan metrik meta-cognition.

#### POST /cognitive/meta/choose-pipeline

Memilih pipeline untuk sebuah task.

#### POST /budget/estimate

Memperkirakan cognitive budget untuk sebuah task.

#### POST /prompt/compile

Mengompilasi prompt untuk tipe agent.

### Organization

#### POST /organization

Membuat node organisasi.

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

#### GET /organization/{node_id}

Mendapatkan node organisasi.

#### GET /organization/{node_id}/subtree

Mendapatkan subtree organisasi.

### Orchestrator v2

#### POST /v2/chat

Mengirim pesan ke orchestrator v2.

#### GET /v2/tasks/{task_id}

Mendapatkan status task dari orchestrator v2.

### Marketplace

#### POST /marketplace/publish

Menerbitkan Plugin.

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

Mendaftar Plugin yang tersedia.

#### GET /marketplace/plugins/search

Mencari Plugin.

#### POST /marketplace/install/{plugin_id}

Memasang Plugin.

#### POST /marketplace/uninstall/{plugin_id}

Mencopot Plugin.

#### GET /marketplace/installed

Mendaftar Plugin yang terpasang.

### Studio

#### GET /studio/traces/{trace_id}

Mendapatkan detail trace untuk debugging.

#### GET /studio/metrics

Mendapatkan metrik observability.

#### GET /studio/artifacts/{project_id}

Mendapatkan artifact untuk sebuah proyek.

#### GET /studio/graph/{project_id}

Mendapatkan Knowledge Graph.

#### GET /studio/memory

Mencari memory berdasarkan layer.

#### GET /studio/reputation

Mendapatkan leaderboard reputasi agent.

#### GET /studio/cognitive/services

Mendaftar layanan kognitif yang tersedia.

#### GET /studio/cognitive/pipelines

Mendaftar preset pipeline adaptif.

#### GET /studio/cognitive/meta/metrics

Mendapatkan metrik meta-cognition.

#### GET /studio/export/{project_id}

Mengekspor data proyek.

### Workspace

#### GET /workspaces

Mendaftar semua workspace.

#### POST /workspaces

Membuat workspace baru.

**Request:**
```json
{
  "name": "My Project",
  "description": "Optional description"
}
```

#### GET /workspaces/{workspace_id}

Mendapatkan detail workspace.

#### DELETE /workspaces/{workspace_id}

Menghapus workspace.

#### POST /workspaces/{workspace_id}/files

Mengunggah file ke workspace.

#### GET /workspaces/{workspace_id}/files

Mendaftar file di workspace.

#### GET /workspaces/{workspace_id}/files/{filename}

Mendapatkan file tertentu.

#### DELETE /workspaces/{workspace_id}/files/{filename}

Menghapus file di workspace.

#### POST /workspaces/{workspace_id}/memory

Menetapkan memory key.

#### GET /workspaces/{workspace_id}/memory/{key}

Mendapatkan nilai memory.

### Execution

#### POST /executions/run

Menjalankan eksekusi end-to-end.

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

#### POST /executions

Membuat execution session baru.

#### GET /executions

Mendaftar semua execution session.

#### GET /executions/{execution_id}

Mendapatkan detail execution session.

#### PATCH /executions/{execution_id}/phases/{phase_id}

Memperbarui status fase.

**Request:**
```json
{
  "status": "running",
  "progress": 45.0
}
```

#### POST /executions/{execution_id}/phases

Menambahkan fase eksekusi.

#### POST /executions/{execution_id}/progress

Memperbarui progress eksekusi.

**Request:**
```json
{
  "progress": 65.0,
  "eta_seconds": 120
}
```

#### POST /executions/{execution_id}/cancel

Membatalkan eksekusi yang sedang berjalan.

#### GET /executions/{execution_id}/logs

Mendapatkan log eksekusi.

#### POST /executions/{execution_id}/logs

Menambahkan log eksekusi.

#### GET /executions/{execution_id}/artifacts

Mendaftar artifact yang dihasilkan oleh eksekusi.

#### POST /executions/{execution_id}/artifacts

Menambahkan artifact ke eksekusi.

#### DELETE /executions/{execution_id}

Menghapus execution session.

### Artifact

#### GET /artifacts

Mendaftar artifact, difilter secara opsional.

**Query params:** `workspace_id`, `artifact_type`

#### POST /artifacts

Membuat artifact.

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

#### GET /artifacts/{artifact_id}

Mendapatkan detail artifact.

#### GET /artifacts/{artifact_id}/versions/{version}

Mendapatkan versi tertentu.

#### POST /artifacts/{artifact_id}/versions

Menambahkan versi baru.

#### POST /artifacts/{artifact_id}/restore/{version}

Mengembalikan ke versi sebelumnya.

#### DELETE /artifacts/{artifact_id}

Menghapus artifact.

### Capability Discovery

#### GET /capabilities

Mendaftar semua capability yang tersedia.

**Response:**
```json
{
  "capabilities": [ ... ],
  "domains": [ ... ]
}
```

#### GET /capabilities/{capability_id}

Mendapatkan detail capability.

### Notification

#### GET /notifications/{recipient}

Mendapatkan notification untuk recipient.

**Query params:** `limit` (default 20)

#### POST /notifications

Membuat notification.

#### PATCH /notifications/{recipient}/read/{notification_id}

Menandai notification telah dibaca.

### Model Routing

#### GET /providers

Mendaftar provider model yang tersedia.

#### GET /health

Pemeriksaan kesehatan untuk model gateway.

#### POST /route

Merutekan permintaan LLM ke provider.

### Long Tasks

#### POST /longtasks

Menjadwalkan workflow berjalan lama.

**Request:**
```json
{
  "name": "my-workflow",
  "workflow": [ ... ]
}
```

#### POST /longtasks/{task_id}/start

Memulai workflow yang dijadwalkan.

#### GET /longtasks/{task_id}

Mendapatkan status task.

#### POST /longtasks/{task_id}/pause

Menjeda workflow yang sedang berjalan.

#### POST /longtasks/{task_id}/resume

Melanjutkan workflow yang ditentukan.

### Goals

#### POST /goals

Membuat goal.

#### POST /goals/{goal_id}/execute

Menjalankan goal.

#### GET /goals/{goal_id}

Mendapatkan goal berdasarkan ID.

### Reputation & Experience

#### GET /reputation/leaderboard

Mendapatkan leaderboard agent.

#### POST /reputation/record

Mencatat event reputasi agent.

#### GET /experience/search

Mencari database pengalaman.

#### POST /experience/record

Mencatat pengalaman baru.

### Observability

#### GET /observability/traces/{trace_id}

Mendapatkan detail trace.

#### GET /observability/metrics

Mendapatkan metrik observability.

#### GET /metrics

Mendapatkan metrik telemetry agregat.

#### GET /metrics/analysis

Mendapatkan metrik analisis.

#### GET /metrics/chat

Mendapatkan metrik chat.

#### GET /metrics/parser

Mendapatkan metrik parser.

#### GET /metrics/reasoning

Mendapatkan metrik reasoning.

### Governance

#### POST /governance/policies

Membuat policy governance.

### Recovery

#### GET /recovery/checkpoints

Mendaftar checkpoint pemulihan.

### Evaluation

#### POST /evaluation/benchmarks

Mendaftarkan Benchmark.

### MCP

#### GET /mcp/tools

Mendaftar MCP tools.

**Query params:** `permissions` (dipisahkan koma)

#### GET /mcp/plugins

Mendaftar MCP Plugins.

### Graph

#### POST /graph/nodes

Membuat graph node.

#### POST /graph/edges

Membuat graph edge.

#### GET /graph/nodes/{node_id}/related

Mendapatkan node terkait.

### Attachments

#### POST /attachments/upload

Mengunggah file.

#### POST /attachments/analyze

Menganalisis file.

#### POST /attachments/diff

Membandingkan file.

### Distributed

#### POST /distributed/nodes

Mendaftarkan node terdistribusi.

#### GET /distributed/cluster

Mendapatkan status cluster.

#### GET /distributed/nodes/{node_id}

Mendapatkan node terdistribusi.

### Benchmark

#### GET /benchmark/suite

Mendapatkan daftar suite Benchmark.

#### POST /benchmark/run

Menjalankan Benchmark.

#### GET /benchmark/capability-scores

Mendapatkan skor capability.

#### GET /benchmark/cce/status

Mendapatkan status CCE benchmark.

---

## Error Response

Semua error mengikuti format ini:

```json
{
  "detail": "Error message"
}
```

Kode status HTTP umum:
- `400` — Bad request
- `401` — Unauthorized
- `403` — Forbidden
- `404` — Not found
- `422` — Validation error
- `500` — Internal server error

