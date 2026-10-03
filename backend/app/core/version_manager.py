"""
RFC-0001 Stable Contract — Version Manager.

Handles backward-compatible contract version changes, semantic
versioning enforcement, and fallback resolution when packs target
different contract versions.
"""

from __future__ import annotations

import logging
from typing import Any

from backend.app.core.schemas import ContractVersion

logger = logging.getLogger(__name__)


class VersionManager:
    """Manages contract version compatibility and fallback (RFC-0001 § Version Manager)."""

    def __init__(self):
        self._current_version = ContractVersion()
        self._compatibility_matrix: dict[str, list[str]] = {
            "1.0.0": ["1.0.0", "1.0.1", "1.1.0", "1.1.1"],
            "1.1.0": ["1.0.0", "1.1.0"],
            "1.2.0": ["1.0.0", "1.1.0", "1.2.0"],
        }
        self._fallback_handlers: dict[str, Any] = {}

    # -- version operations --------------------------------------------------

    @property
    def current_version(self) -> str:
        return self._current_version.VERSION

    def parse_version(self, version_str: str) -> ContractVersion:
        return ContractVersion.parse(version_str)

    def is_backward_compatible(
        self, requested: str | ContractVersion, current: str | ContractVersion | None = None
    ) -> bool:
        """Check if *requested* version is backward-compatible with *current*.

        A newer minor/patch version within the same major is compatible
        with an older version.  Different majors are incompatible.
        """
        req = (
            requested
            if isinstance(requested, ContractVersion)
            else ContractVersion.parse(requested)
        )
        cur = current or self._current_version
        if not isinstance(cur, ContractVersion):
            cur = ContractVersion.parse(cur)
        return req.is_backward_compatible(cur)

    def resolve_version(
        self,
        requested: str,
        available: list[str],
    ) -> str | None:
        """Resolve to the best compatible version from *available*."""
        req = ContractVersion.parse(requested)

        for ver_str in available:
            ver = ContractVersion.parse(ver_str)
            if ver.MAJOR == req.MAJOR and ver.MINOR >= req.MINOR:
                return ver_str

        # Fallback: exact MAJOR match
        for ver_str in available:
            ver = ContractVersion.parse(ver_str)
            if ver.MAJOR == req.MAJOR:
                return ver_str

        return None

    # -- fallback handlers ---------------------------------------------------

    def register_fallback(self, version: str, handler: Any) -> None:
        self._fallback_handlers[version] = handler
        logger.info(f"Registered fallback handler for contract v{version}")

    def get_fallback(self, version: str) -> Any | None:
        return self._fallback_handlers.get(version)

    def has_fallback(self, version: str) -> bool:
        return version in self._fallback_handlers

    # -- compatibility matrix ------------------------------------------------

    def get_compatible_versions(self, version: str) -> list[str]:
        """Return versions that are compatible with *version*."""
        # Check explicit matrix
        if version in self._compatibility_matrix:
            return self._compatibility_matrix[version]

        # Compute based on semantic versioning rules
        req = ContractVersion.parse(version)
        compatible: list[str] = []

        for ver_str in self.list_known_versions():
            ver = ContractVersion.parse(ver_str)
            if ver.MAJOR == req.MAJOR and ver.MINOR >= req.MINOR:
                compatible.append(ver_str)

        return compatible

    def list_known_versions(self) -> list[str]:
        return list(self._compatibility_matrix.keys())

    def check_compatibility(
        self,
        pack_version: str,
        target_version: str | None = None,
    ) -> dict[str, Any]:
        """Check if *pack_version* is compatible with the target runtime version."""
        target = target_version or self.current_version
        compatible = self.is_backward_compatible(pack_version, target)

        return {
            "pack_version": pack_version,
            "target_version": target,
            "compatible": compatible,
            "has_fallback": self.has_fallback(pack_version),
            "action": "load"
            if compatible
            else ("fallback" if self.has_fallback(pack_version) else "reject"),
        }

    # -- enforcement ---------------------------------------------------------

    def enforce_semver(self, version: str) -> bool:
        """Validate that *version* follows semantic versioning (MAJOR.MINOR.PATCH)."""
        try:
            v = ContractVersion.parse(version)
            return v.MAJOR >= 0 and v.MINOR >= 0 and v.PATCH >= 0
        except (ValueError, AttributeError):
            return False

    def check_deprecation(
        self,
        pack_version: str,
        deprecation_schedule: dict[str, str],
    ) -> dict[str, Any]:
        """Check if a pack's version is scheduled for deprecation."""
        target = deprecation_schedule.get(pack_version, "")
        return {
            "pack_version": pack_version,
            "deprecated": target != "",
            "deprecation_target": target,
            "requires_attention": target == "remove",
        }


version_manager = VersionManager()
