"""
RFC-0001 Stable Contract — Factory Registry.

Provides dynamic pack loading via ``get_app()`` without static imports,
circular-import detection, and pack discovery.
"""

from __future__ import annotations

import importlib
import inspect
import logging
import os
import sys
import threading
from collections.abc import Callable
from typing import Any

logger = logging.getLogger(__name__)


class FactoryRegistry:
    """Registry for dynamically discovering and loading Capability Packs.

    Packs expose a module-level ``get_app(config=None) -> BaseApp`` callable.
    The registry discovers packs by scanning directories listed in the
    ``ECP_PACK_PATHS`` environment variable (default: ``apps/``).
    """

    _instance: FactoryRegistry | None = None
    _lock = threading.Lock()

    def __init__(self):
        self._packs: dict[str, dict[str, Any]] = {}
        self._apps: dict[str, Any] = {}
        self._loaders: dict[str, Callable] = {}

    # -- singleton ----------------------------------------------------------

    @classmethod
    def instance(cls) -> FactoryRegistry:
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls()
        return cls._instance

    # -- discovery ----------------------------------------------------------

    @property
    def pack_paths(self) -> list[str]:
        env = os.environ.get("ECP_PACK_PATHS", "apps")
        return [p.strip() for p in env.split(":") if p.strip()]

    def discover_packs(self, search_dirs: list[str] | None = None) -> list[str]:
        """Scan *search_dirs* (default: :attr:`pack_paths`) for pack modules.

        A pack is any directory containing ``skills.yaml`` or ``__init__.py``
        with a ``get_app`` function.
        Returns a list of discovered pack names.
        """
        dirs = search_dirs or self.pack_paths
        discovered: list[str] = []
        for base in dirs:
            base_path = os.path.abspath(base)
            if not os.path.isdir(base_path):
                continue
            for entry in sorted(os.listdir(base_path)):
                if entry.startswith("_") or entry.startswith("."):
                    continue
                full = os.path.join(base_path, entry)
                if not os.path.isdir(full):
                    continue
                init_file = os.path.join(full, "__init__.py")
                skills_file = os.path.join(full, "skills.yaml")
                if os.path.isfile(init_file) or os.path.isfile(skills_file):
                    discovered.append(entry)
        return discovered

    # -- registration -------------------------------------------------------

    def register(self, name: str, factory: Callable, pack_info: dict[str, Any]) -> None:
        """Manually register a pack factory."""
        self._packs[name] = pack_info
        self._loaders[name] = factory
        self._apps.pop(name, None)
        logger.info(f"Registered pack: {name}")

    # -- dynamic loading ----------------------------------------------------

    def _import_pack(self, pack_name: str) -> Any:
        """Import a pack module by name, preferring ``apps.<name>``."""
        candidates = [f"apps.{pack_name}", pack_name]
        last_err: Exception | None = None
        for mod_name in candidates:
            try:
                module = importlib.import_module(mod_name)
                if hasattr(module, "get_app"):
                    return module
            except ImportError as exc:
                last_err = exc
                continue
        if last_err:
            raise last_err
        raise ImportError(f"Pack '{pack_name}' has no get_app() callable")

    def _check_circular(self, pack_name: str) -> list[str]:
        """Detect circular imports by inspecting the module graph."""
        module_name = f"apps.{pack_name}"
        stack: list[str] = []

        def _detect(current: str, seen: set[str]) -> list[str]:
            if current in seen:
                cycle = [c for c in stack if c == current] + [current]
                return cycle if len(cycle) > 1 else []
            seen.add(current)
            stack.append(current)
            try:
                mod = sys.modules.get(current)
                if mod:
                    for attr_name in dir(mod):
                        attr = getattr(mod, attr_name, None)
                        if inspect.ismodule(attr) and hasattr(attr, "__name__"):
                            child = attr.__name__
                            if child.startswith("apps.") and child != current:
                                result = _detect(child, seen.copy())
                                if result:
                                    return result
            except Exception:
                pass
            stack.pop()
            return []

        return _detect(module_name, set())

    def load_pack(self, pack_name: str, config: dict[str, Any] | None = None) -> Any:
        """Load (or return cached) app instance for *pack_name*."""
        if pack_name in self._apps:
            return self._apps[pack_name]

        module = self._import_pack(pack_name)
        factory = getattr(module, "get_app")
        pack_info = {
            "name": pack_name,
            "module": module.__name__,
            "version": getattr(module, "version", "1.0.0"),
        }
        self._packs[pack_name] = pack_info
        self._loaders[pack_name] = factory

        cycle = self._check_circular(pack_name)
        if cycle:
            logger.warning(f"Circular import detected in {pack_name}: {cycle}")

        app = factory() if config is None else factory(config)
        self._apps[pack_name] = app
        return app

    def get_app(self, name: str, config: dict[str, Any] | None = None) -> Any | None:
        """Return an app instance by pack name (RFC contract entry-point)."""
        if name in self._apps:
            return self._apps[name]
        if name in self._loaders:
            try:
                factory = self._loaders[name]
                app = factory() if config is None else factory(config)
                self._apps[name] = app
                return app
            except Exception as exc:
                logger.error(f"Failed to load pack '{name}': {exc}")
                return None
        try:
            return self.load_pack(name, config)
        except Exception as exc:
            logger.error(f"Failed to load pack '{name}': {exc}")
            return None

    # -- queries -----------------------------------------------------------

    def list_packs(self) -> list[str]:
        return list(self._packs.keys())

    def get_pack_info(self, name: str) -> dict[str, Any] | None:
        return self._packs.get(name)

    def is_loaded(self, name: str) -> bool:
        return name in self._apps

    def all_packs_loaded(self) -> dict[str, Any]:
        return dict(self._apps)

    def clear(self) -> None:
        self._packs.clear()
        self._apps.clear()
        self._loaders.clear()


factory_registry = FactoryRegistry.instance()
