<!-- BILINGUAL_DOCS_START -->
## Bahasa Indonesia / English


### Ringkasan / Summary
Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.
> Terjemahan Indonesia: Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.

- Bahasa Indonesia: konten utama tetap dipertahankan dalam dokumen asli, dan bagian ini memberi konteks ringkas dalam bahasa Indonesia.
- English: the main content remains in the original document, and this section provides a concise bilingual context for international readers.

### Informasi Dokumen / Document Info
- File: `docs/AI_PLANNER.md`
- Judul: Ai Planner
- Status: bilingual header added

<!-- BILINGUAL_DOCS_END -->

# AI Planner

## Overview

AI Planner adalah layer strategis yang membuat rencana eksekusi multi-langkah dari goal/vision tingkat tinggi. Planner menggunakan WorkflowCatalog, IntentResolver, TaskPlanner, dan CapabilityGraph untuk menyusun rencana yang optimal.
> Terjemahan Indonesia: AI Planner adalah lapisan strategi yang membuat rencana eksekusi multi-langkah dari tujuan/visi tingkat tinggi. Planner menggunakan WorkflowCatalog, IntentResolver, TaskPlanner, dan CapabilityGraph untuk menyusun rencana yang optimal.

## Flow

```
Goal / Vision
    ↓
AIPlanner.plan_from_goal()
    ↓
├── 1. Analyze goal via IntentRouter (domain, complexity)
├── 2. Decompose into sub-goals (via CapabilityGraph templates)
├── 3. Find matching workflows from Catalog (via IntentResolver)
├── 4. Order steps with dependency chain
├── 5. Estimate duration
└── 6. Return AIPlan
    ↓
AIPlan (plan_id, steps[], status)
    ↓
AIPlanner.execute_plan(plan_id, executor)
    ↓
WorkflowExecutor → Pipeline → Engine
```

## Data Structures

### PlanStep
- `step_id`: Unique identifier
- `step_type`: WORKFLOW, CAPABILITY, SUB_PLAN, DECISION, PARALLEL
- `description`: Human-readable description
- `workflow_id`: Workflow to execute (if type==WORKFLOW)
- `capability_id`: Capability to execute (if type==CAPABILITY)
- `input_data`: Input for this step
- `depends_on`: List of step_ids that must complete first
- `status`: DRAFT → READY → IN_PROGRESS → COMPLETED/FAILED

### AIPlan
- `plan_id`: Unique identifier
- `goal`: Original goal description
- `steps[]`: Ordered execution steps
- `status`: READY → IN_PROGRESS → COMPLETED/FAILED/CANCELLED
- `progress`: 0.0 - 1.0
- `estimated_duration_minutes`: Estimated total time

## Usage

```python
from apps.organization.ai_planner import ai_planner

# Create plan from goal
plan = ai_planner.plan_from_goal(
    "Audit network security and generate compliance report"
)

# Create plan with explicit workflows
plan = ai_planner.plan_with_workflows(
    "Security workflow",
    workflow_ids=["network-audit-flow", "docs-generation-flow"]
)

# Execute plan
from apps.organization.workflow_executor import workflow_executor
result = await ai_planner.execute_plan(plan.plan_id, workflow_executor)

# Get summary
summary = ai_planner.get_plan_summary(plan.plan_id)

# Cancel plan
ai_planner.cancel_plan(plan.plan_id)
```

## Telemetry Events

- `PlanCreated`: When a plan is created
- `PlanStepAssigned`: When a step is assigned for execution
- `PlanExecutionStarted`: When plan execution begins
- `PlanCompleted`: When all steps complete
- `PlanFailed`: When a step fails
