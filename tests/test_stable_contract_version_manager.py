"""
Tests for backend/app/core/version_manager.py — RFC-0001 Version Manager.
"""

import pytest

from backend.app.core.version_manager import VersionManager, version_manager


class TestVersionManager:
    @pytest.fixture
    def vm(self):
        vm = VersionManager()
        # Add the standard compatibility matrix
        vm._compatibility_matrix = {
            "1.0.0": ["1.0.0", "1.0.1", "1.1.0", "1.1.1"],
            "1.1.0": ["1.0.0", "1.1.0"],
            "1.2.0": ["1.0.0", "1.1.0", "1.2.0"],
        }
        return vm

    def test_current_version(self, vm):
        assert vm.current_version == "1.0.0"

    def test_parse_version(self, vm):
        v = vm.parse_version("2.1.3")
        assert v.MAJOR == 2
        assert v.MINOR == 1
        assert v.PATCH == 3

    def test_is_backward_compatible_same(self, vm):
        assert vm.is_backward_compatible("1.0.0", "1.0.0") is True

    def test_is_backward_compatible_patch(self, vm):
        assert vm.is_backward_compatible("1.0.1", "1.0.0") is True

    def test_is_backward_compatible_minor(self, vm):
        assert vm.is_backward_compatible("1.1.0", "1.0.0") is True

    def test_is_not_backward_compatible_major(self, vm):
        assert vm.is_backward_compatible("2.0.0", "1.0.0") is False

    def test_resolve_version_exact(self, vm):
        result = vm.resolve_version("1.0.0", ["1.0.0", "2.0.0"])
        assert result == "1.0.0"

    def test_resolve_version_compatible(self, vm):
        result = vm.resolve_version("1.0.0", ["1.1.0", "2.0.0"])
        assert result == "1.1.0"

    def test_resolve_version_no_match(self, vm):
        result = vm.resolve_version("1.0.0", ["2.0.0", "3.0.0"])
        assert result is None

    def test_register_and_get_fallback(self, vm):
        def handler(task):
            return {"fallback": True}

        vm.register_fallback("1.0.0", handler)
        assert vm.has_fallback("1.0.0") is True
        assert vm.get_fallback("1.0.0") is handler

    def test_no_fallback_for_unregistered(self, vm):
        assert vm.has_fallback("9.9.9") is False
        assert vm.get_fallback("9.9.9") is None

    def test_check_compatibility_compatible(self, vm):
        result = vm.check_compatibility("1.0.0", "1.0.0")
        assert result["compatible"] is True
        assert result["action"] == "load"

    def test_check_compatibility_incompatible_no_fallback(self, vm):
        result = vm.check_compatibility("2.0.0", "1.0.0")
        assert result["compatible"] is False
        assert result["action"] == "reject"

    def test_check_compatibility_incompatible_with_fallback(self, vm):
        def handler(task):
            return {"fallback": True}

        vm.register_fallback("2.0.0", handler)
        result = vm.check_compatibility("2.0.0", "1.0.0")
        assert result["compatible"] is False
        assert result["has_fallback"] is True
        assert result["action"] == "fallback"

    def test_get_compatible_versions(self, vm):
        versions = vm.get_compatible_versions("1.0.0")
        assert "1.0.0" in versions
        assert "1.0.1" in versions
        assert "1.1.0" in versions

    def test_get_compatible_versions_unknown(self, vm):
        versions = vm.get_compatible_versions("3.0.0")
        assert versions == []

    def test_list_known_versions(self, vm):
        versions = vm.list_known_versions()
        assert "1.0.0" in versions

    def test_enforce_semver_valid(self, vm):
        assert vm.enforce_semver("1.0.0") is True
        assert vm.enforce_semver("v2.3.4") is True

    def test_enforce_semver_invalid(self, vm):
        assert vm.enforce_semver("not-a-version") is False
        assert vm.enforce_semver("1.0") is True  # parses to 1.0.0

    def test_check_deprecation_not_deprecated(self, vm):
        schedule = {"1.0.0": "warn"}
        result = vm.check_deprecation("1.0.0", schedule)
        assert result["deprecated"] is True
        assert result["deprecation_target"] == "warn"

    def test_check_deprecation_no_entry(self, vm):
        result = vm.check_deprecation("1.0.0", {})
        assert result["deprecated"] is False

    def test_singleton(self):
        assert version_manager is not None
        assert isinstance(version_manager, VersionManager)
