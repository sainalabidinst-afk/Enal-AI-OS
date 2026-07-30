"""
Market Data Provider
====================

Interface for fetching market data from various sources.

Current implementation: Binance Public API (free, no API key required for public endpoints)

Future: Bybit, OKX, CSV, Manual input — all via same interface.
"""

import logging
import time
import urllib.request
import urllib.error
import json
from typing import Any
from dataclasses import dataclass, field

from apps.trading_analyst.market_intelligence.models import OHLCV, TradingContext

logger = logging.getLogger(__name__)

BINANCE_BASE = "https://api.binance.com"
TIMEFRAME_MAP = {
    "1m": "1m", "5m": "5m", "15m": "15m", "30m": "30m",
    "1h": "1h", "4h": "4h", "1d": "1d", "1w": "1w",
}
DEFAULT_TIMEFRAMES = ["15m", "1h", "4h", "1d"]
DEFAULT_LIMIT = 100  # candles per request


class MarketProviderError(Exception):
    """Raised when market data provider fails."""


def _fetch_json(url: str) -> Any:
    """Fetch JSON from URL with timeout and error handling."""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "ECP-Trading/1.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        raise MarketProviderError(f"HTTP {e.code}: {e.reason} for {url}")
    except urllib.error.URLError as e:
        raise MarketProviderError(f"Connection failed: {e.reason}")
    except json.JSONDecodeError as e:
        raise MarketProviderError(f"Invalid JSON response: {e}")
    except Exception as e:
        raise MarketProviderError(f"Unexpected error: {e}")


def fetch_ohlcv(symbol: str, timeframe: str, limit: int = DEFAULT_LIMIT) -> list[dict]:
    """
    Fetch OHLCV candlestick data from Binance Public API.

    Args:
        symbol: Trading pair, e.g., "BTCUSDT"
        timeframe: "1m", "5m", "15m", "30m", "1h", "4h", "1d", "1w"
        limit: Number of candles (max 1000)

    Returns:
        List of dicts with keys: timestamp, open, high, low, close, volume

    Raises:
        MarketProviderError: If API call fails
    """
    tf = TIMEFRAME_MAP.get(timeframe)
    if not tf:
        raise ValueError(f"Unsupported timeframe: {timeframe}. Use: {list(TIMEFRAME_MAP.keys())}")

    url = f"{BINANCE_BASE}/api/v3/klines?symbol={symbol.upper()}&interval={tf}&limit={limit}"
    data = _fetch_json(url)

    if not isinstance(data, list):
        raise MarketProviderError(f"Unexpected response format: {type(data)}")

    result = []
    for candle in data:
        result.append({
            "timestamp": int(candle[0]) // 1000,  # Binance returns ms
            "open": float(candle[1]),
            "high": float(candle[2]),
            "low": float(candle[3]),
            "close": float(candle[4]),
            "volume": float(candle[5]),
        })
    return result


def fetch_current_price(symbol: str) -> float:
    """Fetch current price for a symbol."""
    url = f"{BINANCE_BASE}/api/v3/ticker/price?symbol={symbol.upper()}"
    data = _fetch_json(url)
    if isinstance(data, dict) and "price" in data:
        return float(data["price"])
    raise MarketProviderError(f"Could not fetch price for {symbol}: {data}")


def fetch_24hr_ticker(symbol: str) -> dict:
    """Fetch 24hr ticker statistics."""
    url = f"{BINANCE_BASE}/api/v3/ticker/24hr?symbol={symbol.upper()}"
    return _fetch_json(url)


def fetch_multi_timeframe(symbol: str, timeframes: list[str], limit: int = DEFAULT_LIMIT) -> dict[str, list[dict]]:
    """
    Fetch OHLCV for multiple timeframes.

    Returns:
        dict mapping timeframe -> list of candles
    """
    result = {}
    for tf in timeframes:
        try:
            result[tf] = fetch_ohlcv(symbol, tf, limit)
            logger.debug("Fetched %d candles for %s %s", len(result[tf]), symbol, tf)
        except Exception as e:
            logger.warning("Failed to fetch %s %s: %s", symbol, tf, e)
            result[tf] = []
    return result


def get_available_symbols() -> list[str]:
    """Get list of available USDT trading pairs from Binance."""
    url = f"{BINANCE_BASE}/api/v3/exchangeInfo"
    data = _fetch_json(url)
    symbols = []
    for s in data.get("symbols", []):
        if s.get("quoteAsset") == "USDT" and s.get("status") == "TRADING":
            symbols.append(s["symbol"])
    return sorted(symbols)


def validate_symbol(symbol: str) -> bool:
    """Check if a symbol is valid on Binance."""
    try:
        fetch_current_price(symbol)
        return True
    except MarketProviderError:
        return False


async def build_trading_context(symbol: str, timeframes: list[str], exchange: str = "binance") -> TradingContext:
    """Build a TradingContext by fetching market data for multiple timeframes."""
    raw_data = fetch_multi_timeframe(symbol, timeframes)
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
    return TradingContext(
        symbol=symbol.upper(),
        exchange=exchange,
        timeframes=parsed,
        metadata={
            "requested_timeframes": timeframes,
            "fetched_timeframes": [tf for tf, candles in parsed.items() if candles],
        },
    )

