import logging
from dataclasses import dataclass, field
from typing import Any
from enum import Enum

logger = logging.getLogger(__name__)


class PluginManifestVersion:
    V1_0 = "1.0"
    CURRENT = V1_0


class PluginManifestSecurityLevel(str, Enum):
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

    def validate_compatibility(self, manifest: PluginManifest, runtime_version: str, sdk_version: str) -> dict[str, Any]:
        return {
            "runtime_compatible": manifest.required_runtime == runtime_version or runtime_version >= manifest.required_runtime,
            "sdk_compatible": manifest.required_sdk == sdk_version or sdk_version >= manifest.required_sdk,
            "contracts": list(manifest.required_contracts.keys()),
        }


plugin_manifest_registry = PluginManifestRegistry()
