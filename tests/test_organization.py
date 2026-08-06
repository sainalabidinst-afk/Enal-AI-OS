"""
Tests for Organization capability.
"""

import importlib


def test_capability_imports() -> None:
    """Verify that capability modules can be imported."""
    mod = importlib.import_module("apps.organization")
    assert mod is not None


def test_capability_package() -> None:
    """Verify that capability package exists."""
    mod = importlib.import_module("apps.organization.registry")
    assert mod is not None


def test_organization_modules_exist() -> None:
    """Verify that key organization modules exist."""
    importlib.import_module("apps.organization.kernel")
    importlib.import_module("apps.organization.capability_graph")
    importlib.import_module("apps.organization.task_planner")
    importlib.import_module("apps.organization.team_builder")
    importlib.import_module("apps.organization.workflow_executor")
