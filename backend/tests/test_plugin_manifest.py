import pytest

from backend.app.core.plugin_manifest import (
    PluginManifest,
    PluginManifestSecurityLevel,
    PluginManifestVersion,
)


class TestPluginManifestVersion:
    def test_current_version(self):
        assert PluginManifestVersion.CURRENT == "1.0"

    def test_v1_0(self):
        assert PluginManifestVersion.V1_0 == "1.0"


class TestPluginManifestSecurityLevel:
    def test_safe(self):
        assert PluginManifestSecurityLevel.SAFE == "safe"

    def test_restricted(self):
        assert PluginManifestSecurityLevel.RESTRICTED == "restricted"

    def test_privileged(self):
        assert PluginManifestSecurityLevel.PRIVILEGED == "privileged"


class TestPluginManifest:
    def test_valid_manifest_passes_validation(self):
        manifest = PluginManifest(
            id="test-plugin",
            name="Test Plugin",
            version="1.0.0",
            description="A test plugin",
            author="Test Author",
            license="MIT",
            capabilities=["test"],
            permissions=["read"],
            required_contracts={"core": "1.0"},
            entrypoint="main:run",
        )
        errors = manifest.validate()
        assert errors == []

    def test_missing_required_fields(self):
        manifest = PluginManifest()
        errors = manifest.validate()
        assert "Plugin id is required" in errors
        assert "Plugin name is required" in errors
        assert "Plugin version is required" in errors
        assert "Plugin description is required" in errors
        assert "Plugin author is required" in errors
        assert "Plugin license is required" in errors
        assert "Plugin must declare at least one capability" in errors
        assert "Plugin must declare required permissions" in errors
        assert "Plugin must declare required contracts" in errors
        assert "Plugin must declare an entrypoint" in errors

    def test_to_dict_contains_expected_keys(self):
        manifest = PluginManifest(
            id="test-plugin",
            name="Test Plugin",
            version="1.0.0",
            description="A test plugin",
            author="Test Author",
            license="MIT",
            capabilities=["test"],
            permissions=["read"],
            required_contracts={"core": "1.0"},
            entrypoint="main:run",
        )
        data = manifest.to_dict()
        assert data["id"] == "test-plugin"
        assert data["name"] == "Test Plugin"
        assert data["version"] == "1.0.0"
        assert data["security_level"] == PluginManifestSecurityLevel.SAFE
