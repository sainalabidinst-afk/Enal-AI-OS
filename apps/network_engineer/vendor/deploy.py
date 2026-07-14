"""
Vendor Deployment Adapters
===========================

Vendor-specific deployment adapters for controlled deployment.
"""

from abc import ABC, abstractmethod
from typing import Any

from apps.network_engineer.vendor.models import NetworkAST


class VendorDeploymentAdapter(ABC):
    """Base class for vendor deployment adapters."""

    vendor_name: str = "unknown"

    @abstractmethod
    async def deploy(self, device_id: str, config: str) -> dict[str, Any]:
        """Deploy configuration to device."""
        raise NotImplementedError

    @abstractmethod
    async def verify(self, device_id: str, checks: list[str]) -> dict[str, Any]:
        """Verify device state after deployment."""
        raise NotImplementedError

    @abstractmethod
    async def rollback(self, device_id: str, backup_id: str) -> dict[str, Any]:
        """Rollback to previous configuration."""
        raise NotImplementedError
