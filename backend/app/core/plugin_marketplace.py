import logging
from typing import Any
from dataclasses import dataclass, field
from enum import Enum

logger = logging.getLogger(__name__)


class PluginStatus(str, Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    DEPRECATED = "deprecated"
    BANNED = "banned"


@dataclass
class PluginManifest:
    id: str
    name: str
    version: str
    description: str
    author: str
    category: str
    tags: list[str] = field(default_factory=list)
    dependencies: list[str] = field(default_factory=list)
    permissions: list[str] = field(default_factory=list)
    tools: list[dict[str, Any]] = field(default_factory=list)
    status: PluginStatus = PluginStatus.DRAFT
    downloads: int = 0
    rating: float = 0.0
    metadata: dict[str, Any] = field(default_factory=dict)


class PluginMarketplace:
    def __init__(self):
        self._plugins: dict[str, PluginManifest] = {}
        self._installed: dict[str, str] = {}

    async def publish(self, manifest: PluginManifest) -> str:
        self._plugins[manifest.id] = manifest
        logger.info(f"Plugin published: {manifest.id} v{manifest.version}")
        return manifest.id

    async def install(self, plugin_id: str) -> bool:
        plugin = self._plugins.get(plugin_id)
        if not plugin:
            return False
        if plugin.status != PluginStatus.PUBLISHED:
            return False
        self._installed[plugin_id] = plugin.version
        plugin.downloads += 1
        return True

    async def uninstall(self, plugin_id: str) -> bool:
        if plugin_id in self._installed:
            del self._installed[plugin_id]
            return True
        return False

    def get_plugin(self, plugin_id: str) -> PluginManifest | None:
        return self._plugins.get(plugin_id)

    def list_plugins(self, category: str | None = None, status: PluginStatus | None = None) -> list[PluginManifest]:
        plugins = list(self._plugins.values())
        if category:
            plugins = [p for p in plugins if p.category == category]
        if status:
            plugins = [p for p in plugins if p.status == status]
        return sorted(plugins, key=lambda p: p.downloads, reverse=True)

    def search(self, query: str) -> list[PluginManifest]:
        query_lower = query.lower()
        return [p for p in self._plugins.values() if query_lower in p.name.lower() or query_lower in p.description.lower()]

    def get_installed(self) -> list[str]:
        return list(self._installed.keys())

    async def rate(self, plugin_id: str, rating: float):
        plugin = self._plugins.get(plugin_id)
        if plugin:
            plugin.rating = (plugin.rating + rating) / 2


plugin_marketplace = PluginMarketplace()
