# ADR-034: Bulk, Scheduled & Evaluation Architecture

<!-- DOCUMENT_METADATA_START -->
**Pemilik:** Tim Platform
**Canonical Owner:** Lead Platform Engineer
**Terakhir Diverifikasi:** 2026-10-03
**Versi:** 1.0.0
**Status:** Accepted
**SSOT:** Arsitektur bulk execution, scheduled triggers, webhooks, dan evaluation framework
<!-- DOCUMENT_METADATA_END -->

## Abstrak

ADR ini mendokumentasikan keputusan arsitektur untuk Bulk, Scheduled & Evaluation, termasuk BulkExecutor, SchedulerService, WebhookService, dan EvaluatorEngine.

## Konteks

ECP memerlukan kemampuan untuk bulk execution, scheduled tasks, webhooks, dan evaluation framework.

## Keputusan

### 1. Bulk Executor

**Decision:** Semaphore-based concurrency control
**Rationale:**
- Simple dan effective
- Prevent overwhelming system
- Progress tracking built-in

### 2. Scheduler Service

**Decision:** In-memory scheduler dengan cron expressions
**Rationale:**
- Simple untuk MVP
- Cron expressions flexible
- Easy to extend ke distributed scheduler

### 3. Evaluation Framework

**Decision:** QualityScorer dengan criteria-based scoring
**Rationale:**
- Flexible scoring
- Multiple criteria support
- Easy to extend

## Consequences

### Positive
- Concurrent execution control
- Flexible scheduling
- Quality evaluation framework

### Negative
- In-memory scheduler tidak persisten
- Evaluation criteria perlu manual definition

### Neutral
- Uses existing Observability pack untuk metrics

## References

- RFC-0053: Bulk, Scheduled & Evaluation
- SimplAI Bulk/Scheduled: https://simplai.ai/docs/bulk-and-scheduled/
