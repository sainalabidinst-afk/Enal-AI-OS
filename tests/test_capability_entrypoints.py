"""Regression tests for the canonical capability entrypoint contract."""

from importlib import import_module

from apps import APPS
from apps.base import BaseReferenceApp


def test_all_registered_capabilities_expose_valid_entrypoints() -> None:
    """Every canonical capability must load as a concrete reference app."""
    assert len(APPS) == 19

    for capability_id, registered_app in APPS.items():
        module = import_module(f"apps.{capability_id.replace('-', '_')}")
        factory = getattr(module, "get_app", None)
        assert callable(factory), capability_id

        app = factory()
        assert registered_app is not None, capability_id
        assert isinstance(app, BaseReferenceApp), capability_id
        assert app.name == capability_id
        assert callable(app.run)
