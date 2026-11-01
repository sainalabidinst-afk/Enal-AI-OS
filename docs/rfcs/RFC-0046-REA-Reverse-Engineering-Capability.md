# RFC-0046 — REA Reverse Engineering Capability Pack

**Status:** Proposed  
**Author:** Enal AI OS Engineering  
**Last Updated:** 2026-11-01  
**Capability ID:** `reverse-engineer`  
**Category:** Security / Reverse Engineering  
**Target Quality:** A+ (≥95) — Domain Expert (L4)

## 1. Summary

Integrate [morluto/rea](https://github.com/morluto/rea) as a formal ECP
Capability Pack for evidence-based reverse engineering of native binaries,
Electron/JavaScript applications, .NET assemblies, and web apps without
requiring original source code.

## 2. Motivation

ECP currently lacks a dedicated reverse-engineering capability. Security
analysts, malware researchers, and feature-reconstruction workflows require
the ability to:

* Decompile native binaries (C/C++, Rust, Go) without source.
* Inspect Electron/JavaScript packaged applications (ASAR, IPC bridges).
* Decompile .NET assemblies.
* Extract control flow, logic, and feature reconstruction from binaries.

REA provides a modern, agent-oriented, evidence-based toolkit that maps
directly onto ECP's governance and observability requirements.

## 3. Design

### 3.1 Architecture

Three integration layers:

| Layer | Location | Responsibility |
|-------|----------|----------------|
| Capability Pack | `apps/reverse_engineer/` | Pack entrypoint, Pydantic schemas, REA service bridge |
| Agent Skill | `agents/skills/reverse-engineer-anything/SKILL.md` | Agent operating instructions |
| MCP Server | `backend/app/core/mcp_tool_registry.py` | Registered as `Reverse Engineer Anything (morluto)` |

### 3.2 Data Flow

```
User Request
    ↓
ECP Cognitive Pipeline
    ↓
ReverseEngineerCapabilityPack.run()
    ↓
REAService.analyze_target()  →  subprocess: npx rea-agents@latest ...
    ↓
REAAnalysisResult (evidence-based)
    ↓
Caller / downstream packs
```

### 3.3 Schemas

* `REAEvidence` — atomic observation/inference unit with globally unique ID.
* `REAArtifactInspection` — per-artifact inspection entry.
* `REAAnalysisResult` — complete analysis result for a target.
* `REARequest` / `REAResponse` — pack request/response envelopes.

## 4. Scope

### In Scope

* Native binary analysis (PE, ELF, Mach-O) via Ghidra/Rizin/objdump.
* Electron/JavaScript application analysis (ASAR, IPC decompilation).
* .NET assembly analysis.
* Evidence collection with traceable IDs.
* Clean-room feature reconstruction guidance.

### Out of Scope

* Direct binary modification or patching.
* Malware execution in sandboxed environments.
* Network exploitation or C2 communication.
* DRM circumvention or licence key generation.

## 5. Quality Gates

| Metric | Target |
|--------|--------|
| mypy errors | 0 |
| ruff errors | 0 |
| Unit tests | ≥80% coverage |
| Evidence traceability | 100% of inferences traceable to evidence IDs |

## 6. RFC References

* RFC-0001 — Stable Contract Core  
* RFC-0005 — Trading Analysis (evidence pattern reference)  
* RFC-0008 — Security Engineer (governance pattern reference)
