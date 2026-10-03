"""
Tests for backend/app/core/base_app.py — RFC-0001 BaseApp abstract contract.
"""

import pytest

from backend.app.core.base_app import BaseApp


class TestBaseApp:
    def test_cannot_instantiate_abstract_class(self):
        with pytest.raises(TypeError):
            BaseApp()

    def test_subclass_must_implement_all_abstract_methods(self):
        class IncompleteApp(BaseApp):
            pass

        with pytest.raises(TypeError):
            IncompleteApp()

    def test_subclass_with_partial_implementation_fails(self):
        class PartialApp(BaseApp):
            def get_capabilities(self):
                return []

        with pytest.raises(TypeError):
            PartialApp()

    def test_concrete_subclass_works(self):
        class ConcreteApp(BaseApp):
            name = "test_pack"
            version = "1.0.0"

            def get_capabilities(self):
                return [{"id": "test_cap", "name": "Test"}]

            def execute(self, task):
                return {"status": "success", "result": task}

            def validate_input(self, task):
                return True

        app = ConcreteApp(config={"debug": True})
        assert app.name == "test_pack"
        assert app.get_capabilities() == [{"id": "test_cap", "name": "Test"}]
        assert app.execute({"intent": "test"})["status"] == "success"
        assert app.validate_input({}) is True

    def test_contract_version(self):
        assert BaseApp.get_contract_version() == "1.0.0"

    def test_default_lifecycle_hooks_work(self):
        class MinimalApp(BaseApp):
            def get_capabilities(self):
                return []

            def execute(self, task):
                return {"status": "ok"}

            def validate_input(self, task):
                return True

        app = MinimalApp()
        # Should not raise
        app.register_event_handlers()
        app.shutdown()

    def test_to_dict(self):
        class MinimalApp(BaseApp):
            name = "my_pack"
            version = "2.0.0"

            def get_capabilities(self):
                return [{"id": "cap1", "name": "Capability 1"}]

            def execute(self, task):
                return {}

            def validate_input(self, task):
                return True

        app = MinimalApp()
        d = app.to_dict()
        assert d["name"] == "my_pack"
        assert d["version"] == "2.0.0"
        assert d["contract_version"] == "1.0.0"
        assert len(d["capabilities"]) == 1

    def test_initial_config_stored(self):
        class MinimalApp(BaseApp):
            def get_capabilities(self):
                return []

            def execute(self, task):
                return {}

            def validate_input(self, task):
                return True

        app = MinimalApp(config={"key": "value"})
        assert app.config["key"] == "value"
