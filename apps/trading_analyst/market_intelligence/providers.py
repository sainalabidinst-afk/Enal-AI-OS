"""
Market Data Providers
=====================

Multi-provider aggregator with fallback for market data.

Providers (in fallback order):
1. BinanceProvider — public REST API, no key required
2. YahooFinanceProvider — yfinance library, delayed data
3. AlphaVantageProvider — requires API key, 25 req/day free
4. TwelveDataProvider — requires API key, 800 req/day free

Usage:
    provider = MarketDataAggregator()
    data = await provider.get_ohlcv("BTCUSDT", "1h")
"""

from __future__ import annotations

import asyncio
import logging
from abc import ABC, abstractmethod
from typing import Any

from apps.trading_analyst.market_intelligence.models import OHLCV, TradingContext

logger = logging.getLogger(__name__)


class MarketProviderError(Exception):
    """Raised when market data provider fails."""


class RateLimitError(Exception):
    """Raised when market data provider rate limit is hit."""

    def __init__(self, retry_after: float = 60.0, message: str = "Rate limited") -> None:
        self.retry_after = retry_after
        super().__init__(message)


class BaseMarketProvider(ABC):
    """Abstract base class for market data providers."""

    name: str = "base"
    requires_api_key: bool = False

    @abstractmethod
    async def fetch_ohlcv(
        self, symbol: str, timeframe: str, limit: int = 100
    ) -> list[dict]:
        """Fetch OHLCV candlestick data."""

    @abstractmethod
    async def fetch_current_price(self, symbol: str) -> float:
        """Fetch current price."""

    @abstractmethod
    async def fetch_multi_timeframe(
        self, symbol: str, timeframes: list[str], limit: int = 100
    ) -> dict[str, list[dict]]:
        """Fetch OHLCV for multiple timeframes."""


class BinanceProvider(BaseMarketProvider):
    """Binance public API provider (no key required)."""

    name = "binance"
    requires_api_key = False

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

    def _fetch_json(self, url: str) -> Any:
        import json
        import urllib.error
        import urllib.request

        try:
            req = urllib.request.Request(url, headers={"User-Agent": "ECP-Trading/1.0"})
            with urllib.request.urlopen(req, timeout=15) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            if e.code == 429:
                raise RateLimitError(retry_after=60.0, message="Binance rate limited")
            raise MarketProviderError(f"HTTP {e.code}: {e.reason} for {url}")
        except urllib.error.URLError as e:
            raise MarketProviderError(f"Binance connection failed: {e.reason}")
        except Exception as e:
            raise MarketProviderError(f"Binance unexpected error: {e}")

    async def fetch_ohlcv(self, symbol: str, timeframe: str, limit: int = 100) -> list[dict]:
        tf = self.TIMEFRAME_MAP.get(timeframe)
        if not tf:
            raise ValueError(f"Unsupported timeframe: {timeframe}")

        url = f"{self.BINANCE_BASE}/api/v3/klines?symbol={symbol.upper()}&interval={tf}&limit={limit}"
        data = await asyncio.to_thread(self._fetch_json, url)

        if not isinstance(data, list):
            raise MarketProviderError(f"Unexpected response format: {type(data)}")

        result = []
        for candle in data:
            result.append(
                {
                    "timestamp": int(candle[0]) // 1000,
                    "open": float(candle[1]),
                    "high": float(candle[2]),
                    "low": float(candle[3]),
                    "close": float(candle[4]),
                    "volume": float(candle[5]),
                }
            )
        return result

    async def fetch_current_price(self, symbol: str) -> float:
        url = f"{self.BINANCE_BASE}/api/v3/ticker/price?symbol={symbol.upper()}"
        data = await asyncio.to_thread(self._fetch_json, url)
        if isinstance(data, dict) and "price" in data:
            return float(data["price"])
        raise MarketProviderError(f"Could not fetch price for {symbol}: {data}")

    async def fetch_multi_timeframe(
        self, symbol: str, timeframes: list[str], limit: int = 100
    ) -> dict[str, list[dict]]:
        result: dict[str, list[dict]] = {}
        for tf in timeframes:
            try:
                result[tf] = await self.fetch_ohlcv(symbol, tf, limit)
            except Exception as e:
                logger.warning("Binance failed for %s %s: %s", symbol, tf, e)
                result[tf] = []
        return result

    async def fetch_available_symbols(self) -> list[str]:
        """Get list of available trading pairs."""
        url = f"{self.BINANCE_BASE}/api/v3/exchangeInfo"
        data = await asyncio.to_thread(self._fetch_json, url)
        symbols = []
        for s in data.get("symbols", []):
            if s.get("status") == "TRADING":
                symbols.append(s["symbol"])
        return sorted(symbols)


