# ADR-024: Action Connector Architecture

- **Status**: Accepted
- **Date**: 2026-10-02
- **Deciders**: Agent Team
- **Related**: ADR-003 (BaseConnector pattern), ADR-004 (domain logic in services)

## Context

ECP has `ConnectorManager` in `backend/app/connectors/` supporting trading connectors (Binance, Bybit, OKX, Alpaca). Jenny-voice interaction requires general-purpose action connectors: file I/O, email, calendar, smart home. Reusing the trading `ConnectorManager` would conflate trading domain with system-domain actions.

## Decision

Create a **separate** `ActionConnectorManager` with its own:

- `BaseActionConnector` abstract base class
- `ActionRequest` / `ActionResult` dataclasses
- `ActionType` StrEnum
- `safe_path()` path-traversal guard
- Connector implementations: `FileSystemConnector`, `EmailConnector`, `CalendarConnector`, `SmartHomeConnector`

Each connector:
- Follows the **lazy import pattern** (optional deps: aiohttp, paho-mqtt, imaplib)
- Uses `ActionResult(success, data, error, metadata, executed_at, action, connector)` for structured responses
- Implements `connect()`, `disconnect()`, `execute(action, params)`, `list_actions()`, `get_info()`
- `EmailConnector._send_email` catches SMTP exceptions and wraps in `ActionResult` failure
- All file operations go through `safe_path()` to sandbox to base directory

Tool registration for LLM agent use is in `backend/app/connectors/action_tools.py`, registered on startup.

## Consequences

- Trading and action connectors are fully decoupled — no risk of trading config polluting action APIs.
- New connectors can be added by subclassing `BaseActionConnector` and registering in `ActionConnectorManager._create_connector`.
- `ActionConnectorManager` uses a class-level `_connectors` dict that can be shared across instances (singleton usage via module-level `action_connector_manager`).
- All errors are caught and returned as `ActionResult(success=False, error=str(e))` for API consistency — except in cases where `execute()` itself raises (e.g. unknown connector type).
