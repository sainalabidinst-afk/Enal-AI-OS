# RFC-0044: Jenny Action Connectors

- **Status**: Accepted
- **Date**: 2026-10-02
- **Authors**: Agent Team
- **Related**: ADR-024, RFC-0043

## Context

After Phase 1 (voice interface), Jenny needs the ability to **act** on the user's behalf — reading files, sending emails, checking calendars, and controlling smart home devices. ECP's existing `ConnectorManager` only supports trading/economic exchanges. A separate `ActionConnectorManager` is required for general-purpose system interactions.

## Decision

Implement a new **Action Connector Framework** with 4 initial connectors:

| Connector | Actions | Mode |
|-----------|---------|------|
| FileSystem | read_file, write_file, list_directory, search_files, delete_file, file_info | Local |
| Email | send_email, read_emails, list_emails, search_emails | SMTP/IMAP + Gmail API (lazy) |
| Calendar | create_event, list_events, update_event, delete_event | CalDAV + Google Calendar API (lazy) |
| SmartHome | turn_on, turn_off, set_brightness, set_temperature, get_state | MQTT + Home Assistant API (lazy) |

### Architecture

```
backend/app/connectors/
├── base_action.py       # BaseActionConnector, ActionResult, ActionRequest, ActionConnectorManager
├── file_system.py        # FileSystemConnector
├── email.py              # EmailConnector (SMTP/IMAP + Gmail)
├── calendar.py           # CalendarConnector (CalDAV + Google Calendar)
├── smarthome.py          # SmartHomeConnector (MQTT + HA API)
├── __init__.py           # exports
└── action_tools.py       # ToolRegistry registration for LLM agent tool-calling
```

### API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/actions/execute` | Execute an action via any connector |
| GET | `/actions/connectors` | List all registered connectors |
| POST | `/actions/connect` | Connect/lazy-init a connector |
| POST | `/actions/disconnect` | Disconnect a connector |
| GET | `/actions/connectors/{name}/actions` | List actions for a connector |
| GET | `/actions/types` | List all ActionType enum values |

All endpoints registered under `API_V1_STR` prefix with tags `["actions"]`.

## Consequences

- Connectors use **lazy import** for optional dependencies (aiohttp, paho-mqtt, imaplib).
- All file operations are sandboxed via `safe_path()` path-traversal guard.
- Action tools registered in `ToolRegistry` enable LLM agent tool-calling for voice commands like "Jenny, read my calendar".
- `register_action_tools()` called on app startup via `@app.on_event("startup")`.

## Implementation Notes

- See `backend/app/connectors/base_action.py` for framework design.
- See `backend/app/connectors/action_tools.py` for tool registration functions.
- Tests: 27 tests in `backend/tests/test_connectors.py`, all passing.
- MyPy: 0 errors. Ruff: 0 errors.
