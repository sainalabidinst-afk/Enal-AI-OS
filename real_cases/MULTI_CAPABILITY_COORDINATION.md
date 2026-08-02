

# MULTI_CAPABILITY_COORDINATION

<!-- DOCUMENT_METADATA_START -->
**Owner:** Documentation Team
**Canonical Owner:** Documentation Governance Lead
**Last Verified:** 2026-08-02
**Version:** 1.0.0
**Status:** Active
**SSOT:** Real case study documentation
<!-- DOCUMENT_METADATA_END -->

## Handoff Contract

Standard format between capabilities:
```json
{
    "input": {...},
    "output": {...},
    "metadata": {
        "source_capability": "string",
        "target_capability": "string",
        "timestamp": "ISO"
    },
    "status": "success|failed|pending",
    "error": null | "message"
}
```

---

## Execution Sequencing

Rules:
1. Tasks defined in `ExecutionGraph`
2. Dependencies declared in `dependencies` array
3. Run sequentially in topological order
4. Failure stops downstream tasks
5. Completion requires all tasks to succeed

---

## Failure Propagation

If any task fails:
- Session status â†’ `failed`
- Downstream tasks not executed
- Error logged to telemetry
- Artifact created with error details

---

## Stop Conditions

- All tasks completed
- Any task failed
- Explicit cancellation called
- Timeout exceeded (future)

