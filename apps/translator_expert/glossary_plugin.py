"""
Translator Expert — Glossary Domain Plugin.

Allows domain-specific glossaries (finance, legal, medical, technical) to be
persisted and distributed as plugins through the Plugin Marketplace.

Each glossary domain plugin serializes its term mappings so they can be
published, installed, versioned, and shared across workspace nodes.
"""

from __future__ import annotations

import json
import logging
import os
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

from backend.app.core.plugin_marketplace import (
    PluginManifest,
    PluginMarketplace,
    PluginStatus,
    plugin_marketplace,
)

logger = logging.getLogger(__name__)


@dataclass
class GlossaryPluginData:
    """Serialized glossary domain data for plugin distribution."""

    domain: str
    language_pairs: dict[str, dict[str, str]] = field(default_factory=dict)
    version: str = "1.0.0"
    source: str = "translator-expert"
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "domain": self.domain,
            "language_pairs": self.language_pairs,
            "version": self.version,
            "source": self.source,
            "created_at": self.created_at,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "GlossaryPluginData":
        return cls(
            domain=data["domain"],
            language_pairs=data.get("language_pairs", {}),
            version=data.get("version", "1.0.0"),
            source=data.get("source", "translator-expert"),
            created_at=data.get("created_at", ""),
            metadata=data.get("metadata", {}),
        )


class GlossaryPluginRegistry:
    """Registry that converts glossary domains to/from marketplace plugins."""

    def __init__(self) -> None:
        self._marketplace: PluginMarketplace | None = None

    def _get_marketplace(self) -> PluginMarketplace:
        if self._marketplace is None:
            self._marketplace = plugin_marketplace
        return self._marketplace

    def build_plugin_id(self, domain: str, version: str = "1.0.0") -> str:
        return f"glossary:{domain}@{version}"

    def glossary_to_plugin(
        self,
        domain: str,
        language_pairs: dict[str, dict[str, str]],
        version: str = "1.0.0",
    ) -> PluginManifest:
        """Convert a glossary domain into a publishable PluginManifest."""
        plugin_data = GlossaryPluginData(
            domain=domain,
            language_pairs=language_pairs,
            version=version,
        )
        plugin_id = self.build_plugin_id(domain, version)

        return PluginManifest(
            id=plugin_id,
            name=f"Glossary: {domain.title()}",
            version=version,
            description=f"Domain glossary for '{domain}' with {len(language_pairs)} language pair(s)",
            author="Translator Expert",
            category="glossary",
            tags=["translator", "glossary", domain, "localization", "i18n"],
            dependencies=[],
            permissions=["read:glossary"],
            tools=[],
            status=PluginStatus.PUBLISHED,
            metadata={
                "glossary_data": json.dumps(plugin_data.to_dict()),
                "language_pairs": list(language_pairs.keys()),
                "total_terms": sum(len(terms) for terms in language_pairs.values()),
            },
        )

    def plugin_to_glossary(self, manifest: PluginManifest) -> GlossaryPluginData | None:
        """Extract glossary data from a published plugin manifest."""
        raw = manifest.metadata.get("glossary_data")
        if raw is None:
            return None
        if isinstance(raw, str):
            return GlossaryPluginData.from_dict(json.loads(raw))
        if isinstance(raw, dict):
            return GlossaryPluginData.from_dict(raw)
        return None

    async def publish_glossary(
        self,
        domain: str,
        language_pairs: dict[str, dict[str, str]],
        version: str = "1.0.0",
    ) -> str:
        """Publish a glossary domain as a marketplace plugin."""
        manifest = self.glossary_to_plugin(domain, language_pairs, version)
        plugin_id = await self._get_marketplace().publish(manifest)
        logger.info("Published glossary plugin: %s", plugin_id)
        return plugin_id

    async def install_glossary(self, plugin_id: str) -> GlossaryPluginData | None:
        """Install a glossary plugin and return its data."""
        manifest = self._get_marketplace().get_plugin(plugin_id)
        if manifest is None:
            return None
        if manifest.status != PluginStatus.PUBLISHED:
            return None
        installed = await self._get_marketplace().install(plugin_id)
        if not installed:
            return None
        return self.plugin_to_glossary(manifest)

    def list_glossary_plugins(self) -> list[PluginManifest]:
        """List all published glossary plugins."""
        return self._get_marketplace().list_plugins(category="glossary", status=PluginStatus.PUBLISHED)

    def get_installed_glossaries(self) -> list[GlossaryPluginData]:
        """Return data for all installed glossary plugins."""
        installed_ids = self._get_marketplace().get_installed()
        results: list[GlossaryPluginData] = []
        for plugin_id in installed_ids:
            manifest = self._get_marketplace().get_plugin(plugin_id)
            if manifest and manifest.category == "glossary":
                data = self.plugin_to_glossary(manifest)
                if data:
                    results.append(data)
        return results


glossary_plugin_registry = GlossaryPluginRegistry()


def persist_glossary_to_file(plugin_data: GlossaryPluginData, directory: str) -> str:
    """Persist a glossary plugin data to a JSON file for offline distribution."""
    os.makedirs(directory, exist_ok=True)
    filename = f"glossary_{plugin_data.domain}.json"
    path = os.path.join(directory, filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(plugin_data.to_dict(), f, indent=2, ensure_ascii=False)
    logger.info("Persisted glossary plugin to %s", path)
    return path


def load_glossary_from_file(path: str) -> GlossaryPluginData:
    """Load glossary plugin data from a JSON file."""
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return GlossaryPluginData.from_dict(data)


__all__ = [
    "GlossaryPluginData",
    "GlossaryPluginRegistry",
    "glossary_plugin_registry",
    "persist_glossary_to_file",
    "load_glossary_from_file",
]
