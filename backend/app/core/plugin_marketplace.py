import json
import logging
import os  # noqa: I001
from dataclasses import dataclass, field
from enum import Enum, StrEnum  # noqa: F401
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

_DEFAULT_PLUGINS_DIR = os.path.join(
    os.environ.get("ECP_WORKSPACE_DIR", os.getcwd()),
    ".ecp",
    "plugins",
)


class PluginStatus(StrEnum):
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

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "version": self.version,
            "description": self.description,
            "author": self.author,
            "category": self.category,
            "tags": self.tags,
            "dependencies": self.dependencies,
            "permissions": self.permissions,
            "tools": self.tools,
            "status": self.status.value,
            "downloads": self.downloads,
            "rating": self.rating,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "PluginManifest":
        return cls(
            id=data["id"],
            name=data["name"],
            version=data["version"],
            description=data["description"],
            author=data["author"],
            category=data["category"],
            tags=data.get("tags", []),
            dependencies=data.get("dependencies", []),
            permissions=data.get("permissions", []),
            tools=data.get("tools", []),
            status=PluginStatus(data.get("status", PluginStatus.DRAFT)),
            downloads=data.get("downloads", 0),
            rating=data.get("rating", 0.0),
            metadata=data.get("metadata", {}),
        )


class PluginMarketplace:
    def __init__(self, plugins_dir: str | None = None):
        self._plugins: dict[str, PluginManifest] = {}
        self._installed: dict[str, str] = {}
        self._ratings: dict[str, list[float]] = {}
        self._plugins_dir = Path(plugins_dir) if plugins_dir else Path(_DEFAULT_PLUGINS_DIR)
        self._load_published()

    def _plugin_path(self, plugin_id: str) -> Path:
        safe_id = plugin_id.replace(":", "_").replace("@", "_")
        return self._plugins_dir / f"{safe_id}.json"

    def _load_published(self) -> None:
        if not self._plugins_dir.exists():
            return
        for f in self._plugins_dir.glob("*.json"):
            try:
                data = json.loads(f.read_text(encoding="utf-8"))
                manifest = PluginManifest.from_dict(data)
                self._plugins[manifest.id] = manifest
                if (
                    manifest.status == PluginStatus.INSTALLED
                    if hasattr(PluginStatus, "INSTALLED")
                    else manifest.status == PluginStatus.PUBLISHED
                ):
                    self._installed[manifest.id] = manifest.version
            except Exception as exc:
                logger.warning("Failed to load plugin from %s: %s", f, exc)

    def persist_plugin(self, manifest: PluginManifest) -> Path:
        self._plugins_dir.mkdir(parents=True, exist_ok=True)
        path = self._plugin_path(manifest.id)
        path.write_text(
            json.dumps(manifest.to_dict(), indent=2, ensure_ascii=False), encoding="utf-8"
        )
        logger.info("Persisted plugin manifest: %s -> %s", manifest.id, path)
        return path

    def load_plugin_from_disk(self, plugin_id: str) -> PluginManifest | None:
        path = self._plugin_path(plugin_id)
        if not path.exists():
            return None
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            return PluginManifest.from_dict(data)
        except Exception as exc:
            logger.warning("Failed to load plugin from %s: %s", path, exc)
            return None

    def list_persisted_plugins(self) -> list[PluginManifest]:
        if not self._plugins_dir.exists():
            return []
        results: list[PluginManifest] = []
        for f in self._plugins_dir.glob("*.json"):
            try:
                data = json.loads(f.read_text(encoding="utf-8"))
                results.append(PluginManifest.from_dict(data))
            except Exception:
                continue
        return results


class PluginMarketplace:
    def __init__(self):
        self._plugins: dict[str, PluginManifest] = {}
        self._installed: dict[str, str] = {}
        self._ratings: dict[str, list[float]] = {}

    async def publish(self, manifest: PluginManifest) -> str:
        if manifest.id in self._plugins:
            self._plugins[manifest.id].version = manifest.version
            self._plugins[manifest.id].status = PluginStatus.PUBLISHED
        else:
            self._plugins[manifest.id] = manifest
        self.persist_plugin(manifest)
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

    def list_plugins(
        self, category: str | None = None, status: PluginStatus | None = None
    ) -> list[PluginManifest]:  # noqa: E501
        plugins = list(self._plugins.values())
        if category:
            plugins = [p for p in plugins if p.category == category]
        if status:
            plugins = [p for p in plugins if p.status == status]
        return sorted(plugins, key=lambda p: p.downloads, reverse=True)

    def search(self, query: str) -> list[PluginManifest]:
        query_lower = query.lower()
        return [
            p
            for p in self._plugins.values()
            if query_lower in p.name.lower()
            or query_lower in p.description.lower()
            or query_lower in " ".join(p.tags).lower()
        ]  # noqa: E501

    def get_installed(self) -> list[str]:
        return list(self._installed.keys())

    async def rate(self, plugin_id: str, rating: float):
        plugin = self._plugins.get(plugin_id)
        if plugin and 0 <= rating <= 5:
            self._ratings.setdefault(plugin_id, []).append(rating)
            plugin.rating = sum(self._ratings[plugin_id]) / len(self._ratings[plugin_id])

    def get_categories(self) -> list[str]:
        return sorted(set(p.category for p in self._plugins.values()))

    def get_install_count(self, plugin_id: str) -> int:
        plugin = self._plugins.get(plugin_id)
        return plugin.downloads if plugin else 0


plugin_marketplace = PluginMarketplace()
