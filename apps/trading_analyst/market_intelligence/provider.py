"""
Market Data Provider
=====================

Multi-provider aggregator with fallback for market data.

Providers (in fallback order):
1. BinanceProvider — public REST API, no key required
2. YahooFinanceProvider — yfinance library, delayed data

Usage:
    from apps.trading_analyst.market_intelligence.provider import get_provider
    provider = get_provider()
    data = await provider.get_ohlcv("BTCUSDT", "1h")
"""

from __future__ import annotations

import logging
from typing import Any

from apps.trading_analyst.market_intelligence.models import OHLCV, TradingContext
from apps.trading_analyst.market_intelligence.providers import (
    BinanceProvider,
    MarketDataAggregator,
    MarketProviderError,
    RateLimitError,
    YahooFinanceProvider,
)

logger = logging.getLogger(__name__)

BINANCE_BASE = "https://api2.binance.com"
TIMEFRAME_MAP = {
    "1m": "1m",
    "5m": "5m",
    "15m": "15m",
    "30m": "30m",
    "1h": "1h",
    "4h": "4h",
    "1d": "1d",
    "1w": "1w",
}
DEFAULT_TIMEFRAMES = ["15m", "1h", "4h", "1d"]
DEFAULT_LIMIT = 100

# Default aggregator instance
_provider: MarketDataAggregator | None = None


def get_provider() -> MarketDataAggregator:
    """Get default market data provider aggregator."""
    global _provider
    if _provider is None:
        _provider = MarketDataAggregator([BinanceProvider(), YahooFinanceProvider()])
    return _provider


# Backward-compatible sync wrappers
def fetch_ohlcv(symbol: str, timeframe: str, limit: int = DEFAULT_LIMIT) -> list[dict]:
    provider = get_provider()
    return provider.fetch_ohlcv(symbol, timeframe, limit)


def fetch_current_price(symbol: str) -> float:
    provider = get_provider()
    return provider.fetch_current_price(symbol)


def fetch_multi_timeframe(
    symbol: str, timeframes: list[str], limit: int = DEFAULT_LIMIT
) -> dict[str, list[dict]]:
    provider = get_provider()
    return provider.fetch_multi_timeframe(symbol, timeframes, limit)


def get_available_symbols() -> list[str]:
    binance = BinanceProvider()
    import asyncio

    return asyncio.run(binance.fetch_available_symbols())


def validate_symbol(symbol: str) -> bool:
    try:
        fetch_current_price(symbol)
        return True
    except MarketProviderError:
        return False


# Async versions
async def fetch_ohlcv_async(symbol: str, timeframe: str, limit: int = DEFAULT_LIMIT) -> list[dict]:
    provider = get_provider()
    return await provider.fetch_ohlcv(symbol, timeframe, limit)


async def fetch_current_price_async(symbol: str) -> float:
    provider = get_provider()
    return await provider.fetch_current_price(symbol)


async def fetch_multi_timeframe_async(
    symbol: str, timeframes: list[str], limit: int = DEFAULT_LIMIT
) -> dict[str, list[dict]]:
    provider = get_provider()
    return await provider.fetch_multi_timeframe(symbol, timeframes, limit)


async def build_trading_context(
    symbol: str, timeframes: list[str], exchange: str = "binance"
) -> TradingContext:
    provider = get_provider()
    return await provider.build_trading_context(symbol, timeframes, exchange)


__all__ = [
    "get_provider",
    "MarketDataAggregator",
    "BinanceProvider",
    "YahooFinanceProvider",
    "MarketProviderError",
    "RateLimitError",
    "fetch_ohlcv",
    "fetch_current_price",
    "fetch_multi_timeframe",
    "fetch_ohlcv_async",
    "fetch_current_price_async",
    "fetch_multi_timeframe_async",
    "build_trading_context",
    "get_available_symbols",
    "validate_symbol",
    "DEFAULT_TIMEFRAMES",
    "DEFAULT_LIMIT",
    "TIMEFRAME_MAP",
]
