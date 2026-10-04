# Self-Healing & Auto-Remediation Infrastructure

## Responsibility
Detect infrastructure anomalies and execute safe remediation playbooks with consent gating.

## Components
- `AnomalyDetector`
- `RemediationPlanner`
- `ConsentGate`
- `PlaybookExecutor`

## Flow
1. Observability Engine detects anomaly.
2. AnomalyDetector classifies severity.
3. RemediationPlanner generates playbook.
4. If high-risk -> ConsentGate requests approval.
5. PlaybookExecutor executes approved playbook.
6. Audit trail recorded.

## Data Contract
```json
{
  "anomaly_id": "string",
  "severity": "low | medium | high | critical",
  "playbook": "string",
  "requires_consent": true,
  "status": "pending | approved | executed | failed"
}
```

## VS Code Deliverables
- Add `apps/sre_engineer/anomaly_detector.py`
- Add `apps/sre_engineer/remediation_planner.py`
- Add `apps/sre_engineer/playbook_executor.py`
- Update `backend/app/core/observability.py` to emit anomaly events.
