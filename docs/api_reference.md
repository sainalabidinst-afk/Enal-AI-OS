# ECP API Reference

**Status:** Platform RC (2026-07-27) - Runtime: 368 tests passing

## Base URL

```
http://localhost:8000/api/v1
```

## Authentication

All API endpoints require authentication via API key:

```bash
curl -H "X-API-Key: your-api-key" http://localhost:8000/api/v1/health
```

## Endpoints

### Chat

#### POST /chat

Send a message to the AI orchestrator.

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
  "message": "I'll build a full-stack todo app for you...",
  "conversation_id": "conv-123",
  "agent": "orchestrator",
  "tasks_completed": 5,
  "metadata": {}
}
```

#### GET /conversations/{conversation_id}

Get conversation history.

### Cognitive

#### POST /cognitive/process

Full cognitive pipeline processing.

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

### Marketplace

#### POST /marketplace/publish

Publish a plugin.

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

### Studio

#### GET /studio/traces/{trace_id}

Get trace details for debugging.

#### GET /studio/metrics

Get observability metrics.

#### GET /studio/artifacts/{project_id}

Get artifacts for a project.

#### GET /studio/graph

Get the knowledge graph.

#### GET /studio/memory

Search memory by layer.

#### GET /studio/reputation

Get agent reputation leaderboard.

#### GET /studio/cognitive-services

List available cognitive services.

#### GET /studio/pipeline-presets

List adaptive pipeline presets.

#### GET /studio/meta/metrics

Get meta-cognition metrics.

---

### Chat Streaming

#### POST /chat/stream

Send a message and receive Server-Sent Events (SSE) stream.

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

#### POST /workspaces

Create a new workspace.

**Request:**
```json
{
  "name": "My Project",
  "description": "Optional description"
}
```

#### GET /workspaces/{workspace_id}

Get workspace detail.

#### DELETE /workspaces/{workspace_id}

Delete a workspace.

#### POST /workspaces/{workspace_id}/files

Upload a file to workspace.

#### POST /workspaces/{workspace_id}/memory

Set a memory key.

#### GET /workspaces/{workspace_id}/memory/{key}

Get a memory value.

---

### Execution

#### POST /executions/run

Run an execution end-to-end.

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

**Request:**
```json
{
  "status": "running",
  "progress": 45.0
}
```

#### POST /executions/{execution_id}/cancel

Cancel a running execution.

#### POST /executions/{execution_id}/progress

Update execution progress.

**Request:**
```json
{
  "progress": 65.0,
  "eta_seconds": 120
}
```

#### GET /executions/{execution_id}/logs

Get execution logs.

#### GET /executions/{execution_id}/artifacts

List artifacts produced by an execution.

---

### Artifact

#### GET /artifacts

List artifacts, optionally filtered.

**Query params:** `workspace_id`, `artifact_type`

#### POST /artifacts

Create an artifact.

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

#### POST /artifacts/{artifact_id}/versions

Add a new version.

#### POST /artifacts/{artifact_id}/restore/{version}

Restore to a previous version.

#### DELETE /artifacts/{artifact_id}

Delete an artifact.

---

### Capability Discovery

#### GET /capabilities

List all available capabilities.

**Response:**
```json
{
  "capabilities": [ ... ],
  "domains": [ ... ]
}
```

#### GET /capabilities/{capability_id}

Get capability detail.

---

### Notifications

#### GET /notifications/{recipient}

Get notifications for a recipient.

**Query params:** `limit` (default 20)

#### PATCH /notifications/{recipient}/read/{notification_id}

Mark a notification as read.

---

### Model Routing

#### GET /models/providers

List available model providers.

#### GET /models/health

Health check for a specific provider.

**Query params:** `provider`

---

### Long Tasks

#### POST /longtasks

Submit a long-running workflow.

**Request:**
```json
{
  "name": "my-workflow",
  "workflow": [ ... ]
}
```

#### POST /longtasks/{task_id}/start

Start a submitted workflow.

#### POST /longtasks/{task_id}/pause

Pause a running workflow.

#### POST /longtasks/{task_id}/resume

Resume a paused workflow.

---

### Phase3 (Experimental APIs)

#### POST /cognitive/process

Full cognitive pipeline processing.

#### POST /cognitive/reason

Generate hypotheses and reach a decision.

#### POST /cognitive/debate

Run a debate between AI agents.

#### POST /cognitive/verify

Run self-verification pipeline.

#### POST /cognitive/simulate

Simulate a plan (dry-run).

#### GET /cognitive/world/query

Query the world model.

#### POST /cognitive/strategy

Create a strategic roadmap.

#### POST /cognitive/learn

Run a benchmark and learn.

#### POST /cognitive/adaptive

Run adaptive cognitive pipeline.

#### POST /cognitive/meta/optimize

Meta-cognition optimization.

#### GET /cognitive/meta/metrics

Get meta-cognition metrics.

#### POST /cognitive/meta/choose-pipeline

Select pipeline for a task.

#### POST /budget/estimate

Estimate cognitive budget for a task.

#### POST /prompt/compile

Compile a prompt for an agent type.

#### POST /goals

Create a goal.

#### POST /goals/{goal_id}/execute

Execute a goal.

#### GET /goals/{goal_id}

Get a goal by ID.

#### POST /evaluation/benchmarks

Register a benchmark.

#### GET /recovery/checkpoints

List recovery checkpoints.

#### POST /graph/nodes

Create a graph node.

#### POST /graph/edges

Create a graph edge.

#### GET /graph/nodes/{node_id}/related

Get related nodes.

#### POST /mcp/tools

List MCP tools.

**Query params:** `permissions` (comma-separated)

#### GET /mcp/plugins

List MCP plugins.

#### POST /reputation/record

Record an agent reputation event.

#### GET /reputation/leaderboard

Get agent leaderboard.

#### GET /experience/search

Search experience database.

#### POST /experience/record

Record a new experience.

#### GET /observability/traces/{trace_id}

Get trace details.

#### GET /observability/metrics

Get observability metrics.

#### POST /governance/policies

Create a governance policy.

#### POST /artifacts (Phase3)

Create an artifact via Phase3 API.

#### GET /artifacts/{artifact_id} (Phase3)

Get artifact via Phase3 API.

---

## Error Responses

All errors follow this format:

```json
{
  "detail": "Error message"
}
```

Common HTTP status codes:
- `400` — Bad request
- `401` — Unauthorized
- `403` — Forbidden
- `404` — Not found
- `422` — Validation error
- `500` — Internal server error
