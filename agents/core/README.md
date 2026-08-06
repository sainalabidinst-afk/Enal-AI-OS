# Core Components

Core components are stable platform services that all Capability Packs depend on.

## Components

1. **Runtime Engine** - Adaptive pipeline execution, task orchestration
2. **Memory System** - 7-layer memory (working, conversation, knowledge, long-term, session, project, episodic)
3. **Event Bus** - Event-driven communication between services
4. **Task Queue** - Async task management with checkpoint/resume
5. **Tool Registry** - Tool registration, discovery, and schema management
6. **MCP Registry** - Model Context Protocol plugin registry
7. **Plugin Manifest** - Plugin validation and compatibility checking
8. **Workspace Service** - Workspace CRUD and file management
9. **Artifact Service** - Artifact versioning and lifecycle
10. **Governance** - Approval workflows, tenant isolation, RBAC
11. **Security Model** - Authentication, authorization, audit logging
12. **Contracts** - Stable interface contracts between services

## Usage

```python
from backend.app.core.tool_registry import tool_registry
from backend.app.core.mcp_registry import mcp_registry
from backend.app.core.workspace_service import workspace_service
```

Capability Packs import from Core, never the reverse.
