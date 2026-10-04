"""
Tests for Plugin Marketplace
=============================
Tests for plugin discovery, installation, and management.

Every test gets its own ``plugins_dir``. ``PluginMarketplace`` persists manifests
to disk on ``publish()`` and reloads them in ``__init__``, so sharing the default
``.ecp/plugins`` directory leaks state between tests (and pollutes the repo).
"""


def _marketplace(tmp_path):
    """Build a marketplace backed by an isolated, empty plugins directory."""
    from backend.app.core.plugin_marketplace import PluginMarketplace

    return PluginMarketplace(plugins_dir=str(tmp_path / "plugins"))


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

    def test_publish_plugin(self, tmp_path):
        from backend.app.core.plugin_marketplace import PluginManifest, PluginStatus

        mp = _marketplace(tmp_path)
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

    def test_publish_persists_manifest(self, tmp_path):
        from backend.app.core.plugin_marketplace import PluginManifest, PluginStatus

        mp = _marketplace(tmp_path)
        manifest = PluginManifest(
            id="persisted-plugin",
            name="Persisted",
            version="1.0.0",
            description="Survives a restart",
            author="test-author",
            category="testing",
            status=PluginStatus.PUBLISHED,
        )
        import asyncio

        asyncio.run(mp.publish(manifest))

        reloaded = _marketplace(tmp_path)
        assert reloaded.get_plugin("persisted-plugin") is not None

    def test_install_plugin(self, tmp_path):
        from backend.app.core.plugin_marketplace import PluginManifest, PluginStatus

        mp = _marketplace(tmp_path)
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

    def test_install_unpublished_fails(self, tmp_path):
        from backend.app.core.plugin_marketplace import PluginManifest, PluginStatus

        mp = _marketplace(tmp_path)
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

    def test_install_unknown_plugin_fails(self, tmp_path):
        import asyncio

        mp = _marketplace(tmp_path)
        assert asyncio.run(mp.install("does-not-exist")) is False

    def test_uninstall_plugin(self, tmp_path):
        from backend.app.core.plugin_marketplace import PluginManifest, PluginStatus

        mp = _marketplace(tmp_path)
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

    def test_search_plugins(self, tmp_path):
        from backend.app.core.plugin_marketplace import PluginManifest, PluginStatus

        mp = _marketplace(tmp_path)
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

    def test_search_matches_tags(self, tmp_path):
        from backend.app.core.plugin_marketplace import PluginManifest, PluginStatus

        mp = _marketplace(tmp_path)
        manifest = PluginManifest(
            id="tagged-plugin",
            name="Unrelated Name",
            version="1.0.0",
            description="Unrelated description",
            author="test",
            category="misc",
            tags=["observability"],
            status=PluginStatus.PUBLISHED,
        )
        import asyncio

        asyncio.run(mp.publish(manifest))
        assert [p.id for p in mp.search("observability")] == ["tagged-plugin"]

    def test_list_categories(self, tmp_path):
        from backend.app.core.plugin_marketplace import PluginManifest, PluginStatus

        mp = _marketplace(tmp_path)
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
        assert categories == ["network"]

    def test_rate_plugin(self, tmp_path):
        from backend.app.core.plugin_marketplace import PluginManifest, PluginStatus

        mp = _marketplace(tmp_path)
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

    def test_isolated_from_default_plugins_dir(self, tmp_path):
        """A marketplace must not see manifests written by another instance."""
        from backend.app.core.plugin_marketplace import PluginManifest, PluginStatus

        first = _marketplace(tmp_path)
        manifest = PluginManifest(
            id="leaky-plugin",
            name="Leaky",
            version="1.0",
            description="Should stay in its own directory",
            author="a",
            category="test",
            status=PluginStatus.PUBLISHED,
        )
        import asyncio

        asyncio.run(first.publish(manifest))

        second = _marketplace(tmp_path / "other")
        assert second.get_plugin("leaky-plugin") is None
        assert second.get_categories() == []
