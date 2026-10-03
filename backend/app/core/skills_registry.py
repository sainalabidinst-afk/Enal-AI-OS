"""
RFC-0001 Stable Contract — Skills Registry.

Parses and validates ``skills.yaml`` manifests that declare each
Capability Pack's capabilities, dependencies, pipeline stages, and
metadata using the schema defined in RFC-0001 § Skema Skills.yaml.
"""

from __future__ import annotations

import logging
import os
from pathlib import Path
from typing import Any

import yaml

from backend.app.core.schemas import (
    CapabilityEntry,
    CapabilityPackConfig,
    ComplianceReport,
    PipelineStage,
)

logger = logging.getLogger(__name__)


class SkillsRegistry:
    """Registry for pack ``skills.yaml`` manifests.

    Supports:
      - Discovering packs by scanning a base directory
      - Parsing and validating manifests against the RFC schema
      - Looking up capabilities by pack or pack by capability
      - Resolving dependency graphs (circular detection)
    """

    def __init__(self):
        self._packs: dict[str, CapabilityPackConfig] = {}
        self._capability_to_pack: dict[str, str] = {}
        self._base_dirs: list[str] = ["apps"]

    # -- configuration ------------------------------------------------------

    def configure(self, base_dirs: list[str]) -> None:
        self._base_dirs = base_dirs

    # -- discovery & loading ------------------------------------------------

    def discover(self, base_dirs: list[str] | None = None) -> list[str]:
        dirs = base_dirs or self._base_dirs
        found: list[str] = []
        for base in dirs:
            base_path = Path(base)
            if not base_path.is_dir():
                continue
            for entry in sorted(os.listdir(base_path)):
                if entry.startswith("__") or entry.startswith("."):
                    continue
                pack_dir = base_path / entry
                if not pack_dir.is_dir():
                    continue
                if self.has_manifest(str(pack_dir)):
                    found.append(entry)
        return found

    @staticmethod
    def has_manifest(pack_path: str) -> bool:
        return os.path.isfile(os.path.join(pack_path, "skills.yaml"))

    def load_pack(self, pack_path: str) -> CapabilityPackConfig | None:
        """Load and validate a single pack manifest from *pack_path*."""
        manifest_file = os.path.join(pack_path, "skills.yaml")
        if not os.path.isfile(manifest_file):
            logger.warning(f"No skills.yaml in {pack_path}")
            return None
        return self.load_manifest(manifest_file)

    def load_manifest(self, manifest_path: str) -> CapabilityPackConfig | None:
        """Load a skills.yaml manifest from *manifest_path*, validating via Pydantic."""
        with open(manifest_path, encoding="utf-8") as f:
            raw = yaml.safe_load(f) or {}

        try:
            pack_cfg = self._parse_manifest(raw)
        except Exception as exc:
            logger.error(f"Manifest validation failed for {manifest_path}: {exc}")
            return None
        if pack_cfg:
            self._register(pack_cfg)
        return pack_cfg

    def _parse_manifest(self, raw: dict[str, Any]) -> CapabilityPackConfig | None:
        """Parse a raw YAML dict into a validated CapabilityPackConfig.

        Returns ``None`` if the ``capability_pack`` key is absent.
        Raises ``ValidationError`` if Pydantic validation fails (so callers
        can capture field-specific errors).
        """
        if "capability_pack" not in raw:
            logger.warning("Manifest missing 'capability_pack' key")
            return None

        pack = raw["capability_pack"]
        cfg = CapabilityPackConfig(**pack)
        return cfg

    def _register(self, cfg: CapabilityPackConfig) -> None:
        self._packs[cfg.id] = cfg
        for cap in cfg.capabilities:
            self._capability_to_pack[cap.id] = cfg.id
        logger.info(
            f"Registered pack '{cfg.id}' v{cfg.version} with {len(cfg.capabilities)} capabilities"
        )

    def load_all(self, base_dirs: list[str] | None = None) -> dict[str, CapabilityPackConfig]:
        for pack_name in self.discover(base_dirs):
            for base in base_dirs or self._base_dirs:
                pack_path = os.path.join(base, pack_name)
                if self.has_manifest(pack_path):
                    try:
                        self.load_pack(pack_path)
                    except Exception as exc:
                        logger.error(f"Failed to load pack '{pack_name}': {exc}")
        return dict(self._packs)

    # -- queries -----------------------------------------------------------

    def get_pack(self, pack_id: str) -> CapabilityPackConfig | None:
        return self._packs.get(pack_id)

    def get_capability(self, capability_id: str) -> CapabilityEntry | None:
        for pack in self._packs.values():
            for cap in pack.capabilities:
                if cap.id == capability_id:
                    return cap
        return None

    def get_pack_for_capability(self, capability_id: str) -> CapabilityPackConfig | None:
        pack_id = self._capability_to_pack.get(capability_id)
        return self._packs.get(pack_id) if pack_id else None

    def get_pipeline(self, pack_id: str) -> list[PipelineStage]:
        pack = self._packs.get(pack_id)
        return pack.pipeline if pack else []

    def get_dependencies(self, pack_id: str) -> list[str]:
        pack = self._packs.get(pack_id)
        return pack.dependencies.capabilities if pack else []

    def list_packs(self) -> list[str]:
        return list(self._packs.keys())

    def list_capabilities(self) -> list[str]:
        return list(self._capability_to_pack.keys())

    # -- validation --------------------------------------------------------

    def validate_manifest(self, manifest_path: str) -> ComplianceReport:
        """Validate a manifest file and return a compliance report."""
        pack_id = os.path.basename(manifest_path)
        errors: list[str] = []
        warnings: list[str] = []

        try:
            with open(manifest_path, encoding="utf-8") as f:
                raw = yaml.safe_load(f) or {}
            if "capability_pack" not in raw:
                errors.append("Missing 'capability_pack' top-level key")
                return ComplianceReport(
                    pack_id=pack_id,
                    version="0.0.0",
                    passes=False,
                    errors=errors,
                    warnings=warnings,
                    methods_expected=["capability_pack"],
                    methods_implemented=[],
                )

            pack_cfg = None
            try:
                pack_cfg = self._parse_manifest(raw)
            except Exception as exc:
                errors.append(str(exc))

            if pack_cfg is None:
                if not errors:
                    # _parse_manifest logged the error but didn't raise
                    errors.append("Failed to parse manifest: required field is missing or invalid")
                return ComplianceReport(
                    pack_id=pack_id,
                    version="0.0.0",
                    passes=False,
                    errors=errors,
                    warnings=warnings,
                    methods_expected=[],
                    methods_implemented=[],
                )

            if not pack_cfg.id:
                errors.append("Pack id is required")
            if not pack_cfg.entry_point:
                warnings.append("Pack should declare entry_point")
            if not pack_cfg.capabilities:
                warnings.append("Pack should declare at least one capability")
            if not pack_cfg.pipeline:
                warnings.append("Pack should declare pipeline stages")

            return ComplianceReport(
                pack_id=pack_cfg.id,
                version=pack_cfg.version,
                passes=len(errors) == 0,
                errors=errors,
                warnings=warnings,
                methods_expected=[
                    "capability_pack",
                    "id",
                    "version",
                    "capabilities",
                    "pipeline",
                ],
                methods_implemented=[
                    "capability_pack",
                    "id",
                    "version",
                    "capabilities",
                    "pipeline",
                ],
            )
        except Exception as exc:
            errors.append(f"Validation error: {exc}")
            return ComplianceReport(
                pack_id=pack_id,
                version="0.0.0",
                passes=False,
                errors=errors,
                warnings=warnings,
                methods_expected=[],
                methods_implemented=[],
            )

    def detect_circular_dependencies(self) -> list[list[str]]:
        """Detect circular dependencies between packs.

        Resolves capability dependency IDs to pack IDs via the
        capability-to-pack map, then runs DFS cycle detection.

        Returns a list of cycles, each cycle being a list of pack IDs.
        """
        graph: dict[str, list[str]] = {}
        for pack in self._packs.values():
            resolved: list[str] = []
            for dep_cap in pack.dependencies.capabilities:
                dep_pack = self._capability_to_pack.get(dep_cap)
                if dep_pack and dep_pack != pack.id:
                    resolved.append(dep_pack)
                elif dep_cap in self._packs:
                    resolved.append(dep_cap)
            graph[pack.id] = resolved

        cycles: list[list[str]] = []
        visited: set[str] = set()
        rec_stack: set[str] = set()

        def _dfs(node: str, path: list[str]) -> None:
            visited.add(node)
            rec_stack.add(node)
            path.append(node)
            for neighbor in graph.get(node, []):
                if neighbor not in self._packs:
                    continue
                if neighbor not in visited:
                    _dfs(neighbor, path)
                elif neighbor in rec_stack:
                    idx = path.index(neighbor)
                    cycles.append(path[idx:] + [neighbor])
            path.pop()
            rec_stack.discard(node)

        for pack_id in list(self._packs.keys()):
            if pack_id not in visited:
                _dfs(pack_id, [])

        return cycles

    def clear(self) -> None:
        self._packs.clear()
        self._capability_to_pack.clear()


skills_registry = SkillsRegistry()
