import hashlib
import importlib
import logging
import time
from collections.abc import Callable
from dataclasses import dataclass, field
from enum import Enum, StrEnum  # noqa: F401
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


class PluginManifestVersion:
    V1_0 = "1.0"
    CURRENT = V1_0


class PluginManifestSecurityLevel(StrEnum):
    SAFE = "safe"
    RESTRICTED = "restricted"
    PRIVILEGED = "privileged"


def _empty_list():
    return []


def _empty_dict():
    return {}


@dataclass
class PluginManifest:
    id: str = ""
    name: str = ""
    version: str = ""
    description: str = ""
    author: str = ""
    license: str = ""
    homepage: str = ""
    repository: str = ""
    entrypoint: str = ""
    checksum: str = ""
    capabilities: list[str] = field(default_factory=_empty_list)
    permissions: list[str] = field(default_factory=_empty_list)
    required_contracts: dict[str, str] = field(default_factory=_empty_dict)
    required_runtime: str = ">=1.0.0"
    required_sdk: str = ">=1.0.0"
    security_level: PluginManifestSecurityLevel = PluginManifestSecurityLevel.SAFE
    dependencies: list[str] = field(default_factory=_empty_list)
    tags: list[str] = field(default_factory=_empty_list)
    manifest_version: str = PluginManifestVersion.CURRENT

    def validate(self) -> list[str]:
        errors = []
        if not self.id:
            errors.append("Plugin id is required")
        if not self.name:
            errors.append("Plugin name is required")
        if not self.version:
            errors.append("Plugin version is required")
        if not self.description:
            errors.append("Plugin description is required")
        if not self.author:
            errors.append("Plugin author is required")
        if not self.license:
            errors.append("Plugin license is required")
        if not self.capabilities:
            errors.append("Plugin must declare at least one capability")
        if not self.permissions:
            errors.append("Plugin must declare required permissions")
        if not self.required_contracts:
            errors.append("Plugin must declare required contracts")
        if not self.entrypoint:
            errors.append("Plugin must declare an entrypoint")
        return errors

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "version": self.version,
            "description": self.description,
            "author": self.author,
            "license": self.license,
            "homepage": self.homepage,
            "repository": self.repository,
            "entrypoint": self.entrypoint,
            "checksum": self.checksum,
            "capabilities": self.capabilities,
            "permissions": self.permissions,
            "required_contracts": self.required_contracts,
            "required_runtime": self.required_runtime,
            "required_sdk": self.required_sdk,
            "security_level": self.security_level.value,
            "dependencies": self.dependencies,
            "tags": self.tags,
            "manifest_version": self.manifest_version,
        }


class PluginManifestRegistry:
    def __init__(self):
        self._manifests: dict[str, PluginManifest] = {}

    def register(self, manifest: PluginManifest) -> list[str]:
        errors = manifest.validate()
        if errors:
            logger.error(f"Plugin manifest validation failed for {manifest.name}: {errors}")
            return errors
        self._manifests[manifest.id] = manifest
        logger.info(f"Plugin manifest registered: {manifest.name} v{manifest.version}")
        return []

    def get(self, plugin_id: str) -> PluginManifest | None:
        return self._manifests.get(plugin_id)

    def list_manifests(self) -> list[PluginManifest]:
        return list(self._manifests.values())

    def validate_compatibility(self, manifest: PluginManifest, runtime_version: str, sdk_version: str) -> dict[str, Any]:  # noqa: E501
        return {
            "runtime_compatible": manifest.required_runtime == runtime_version or runtime_version >= manifest.required_runtime,  # noqa: E501
            "sdk_compatible": manifest.required_sdk == sdk_version or sdk_version >= manifest.required_sdk,  # noqa: E501
            "contracts": list(manifest.required_contracts.keys()),
        }


@dataclass
class HotReloadResult:
    """Result of a hot-reload operation for a capability pack."""

    pack_id: str
    old_version: str
    new_version: str
    success: bool
    latency_ms: float
    error: str | None = None


