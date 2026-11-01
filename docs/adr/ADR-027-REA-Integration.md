# ADR-027 — REA Integration for Reverse Engineering Capability Pack

**Status:** Accepted  
**Date:** 2026-11-01  
**Deciders:** Enal AI OS Engineering  
**Capability ID:** `reverse-engineer`

## 1. Context

ECP needs a reverse-engineering capability to support security analysis,
malware research, and feature reconstruction without original source code.
The morluto/rea toolkit provides a modern, evidence-based, agent-oriented
approach that aligns with ECP's governance model.

## 2. Decision

Integrate REA as a Capability Pack at `apps/reverse_engineer/`, exposed
through:

1. A `BaseApp` subclass (`ReverseEngineerCapabilityPack`) implementing the
   ECP cognitive pipeline contract.
2. An MCP server registration in `mcp_tool_registry` for subprocess-based
   invocation (`npx -y rea-agents@latest mcp`).
3. Pydantic v2 schemas (`models.py`) enforcing evidence-based output
   contracts.
4. An Agent Skill markdown (`SKILL.md`) guiding agent behaviour.

## 3. Alternatives Considered

| Option | Pros | Cons |
|--------|------|------|
| Wrap REA as a standalone microservice | Isolation, language flexibility | Operational overhead, network latency |
| Embed REA logic directly in Python | No external dependency | Duplicates REA effort, maintenance burden |
| **Integrate REA via subprocess + MCP (chosen)** | Leverages existing toolkit, evidence-based output, minimal ECP code | Requires Node.js/rea-agents on host |

## 4. Consequences

### Positive

* Evidence-based reasoning — every inference traces to an evidence ID.
* Multi-target support — native, Electron/JS, .NET, web.
* Minimal ECP code — REA does the heavy lifting.
* Graceful degradation — pack reports unavailability when CLI is missing.

### Negative

* Requires `rea-agents` CLI and Node.js on the host.
* Subprocess invocation adds latency for large binaries.
* MCP server registration is best-effort; host must have `npx` available.

## 5. Related Documents

* RFC-0046 — REA Reverse Engineering Capability Pack  
* CAPABILITY_GUIDE.md — ECP capability pack standards  
* CAPABILITY_STRATEGY.md — Pack evolution roadmap
