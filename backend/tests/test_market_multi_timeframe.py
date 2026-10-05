"""Unit tests for MarketDataAggregator multi-timeframe methods."""

from __future__ import annotations

import pytest

from apps.trading_analyst.market_intelligence.providers import (
    MarketDataAggregator,
    MarketProviderError,
)


class FakeProvider:
    name = "fake"

    def __init__(self, data: dict[str, list[dict]] | None = None, fail: bool = False) -> None:
        self.data = data or {}
        self.fail = fail

    async def fetch_ohlcv(self, symbol: str, timeframe: str, limit: int = 100) -> list[dict]:
        if self.fail:
            raise MarketProviderError("fake provider failed")
        return self.data.get(timeframe, [])

    async def fetch_current_price(self, symbol: str) -> float:
        if self.fail:
            raise MarketProviderError("fake provider failed")
        return 100.0

    async def fetch_multi_timeframe(
        self, symbol: str, timeframes: list[str], limit: int = 100
    ) -> dict[str, list[dict]]:
        if self.fail:
            raise MarketProviderError("fake provider failed")
        return {tf: self.data.get(tf, []) for tf in timeframes}


@pytest.mark.asyncio
async def test_fetch_multi_timeframe_returns_all_requested_timeframes():
    data = {
        "15m": [{"timestamp": 1, "open": 1.0, "high": 2.0, "low": 0.5, "close": 1.5, "volume": 100.0}],
        "1h": [{"timestamp": 1, "open": 1.0, "high": 2.0, "low": 0.5, "close": 1.5, "volume": 100.0}],
        "4h": [{"timestamp": 1, "open": 1.0, "high": 2.0, "low": 0.5, "close": 1.5, "volume": 100.0}],
        "1d": [{"timestamp": 1, "open": 1.0, "high": 2.0, "low": 0.5, "close": 1.5, "volume": 100.0}],
    }
    aggregator = MarketDataAggregator([FakeProvider(data=data)])
    result = await aggregator.fetch_multi_timeframe("BTCUSDT", ["15m", "1h", "4h", "1d"])
    assert set(result.keys()) == {"15m", "1h", "4h", "1d"}
    for tf, candles in result.items():
        assert len(candles) == 1
        assert candles[0]["close"] == 1.5


@pytest.mark.asyncio
async def test_fetch_multi_timeframe_falls_back_when_provider_fails():
    aggregator = MarketDataAggregator([FakeProvider(fail=True), FakeProvider()])
    result = await aggregator.fetch_multi_timeframe("BTCUSDT", ["1h"])
    assert result["1h"] == []


@pytest.mark.asyncio
async def test_fetch_multi_timeframe_is_alias_for_get_multi_timeframe():
    data = {
        "1h": [{"timestamp": 1, "open": 1.0, "high": 2.0, "low": 0.5, "close": 1.5, "volume": 100.0}],
    }
    aggregator = MarketDataAggregator([FakeProvider(data=data)])
    via_get = await aggregator.get_multi_timeframe("BTCUSDT", ["1h"])
    via_fetch = await aggregator.fetch_multi_timeframe("BTCUSDT", ["1h"])
    assert via_get == via_fetch
