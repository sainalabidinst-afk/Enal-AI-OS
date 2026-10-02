# ADR-025: Consent & Permission Architecture

- **Status**: Accepted
- **Date**: 2026-10-02
- **Deciders**: Agent Team
- **Related**: ADR-024 (Action Connector Architecture), RFC-0044, RFC-0045

## Context

Jenny's voice-first interaction triggers real-world actions (email, calendar, smart home). Each action must be classified by safety risk and routed through an appropriate consent flow:

- Low-risk read-only actions should be auto-approved for smooth UX.
- Medium-risk actions (writing files, sending emails) require a confirmation dialog.
- High-risk actions (trading, system config, IoT control) require explicit approval with timeout.

## Decision

Implement a `ConsentManager` with:

1. **Risk classification** — `classify_risk()` function maps action types to `RiskLevel.LOW|MEDIUM|HIGH` using predefined frozensets. Unknown actions default to MEDIUM for safety.

2. **Consent lifecycle** — `ConsentRequest` dataclass tracks status (PENDING → APPROVED|DENIED|EXPIRED) with `created_at`, `expires_at`, `timeout_seconds` (default 30s). Uses `>=` comparison for expiry check.

3. **Manager API** — `ConsentManager` provides `request()`, `approve()`, `deny()`, `check_timeout()`, `get_pending_count()`, `get_history()`, `cleanup()`.

4. **Storage** — In-memory dict for active requests + deque (maxlen=1000) for history. Module-level singleton `consent_manager`.

5. **API layer** — REST endpoints in `backend/app/api/consent.py` using FastAPI `APIRouter`, registered under `/api/v1/consent`.

6. **Frontend contract** — Frontend polls `GET /consent/pending` or receives WebSocket notification (Phase 1 WebSocket pattern). User approval via `POST /consent/respond`.

## Consequences

- **Pros**: Simple, no DB required for basic flow. Risk classification is deterministic and auditable.
- **Cons**: In-memory storage is lost on restart. For production, persist to DB with TTL.
- **Security**: Consent request IDs use UUID4 (unpredictable). All requests logged at INFO/WARNING level.
- **Future**: Add biometric verification for high-risk actions, integrate with existing `Observability` anomaly detection.
