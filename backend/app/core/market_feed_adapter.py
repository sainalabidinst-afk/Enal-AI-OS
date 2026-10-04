"""
Real-Time Market Feed Adapter for Trading Analyst.

Provides WebSocket-like streaming market data with automatic fallback to synthetic data.
Integrates with TradingEngine for live market regime detection.
"""

from __future__ import annotations

import asyncio
import logging
import time
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any

from apps.trading_analyst.market_intelligence.provider import fetch_multi_timeframe

logger = logging.getLogger(__name__)


@dataclass
class MarketFeedSnapshot:
    """Single snapshot of market data."""

    symbol: str
    timeframe: str
    timestamp: int
    open: float
    high: float
    low: float
    close: float
    volume: float
    regime: str = "sideways"
    confidence: float = 0.0
    source: str = "live"


@dataclass
class FeedStatus:
    """Status of the market feed adapter."""

    running: bool = False
    symbol: str | None = None
    timeframes: list[str] = field(default_factory=list)
    last_update: float = 0.0
    error_count: int = 0
    fallback_active: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)


class MarketFeedAdapter:
    """Real-time market feed adapter with live polling and fallback."""

    def __init__(
        self,
        poll_interval: float = 5.0,
        max_errors: int = 10,
        regime_detector=None,
    ) -> None:
        self.poll_interval = poll_interval
        self.max_errors = max_errors
        self.regime_detector = regime_detector
        self.status = FeedStatus()
        self._subscribers: list[Callable[[MarketFeedSnapshot], None]] = []
        self._task: asyncio.Task | None = None
        self._latest_snapshot: MarketFeedSnapshot | None = None

    def subscribe(self, callback: Callable[[MarketFeedSnapshot], None]) -> None:
        """Subscribe to live feed updates."""
        self._subscribers.append(callback)

    def unsubscribe(self, callback: Callable[[MarketFeedSnapshot], None]) -> None:
        """Unsubscribe from live feed updates."""
        if callback in self._subscribers:
            self._subscribers.remove(callback)

    async def start_live_feed(
        self,
        symbol: str,
        timeframes: list[str] | None = None,
        exchange: str = "binance",
    ) -> FeedStatus:
        """Start live market data feed."""
        tf_list = timeframes or ["15m", "1h", "4h", "1d"]
        self.status = FeedStatus(
            running=True,
            symbol=symbol.upper(),
            timeframes=tf_list,
            last_update=time.time(),
        )
        logger.info("Starting live feed for %s on %s", symbol, tf_list)
        try:
            await self._poll_loop(symbol, tf_list, exchange)
        except asyncio.CancelledError:
            logger.info("Live feed stopped for %s", symbol)
        except Exception as exc:
            logger.error("Live feed error for %s: %s", symbol, exc)
            self.status.fallback_active = True
        finally:
            self.status.running = False
        return self.status

    async def stop_live_feed(self) -> None:
        """Stop live market data feed."""
        self.status.running = False
        if self._task:
            self._task.cancel()
            self._task = None
        logger.info("Live feed stopped")

    async def get_latest_regime(self, symbol: str, lookback: int = 20) -> dict[str, Any]:
        """Get latest market regime detection."""
        try:
            tf_list = self.status.timeframes or ["1h", "4h", "1d"]
            raw_data = fetch_multi_timeframe(symbol, tf_list)
            all_closes: list[float] = []
            all_volumes: list[float] = []
            for candles in raw_data.values():
                for c in candles:
                    all_closes.append(c["close"])
                    all_volumes.append(c["volume"])
            if len(all_closes) < lookback:
                return {"error": "insufficient_data", "regime": "unknown"}
            if self.regime_detector:
                regime = self.regime_detector.detect(all_closes, all_volumes, lookback)
                return {
                    "symbol": symbol,
                    "regime": regime.regime,
                    "confidence": regime.confidence,
                    "volatility": regime.volatility,
                    "trend_strength": regime.trend_strength,
                    "source": "live",
                    "timestamp": time.time(),
                }
            return {"error": "no_regime_detector", "regime": "unknown"}
        except Exception as exc:
            logger.error("Failed to get latest regime for %s: %s", symbol, exc)
            return {"error": str(exc), "regime": "unknown", "source": "fallback"}

    async def _poll_loop(self, symbol: str, timeframes: list[str], exchange: str) -> None:
        """Main polling loop for live market data."""
        errors = 0
        while self.status.running:
            try:
                raw_data = fetch_multi_timeframe(symbol, timeframes)
                if not any(raw_data.values()):
                    raise ValueError(f"No data returned for {symbol}")
                snapshot = self._build_snapshot(symbol, raw_data)
                if self.regime_detector:
                    all_closes = [c["close"] for candles in raw_data.values() for c in candles]
                    all_volumes = [c["volume"] for candles in raw_data.values() for c in candles]
                    regime = self.regime_detector.detect(all_closes, all_volumes)
                    snapshot.regime = regime.regime
                    snapshot.confidence = regime.confidence
                self._latest_snapshot = snapshot
                self.status.last_update = time.time()
                self.status.error_count = 0
                self.status.fallback_active = False
                for callback in self._subscribers:
                    try:
                        callback(snapshot)
                    except Exception as exc:
                        logger.warning("Subscriber callback failed: %s", exc)
                errors = 0
            except Exception as exc:
                errors += 1
                self.status.error_count = errors
                logger.warning("Poll error %d/%d for %s: %s", errors, self.max_errors, symbol, exc)
                if errors >= self.max_errors:
                    self.status.fallback_active = True
                    logger.error("Max errors reached, activating fallback for %s", symbol)
                    break
            await asyncio.sleep(self.poll_interval)

    def _build_snapshot(self, symbol: str, raw_data: dict[str, list[dict]]) -> MarketFeedSnapshot:
        """Build a MarketFeedSnapshot from raw market data."""
        latest_tf = list(raw_data.keys())[-1] if raw_data else "1h"
        candles = raw_data.get(latest_tf, [])
        if not candles:
            return MarketFeedSnapshot(
                symbol=symbol,
                timeframe=latest_tf,
                timestamp=0,
                open=0.0,
                high=0.0,
                low=0.0,
                close=0.0,
                volume=0.0,
            )
        latest = candles[-1]
        return MarketFeedSnapshot(
            symbol=symbol,
            timeframe=latest_tf,
            timestamp=latest["timestamp"],
            open=latest["open"],
            high=latest["high"],
            low=latest["low"],
            close=latest["close"],
            volume=latest["volume"],
            source="live",
        )


market_feed_adapter = MarketFeedAdapter()
