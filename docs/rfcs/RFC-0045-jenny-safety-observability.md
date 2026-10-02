# RFC-0045: Jenny Safety & Observability

- **Status**: Accepted
- **Date**: 2026-10-02
- **Authors**: Agent Team
- **Related**: ADR-025, RFC-0043, RFC-0044

## Context

After Phase 1 (voice) and Phase 2 (action connectors), Jenny can now act on the user's behalf. This introduces safety risks:

1. **Unauthorized actions** — high-risk actions (trading, system config, IoT) could be triggered maliciously or by misclassification.
2. **Anomalies** — cost spikes, latency spikes, error rate anomalies in cognitive pipeline.
3. **Safety violations** — hallucination, toxicity, bias in voice responses.

## Decision

Implement a **Consent & Safety Manager** with risk-based action classification and anomaly detection.

### Risk-Based Action Classification

| Level | Actions | Consent Required |
|-------|---------|-----------------|
| **Low** | read_file, list_directory, list_events, list_emails, get_state | No — auto-approved |
| **Medium** | write_file, send_email, create_event, turn_on, turn_off, set_brightness, set_temperature | Yes — user confirmation |
| **High** | trading, system_config, system_restart, factory_reset | Yes — explicit approval + timeout |

### Consent Flow

```
1. Action Layer calls ConsentManager.request(action_type, params, session_id)
2. Returns ConsentRequest with request_id, risk_level, timeout_seconds
3. Frontend shows consent dialog (consent-dialog.tsx)
4. User approves/denies via POST /consent/respond
5. If expired before response → status = EXPIRED
```

### Anomaly Detection

Added `anomaly_detect()` and `check_span_anomaly()` methods to existing `Observability` class:

- **Z-score detection**: flags values > 2 std dev from mean of history
- **Baseline deviation**: flags values > 1.5x baseline
- **Span anomaly**: checks error, latency > 5s, tokens > 8000

### API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/consent/request` | Create consent request |
| POST | `/consent/respond` | Approve or deny |
| GET | `/consent/pending` | List pending requests |
| GET | `/consent/history` | View consent history |
| GET | `/consent/classify` | Classify risk of an action |

## Architecture

```
backend/app/core/
├── consent.py          # ConsentManager, ConsentRequest, RiskLevel, classify_risk
├── observability.py    # +anomaly_detect, +check_span_anomaly, +AnomalyResult, +AnomalyType

backend/app/api/
└── consent.py          # Consent API endpoints
```

## Consequences

- All medium/high-risk actions are gated behind consent — user must explicitly approve.
- Consent requests auto-expire after 30s (configurable).
- Anomalies are logged but don't block — suitable for alerting/detection.
- Existing `Observability` class extended without breaking changes.
- Tests: 23 tests in `backend/tests/test_consent_safety.py`, all passing.
- MyPy: 0 errors. Ruff: 0 errors.
