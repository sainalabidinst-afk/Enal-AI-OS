# ADR-033: A2A/MCP Integration Architecture

<!-- DOCUMENT_METADATA_START -->
**Pemilik:** Tim Integrasi
**Canonical Owner:** Lead Platform Engineer
**Terakhir Diverifikasi:** 2026-10-03
**Versi:** 1.0.0
**Status:** Accepted
**SSOT:** Arsitektur integrasi Agent-to-Agent dan Model Context Protocol
<!-- DOCUMENT_METADATA_END -->

## Abstrak

ADR ini mendokumentasikan keputusan arsitektur untuk A2A dan MCP integration, termasuk registry, invoker, dan proxy patterns.

## Konteks

ECP memerlukan integrasi dengan ekosistem AI yang lebih luas melalui A2A protocol dan MCP.

## Keputusan

### 1. A2A Registry Pattern

**Decision:** Registry + Invoker pattern
**Rationale:**
- Clear separation registration/execution
- Extensible untuk new agents
- Testable secara terisolasi

### 2. MCP Proxy Pattern

**Decision:** Proxy pattern untuk MCP tool calls
**Rationale:**
- Abstraction layer
- Consistent interface
- Easy to extend

### 3. Frontend Management

**Decision:** A2AConfig + MCPConnector components
**Rationale:**
- Visual management interface
- Real-time status updates
- Easy to use

## Consequences

### Positive
- Clean integration architecture
- Extensible untuk new protocols
- Visual management interface

### Negative
- Additional complexity
- More components to maintain

### Neutral
- Uses existing ToolRegistry untuk integration

## References

- RFC-0052: A2A/MCP Integration
- MCP Specification: https://modelcontextprotocol.io/