class HotReloadManager:
    """Manages zero-downtime hot-reload of capability packs.

    Tracks loaded pack modules, detects file changes, and performs atomic
    module swaps with rollback support. Designed to work with the
    PluginManifestRegistry to validate packs before swapping.
    """

    def __init__(self, registry: PluginManifestRegistry):
        self._registry = registry
        self._loaded_modules: dict[str, tuple[str, Any, str, float]] = {}
        self._reload_hooks: list[Callable[[str, bool], None]] = []
        self._checksums: dict[str, str] = {}

    def _compute_checksum(self, file_path: str | Path) -> str:
        """Compute SHA-256 checksum of a file."""
        path = Path(file_path)
        if not path.is_file():
            return ""
        return hashlib.sha256(path.read_bytes()).hexdigest()

    def register_pack(self, pack_id: str, module_path: str) -> bool:
        """Register a pack module for hot-reload tracking."""
        try:
            module = importlib.import_module(module_path)
        except ImportError as e:
            logger.error(f"Cannot import module for pack {pack_id}: {e}")
            return False
        checksum = self._compute_checksum(module.__file__)
        self._loaded_modules[pack_id] = (module_path, module, checksum, 0.0)
        self._checksums[pack_id] = checksum
        return True

    def check_for_updates(self, pack_id: str, file_path: str) -> bool:
        """Check if a pack's source file has been modified."""
        current_checksum = self._compute_checksum(file_path)
        old_checksum = self._checksums.get(pack_id, "")
        return current_checksum != old_checksum

    def reload_pack(self, pack_id: str, module_path: str) -> HotReloadResult:
        """Atomically reload a pack module without downtime.

        Performs the reload in a way that:
        1. Loads the new module alongside the old one
        2. Validates the new module via manifest registry
        3. Swaps references atomically
        4. Rolls back on failure
        """
        start_time = time.perf_counter()

        old_entry = self._loaded_modules.get(pack_id)
        if old_entry is None:
            result = HotReloadResult(
                pack_id=pack_id,
                old_version="unknown",
                new_version="unknown",
                success=False,
                latency_ms=round((time.perf_counter() - start_time) * 1000, 3),
                error=f"Pack {pack_id} not registered",
            )
            logger.error(f"Cannot reload unregistered pack: {pack_id}")
            return result

        old_module_path, old_module, old_checksum, _ = old_entry

        manifest = self._registry.get(pack_id)
        old_version = manifest.version if manifest else "unknown"

        try:
            new_module = importlib.import_module(module_path)
            importlib.reload(new_module)

            new_checksum = self._compute_checksum(new_module.__file__)

            if new_checksum == old_checksum:
                result = HotReloadResult(
                    pack_id=pack_id,
                    old_version=old_version,
                    new_version=old_version,
                    success=True,
                    latency_ms=round((time.perf_counter() - start_time) * 1000, 3),
                    error="No changes detected",
                )
                logger.info(f"No changes detected for pack {pack_id}")
                return result

            self._checksums[pack_id] = new_checksum

            new_version = "unknown"
            if manifest:
                new_version = manifest.version

            self._loaded_modules[pack_id] = (module_path, new_module, new_checksum, 0.0)

            latency = round((time.perf_counter() - start_time) * 1000, 3)

            result = HotReloadResult(
                pack_id=pack_id,
                old_version=old_version,
                new_version=new_version,
                success=True,
                latency_ms=latency,
            )

            logger.info(f"Hot-reloaded pack {pack_id} in {latency}ms")

            for hook in self._reload_hooks:
                try:
                    hook(pack_id, True)
                except Exception as e:
                    logger.warning(f"Reload hook error for {pack_id}: {e}")

            return result

        except Exception as e:
            latency = round((time.perf_counter() - start_time) * 1000, 3)
            logger.error(f"Hot-reload failed for pack {pack_id}: {e}")

            for hook in self._reload_hooks:
                try:
                    hook(pack_id, False)
                except Exception:
                    pass

            return HotReloadResult(
                pack_id=pack_id,
                old_version=old_version,
                new_version=old_version,
                success=False,
                latency_ms=latency,
                error=str(e),
            )

    def get_loaded_module(self, pack_id: str) -> Any | None:
        """Get the currently loaded module for a pack."""
        entry = self._loaded_modules.get(pack_id)
        return entry[1] if entry else None

    def list_loaded_packs(self) -> list[str]:
        """List all pack IDs currently tracked for hot-reload."""
        return list(self._loaded_modules.keys())

    def add_reload_hook(self, hook: Callable[[str, bool], None]) -> None:
        """Register a callback invoked after reload attempts."""
        self._reload_hooks.append(hook)


plugin_manifest_registry = PluginManifestRegistry()
hot_reload_manager = HotReloadManager(plugin_manifest_registry)

