"""
Golden Test Runner for RFC-0001 Stable Contract.

Executes the 10 golden test scenarios defined in
``golden_tests/stable_contract/gt_*_*.json`` and reports pass/fail.
"""

from __future__ import annotations

import asyncio
import json
import os
import sys
import traceback
from pathlib import Path
from typing import Any

# Set test environment
os.environ.setdefault("SECRET_KEY", "test-secret-key")
os.environ.setdefault("TESTING", "true")
os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest

from backend.app.core.base_app import BaseApp
from backend.app.core.contract_validator import ContractValidator
from backend.app.core.event_bus import StableEventBus
from backend.app.core.factory_registry import FactoryRegistry
from backend.app.core.observability import (
    MetricsCollector,
    Observability,
    SpanType,
    StructuredLogger,
)
from backend.app.core.pipeline_engine import PipelineEngine, PipelineStage
from backend.app.core.plugin_manifest import (
    HotReloadManager,
    PluginManifest,
    PluginManifestRegistry,
)
from backend.app.core.schemas import (
    CapabilityPackConfig,
    Event,
    TaskIntentRequest,
)
from backend.app.core.skills_registry import SkillsRegistry
from backend.app.core.version_manager import VersionManager


class GoldenTestRunner:
    """Runs golden tests and collects pass/fail results."""

    def __init__(self):
        self.results: list[dict[str, Any]] = []

    def run_all(self) -> dict[str, Any]:
        scenario_dir = Path(__file__).resolve().parent.parent / "golden_tests" / "stable_contract"
        scenarios = sorted(scenario_dir.glob("gt_*.json"))

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            for scenario_path in scenarios:
                result = loop.run_until_complete(self._run_scenario(scenario_path))
                self.results.append(result)
        finally:
            loop.close()

        passed = sum(1 for r in self.results if r["passed"])
        total = len(self.results)
        return {
            "total": total,
            "passed": passed,
            "failed": total - passed,
            "pass_rate": f"{passed / total * 100:.0f}%" if total else "0%",
            "results": self.results,
        }

    async def run_all_async(self) -> dict[str, Any]:
        """Async-compatible version for use inside pytest-asyncio."""
        scenario_dir = Path(__file__).resolve().parent.parent / "golden_tests" / "stable_contract"
        scenarios = sorted(scenario_dir.glob("gt_*.json"))

        for scenario_path in scenarios:
            result = await self._run_scenario(scenario_path)
            self.results.append(result)

        passed = sum(1 for r in self.results if r["passed"])
        total = len(self.results)
        return {
            "total": total,
            "passed": passed,
            "failed": total - passed,
            "pass_rate": f"{passed / total * 100:.0f}%" if total else "0%",
            "results": self.results,
        }

    async def _run_scenario(self, path: Path) -> dict[str, Any]:
        scenario = json.loads(path.read_text())
        scenario_id = scenario["scenario_id"]

        checks: list[dict[str, Any]] = []
        try:
            if scenario_id == "gt_01_baseapp_contract":
                checks = await self._test_baseapp()
            elif scenario_id == "gt_02_event_bus_cross_pack":
                checks = await self._test_event_bus()
            elif scenario_id == "gt_03_dynamic_pack_loading":
                checks = await self._test_dynamic_loading()
            elif scenario_id == "gt_04_circular_import_detection":
                checks = await self._test_circular_detection()
            elif scenario_id == "gt_05_multi_pack_pipeline":
                checks = await self._test_pipeline()
            elif scenario_id == "gt_06_failure_isolation":
                checks = await self._test_failure_isolation()
            elif scenario_id == "gt_07_skills_yaml_validation":
                checks = await self._test_skills_yaml()
            elif scenario_id == "gt_08_trace_propagation":
                checks = await self._test_trace_propagation()
            elif scenario_id == "gt_09_version_resolution":
                checks = await self._test_version_resolution()
            elif scenario_id == "gt_10_observability_standards":
                checks = await self._test_observability()
            elif scenario_id == "gt_11_hot_reload":
                checks = await self._test_hot_reload()

            all_passed = all(c["passed"] for c in checks)
        except Exception as e:
            all_passed = False
            checks = [
                {
                    "name": "execution",
                    "passed": False,
                    "error": str(e),
                    "traceback": traceback.format_exc(),
                }
            ]

        return {
            "scenario_id": scenario_id,
            "title": scenario.get("title", ""),
            "passed": all_passed,
            "checks": checks,
        }

    async def _test_baseapp(self) -> list[dict[str, Any]]:
        checks = []

        # 1. Abstract instantiation
        try:
            BaseApp()
            checks.append({"name": "abstract_instantiation_raises", "passed": False})
        except TypeError:
            checks.append({"name": "abstract_instantiation_raises", "passed": True})

        # 2. Concrete subclass works
        class GoodApp(BaseApp):
            def get_capabilities(self):
                return [{"id": "cap", "name": "Cap"}]

            def execute(self, task):
                return {"status": "ok"}

            def validate_input(self, task):
                return True

        app = GoodApp()
        checks.append(
            {
                "name": "full_implementation_succeeds",
                "passed": isinstance(app, BaseApp) and app.get_contract_version() == "1.0.0",
            }
        )

        # 3. Validate via ContractValidator
        cv = ContractValidator()
        report = cv.validate_baseapp(GoodApp)
        checks.append(
            {
                "name": "contract_compliance_100pct",
                "passed": report.passes and len(report.errors) == 0,
            }
        )

        return checks

    async def _test_event_bus(self) -> list[dict[str, Any]]:
        checks = []
        bus = StableEventBus(use_redis=False)

        # 1. Subscribe + publish
        received = []

        async def handler(event):
            received.append(event)

        bus.subscribe("test.gt", handler)
        ev = Event(event_type="test.gt", payload={"msg": "hello"}, trace_id="trace-1")
        await bus.publish(ev)
        checks.append({"name": "event_delivery", "passed": len(received) == 1})

        # 2. Dict validation
        received.clear()
        await bus.publish({"event_type": "test.gt", "payload": {"x": 1}, "trace_id": "trace-2"})
        checks.append(
            {
                "name": "pydantic_validation",
                "passed": len(received) == 1 and isinstance(received[0], Event),
            }
        )

        # 3. Invalid payload raises
        raised = False
        try:
            await bus.publish({"payload": {}})
        except Exception:
            raised = True
        checks.append({"name": "invalid_payload_raises", "passed": raised})

        # 4. Handler error isolation
        received.clear()

        async def bad_handler(event):
            raise ValueError("oops")

        bus.subscribe("test.bad", bad_handler)
        bus.subscribe("test.bad", handler)
        await bus.publish(Event(event_type="test.bad", payload={}))
        checks.append({"name": "handler_error_isolated", "passed": len(received) == 1})

        # 5. Trace ID propagation
        received.clear()
        await bus.publish(Event(event_type="test.gt", payload={}, trace_id="trace-2"))
        checks.append({"name": "trace_id_propagated", "passed": received[0].trace_id == "trace-2"})

        return checks

    async def _test_dynamic_loading(self) -> list[dict[str, Any]]:
        checks = []
        reg = FactoryRegistry()

        # Load an existing pack
        app = reg.get_app("code_engineer")
        checks.append(
            {
                "name": "dynamic_load_existing_pack",
                "passed": app is not None and app.name == "code-engineer",
            }
        )

        # Loading again returns cached instance
        app2 = reg.get_app("code_engineer")
        checks.append({"name": "cached_instance", "passed": app is app2})

        # Unknown pack returns None
        checks.append(
            {"name": "unknown_pack_returns_none", "passed": reg.get_app("nonexistent_pack") is None}
        )

        # discover_packs finds packs
        packs = reg.discover_packs(["apps"])
        checks.append({"name": "discovery_finds_packs", "passed": len(packs) >= 10})

        return checks

    async def _test_circular_detection(self) -> list[dict[str, Any]]:
        checks = []
        sr = SkillsRegistry()

        # Create circular dependency manifest
        manifest_a = {
            "capability_pack": {
                "id": "circ_a",
                "version": "1.0.0",
                "entry_point": "apps.circ_a.engine",
                "capabilities": [{"id": "cap_a", "name": "A", "description": ""}],
                "dependencies": {"capabilities": ["cap_b"], "external": []},
                "pipeline": [],
            }
        }
        manifest_b = {
            "capability_pack": {
                "id": "circ_b",
                "version": "1.0.0",
                "entry_point": "apps.circ_b.engine",
                "capabilities": [{"id": "cap_b", "name": "B", "description": ""}],
                "dependencies": {"capabilities": ["cap_a"], "external": []},
                "pipeline": [],
            }
        }

        # Parse and register
        sr._parse_manifest(manifest_a)
        sr._register(CapabilityPackConfig(**manifest_a["capability_pack"]))
        sr._register(CapabilityPackConfig(**manifest_b["capability_pack"]))

        cycles = sr.detect_circular_dependencies()
        checks.append(
            {
                "name": "cycle_detected",
                "passed": len(cycles) > 0 and "circ_a" in cycles[0] and "circ_b" in cycles[0],
            }
        )

        return checks

    async def _test_pipeline(self) -> list[dict[str, Any]]:
        checks = []
        engine = PipelineEngine(use_redis=False)
        engine.clear()

        engine.define_pipeline(
            "gt_pack",
            [
                PipelineStage(name="parse", capability="parse"),
                PipelineStage(name="analyze", capability="analyze"),
                PipelineStage(name="generate", capability="generate"),
            ],
        )

        call_order = []

        async def parse_handler(ctx):
            call_order.append("parse")
            return {"parsed": True}

        async def analyze_handler(ctx):
            call_order.append("analyze")
            ctx.get("parse", {})
            return {"analyzed": True}

        async def generate_handler(ctx):
            call_order.append("generate")
            return {"generated": True}

        engine.register_stage_handler("parse", parse_handler)
        engine.register_stage_handler("analyze", analyze_handler)
        engine.register_stage_handler("generate", generate_handler)

        task = TaskIntentRequest(intent="gt_pack.test")
        result = await engine.execute_pipeline(task, "gt_pack")

        checks.append(
            {"name": "stages_in_order", "passed": call_order == ["parse", "analyze", "generate"]}
        )
        checks.append({"name": "pipeline_completed", "passed": result.status == "success"})
        checks.append(
            {
                "name": "events_emitted",
                "passed": len(result.events_emitted) >= 4,  # started + 2 stages x 2 + completed
            }
        )

        return checks

    async def _test_failure_isolation(self) -> list[dict[str, Any]]:
        checks = []
        engine = PipelineEngine(use_redis=False)
        engine.clear()

        # Pipeline with failing handler
        engine.define_pipeline(
            "fail_pack",
            [
                PipelineStage(name="ok", capability="ok_cap"),
                PipelineStage(name="fail", capability="fail_cap"),
            ],
        )

        async def ok_handler(ctx):
            return {"ok": True}

        async def fail_handler(ctx):
            raise RuntimeError("pack crashed")

        engine.register_stage_handler("ok_cap", ok_handler)
        engine.register_stage_handler("fail_cap", fail_handler)

        task = TaskIntentRequest(intent="fail_pack.test")
        result = await engine.execute_pipeline(task, "fail_pack")

        checks.append(
            {
                "name": "pipeline_failure_recorded",
                "passed": result.status == "failure" and result.error is not None,
            }
        )

        # Second pack still works
        engine.define_pipeline(
            "good_pack",
            [
                PipelineStage(name="step", capability="ok_cap2"),
            ],
        )

        async def ok_handler2(ctx):
            return {"ok": True}

        engine.register_stage_handler("ok_cap2", ok_handler2)
        task2 = TaskIntentRequest(intent="good_pack.test")
        result2 = await engine.execute_pipeline(task2, "good_pack")

        checks.append({"name": "core_remains_operational", "passed": result2.status == "success"})

        # Event bus handler error isolation
        bus = StableEventBus(use_redis=False)
        received = []

        async def good_handler(event):
            received.append(event)

        async def bad_handler(event):
            raise ValueError("handler error")

        bus.subscribe("test.fail", bad_handler)
        bus.subscribe("test.fail", good_handler)
        await bus.publish(Event(event_type="test.fail", payload={}))

        checks.append({"name": "event_handler_error_isolated", "passed": len(received) == 1})

        return checks

    async def _test_skills_yaml(self) -> list[dict[str, Any]]:
        checks = []
        sr = SkillsRegistry()

        import tempfile

        import yaml

        manifest = {
            "capability_pack": {
                "id": "yaml_pack",
                "version": "1.0.0",
                "display_name": "YAML Pack",
                "entry_point": "apps.yaml_pack.engine",
                "capabilities": [{"id": "cap", "name": "Cap", "description": "desc"}],
                "pipeline": [{"stage": "s1", "capability": "cap"}],
            }
        }

        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            yaml.dump(manifest, f)
            path = f.name

        cfg = sr.load_manifest(path)
        checks.append(
            {"name": "valid_manifest_loads", "passed": cfg is not None and cfg.id == "yaml_pack"}
        )

        # Invalid manifest (missing capability_pack)
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            yaml.dump({"foo": "bar"}, f)
            bad_path = f.name

        cfg_bad = sr.load_manifest(bad_path)
        checks.append({"name": "invalid_manifest_rejected", "passed": cfg_bad is None})

        # Validation report
        report = sr.validate_manifest(path)
        checks.append({"name": "validation_report_passes", "passed": report.passes is True})

        # Pydantic ValidationError for missing id
        raised = False
        try:
            CapabilityPackConfig(version="1.0.0")
        except Exception:
            raised = True
        checks.append({"name": "pydantic_validation_error_on_missing_id", "passed": raised})

        os.unlink(path)
        os.unlink(bad_path)
        return checks

    async def _test_trace_propagation(self) -> list[dict[str, Any]]:
        checks = []
        bus = StableEventBus(use_redis=False)

        task = TaskIntentRequest(intent="test", metadata={"trace_id": "trace-xyz"})
        checks.append(
            {"name": "trace_id_in_task_request", "passed": task.metadata.trace_id == "trace-xyz"}
        )

        await bus.publish(Event(event_type="step1", payload={}, trace_id="trace-xyz"))
        await bus.publish(Event(event_type="step2", payload={}, trace_id="trace-xyz"))

        events = bus.get_events(trace_id="trace-xyz")
        checks.append({"name": "events_retrievable_by_trace_id", "passed": len(events) == 2})

        other_events = bus.get_events(trace_id="trace-abc")
        checks.append({"name": "filtering_by_different_trace_id", "passed": len(other_events) == 0})

        # Also test by event_type
        step1_events = bus.get_events(event_type="step1", trace_id="trace-xyz")
        checks.append(
            {"name": "filtering_by_event_type_and_trace", "passed": len(step1_events) == 1}
        )

        return checks

    async def _test_version_resolution(self) -> list[dict[str, Any]]:
        checks = []
        vm = VersionManager()

        checks.append(
            {
                "name": "same_version_compatible",
                "passed": vm.is_backward_compatible("1.0.0", "1.0.0") is True,
            }
        )
        checks.append(
            {
                "name": "minor_version_compatible",
                "passed": vm.is_backward_compatible("1.1.0", "1.0.0") is True,
            }
        )
        checks.append(
            {
                "name": "major_version_incompatible",
                "passed": vm.is_backward_compatible("2.0.0", "1.0.0") is False,
            }
        )

        # Fallback handler
        def fallback_handler(task):
            return {"fallback": True}

        vm.register_fallback("2.0.0", fallback_handler)
        result = vm.check_compatibility("2.0.0", "1.0.0")
        checks.append(
            {"name": "fallback_handler_available", "passed": result["action"] == "fallback"}
        )

        # Version resolution
        resolved = vm.resolve_version("1.0.0", ["1.1.0", "2.0.0"])
        checks.append({"name": "best_compatible_version_resolved", "passed": resolved == "1.1.0"})

        return checks

    async def _test_observability(self) -> list[dict[str, Any]]:
        checks = []

        # Structured logging
        logger = StructuredLogger("gt_observability")
        import io
        import logging

        buf = io.StringIO()
        handler = logging.StreamHandler(buf)
        handler.setLevel(logging.DEBUG)
        logger._logger.addHandler(handler)
        logger._logger.setLevel(logging.DEBUG)

        logger.info("test message", task_id="t1", pack="test")
        log_output = buf.getvalue()
        log_data = json.loads(log_output.strip())
        checks.append(
            {
                "name": "structured_logging_json",
                "passed": log_data["message"] == "test message" and log_data["task_id"] == "t1",
            }
        )

        # Sensitive data redaction
        buf2 = io.StringIO()
        handler2 = logging.StreamHandler(buf2)
        handler2.setLevel(logging.DEBUG)
        logger2 = StructuredLogger("gt_security")
        logger2._logger.addHandler(handler2)
        logger2._logger.setLevel(logging.DEBUG)
        logger2.info("login", password="secret123")
        log_output2 = buf2.getvalue()
        log_data2 = json.loads(log_output2.strip())
        checks.append(
            {"name": "sensitive_data_redacted", "passed": log_data2["password"] == "***REDACTED***"}
        )

        # Metrics
        mc = MetricsCollector()
        mc.increment("events_published", 5)
        mc.gauge("memory_mb", 256.0)
        mc.histogram("latency_ms", 42.0)
        mc.histogram("latency_ms", 87.0)
        metrics = mc.get_metrics()
        checks.append(
            {
                "name": "metrics_collected",
                "passed": metrics["counters"]["events_published"] == 5
                and metrics["gauges"]["memory_mb"] == 256.0
                and metrics["histograms"]["latency_ms"]["count"] == 2,
            }
        )

        # Tracing
        obs = Observability()
        trace_id = obs.start_trace("gt_trace")
        span = obs.start_span("gt_task", SpanType.TASK, agent="test_pack")
        obs.end_span(span, output={"result": "ok"})
        trace = obs.get_trace(trace_id)
        checks.append(
            {
                "name": "tracing_with_metrics",
                "passed": len(trace) == 2
                and trace[1]["success"] is True
                and trace[1]["latency_ms"] >= 0,
            }
        )

        # All events recorded
        bus = StableEventBus(use_redis=False)
        for i in range(10):
            await bus.publish(Event(event_type="test.record", payload={"i": i}))
        checks.append({"name": "all_events_recorded", "passed": len(bus.event_log) == 10})

        return checks

    async def _test_hot_reload(self) -> list[dict[str, Any]]:
        checks = []

        registry = PluginManifestRegistry()
        manager = HotReloadManager(registry)
        checks.append({"name": "manager_initializes", "passed": manager is not None})

        manifest = PluginManifest(
            id="test_hot_reload_pack",
            name="Test Hot Reload Pack",
            version="1.0.0",
            description="Test pack for hot reload",
            author="ECP",
            license="MIT",
            capabilities=["test"],
            permissions=["read"],
            required_contracts={"test": "1.0.0"},
            entrypoint="backend.app.core.plugin_manifest",
        )
        registry.register(manifest)

        success = manager.register_pack("test_hot_reload_pack", "backend.app.core.plugin_manifest")
        checks.append({"name": "pack_registered", "passed": success})

        loaded = manager.list_loaded_packs()
        checks.append({"name": "pack_in_loaded_list", "passed": "test_hot_reload_pack" in loaded})

        import backend.app.core.plugin_manifest as pm

        has_changed = manager.check_for_updates("test_hot_reload_pack", pm.__file__)
        checks.append({"name": "no_changes_detected", "passed": not has_changed})

        result = manager.reload_pack("test_hot_reload_pack", "backend.app.core.plugin_manifest")
        checks.append({"name": "reload_successful", "passed": result.success})
        checks.append({"name": "latency_under_100ms", "passed": result.latency_ms < 100})

        err_result = manager.reload_pack("nonexistent_pack", "backend.app.core.plugin_manifest")
        checks.append(
            {
                "name": "error_on_unregistered",
                "passed": not err_result.success and err_result.error is not None,
            }
        )

        return checks


