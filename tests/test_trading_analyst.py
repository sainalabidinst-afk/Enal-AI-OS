"""
Trading Analyst Golden Tests
=============================

Tests for the Trading Analyst Capability Pack:
TradingEngine, analyzers, models, and pipeline integration.
"""
from __future__ import annotations

import asyncio

import pytest

from apps.trading_analyst.engine import TradingEngine
from apps.trading_analyst.market_intelligence.models import (
    AnalysisResult,
    Bias,
    MarketEvidence,
    OHLCV,
    RiskLevel,
    TradingContext,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def engine():
    return TradingEngine()


@pytest.fixture
def sample_ohlcv():
    return [
        OHLCV(timestamp=1_700_000_000 + i * 60, open=100.0, high=101.0, low=99.0, close=100.5, volume=1500.0)
        for i in range(120)
    ]


@pytest.fixture
def sample_context(sample_ohlcv):
    return TradingContext(
        symbol="BTCUSDT",
        exchange="binance",
        timeframes={"1h": sample_ohlcv},
        metadata={"source": "synthetic", "seeded": True},
    )


# ---------------------------------------------------------------------------
# Model Tests
# ---------------------------------------------------------------------------

class TestModels:
    def test_ohlcv_negative_close_raises(self):
        with pytest.raises(ValueError):
            OHLCV(timestamp=1, open=100.0, high=101.0, low=99.0, close=-1.0, volume=100.0)

    def test_market_evidence_strength_clamped(self):
        ev = MarketEvidence(
            id="ev-1", type="test", description="test", timeframe="1h",
            strength=1.5, direction="bullish", source="test",
        )
        assert ev.strength == 1.0

    def test_market_evidence_confidence_clamped(self):
        ev = MarketEvidence(
            id="ev-1", type="test", description="test", timeframe="1h",
            strength=0.5, direction="bullish", source="test", confidence=-0.5,
        )
        assert ev.confidence == 0.0

    def test_analysis_result_defaults(self):
        result = AnalysisResult(symbol="BTCUSDT")
        assert result.bias == Bias.NEUTRAL
        assert result.confidence == 0.0
        assert result.risk_level == RiskLevel.MEDIUM
        assert result.evidence == []

    def test_analysis_result_to_dict(self):
        result = AnalysisResult(
            symbol="BTCUSDT",
            bias=Bias.BULLISH,
            confidence=0.85,
            risk_level=RiskLevel.LOW,
        )
        data = result.to_dict()
        assert data["symbol"] == "BTCUSDT"
        assert data["bias"] == "bullish"
        assert data["confidence"] == 85
        assert data["risk_level"] == "low"


# ---------------------------------------------------------------------------
# Engine Tests
# ---------------------------------------------------------------------------

class TestTradingEngine:
    def test_engine_initializes_analyzers(self, engine):
        assert engine.analyzer is not None
        assert engine.wyckoff is not None
        assert engine.smc is not None
        assert engine.elliott is not None
        assert engine.volume_profile is not None
        assert engine.psychology is not None
        assert engine.macro is not None
        assert engine.derivatives is not None

    def test_synthetic_context_deterministic(self, engine):
        ctx1 = engine._build_synthetic_context("BTCUSDT", ["1h"], "binance")
        ctx2 = engine._build_synthetic_context("BTCUSDT", ["1h"], "binance")
        assert len(ctx1.timeframes["1h"]) == len(ctx2.timeframes["1h"])
        assert ctx1.timeframes["1h"][0].close == ctx2.timeframes["1h"][0].close

    def test_synthetic_context_produces_candles(self, engine):
        ctx = engine._build_synthetic_context("BTCUSDT", ["1h", "4h"], "binance")
        assert "1h" in ctx.timeframes
        assert "4h" in ctx.timeframes
        assert len(ctx.timeframes["1h"]) == 120
        assert len(ctx.timeframes["4h"]) == 120

    def test_synthetic_context_symbol_uppercased(self, engine):
        ctx = engine._build_synthetic_context("btcusdt", ["1h"], "binance")
        assert ctx.symbol == "BTCUSDT"

    @pytest.mark.asyncio
    async def test_analyze_market_returns_result(self, engine):
        result = await engine.analyze_market("BTCUSDT", use_live_data=False)
        assert isinstance(result, AnalysisResult)
        assert result.symbol == "BTCUSDT"

    @pytest.mark.asyncio
    async def test_analyze_market_produces_evidence(self, engine):
        result = await engine.analyze_market("BTCUSDT", use_live_data=False)
        assert len(result.evidence) >= 1

    @pytest.mark.asyncio
    async def test_analyze_market_all_domains_detected(self, engine):
        macro_data = {
            "current_rate": 4.5,
            "previous_rate": 4.75,
            "central_bank": "Fed",
            "cpi": 3.2,
            "core_cpi": 3.5,
            "gdp_growth": 2.1,
            "unemployment": 3.8,
            "pmi": 52.0,
            "vix": 18.5,
            "dxy": 103.0,
            "bond_yield_10y": 4.2,
            "spy_performance_1m": 0.02,
        }
        derivatives_data = {
            "current_iv": 25.0,
            "historical_iv": 20.0,
            "iv_percentile": 0.6,
            "put_volume": 1000.0,
            "call_volume": 800.0,
            "put_oi": 5000.0,
            "call_oi": 4000.0,
            "otm_put_iv": 28.0,
            "atm_iv": 22.0,
            "otm_call_iv": 26.0,
            "spot_price": 50000.0,
            "futures_price": 50500.0,
            "commercial_long": 0.4,
            "commercial_short": 0.3,
            "large_spec_long": 0.35,
            "large_spec_short": 0.25,
            "small_spec_long": 0.1,
            "small_spec_short": 0.15,
            "open_interest": 100000.0,
            "option_chain": {"strikes": [50000, 51000, 52000], "current_price": 50000.0},
            "current_price": 50000.0,
        }
        result = await engine.analyze_market("BTCUSDT", use_live_data=False, macro_data=macro_data, derivatives_data=derivatives_data)
        evidence_types = {ev.type for ev in result.evidence}
        domain_prefixes = {
            "wyckoff": "wyckoff",
            "smc": "smc_",
            "elliott_wave": "elliott_wave",
            "volume_profile": "volume_profile",
            "psychology": "psychology",
            "macro": "macro",
            "derivatives": "derivatives",
        }
        for domain, prefix in domain_prefixes.items():
            assert any(t.startswith(prefix) for t in evidence_types), f"Missing domain: {domain}"

    @pytest.mark.asyncio
    async def test_analyze_market_confidence_in_range(self, engine):
        result = await engine.analyze_market("BTCUSDT", use_live_data=False)
        assert 0.0 <= result.confidence <= 1.0

    @pytest.mark.asyncio
    async def test_analyze_market_bias_is_valid(self, engine):
        result = await engine.analyze_market("BTCUSDT", use_live_data=False)
        assert result.bias in Bias

    @pytest.mark.asyncio
    async def test_analyze_market_risk_level_is_valid(self, engine):
        result = await engine.analyze_market("BTCUSDT", use_live_data=False)
        assert result.risk_level in RiskLevel

    @pytest.mark.asyncio
    async def test_analyze_full_returns_dict(self, engine):
        result = await engine.analyze_full("BTCUSDT", use_live_data=False)
        assert isinstance(result, dict)
        assert "symbol" in result
        assert "bias" in result
        assert "risk_level" in result
        assert "market" in result
        assert "risk_assessment" in result
        assert "strategy" in result

    @pytest.mark.asyncio
    async def test_analyze_full_strategy_bullish(self, engine):
        result = await engine.analyze_full("BTCUSDT", use_live_data=False)
        if result["bias"] == "bullish":
            assert result["strategy"]["strategy"] == "momentum"
        elif result["bias"] == "bearish":
            assert result["strategy"]["strategy"] == "counter-trend-watch"
        else:
            assert result["strategy"]["strategy"] == "wait"

    @pytest.mark.asyncio
    async def test_analyze_full_risk_assessment_fields(self, engine):
        result = await engine.analyze_full("BTCUSDT", use_live_data=False)
        risk = result["risk_assessment"]
        assert "symbol" in risk
        assert "bias" in risk
        assert "risk_level" in risk
        assert "max_drawdown" in risk
        assert "var_95" in risk

    @pytest.mark.asyncio
    async def test_assess_risk_returns_dict(self, engine):
        risk = await engine.assess_risk("BTCUSDT", position_size=1000.0)
        assert isinstance(risk, dict)
        assert "symbol" in risk
        assert "risk_level" in risk
        assert "position_size" in risk
        assert risk["position_size"] == 1000.0

    @pytest.mark.asyncio
    async def test_generate_strategy_returns_dict(self, engine):
        strategy = await engine.generate_strategy("BTCUSDT", risk_tolerance="medium")
        assert isinstance(strategy, dict)
        assert "symbol" in strategy
        assert "strategy" in strategy
        assert "confidence" in strategy

    def test_analyze_portfolio_returns_default(self, engine):
        portfolio = asyncio.run(engine.analyze_portfolio())
        assert isinstance(portfolio, dict)
        assert portfolio["total_value"] == 0.0

    @pytest.mark.asyncio
    async def test_result_to_dict_serializable(self, engine):
        result = await engine.analyze_market("BTCUSDT", use_live_data=False)
        data = result.to_dict()
        assert isinstance(data, dict)
        assert "evidence" in data
        assert isinstance(data["evidence"], list)
        for ev in data["evidence"]:
            assert "id" in ev
            assert "type" in ev
            assert "direction" in ev
            assert 0.0 <= ev["strength"] <= 1.0

    @pytest.mark.asyncio
    async def test_multiple_timeframes_analysis(self, engine):
        result = await engine.analyze_market("BTCUSDT", timeframes=["1h", "4h"], use_live_data=False)
        assert isinstance(result, AnalysisResult)
        assert len(result.evidence) >= 1

    @pytest.mark.asyncio
    async def test_different_symbols_produce_results(self, engine):
        btc = await engine.analyze_market("BTCUSDT", use_live_data=False)
        eth = await engine.analyze_market("ETHUSDT", use_live_data=False)
        assert btc.symbol == "BTCUSDT"
        assert eth.symbol == "ETHUSDT"
        assert len(btc.evidence) >= 1
        assert len(eth.evidence) >= 1
