"""
Action Connector Framework
==========================

Provides a unified interface for Jenny to interact with external systems
(File System, Email, Calendar, Smart Home/IoT). Each connector is a thin
adapter — business logic resides in domain services (ADR-003, ADR-004).

ADR-024: Action Connector Architecture — extends BaseConnector pattern
       for general-purpose system interactions beyond trading.

Usage::

    manager = ActionConnectorManager()
    fs = await manager.get_connector("file_system")
    result = await fs.execute("read_file", path="/home/docs/report.pdf")
    email = await manager.get_connector("email")
    await email.execute("send_email", to="team@example.com", subject="Report", body="...")
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


class ActionType(StrEnum):
    """Supported action connector types."""

    FILE_SYSTEM = "file_system"
    EMAIL = "email"
    CALENDAR = "calendar"
    SMART_HOME = "smart_home"
    PAPER = "paper"


@dataclass
class ActionRequest:
    """Request to execute an action on a connector."""

    action: str
    params: dict[str, Any] = field(default_factory=dict)
    connector: str = ""
    requester: str = "janny"


@dataclass
class ActionResult:
    """Result of an action execution."""

    success: bool
    data: dict[str, Any] = field(default_factory=dict)
    error: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    executed_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    action: str = ""
    connector: str = ""


class ActionConnectorError(Exception):
    """Base exception for action connector operations."""


class ActionNotImplementedError(ActionConnectorError):
    """Raised when a connector does not implement the requested action."""


class BaseActionConnector:
    """
    Abstract base class for action connectors.

    Subclasses must implement:
        - connect() / disconnect()
        - execute(action, params) -> ActionResult
        - list_actions() -> list[str]
        - get_info() -> dict[str, Any]
    """

    def __init__(self, connector_type: ActionType = ActionType.FILE_SYSTEM) -> None:
        self.connector_type = connector_type
        self._connected = False
        self._config: dict[str, Any] = {}

    async def connect(self) -> None:
        """Initialize the connector. Must be called before use."""
        raise NotImplementedError

    async def disconnect(self) -> None:
        """Clean up resources."""
        self._connected = False

    async def execute(self, action: str, params: dict[str, Any]) -> ActionResult:
        """Execute an action on the connected system.

        Args:
            action: The action name (e.g. "read_file", "send_email").
            params: Action-specific parameters.

        Returns:
            ActionResult with success status, data, and metadata.
        """
        raise NotImplementedError

    async def list_actions(self) -> list[str]:
        """List available actions for this connector."""
        raise NotImplementedError

    async def get_info(self) -> dict[str, Any]:
        """Get connector status information."""
        return {
            "connector": self.connector_type.value,
            "connected": self._connected,
        }

    @property
    def connected(self) -> bool:
        return self._connected


class ActionConnectorManager:
    """
    Manages action connectors for external system integrations.

    Usage::

        manager = ActionConnectorManager()
        fs = await manager.get_connector("file_system")
        result = await fs.execute("read_file", {"path": "/tmp/test.txt"})
    """

    _connectors: dict[str, BaseActionConnector] = {}

    def __init__(self) -> None:
        self._connectors: dict[str, BaseActionConnector] = {}

    def register(self, connector_name: str, connector: BaseActionConnector) -> None:
        self._connectors[connector_name.lower()] = connector

    async def get_connector(self, connector_name: str) -> BaseActionConnector:
        key = connector_name.lower()
        if key in self._connectors:
            return self._connectors[key]
        return await self._create_connector(connector_name)

    async def _create_connector(self, connector_name: str) -> BaseActionConnector:
        key = connector_name.lower()
        connector_map: dict[str, tuple[str, str, ActionType]] = {
            "file_system": (
                "backend.app.connectors.file_system",
                "FileSystemConnector",
                ActionType.FILE_SYSTEM,
            ),  # noqa: E501
            "email": ("backend.app.connectors.email", "EmailConnector", ActionType.EMAIL),  # noqa: E501
            "calendar": (
                "backend.app.connectors.calendar",
                "CalendarConnector",
                ActionType.CALENDAR,
            ),  # noqa: E501
            "smart_home": (
                "backend.app.connectors.smarthome",
                "SmartHomeConnector",
                ActionType.SMART_HOME,
            ),  # noqa: E501
            "paper": (
                "backend.app.connectors.file_system",
                "FileSystemConnector",
                ActionType.FILE_SYSTEM,
            ),  # noqa: E501
        }

        if key not in connector_map:
            raise ActionConnectorError(f"Unknown action connector type: {connector_name}")

        mod_path, class_name, conn_type = connector_map[key]
        try:
            import importlib

            mod = importlib.import_module(mod_path)
            conn_cls = getattr(mod, class_name)
            connector: BaseActionConnector = conn_cls(connector_type=conn_type)
            self._connectors[key] = connector
            return connector
        except ImportError as e:
            raise ActionConnectorError(
                f"Action connector '{connector_name}' requires additional packages. "
                f"Install the required dependencies."
            ) from e

    async def list_connectors(self) -> list[dict[str, Any]]:
        results = []
        for name, connector in self._connectors.items():
            results.append(await connector.get_info())
        return results

    async def close_all(self) -> None:
        for connector in self._connectors.values():
            try:
                await connector.disconnect()
            except Exception as e:
                logger.warning("Error disconnecting %s: %s", connector, e)
        self._connectors.clear()


action_connector_manager = ActionConnectorManager()


def safe_path(base_path: str, requested_path: str) -> Path:
    """Resolve and validate a path is within the allowed base directory.

    Prevents path traversal attacks (e.g. ../../etc/passwd).
    """
    base = Path(base_path).resolve()
    target = (base / requested_path).resolve()
    if not str(target).startswith(str(base)):
        raise ActionConnectorError(f"Path '{requested_path}' escapes base directory '{base_path}'")
    return target
