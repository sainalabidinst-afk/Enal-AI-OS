"""
RFC-0001 Stable Contract — Contract Validator.

Validates that a Capability Pack:
  - Implements BaseApp correctly (all abstract methods)
  - Has a properly structured skills.yaml manifest
  - Does not introduce circular imports
  - Reports compliance as a structured report
"""

from __future__ import annotations

import inspect
import logging
import sys
from typing import Any

from backend.app.core.base_app import BaseApp
from backend.app.core.schemas import (
    CapabilityPackConfig,
    ComplianceReport,
    TaskIntentRequest,
    TaskResult,
    TaskResultMetrics,
)
from backend.app.core.skills_registry import SkillsRegistry

logger = logging.getLogger(__name__)

EXPECTED_BASEAPP_METHODS = [
    "get_capabilities",
    "execute",
    "validate_input",
    "register_event_handlers",
    "shutdown",
]


class ContractValidator:
    """Enforces pack contract compliance (RFC-0001 § Contract Validator)."""

    def __init__(self, skills_registry: SkillsRegistry | None = None):
        self._skills_registry = skills_registry or SkillsRegistry()

    # -- BaseApp compliance --------------------------------------------------

    def validate_baseapp(self, app_class: type) -> ComplianceReport:
        """Validate that *app_class* correctly implements BaseApp."""
        errors: list[str] = []
        warnings: list[str] = []
        implemented: list[str] = []
        expected: list[str] = list(EXPECTED_BASEAPP_METHODS)

        if not isinstance(app_class, type):
            errors.append("Provided object is not a class")
            return ComplianceReport(
                pack_id=getattr(app_class, "__name__", str(app_class)),
                version="0.0.0",
                passes=False,
                errors=errors,
                warnings=warnings,
                methods_expected=expected,
                methods_implemented=[],
            )

        if not issubclass(app_class, BaseApp):
            errors.append(f"{app_class.__name__} does not extend BaseApp")
            return ComplianceReport(
                pack_id=app_class.__name__,
                version="0.0.0",
                passes=False,
                errors=errors,
                warnings=warnings,
                methods_expected=expected,
                methods_implemented=[],
            )

        for method_name in EXPECTED_BASEAPP_METHODS:
            method = getattr(app_class, method_name, None)
            is_abstract = False
            if method is not None:
                # Check if the abstractmethod decorator is still in place
                if hasattr(method, "__isabstractmethod__"):
                    is_abstract = method.__isabstractmethod__
                if not is_abstract:
                    implemented.append(method_name)
                else:
                    errors.append(f"Method '{method_name}' is still abstract")
            else:
                errors.append(f"Missing method: {method_name}")

        # Check for required class attributes
        for attr in ("name", "version"):
            if not hasattr(app_class, attr):
                warnings.append(f"Missing class attribute: {attr}")

        pack_id = getattr(app_class, "name", app_class.__name__)
        version = getattr(app_class, "version", "0.0.0")

        return ComplianceReport(
            pack_id=pack_id,
            version=version,
            passes=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            methods_expected=expected,
            methods_implemented=implemented,
        )

    # -- Manifest compliance -------------------------------------------------

    def validate_manifest(
        self, manifest: dict[str, Any] | CapabilityPackConfig
    ) -> ComplianceReport:
        """Validate a skills.yaml manifest against the RFC schema."""
        errors: list[str] = []
        warnings: list[str] = []
        expected: list[str] = []
        implemented: list[str] = []

        if isinstance(manifest, dict):
            if "capability_pack" in manifest:
                pack = manifest["capability_pack"]
            else:
                # Already a pack config dict (from model_dump of CapabilityPackConfig)
                pack = manifest
            try:
                from pydantic import ValidationError

                cfg = CapabilityPackConfig(**pack)
            except ValidationError as exc:
                field_errors = []
                for err in exc.errors():
                    loc = ".".join(str(x) for x in err["loc"])
                    field_errors.append(f"Field '{loc}': {err['msg']}")
                for field_name in ("id", "version", "entry_point"):
                    if field_name not in pack or not pack[field_name]:
                        if field_name not in field_errors:
                            field_errors.append(f"Missing required field: {field_name}")
                return ComplianceReport(
                    pack_id=pack.get("id", ""),
                    version=pack.get("version", "0.0.0"),
                    passes=False,
                    errors=field_errors,
                    warnings=[],
                    methods_expected=[
                        "capability_pack",
                        "id",
                        "version",
                        "capabilities",
                        "pipeline",
                    ],
                    methods_implemented=[],
                )
            except Exception as exc:
                return ComplianceReport(
                    pack_id="",
                    version="0.0.0",
                    passes=False,
                    errors=[f"Failed to parse manifest: {exc}"],
                    warnings=[],
                    methods_expected=[],
                    methods_implemented=[],
                )
        else:
            cfg = manifest

        pack_id = cfg.id
        version = cfg.version

        # Required fields
        for field_name in ("id", "version", "entry_point"):
            expected.append(field_name)
            if getattr(cfg, field_name, None):
                implemented.append(field_name)
            else:
                errors.append(f"Missing required field: {field_name}")

        expected.append("capabilities")
        if cfg.capabilities:
            implemented.append("capabilities")
        else:
            warnings.append("No capabilities declared")

        expected.append("pipeline")
        if cfg.pipeline:
            implemented.append("pipeline")
        else:
            warnings.append("No pipeline stages declared")

        # Validate capability entries
        for cap in cfg.capabilities:
            if not cap.id:
                errors.append("Capability entry missing id")
            if not cap.name:
                warnings.append(f"Capability '{cap.id}' missing name")

        # Validate pipeline stages reference declared capabilities
        declared_caps = {c.id for c in cfg.capabilities}
        for stage in cfg.pipeline:
            if stage.capability not in declared_caps:
                warnings.append(
                    f"Pipeline stage '{stage.stage}' references "
                    f"undeclared capability '{stage.capability}'"
                )

        # Validate dependencies reference declared capabilities
        for dep in cfg.dependencies.capabilities:
            if dep not in declared_caps:
                warnings.append(f"Dependency '{dep}' is not declared in this pack")

        return ComplianceReport(
            pack_id=pack_id,
            version=version,
            passes=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            methods_expected=expected,
            methods_implemented=implemented,
        )

    # -- Task/Result contract compliance ------------------------------------

    def validate_task_request(
        self, task: dict[str, Any] | TaskIntentRequest
    ) -> tuple[bool, list[str]]:
        """Validate a task request against the RFC-0001 input contract."""
        errors: list[str] = []
        try:
            if isinstance(task, dict):
                task = TaskIntentRequest.model_validate(task)
        except Exception as exc:
            errors.append(f"Task request validation failed: {exc}")
            return False, errors

        if not task.task_id:
            errors.append("task_id is required")
        if not task.intent:
            errors.append("intent is required")
        if not isinstance(task.context.user_input, str):
            errors.append("context.user_input must be a string")
        if task.timeout_ms <= 0:
            errors.append("timeout_ms must be > 0")

        return len(errors) == 0, errors

    def validate_task_result(self, result: dict[str, Any] | TaskResult) -> tuple[bool, list[str]]:
        """Validate a task result against the RFC-0001 output contract."""
        errors: list[str] = []
        try:
            if isinstance(result, dict):
                result = TaskResult.model_validate(result)
        except Exception as exc:
            errors.append(f"Task result validation failed: {exc}")
            return False, errors

        if not result.task_id:
            errors.append("task_id is required")
        if not result.intent:
            errors.append("intent is required")
        if result.status not in ("success", "failure", "timeout", "partial"):
            errors.append(f"invalid status: {result.status}")
        if not isinstance(result.metrics, TaskResultMetrics):
            errors.append("metrics must be a TaskResultMetrics instance")

        return len(errors) == 0, errors

    # -- Circular import detection ------------------------------------------

    def detect_circular_imports(self, pack_dirs: list[str] | None = None) -> list[list[str]]:
        """Detect circular imports across pack modules.

        Scans all ``apps.*`` modules currently in ``sys.modules`` and
        builds an import graph, returning any cycles found.
        """
        graph: dict[str, list[str]] = {}

        for mod_name, mod in list(sys.modules.items()):
            if not mod_name.startswith("apps."):
                continue
            if not hasattr(mod, "__file__") or mod.__file__ is None:
                continue
            deps: list[str] = []
            try:
                inspect.getsource(mod)
            except Exception:
                pass

            # Use a simpler approach: check the module's imported names
            for attr_name in dir(mod):
                attr = getattr(mod, attr_name, None)
                if inspect.ismodule(attr):
                    dep_name = getattr(attr, "__name__", "")
                    if dep_name.startswith("apps."):
                        deps.append(dep_name)
            graph[mod_name] = deps

        # DFS cycle detection
        cycles: list[list[str]] = []
        visited: set[str] = set()
        rec_stack: set[str] = set()

        def _dfs(node: str, path: list[str]) -> None:
            visited.add(node)
            rec_stack.add(node)
            path.append(node)
            for neighbor in graph.get(node, []):
                if neighbor not in graph:
                    continue
                if neighbor not in visited:
                    _dfs(neighbor, path)
                elif neighbor in rec_stack:
                    idx = path.index(neighbor)
                    cycles.append(list(path[idx:]))
            path.pop()
            rec_stack.discard(node)

        for mod_name in list(graph.keys()):
            if mod_name not in visited:
                _dfs(mod_name, [])

        return cycles

    # -- Full validation -----------------------------------------------------

    def validate_pack(
        self,
        app_class: type,
        manifest_path: str | None = None,
    ) -> ComplianceReport:
        """Run full pack validation: BaseApp + manifest + imports."""
        baseapp_report = self.validate_baseapp(app_class)
        reports: list[ComplianceReport] = [baseapp_report]

        if manifest_path:
            manifest = self._skills_registry.load_manifest(manifest_path)
            if manifest:
                manifest_report = self.validate_manifest(manifest.model_dump())
                reports.append(manifest_report)

        circular = self.detect_circular_imports()
        if circular:
            for cycle in circular:
                baseapp_report.warnings.append(f"Circular import detected: {' -> '.join(cycle)}")

        # Aggregate
        all_pass = all(r.passes for r in reports)
        all_errors = [e for r in reports for e in r.errors]
        all_warnings = [w for r in reports for w in r.warnings]
        all_methods_expected = list(dict.fromkeys(m for r in reports for m in r.methods_expected))
        all_methods_implemented = list(
            dict.fromkeys(m for r in reports for m in r.methods_implemented)
        )

        return ComplianceReport(
            pack_id=baseapp_report.pack_id,
            version=baseapp_report.version,
            passes=all_pass and len(circular) == 0,
            errors=all_errors,
            warnings=all_warnings,
            methods_expected=all_methods_expected,
            methods_implemented=all_methods_implemented,
        )


contract_validator = ContractValidator()
