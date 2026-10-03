# RFC-0053: Bulk, Scheduled & Evaluation

<!-- DOCUMENT_METADATA_START -->
**Pemilik:** Tim Platform
**Canonical Owner:** Lead Platform Engineer
**Terakhir Diverifikasi:** 2026-10-03
**Versi:** 1.0.0
**Status:** Draft → Proposed
**SSOT:** Rancangan bulk execution, scheduled triggers, webhooks, dan evaluation framework untuk ECP
<!-- DOCUMENT_METADATA_END -->

## Abstrak

RFC ini mendefinisikan Bulk, Scheduled & Evaluation untuk ECP, yang menyediakan:
1. Bulk execution dengan concurrency control
2. Scheduled triggers (cron-like)
3. Webhook notifications
4. Evaluation framework untuk quality scoring

## Konteks

ECP memerlukan kemampuan untuk:
1. Menjalankan banyak task secara bersamaan (bulk run)
2. Menjadwalkan task berdasarkan cron expression
3. Mengirim webhook notifications saat task complete
4. Mengevaluasi kualitas output agent/tool

## Keputusan

### 1. Bulk Executor

**Core Components:**
- `BulkExecutor` — Execute bulk tasks dengan concurrency control
- `AsyncQueue` — Priority queue untuk async tasks

**Features:**
- Max concurrency control
- Progress tracking
- Error handling per task

### 2. Scheduler Service

**Core Components:**
- `SchedulerService` — Manage scheduled executions
- `ScheduledJob` — Job definition dengan cron, payload, next_run

**Features:**
- Cron-like scheduling
- Job list/cancel
- Next run calculation

### 3. Webhook Service

**Core Components:**
- `WebhookService` — Send webhook notifications

**Features:**
- Send webhook ke URL
- Payload customization
- Retry logic (future)

### 4. Evaluation Framework

**Core Components:**
- `EvaluatorEngine` — Run evaluations
- `QualityScorer` — Score agent/tool outputs
- `ScheduledEvaluator` — Run evals on schedule
- `MetricDetails` — Per-metric deep-dive

**Metrics:**
- Relevance
- Accuracy
- Coherence
- Completeness

### 5. Frontend Route

`/bulk-evaluation` — `BulkEvaluationPage` rendering `BulkRun`, `ScheduleConfig`, `EvaluationDashboard`

### 6. API Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/api/v1/bulk/run` | Run bulk tasks |
| POST | `/api/v1/schedule` | Create schedule |
| GET | `/api/v1/schedule` | List schedules |
| DELETE | `/api/v1/schedule/{job_id}` | Delete schedule |
| POST | `/api/v1/webhooks/send` | Send webhook |
| POST | `/api/v1/evaluate` | Evaluate output |
| GET | `/api/v1/evaluate/results` | Get evaluation results |

## Implementasi

### Frontend Components

- `BulkRun.tsx` — Bulk execution UI
- `ScheduleConfig.tsx` — Schedule management UI
- `EvaluationDashboard.tsx` — Evaluation results UI
- `MetricDetails.tsx` — Per-metric analytics UI

### Backend Modules

- `backend/app/core/bulk_executor.py` — BulkExecutor
- `backend/app/core/scheduler_service.py` — SchedulerService
- `backend/app/core/webhook_service.py` — WebhookService
- `backend/app/core/async_queue.py` — AsyncQueue
- `backend/app/core/evaluator_engine.py` — EvaluatorEngine
- `backend/app/core/quality_scorer.py` — QualityScorer
- `backend/app/core/scheduled_evaluator.py` — ScheduledEvaluator
- `backend/app/core/metric_details.py` — MetricDetails
- `backend/app/api/bulk_evaluation.py` — API endpoints

## Dependencies

- RFC-0046: Visual Builder Foundation
- RFC-0047: Visual Agent Builder
- RFC-0048: Visual Tool Builder

## Testing

- TypeScript: 0 errors
- Ruff: 0 errors
- Mypy: 0 errors

## References

- SimplAI Bulk/Scheduled: https://simplai.ai/docs/bulk-and-scheduled/
- SimplAI Evaluation: https://simplai.ai/docs/evaluation/
