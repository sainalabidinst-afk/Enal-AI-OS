# Self-Development ECP Meta-Analysis Plan

**Project:** Enal-AI-OS  
**Capability Pack:** Self-Development  
**Objective:** Extend Self-Development to analyze ECP itself and propose new capability packs  
**Date:** 2026-10-03  
**Status:** Draft  

---

## 1. Current State

### 1.1 Existing Capability
- **Scope:** Project analysis, code smell detection, patch generation, approval workflow
- **Engine:** `SelfDevelopmentEngine` with `ProjectScanner`, `SmellTaxonomy`, `SuggestionGenerator`, `RiskModeler`
- **Output:** Project analysis, problem list, solutions, patches, test reports
- **Mode:** Single mode — analyzes external project code only

### 1.2 Limitations
- Cannot analyze ECP platform itself (core modules, capability packs, cross-pack patterns)
- Cannot propose new capability packs or improvements to existing packs
- No governance issue detection for the platform
- No cross-pack pattern learning and extraction
- Limited to project-level analysis, not platform-level meta-analysis

---

## 2. Target State

### 2.1 New Capabilities
1. **ECP Platform Analysis** — Scan ECP core modules, capability packs, hotspots, governance issues
2. **Capability Proposal** — Propose new capability packs based on platform gaps and reuse potential
3. **Improvement Proposal** — Propose improvements to existing packs based on cross-pack patterns
4. **Cross-Pack Learning** — Identify reusable patterns across packs and propose extractions to core

### 2.2 Trigger Mechanism
- When user input contains keywords: `ecp`, `platform`, `core`, `meta-analysis`, `improve ECP`
- Switches from project analysis mode to ECP meta-analysis mode
- Returns structured ECP analysis, capability proposals, and improvement proposals

---

## 3. Implementation Plan

### 3.1 Schema Extensions (`apps/self_development/schemas.py`)

**New enums:**
- `CapabilityTier` — tier_a, tier_b, tier_c, platform
- `ProposalStatus` — draft, submitted, approved, rejected, implemented

**New dataclasses:**
- `ECPPlatformAnalysis` — core modules, capability packs, total files, complexity, hotspots, governance issues, pack gaps, cross-pack patterns
- `CapabilityProposal` — id, name, domain, description, tier, reuse_potential, estimated_effort, risk, confidence, rationale, required_packs, status
- `ImprovementProposal` — id, target_type, target_id, improvement_type, description, estimated_effort, risk, confidence, expected_impact, status
- `CrossPackPattern` — id, pattern_type, description, source_packs, target_packs, reusability_score, implementation_complexity

**Extended enums:**
- `ProblemType` — add `capability_gap`, `pack_overlap`, `governance_violation`, `documentation_gap`
- `ImprovementType` — add `new_capability`, `pack_merge`, `pack_split`, `governance`

---

### 3.2 ECP Analyzer Module (`apps/self_development/ecp_analyzer.py`)

**New module:** `ECPAnalyzer`

**Responsibilities:**
- Scan ECP directory structure for core modules and capability packs
- Detect governance issues (missing benchmarks, real_cases, docs per pack)
- Detect capability gaps (expected packs not yet implemented)
- Detect cross-pack patterns (shared modules, shared tools)
- Propose new capabilities based on gaps
- Propose improvements based on governance issues and patterns

**Key methods:**
- `analyze()` → `ECPPlatformAnalysis`
- `propose_capabilities(analysis)` → `list[CapabilityProposal]`
- `propose_improvements(analysis)` → `list[ImprovementProposal]`
- `_find_hotspots()` → list of hotspot file paths
- `_detect_governance_issues()` → list of governance issues
- `_detect_pack_gaps()` → list of missing capability packs
- `_detect_cross_pack_patterns()` → list of shared patterns

**Known limitation:**
- Core module counting by `backend/app/core/*.py` returns 0 due to current path filtering; needs refinement in future iteration

---

### 3.3 Engine Extensions (`apps/self_development/engine.py`)

**New methods:**
- `analyze_ecp(ecp_root=None)` → dict with platform analysis
- `propose_capabilities(ecp_root=None)` → list of capability proposals
- `propose_improvements(ecp_root=None)` → list of improvement proposals

**Behavior:**
- `analyze_ecp()` creates `ECPAnalyzer`, runs `analyze()`, returns structured dict
- `propose_capabilities()` creates `ECPAnalyzer`, runs `analyze()` + `propose_capabilities()`, returns list
- `propose_improvements()` creates `ECPAnalyzer`, runs `analyze()` + `propose_improvements()`, returns list

---

### 3.4 Worker Extensions (`apps/self_development/worker.py`)

**New methods:**
- `analyze_ecp(ecp_root=None)` → delegates to engine
- `propose_capabilities(ecp_root=None)` → delegates to engine
- `propose_improvements(ecp_root=None)` → delegates to engine

---

### 3.5 App Routing (`apps/self_development/__init__.py`)

**New mode:** ECP meta-analysis

**Trigger keywords:**
- `"ecp"` — e.g., "analyze ecp", "ecp improvements"
- `"platform"` — e.g., "analyze platform", "platform gaps"
- `"core"` — e.g., "improve core", "core modules"