class YahooFinanceProvider(BaseMarketProvider):
    """Yahoo Finance provider via yfinance library (delayed data, no key required)."""

    name = "yahoo_finance"
    requires_api_key = False

    def _normalize_symbol(self, symbol: str) -> str:
        """Normalize symbol for Yahoo Finance."""
        symbol = symbol.upper()
        if symbol.endswith("USDT") and not symbol.endswith("USD"):
            symbol = symbol[:-4] + "-USD"
        return symbol

    def _normalize_timeframe(self, timeframe: str) -> str:
        """Normalize timeframe for yfinance."""
        mapping = {
            "1m": "1m",
            "5m": "5m",
            "15m": "15m",
            "30m": "30m",
            "1h": "60m",
            "4h": "4h",
            "1d": "1d",
            "1w": "1wk",
        }
        return mapping.get(timeframe, "1d")

    async def _run_sync(self, func, *args: Any, **kwargs: Any) -> Any:
        """Run synchronous yfinance call in thread pool."""
        return await asyncio.to_thread(func, *args, **kwargs)

    async def fetch_ohlcv(self, symbol: str, timeframe: str, limit: int = 100) -> list[dict]:
        import yfinance as yf

        yf_symbol = self._normalize_symbol(symbol)
        yf_tf = self._normalize_timeframe(timeframe)

        def _fetch() -> list[dict]:
            ticker = yf.Ticker(yf_symbol)
            hist = ticker.history(period="60d", interval=yf_tf)
            if hist.empty:
                raise MarketProviderError(f"No data for {yf_symbol}")
            result = []
            for idx, row in hist.tail(limit).iterrows():
                result.append(
                    {
                        "timestamp": int(idx.timestamp()),
                        "open": float(row["Open"]),
                        "high": float(row["High"]),
                        "low": float(row["Low"]),
                        "close": float(row["Close"]),
                        "volume": float(row["Volume"]),
                    }
                )
            return result

        return await self._run_sync(_fetch)

    async def fetch_current_price(self, symbol: str) -> float:
        import yfinance as yf

        yf_symbol = self._normalize_symbol(symbol)

        def _fetch() -> float:
            ticker = yf.Ticker(yf_symbol)
            info = ticker.info
            price = info.get("regularMarketPrice") or info.get("currentPrice")
            if price is None:
                raise MarketProviderError(f"No price for {yf_symbol}")
            return float(price)

        return await self._run_sync(_fetch)

    async def fetch_multi_timeframe(
        self, symbol: str, timeframes: list[str], limit: int = 100
    ) -> dict[str, list[dict]]:
        result: dict[str, list[dict]] = {}
        for tf in timeframes:
            try:
                result[tf] = await self.fetch_ohlcv(symbol, tf, limit)
            except Exception as e:
                logger.warning("Yahoo Finance failed for %s %s: %s", symbol, tf, e)
                result[tf] = []
        return result


class MarketDataAggregator:
    """Aggregates multiple market data providers with fallback logic."""

    def __init__(self, providers: list[BaseMarketProvider] | None = None) -> None:
        if providers is None:
            self.providers: list[BaseMarketProvider] = [
                BinanceProvider(),
                YahooFinanceProvider(),
            ]
        else:
            self.providers = providers

    async def get_ohlcv(self, symbol: str, timeframe: str, limit: int = 100) -> list[dict]:
        """Try providers in order, return first successful result."""
        errors: list[str] = []
        for provider in self.providers:
            try:
                data = await provider.fetch_ohlcv(symbol, timeframe, limit)
                if data:
                    logger.info("OHLCV from %s: %d candles for %s", provider.name, len(data), symbol)
                    return data
            except Exception as e:
                logger.warning("Provider %s failed for %s %s: %s", provider.name, symbol, timeframe, e)
                errors.append(f"{provider.name}: {e}")

        raise MarketProviderError(
            f"All providers failed for {symbol} {timeframe}: {'; '.join(errors)}"
        )

    async def get_current_price(self, symbol: str) -> float:
        """Try providers in order, return first successful price."""
        errors: list[str] = []
        for provider in self.providers:
            try:
                price = await provider.fetch_current_price(symbol)
                logger.info("Price from %s: %.2f for %s", provider.name, price, symbol)
                return price
            except Exception as e:
                logger.warning("Provider %s failed for price %s: %s", provider.name, symbol, e)
                errors.append(f"{provider.name}: {e}")

        raise MarketProviderError(f"All providers failed for price {symbol}: {'; '.join(errors)}")

    async def get_multi_timeframe(
        self, symbol: str, timeframes: list[str], limit: int = 100
    ) -> dict[str, list[dict]]:
        """Aggregate timeframes, trying providers per timeframe."""
        result: dict[str, list[dict]] = {}
        for tf in timeframes:
            try:
                result[tf] = await self.get_ohlcv(symbol, tf, limit)
            except Exception as e:
                logger.warning("All providers failed for %s %s: %s", symbol, tf, e)
                result[tf] = []
        return result

    async def build_trading_context(
        self, symbol: str, timeframes: list[str], exchange: str = "binance"
    ) -> TradingContext:
        """Build TradingContext using aggregated providers."""
        from apps.trading_analyst.market_intelligence.models import OHLCV

        raw_data = await self.get_multi_timeframe(symbol, timeframes)
        parsed: dict[str, list[OHLCV]] = {}
        for tf, candles in raw_data.items():
            parsed[tf] = [
                OHLCV(
                    timestamp=c["timestamp"],
                    open=c["open"],
                    high=c["high"],
                    low=c["low"],
                    close=c["close"],
                    volume=c["volume"],
                )
                for c in candles
            ]
        if not any(parsed.values()):
            raise MarketProviderError(f"No market data available for {symbol}")

        return TradingContext(
            symbol=symbol.upper(),
            exchange=exchange,
            timeframes=parsed,
            metadata={
                "requested_timeframes": timeframes,
                "fetched_timeframes": [tf for tf, candles in parsed.items() if candles],
                "provider_aggregator": True,
            },
        )
