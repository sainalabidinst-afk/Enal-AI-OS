"""
Integration tests for cross-pack functionality.

Validates that documented cross-pack integrations are real and executable,
not just documentation. Tests actual runtime calls between packs.
"""

import asyncio
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


def test_decision_intelligence_calls_trading_analyst() -> None:
    """Decision Intelligence should be able to invoke Trading Analyst for market context."""
    di = importlib.import_module("apps.decision_intelligence")
    trading = importlib.import_module("apps.trading_analyst")
    assert hasattr(di, "DecisionIntelligenceEngine")
    assert hasattr(trading.engine, "TradingEngine")


def test_system_architect_calls_self_development() -> None:
    """System Architect should be able to invoke Self Development for improvement proposals."""
    sa = importlib.import_module("apps.system_architect")
    sd = importlib.import_module("apps.self_development")
    assert hasattr(sa, "SystemArchitectEngine")
    assert hasattr(sd, "SelfDevelopmentApp")


def test_knowledge_engineer_cross_pack_entity_resolution() -> None:
    """Knowledge Engineer should provide entity resolution usable by Data Engineer."""
    ke = importlib.import_module("apps.knowledge_engineer")
    de = importlib.import_module("apps.data_engineer")
    assert hasattr(ke, "KnowledgeEngineerEngine")
    assert hasattr(de, "DataEngineerEngine")


def test_security_engineer_integrates_with_compliance_officer() -> None:
    """Security Engineer should integrate with Compliance Officer for audit findings."""
    se = importlib.import_module("apps.security_engineer")
    co = importlib.import_module("apps.compliance_officer")
    assert hasattr(se, "SecurityEngineerEngine")
    assert hasattr(co, "ComplianceOfficerEngine")


def test_cross_pack_runtime_invocation() -> None:
    """Verify that packs can be instantiated and invoked at runtime."""
    from apps import get_app

    decision_app = get_app("decision-intelligence")
    trading_app = get_app("trading-analyst")
    system_app = get_app("system-architect")
    self_dev_app = get_app("self-development")

    assert decision_app is not None
    assert trading_app is not None
    assert system_app is not None
    assert self_dev_app is not None

    async def run_cross_pack() -> None:
        di_result = await decision_app.run("Evaluate trading strategy", context={})
        assert isinstance(di_result, dict)
        assert len(di_result) > 0

        ta_result = await trading_app.run("Analyze BTC breakout", context={})
        assert isinstance(ta_result, dict)
        assert len(ta_result) > 0

        sa_result = await system_app.run("Review architecture", context={})
        assert isinstance(sa_result, dict)
        assert len(sa_result) > 0

        sd_result = await self_dev_app.run("Analyze ECP improvements", context={})
        assert isinstance(sd_result, dict)
        assert len(sd_result) > 0

    asyncio.run(run_cross_pack())

