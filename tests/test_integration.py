"""
Smoke tests for Integration capability.
"""

import importlib


def test_capability_imports() -> None:
    """Verify that capability modules can be imported."""
    mod = importlib.import_module("apps.integration")
    assert mod is not None


def test_capability_package() -> None:
    """Verify that capability package exists."""
    mod = importlib.import_module("apps.integration.orchestrator")
    assert mod is not None


def test_integration_modules_exist() -> None:
    """Verify that key integration modules exist."""
    importlib.import_module("apps.integration.context")
    importlib.import_module("apps.integration.registry")
    importlib.import_module("apps.integration.workflow")
    importlib.import_module("apps.integration.orchestrator")
    importlib.import_module("apps.integration.evidence_adapter")
