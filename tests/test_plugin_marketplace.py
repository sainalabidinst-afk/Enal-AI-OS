"""
Tests for Plugin Marketplace
=============================
Tests for plugin discovery, installation, and management.
"""

import pytest


class TestPluginManifest:
    """Tests for PluginManifest."""

    def test_manifest_creation(self):
        from backend.app.core.plugin_marketplace import PluginManifest, PluginStatus
        manifest = PluginManifest(
            id="test-plugin",
            name="Test Plugin",
            version="1.0.0",
            description="A test plugin",
            author="test-author",
            category="testing",
        )
        assert manifest.id == "test-plugin"
        assert manifest.status == PluginStatus.DRAFT


class TestPluginMarketplace:
    """Tests for PluginMarketplace."""

    def test_publish_plugin(self):
        from backend.app.core.plugin_marketplace import PluginMarketplace, PluginManifest, PluginStatus
        mp = PluginMarketplace()
        manifest = PluginManifest(
            id="test-plugin",
            name="Test Plugin",
            version="1.0.0",
            description="A test plugin",
            author="test-author",
            category="testing",
            status=PluginStatus.PUBLISHED,
        )
        import asyncio
        asyncio.run(mp.publish(manifest))
        assert mp.get_plugin("test-plugin") is not None

    def test_install_plugin(self):
        from backend.app.core.plugin_marketplace import PluginMarketplace, PluginManifest, PluginStatus
        mp = PluginMarketplace()
        manifest = PluginManifest(
            id="test-plugin",
            name="Test Plugin",
            version="1.0.0",
            description="A test plugin",
            author="test-author",
            category="testing",
            status=PluginStatus.PUBLISHED,
        )
        import asyncio
        asyncio.run(mp.publish(manifest))
        result = asyncio.run(mp.install("test-plugin"))
        assert result is True
        assert "test-plugin" in mp.get_installed()

    def test_install_unpublished_fails(self):
        from backend.app.core.plugin_marketplace import PluginMarketplace, PluginManifest, PluginStatus
        mp = PluginMarketplace()
        manifest = PluginManifest(
            id="draft-plugin",
            name="Draft Plugin",
            version="1.0.0",
            description="Not published",
            author="test-author",
            category="testing",
            status=PluginStatus.DRAFT,
        )
        import asyncio
        asyncio.run(mp.publish(manifest))
        result = asyncio.run(mp.install("draft-plugin"))
        assert result is False

    def test_uninstall_plugin(self):
        from backend.app.core.plugin_marketplace import PluginMarketplace, PluginManifest, PluginStatus
        mp = PluginMarketplace()
        manifest = PluginManifest(
            id="test-plugin",
            name="Test Plugin",
            version="1.0.0",
            description="A test plugin",
            author="test-author",
            category="testing",
            status=PluginStatus.PUBLISHED,
        )
        import asyncio
        asyncio.run(mp.publish(manifest))
        asyncio.run(mp.install("test-plugin"))
        result = asyncio.run(mp.uninstall("test-plugin"))
        assert result is True
        assert "test-plugin" not in mp.get_installed()

    def test_search_plugins(self):
        from backend.app.core.plugin_marketplace import PluginMarketplace, PluginManifest, PluginStatus
        mp = PluginMarketplace()
        manifest = PluginManifest(
            id="network-plugin",
            name="Network Analyzer",
            version="1.0.0",
            description="Analyzes networks",
            author="test",
            category="network",
            tags=["networking", "security"],
            status=PluginStatus.PUBLISHED,
        )
        import asyncio
        asyncio.run(mp.publish(manifest))
        results = mp.search("network")
        assert len(results) == 1

    def test_list_categories(self):
        from backend.app.core.plugin_marketplace import PluginMarketplace, PluginManifest, PluginStatus
        mp = PluginMarketplace()
        manifest = PluginManifest(
            id="net-plugin",
            name="Net",
            version="1.0",
            description="Network",
            author="a",
            category="network",
            status=PluginStatus.PUBLISHED,
        )
        import asyncio
        asyncio.run(mp.publish(manifest))
        categories = mp.get_categories()
        assert "network" in categories

    def test_rate_plugin(self):
        from backend.app.core.plugin_marketplace import PluginMarketplace, PluginManifest, PluginStatus
        mp = PluginMarketplace()
        manifest = PluginManifest(
            id="rated-plugin",
            name="Rated",
            version="1.0",
            description="Test",
            author="a",
            category="test",
            status=PluginStatus.PUBLISHED,
        )
        import asyncio
        asyncio.run(mp.publish(manifest))
        asyncio.run(mp.rate("rated-plugin", 4.0))
        asyncio.run(mp.rate("rated-plugin", 5.0))
        assert mp.get_plugin("rated-plugin").rating == 4.5