# AI Planner

## Ringkasan

AI Planner adalah lapisan strategi yang membuat rencana eksekusi multi-langkah dari tujuan/visi tingkat tinggi. Planner menggunakan WorkflowCatalog, IntentResolver, TaskPlanner, dan CapabilityGraph untuk menyusun rencana yang optimal.

## Alur

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

## Struktur Data

### PlanStep
- `step_id`: Pengidentifikasi unik
- `step_type`: WORKFLOW, CAPABILITY, SUB_PLAN, DECISION, PARALLEL
- `description`: Deskripsi yang dapat dibaca manusia
- `workflow_id`: Workflow yang akan dijalankan (jika type==WORKFLOW)
- `capability_id`: Capability untuk dieksekusi (jika type==CAPABILITY)
- `input_data`: Input untuk langkah ini
- `depends_on`: Daftar step_id yang harus diselesaikan terlebih dahulu
- `status`: DRAFT → READY → IN_PROGRESS → COMPLETED/FAILED

### AIPlan
- `plan_id`: Pengidentifikasi unik
- `goal`: Deskripsi tujuan asli
- `steps[]`: Langkah-langkah eksekusi yang diurutkan
- `status`: READY → IN_PROGRESS → COMPLETED/FAILED/CANCELED
- `progress`: 0.0 - 1.0
- `estimated_duration_minutes`: Estimasi total waktu

## Penggunaan

```python
from apps.organization.ai_planner import ai_planner

# Buat rencana dari tujuan
plan = ai_planner.plan_from_goal(
    "Audit network security and generate compliance report"
)

# Buat rencana dengan workflow eksplisit
plan = ai_planner.plan_with_workflows(
    "Security workflow",
    workflow_ids=["network-audit-flow", "docs-generation-flow"]
)

# Eksekusi rencana
from apps.organization.workflow_executor import workflow_executor
result = await ai_planner.execute_plan(plan.plan_id, workflow_executor)

# Dapatkan ringkasan
summary = ai_planner.get_plan_summary(plan.plan_id)

# Batalkan rencana
ai_planner.cancel_plan(plan.plan_id)
```

## Telemetry Events

- `PlanCreated`: Saat rencana dibuat
- `PlanStepAssigned`: Ketika sebuah langkah ditetapkan untuk eksekusi
- `PlanExecutionStarted`: Ketika eksekusi rencana dimulai
- `PlanCompleted`: Ketika semua langkah selesai
- `PlanFailed`: Ketika suatu langkah gagal

