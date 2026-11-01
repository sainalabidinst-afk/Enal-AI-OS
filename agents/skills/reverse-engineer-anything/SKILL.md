---
name: reverse-engineer-anything
description: Reverse engineer native, managed, Electron/JavaScript, packaged, and browser applications with REA. Use shipped-artifact or approved runtime evidence to explain features, compare versions, decompile code, or guide reconstruction.
---

# Reverse Engineer Anything (REA) Guidelines

## 1. Evidence-First Approach

Every conclusion produced by this skill MUST distinguish clearly between:

* **Observations** — direct, artifact-backed facts (offsets, strings, API boundaries, AST nodes).
* **Inferences** — logical deductions drawn from observations.
* **Unknowns** — items that could not be determined from the available evidence.

Do not make general guesses without referencing an offset, IPC channel, AST node, or evidence ID.

## 2. Sequential & Staged Workflow

1. **Inventory** — Start with the smallest possible inspection (ASAR headers, ELF/PE headers, API boundaries, package metadata).
2. **Hypothesis** — Formulate a specific hypothesis about a feature, function, or data flow.
3. **Targeted Decompile** — Use `rea-agents` MCP tooling to decompile only the relevant region.
4. **Correlate** — Cross-reference findings across static analysis, dynamic traces, and network/IPC logs.
5. **Reconstruct** — After evidence is collected, produce a clean-room reconstruction compatible with the ECP architecture.

## 3. Supported Targets

| Target Type | Examples | REA Provider |
|-------------|----------|--------------|
| Native binaries | `.exe`, `.dll`, `.so`, `.dylib` (C/C++, Rust, Go) | Ghidra, Rizin, objdump, Hopper |
| Electron / JavaScript | `.asar`, `.js`, packaged apps | ASAR parser, IPC decompiler |
| .NET assemblies | `.dll`, `.exe` (managed) | .NET decompiler |
| Web applications | Bundles, SPA artifacts | Web app parser |

## 4. ECP Integration Points

| Layer | Path | Purpose |
|-------|------|---------|
| Capability Pack | `apps/reverse_engineer/` | Pack entrypoint, service bridging, Pydantic schemas |
| MCP Server | `mcp_tool_registry` | Registered as `Reverse Engineer Anything (morluto)` |
| Agent Skill | `agents/skills/reverse-engineer-anything/SKILL.md` | This document |

## 5. Example ECP Usage

```python
from apps.reverse_engineer.app import ReverseEngineerCapabilityPack

pack = ReverseEngineerCapabilityPack()
result = await pack.run(
    user_input="Analyse the clipboard-copy feature in target.exe",
    context={"target_path": "/path/to/target.exe", "deep_analysis": True},
)
# result -> REAResponse with REAAnalysisResult containing evidence IDs
```

## 6. Output Contract

Every REA analysis result includes:

* `evidence_id` — traceable evidence reference
* `observations` — what was directly seen
* `inferences` — logical deductions
* `unknowns` — what could not be determined
* `confidence` — per-artifact confidence score (0.0–1.0)
