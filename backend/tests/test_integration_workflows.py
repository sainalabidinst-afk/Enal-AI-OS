import pytest
from apps.integration.orchestrator import IntegrationEngine
from apps.trading_analyst.market_intelligence import provider as market_provider


def _fake_market_data(symbol: str, timeframes: list[str], limit: int = 100) -> dict[str, list[dict]]:
    candles = []
    for index in range(max(30, limit)):
        price = 100.0 + index
        candles.append(
            {
                "timestamp": index,
                "open": price - 0.5,
                "high": price + 1.0,
                "low": price - 1.0,
                "close": price,
                "volume": 1000.0 + index,
            }
        )
    return {timeframe: list(candles) for timeframe in timeframes}


@pytest.mark.asyncio
async def test_trading_analysis_workflow_produces_context(monkeypatch):
    monkeypatch.setattr(market_provider, "fetch_multi_timeframe", _fake_market_data)
    engine = IntegrationEngine()
    result = await engine.trading_analysis_with_knowledge(
        symbol="BTCUSDT",
        timeframes=["1h"],
        exchange="binance",
    )

    assert result.success is True
    assert result.context is not None
    assert result.context.workflow_type == "trading_analysis_with_knowledge"
    assert result.context.get_input("symbol") == "BTCUSDT"
    assert result.context.get_input("exchange") == "binance"
    assert result.context.get_output("market_evidence")
    assert result.context.get_output("reasoning_output") is not None


@pytest.mark.asyncio
async def test_trading_analysis_fails_when_market_data_is_unavailable(monkeypatch):
    monkeypatch.setattr(
        market_provider,
        "fetch_multi_timeframe",
        lambda symbol, timeframes, limit=100: {timeframe: [] for timeframe in timeframes},
    )
    result = await IntegrationEngine().trading_analysis_with_knowledge(
        symbol="BTCUSDT",
        timeframes=["1h"],
        exchange="binance",
    )

    assert result.success is False
    assert "No market data available" in (result.error or "")
    assert result.context.outputs == {}


@pytest.mark.asyncio
async def test_network_design_review_workflow_produces_context():
    engine = IntegrationEngine()
    result = await engine.network_design_review_with_knowledge(
        topology_description="3-tier datacenter",
        requirements="Support 500 branches",
    )

    assert result.success is True
    assert result.context is not None
    assert result.context.workflow_type == "network_design_review_with_knowledge"
    assert result.context.get_input("topology_description") == "3-tier datacenter"


@pytest.mark.asyncio
async def test_self_improvement_workflow_is_roadmap_placeholder():
    engine = IntegrationEngine()
    result = await engine.self_improvement_cycle(
        project_path="/tmp/project",
        analysis_type="full",
    )

    assert result.success is True
    assert result.context is not None
    assert result.context.workflow_type == "self_improvement_cycle"
    improvement = result.context.get_intermediate("self_improvement", {})
    assert improvement.get("status") == "roadmap"


def test_registry_descriptor_contract():
    from apps.integration.registry import capability_registry

    descriptor = capability_registry.resolve("trading-analysis")
    assert descriptor is not None
    assert descriptor.capability_id == "trading-analysis"
    assert descriptor.domain == "trading"
    assert len(descriptor.inputs) > 0
    assert len(descriptor.outputs) > 0
