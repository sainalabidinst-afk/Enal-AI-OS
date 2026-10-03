"""
RFC-0001 Stable Contract — BaseApp abstract class.

Defines the uniform interface that every Capability Pack must implement.
This is the canonical contract referenced by all pack implementations.
"""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from typing import Any

from backend.app.core.schemas import (
    CONTRACT_VERSION,
    ContractVersion,
)

logger = logging.getLogger(__name__)


class BaseApp(ABC):
    """Abstract base contract for all Capability Packs (RFC-0001 § BaseApp Contract).

    Every pack MUST extend this class and implement all ``@abstractmethod``
    members.  Optional lifecycle hooks have safe no-op defaults.
    """

    contract_version: str = CONTRACT_VERSION.VERSION
    _contract_version: ContractVersion = CONTRACT_VERSION

    def __init__(self, config: dict[str, Any] | None = None):
        self.config: dict[str, Any] = config or {}
        self._event_bus: Any = None
        self._experience_memory: Any = None

    # ------------------------------------------------------------------
    # Abstract contract methods (must be implemented by every pack)
    # ------------------------------------------------------------------

    @abstractmethod
    def get_capabilities(self) -> list[dict[str, Any]]:
        """Return the list of capabilities provided by this pack."""

    @abstractmethod
    def execute(self, task: dict[str, Any]) -> dict[str, Any]:
        """Execute *task* and return a result dictionary."""

    @abstractmethod
    def validate_input(self, task: dict[str, Any]) -> bool:
        """Validate that *task* conforms to the expected input schema."""

    # ------------------------------------------------------------------
    # Optional lifecycle hooks (safe defaults)
    # ------------------------------------------------------------------

    def register_event_handlers(self) -> None:
        """Register handlers for events this pack listens to.

        Override to subscribe to the Event Bus.  Default is a no-op.
        """

    def shutdown(self) -> None:
        """Clean up resources before the pack is unloaded.

        Override for graceful shutdown.  Default is a no-op.
        """

    # ------------------------------------------------------------------
    # Convenience helpers
    # ------------------------------------------------------------------

    @classmethod
    def get_contract_version(cls) -> str:
        """Return the stable-contract version this pack was built against."""
        return cls._contract_version.VERSION

    def to_dict(self) -> dict[str, Any]:
        """Return pack metadata as a plain dict."""
        return {
            "name": getattr(self, "name", type(self).__name__),
            "version": getattr(self, "version", "1.0.0"),
            "contract_version": self.contract_version,
            "capabilities": self.get_capabilities(),
        }


class BaseAppV1(BaseApp):
    """Alias for explicit version targeting."""


__all__ = ["BaseApp", "BaseAppV1"]
