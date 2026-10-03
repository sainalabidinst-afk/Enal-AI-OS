"""
Tests for backend/app/core/factory_registry.py — RFC-0001 Factory Registry.
"""

import pytest

from backend.app.core.base_app import BaseApp
from backend.app.core.factory_registry import FactoryRegistry


class _TestApp(BaseApp):
    name = "test_app"
    version = "1.0.0"

    def get_capabilities(self):
        return [{"id": "test", "name": "Test"}]

    def execute(self, task):
        return {"status": "ok"}

    def validate_input(self, task):
        return True


def get_app(config=None):
    return _TestApp(config)


class TestFactoryRegistry:
    @pytest.fixture
    def registry(self, monkeypatch):
        monkeypatch.setattr(FactoryRegistry, "_instance", None)
        reg = FactoryRegistry()
        yield reg
        reg.clear()

    def test_register_and_get(self, registry):
        registry.register("test_pack", get_app, {"name": "test_pack"})
        assert "test_pack" in registry.list_packs()
        app = registry.get_app("test_pack")
        assert isinstance(app, _TestApp)
        assert app.name == "test_app"

    def test_get_app_unknown_returns_none(self, registry):
        assert registry.get_app("nonexistent") is None

    def test_get_app_cached(self, registry):
        registry.register("cached_pack", get_app, {})
        app1 = registry.get_app("cached_pack")
        app2 = registry.get_app("cached_pack")
        assert app1 is app2

    def test_is_loaded(self, registry):
        assert not registry.is_loaded("test_pack")
        registry.register("test_pack", get_app, {})
        registry.get_app("test_pack")
        assert registry.is_loaded("test_pack")

    def test_discover_packs(self, registry, tmp_path):
        pack_dir = tmp_path / "my_pack"
        pack_dir.mkdir()
        (pack_dir / "__init__.py").write_text("def get_app():\n    return None\n")

        packs = registry.discover_packs([str(tmp_path)])
        assert "my_pack" in packs

    def test_discover_ignores_underscore_dirs(self, registry, tmp_path):
        for name in ["__pycache__", ".hidden", "_internal"]:
            d = tmp_path / name
            d.mkdir()
            (d / "__init__.py").write_text("")

        packs = registry.discover_packs([str(tmp_path)])
        assert len(packs) == 0

    def test_load_pack_from_apps(self, registry):
        # Should be able to load an existing pack from apps/
        app = registry.load_pack("code_engineer")
        assert app is not None
        assert app.name == "code-engineer"

    def test_get_pack_info(self, registry):
        registry.register("info_pack", get_app, {"name": "info_pack", "version": "1.2.0"})
        info = registry.get_pack_info("info_pack")
        assert info is not None
        assert info["version"] == "1.2.0"

    def test_clear_resets_state(self, registry):
        registry.register("pack1", get_app, {})
        registry.clear()
        assert len(registry.list_packs()) == 0

    def test_circular_import_detection_no_cycle(self, registry):
        # code_engineer doesn't have circular imports
        cycle = registry._check_circular("code_engineer")
        assert cycle == []

    def test_instance_singleton(self):
        r1 = FactoryRegistry.instance()
        r2 = FactoryRegistry.instance()
        assert r1 is r2
