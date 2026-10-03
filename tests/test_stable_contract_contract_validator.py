"""
Tests for backend/app/core/contract_validator.py — RFC-0001 Contract Validator.
"""

import pytest

from backend.app.core.base_app import BaseApp
from backend.app.core.contract_validator import (
    EXPECTED_BASEAPP_METHODS,
    ContractValidator,
)
from backend.app.core.schemas import TaskIntentRequest, TaskResult


class TestContractValidator:
    @pytest.fixture
    def validator(self):
        return ContractValidator()

    # -- BaseApp validation -------------------------------------------------

    def test_validate_baseapp_concrete_class(self, validator):
        class GoodApp(BaseApp):
            name = "good"
            version = "1.0.0"

            def get_capabilities(self):
                return [{"id": "cap", "name": "Cap"}]

            def execute(self, task):
                return {"ok": True}

            def validate_input(self, task):
                return True

        report = validator.validate_baseapp(GoodApp)
        assert report.passes is True
        assert report.pack_id == "good"
        assert len(report.errors) == 0
        assert len(report.methods_implemented) == 5

    def test_validate_baseapp_not_subclass(self, validator):
        class NotAnApp:
            pass

        report = validator.validate_baseapp(NotAnApp)
        assert report.passes is False
        assert len(report.errors) > 0

    def test_validate_baseapp_missing_methods(self, validator):
        class IncompleteApp(BaseApp):
            def get_capabilities(self):
                return []

        report = validator.validate_baseapp(IncompleteApp)
        assert report.passes is False
        assert any("execute" in e for e in report.errors)
        assert any("validate_input" in e for e in report.errors)

    def test_validate_baseapp_not_a_class(self, validator):
        report = validator.validate_baseapp("not a class")
        assert report.passes is False

    def test_expected_methods_constant(self):
        assert "get_capabilities" in EXPECTED_BASEAPP_METHODS
        assert "execute" in EXPECTED_BASEAPP_METHODS
        assert "validate_input" in EXPECTED_BASEAPP_METHODS
        assert "register_event_handlers" in EXPECTED_BASEAPP_METHODS
        assert "shutdown" in EXPECTED_BASEAPP_METHODS

    # -- Manifest validation ------------------------------------------------

    def test_validate_manifest_valid(self, validator):
        manifest = {
            "capability_pack": {
                "id": "test_pack",
                "version": "1.0.0",
                "entry_point": "apps.test.engine",
                "capabilities": [{"id": "cap1", "name": "Cap1", "description": "desc"}],
                "pipeline": [{"stage": "step1", "capability": "cap1"}],
            }
        }
        report = validator.validate_manifest(manifest)
        assert report.passes is True
        assert report.pack_id == "test_pack"

    def test_validate_manifest_missing_required_field(self, validator):
        manifest = {
            "capability_pack": {
                "version": "1.0.0",
                "capabilities": [],
            }
        }
        report = validator.validate_manifest(manifest)
        assert report.passes is False
        assert any("id" in e for e in report.errors)

    def test_validate_manifest_pipeline_references_undeclared(self, validator):
        manifest = {
            "capability_pack": {
                "id": "test_pack",
                "version": "1.0.0",
                "entry_point": "apps.test.engine",
                "capabilities": [],
                "pipeline": [{"stage": "step1", "capability": "undeclared_cap"}],
            }
        }
        report = validator.validate_manifest(manifest)
        assert any("undeclared" in w for w in report.warnings)

    # -- Task request validation --------------------------------------------

    def test_validate_task_request_valid(self, validator):
        task = TaskIntentRequest(intent="code_engineer.generate")
        ok, errors = validator.validate_task_request(task)
        assert ok is True
        assert len(errors) == 0

    def test_validate_task_request_from_dict(self, validator):
        task_dict = {"intent": "test.intent", "priority": "high"}
        ok, errors = validator.validate_task_request(task_dict)
        assert ok is True

    def test_validate_task_request_missing_intent(self, validator):
        task_dict = {"intent": ""}
        ok, errors = validator.validate_task_request(task_dict)
        assert ok is False
        assert "intent" in errors[0]

    def test_validate_task_request_invalid_priority(self, validator):
        task_dict = {"intent": "test", "priority": "invalid"}
        ok, errors = validator.validate_task_request(task_dict)
        assert ok is False

    # -- Task result validation --------------------------------------------

    def test_validate_task_result_valid(self, validator):
        result = TaskResult(task_id="t1", intent="test.intent")
        ok, errors = validator.validate_task_result(result)
        assert ok is True

    def test_validate_task_result_from_dict(self, validator):
        result_dict = {
            "task_id": "t1",
            "intent": "test.intent",
            "status": "success",
        }
        ok, errors = validator.validate_task_result(result_dict)
        assert ok is True

    def test_validate_task_result_missing_task_id(self, validator):
        ok, errors = validator.validate_task_result({"task_id": "", "intent": "test"})
        assert ok is False

    # -- Circular import detection -----------------------------------------

    def test_detect_circular_imports_no_crash(self, validator):
        cycles = validator.detect_circular_imports()
        assert isinstance(cycles, list)

    def test_full_pack_validation(self, validator, tmp_path):
        import yaml

        class GoodApp(BaseApp):
            name = "full_test"
            version = "1.0.0"

            def get_capabilities(self):
                return [{"id": "cap1", "name": "Cap1"}]

            def execute(self, task):
                return {}

            def validate_input(self, task):
                return True

        manifest = {
            "capability_pack": {
                "id": "full_test",
                "version": "1.0.0",
                "entry_point": "apps.test.engine",
                "capabilities": [{"id": "cap1", "name": "Cap1", "description": "d"}],
                "pipeline": [{"stage": "s1", "capability": "cap1"}],
            }
        }
        manifest_path = tmp_path / "skills.yaml"
        with open(manifest_path, "w") as f:
            yaml.dump(manifest, f)

        report = validator.validate_pack(GoodApp, str(manifest_path))
        assert report.passes is True