**Response structure:**
```json
{
  "app": "self-development",
  "version": "2.0.0",
  "input": "...",
  "pipeline": [...],
  "result": {
    "mode": "ecp_meta_analysis",
    "ecp_analysis": { ... },
    "capability_proposals": [ ... ],
    "improvement_proposals": [ ... ],
    "requires_approval": true
  },
  "metadata": {
    "category": "self-development",
    "capabilities_used": [
      "platform-analysis",
      "capability-proposal",
      "cross-pack-learning",
      "governance",
      "approval-management"
    ]
  }
}
```

---

## 4. Testing Plan

### 4.1 Unit Tests (`tests/test_self_development_ecp.py`)

| Test | Description |
|------|-------------|
| `test_analyze_ecp_returns_platform_metrics` | Verifies analyze_ecp returns all required keys |
| `test_propose_capabilities_returns_proposals` | Verifies proposals have correct structure and non-empty |
| `test_propose_improvements_returns_improvements` | Verifies improvements have correct structure |
| `test_app_run_ecp_mode` | Verifies app.run switches to ECP mode on trigger keywords |

### 4.2 Integration Tests
- Test via `/api/v1/capabilities/self-development/execute` endpoint
- Test with frontend generic capability workspace
- Verify approval workflow for proposed capabilities/improvements

### 4.3 Test Results
- All 4 new tests pass (verified 2026-10-03)
- Existing 2 tests still pass (backward compatibility)

---

## 5. Known Issues & Future Work

### 5.1 Current Limitations
1. **Core module counting returns 0** — `backend/app/core/*.py` filtering needs refinement
2. **Proposals are static** — Candidates hardcoded in `ecp_analyzer.py`, not dynamically generated from actual code analysis
3. **No actual code extraction** — Patterns detected but not extracted into refactorable patches
4. **No persistence** — Proposals not saved to database for approval workflow
5. **No frontend integration** — ECP mode only accessible via API, not in dedicated UI

### 5.2 Future Enhancements
1. **Dynamic candidate generation** — Use LLM to analyze codebase and propose capabilities dynamically
2. **Patch generation for ECP** — Generate actual code patches for proposed improvements
3. **Persistence layer** — Save proposals to database with approval workflow
4. **Frontend ECP workspace** — Dedicated UI for ECP meta-analysis
5. **Cross-pack refactoring** — Actually extract shared patterns into core modules
6. **Benchmark integration** — Propose capabilities based on benchmark gaps
7. **Real-case generation** — Propose capabilities based on missing real-case coverage

---

## 6. Files Changed

| File | Status | Description |
|------|--------|-------------|
| `apps/self_development/schemas.py` | ✅ Modified | Added ECPPlatformAnalysis, CapabilityProposal, ImprovementProposal, CrossPackPattern |
| `apps/self_development/ecp_analyzer.py` | ✅ Created | New ECP platform analyzer module |
| `apps/self_development/engine.py` | ✅ Modified | Added analyze_ecp, propose_capabilities, propose_improvements |
| `apps/self_development/worker.py` | ✅ Modified | Added ECP analysis delegation methods |
| `apps/self_development/__init__.py` | ✅ Modified | Added ECP meta-analysis routing |
| `tests/test_self_development_ecp.py` | ✅ Created | New tests for ECP meta-analysis |

---

## 7. Verification

### 7.1 Test Execution
```bash
python -m pytest tests/test_self_development.py -v
python -m pytest tests/test_self_development_ecp.py -v
```

### 7.2 Test Results
- `tests/test_self_development.py`: 2 passed ✅
- `tests/test_self_development_ecp.py`: 4 passed ✅

### 7.3 Manual Verification
```python
from apps.self_development import get_app

app = get_app()

# ECP mode
result = await app.run("analyze ecp platform improvements", context={})
print(result["result"]["mode"])  # "ecp_meta_analysis"

# Regular mode still works
result = await app.run("analyze my project", context={})
print(result["result"]["mode"])  # "project_analysis"
```

---

## 8. Next Steps

1. **Fix core module counting** — Refine `ECPAnalyzer.analyze()` to correctly count `backend/app/core/*.py`
2. **Add persistence** — Store proposals in database for approval workflow
3. **Add frontend integration** — Create ECP meta-analysis UI in workspace
4. **Dynamic proposals** — Replace static candidate list with LLM-based analysis
5. **Patch generation** — Generate actual refactoring patches for cross-pack patterns
6. **Benchmark integration** — Propose capabilities based on benchmark gaps
7. **Approval workflow** — Connect proposals to existing governance system

---

## 9. Approval

| Role | Name | Status |
|------|------|--------|
| **Requested by** | User | ✅ Requested |
| **Implemented by** | Kilo | ✅ Implemented |
| **Reviewed by** | — | ⏳ Pending |
| **Approved by** | — | ⏳ Pending |

---

**Next Review:** 2026-10-10  
**Related Docs:** `docs/capabilities/self-development.md`, `docs/plans/SimplAI_Parity_Plan.md`
