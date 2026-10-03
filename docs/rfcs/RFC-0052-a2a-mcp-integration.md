# RFC-0052: A2A/MCP Integration

<!-- DOCUMENT_METADATA_START -->
**Pemilik:** Tim Integrasi
**Canonical Owner:** Lead Platform Engineer
**Terakhir Diverifikasi:** 2026-10-03
**Versi:** 1.0.0
**Status:** Draft → Proposed
**SSOT:** Rancangan integrasi Agent-to-Agent (A2A) dan Model Context Protocol (MCP) untuk ECP
<!-- DOCUMENT_METADATA_END -->

## Abstrak

RFC ini mendefinisikan integrasi A2A dan MCP untuk ECP, yang memungkinkan:
1. Agent memanggil agent lain (A2A)
2. Agent menggunakan tool dari MCP servers
3. Registry untuk external agents dan MCP servers

## Konteks

ECP memerlukan integrasi dengan ekosistem AI yang lebih luas:
1. A2A protocol untuk agent-to-agent invocation
2. MCP untuk standardized tool access
3. Registry untuk managing external connections

## Keputusan

### 1. A2A Registry

**Core Components:**
- `A2ARegistry` — Register external A2A agents
- `A2AInvoker` — Invoke external agents

**Features:**
- Register agent dengan name, endpoint, capabilities
- List registered agents
- Unregister agents
- Invoke agent dengan payload

### 2. MCP Tool Registry

**Core Components:**
- `MCPToolRegistry` — Register MCP servers
- `MCPToolProxy` — Proxy tool calls to MCP servers

**Features:**
- Register server dengan name, endpoint
- Connect/disconnect servers
- List servers
- Call tools on servers

### 3. Frontend Components

- `A2AConfig.tsx` — Configure A2A bindings
- `MCPConnector.tsx` — Connect MCP servers
- `ExternalAgentCard.tsx` — Display external agent

### 4. API Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/api/v1/a2a/register` | Register A2A agent |
| GET | `/api/v1/a2a` | List A2A agents |
| POST | `/api/v1/a2a/invoke` | Invoke A2A agent |
| POST | `/api/v1/mcp/servers` | Register MCP server |
| POST | `/api/v1/mcp/servers/{id}/connect` | Connect MCP server |
| POST | `/api/v1/mcp/servers/{id}/disconnect` | Disconnect MCP server |
| GET | `/api/v1/mcp/servers` | List MCP servers |
| POST | `/api/v1/mcp/tools/call` | Call MCP tool |

## Implementasi

### Frontend Components

- `A2AConfig.tsx` — A2A agent configuration
- `MCPConnector.tsx` — MCP server management
- `ExternalAgentCard.tsx` — External agent display

### Backend Modules

- `backend/app/core/a2a_registry.py` — A2ARegistry
- `backend/app/core/a2a_invoker.py` — A2AInvoker
- `backend/app/core/mcp_tool_registry.py` — MCPToolRegistry
- `backend/app/core/mcp_tool_proxy.py` — MCPToolProxy
- `backend/app/api/a2a_mcp.py` — API endpoints

## Dependencies

- RFC-0046: Visual Builder Foundation

## Testing

- TypeScript: 0 errors
- Ruff: 0 errors
- Mypy: 0 errors

## References

- SimplAI A2A/MCP: https://simplai.ai/docs/connections-and-integrations/
- MCP Specification: https://modelcontextprotocol.io/