if __name__ == "__main__":
    runner = GoldenTestRunner()
    results = runner.run_all()
    print(json.dumps(results, indent=2))


async def test_all_golden_scenarios():
    """Run all golden scenarios via pytest."""
    runner = GoldenTestRunner()
    results = await runner.run_all_async()
    failed_ids = [r["scenario_id"] for r in results["results"] if not r["passed"]]
    assert results["failed"] == 0, f"{results['failed']} scenario(s) failed: {failed_ids}"


@pytest.mark.parametrize(
    "scenario_id",
    [
        "gt_01_baseapp_contract",
        "gt_02_event_bus_cross_pack",
        "gt_03_dynamic_pack_loading",
        "gt_04_circular_import_detection",
        "gt_05_multi_pack_pipeline",
        "gt_06_failure_isolation",
        "gt_07_skills_yaml_validation",
        "gt_08_trace_propagation",
        "gt_09_version_resolution",
        "gt_10_observability_standards",
        "gt_11_hot_reload",
    ],
)
async def test_golden_scenario(scenario_id):
    """Run a single golden scenario and assert all checks pass."""
    runner = GoldenTestRunner()
    result = await runner.run_all_async()
    matching = [r for r in result["results"] if r["scenario_id"] == scenario_id]
    assert matching, f"Scenario {scenario_id} not found"
    scenario = matching[0]
    failed_checks = [c for c in scenario["checks"] if not c["passed"]]
    assert not failed_checks, f"{scenario_id} failed checks: {failed_checks}"
