"""
Trading API Endpoints
=====================

Endpoints:
- POST /api/v1/trading/analyze — Full market analysis
- GET  /api/v1/trading/regime/live — Real-time market regime detection
- GET  /api/v1/trading/feed/status — Live feed connection status
- POST /api/v1/trading/feed/start — Start live market data feed
- POST /api/v1/trading/feed/stop — Stop live market data feed
- GET  /api/v1/trading/health — Health check
"""

import asyncio
import logging
import time
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/trading", tags=["trading"])


class AnalyzeRequest(BaseModel):
    symbol: str = Field(..., description="Trading pair, e.g. BTCUSDT", min_length=2, max_length=20)
    timeframes: list[str] | None = Field(
        default=None,
        description="Timeframes to analyze. Default: 15m, 1h, 4h, 1d",
    )
    exchange: str = Field(default="binance", description="Exchange name")


class AnalyzeResponse(BaseModel):
    success: bool
    data: dict[str, Any] | None = None
    error: str | None = None


class FeedStartRequest(BaseModel):
    symbol: str = Field(..., min_length=2, max_length=20)
    timeframes: list[str] | None = Field(default=None)
    poll_interval: float = Field(default=5.0, ge=1.0, le=60.0)


@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze_market(req: AnalyzeRequest):
    """
    Analyze market conditions for a given symbol.

    Returns structured analysis with evidence, confidence scores, and summary.
    Does NOT return trading signals (BUY/SELL).
    """
    from apps.trading_analyst.market_intelligence.analyzer import MarketAnalyzer
    from apps.trading_analyst.market_intelligence.provider import (
        DEFAULT_TIMEFRAMES,
        build_trading_context,
    )
    from apps.trading_analyst.market_intelligence.summary import MarketSummaryGenerator

    start = time.monotonic()

    try:
        symbol = req.symbol.upper().strip()
        timeframes = req.timeframes or DEFAULT_TIMEFRAMES

        ctx = await build_trading_context(symbol, timeframes, req.exchange)
        if not ctx.timeframes:
            raise HTTPException(
                status_code=502,
                detail=f"Failed to fetch market data for {symbol}. Check symbol and try again.",
            )

        latency_ms = (time.monotonic() - start) * 1000

        analyzer = MarketAnalyzer()
        raw_evidence = await analyzer.analyze(ctx)
        analyzed_timeframes = analyzer.get_analyzed_timeframes()

        if not analyzed_timeframes:
            raise HTTPException(
                status_code=422,
                detail=(
                    f"Insufficient data to analyze {symbol}. "
                    "Need at least 20 candles per timeframe."
                ),
            )

        generator = MarketSummaryGenerator()
        result = generator.generate(
            raw_evidence=raw_evidence,
            timeframes=analyzed_timeframes,
            symbol=symbol,
            exchange=req.exchange,
            latency_ms=latency_ms,
        )

        return AnalyzeResponse(
            success=True,
            data=result.to_dict(),
        )

    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except ConnectionError as e:
        raise HTTPException(status_code=502, detail=f"Data provider error: {e}")
    except Exception as e:
        logger.exception("Unexpected error analyzing %s", req.symbol)
        raise HTTPException(status_code=500, detail=f"Analysis failed: {e}")


@router.get("/regime/live")
async def get_live_regime(symbol: str, lookback: int = 20):
    """
    Get real-time market regime detection for a symbol.

    Uses live market data when available, falls back to synthetic data.
    """
    from apps.trading_analyst.engine import trading_engine

    try:
        result = await trading_engine.detect_market_regime(symbol)
        return {"success": True, "data": result}
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Failed to detect regime for %s", symbol)
        raise HTTPException(status_code=500, detail=f"Regime detection failed: {e}")


@router.get("/feed/status")
async def get_feed_status():
    """Get current live feed connection status."""
    from backend.app.core.market_feed_adapter import market_feed_adapter

    status = market_feed_adapter.status
    return {
        "success": True,
        "data": {
            "running": status.running,
            "symbol": status.symbol,
            "timeframes": status.timeframes,
            "last_update": status.last_update,
            "error_count": status.error_count,
            "fallback_active": status.fallback_active,
            "metadata": status.metadata,
        },
    }


@router.post("/feed/start")
async def start_feed(req: FeedStartRequest):
    """Start live market data feed for a symbol."""
    from apps.trading_analyst.market_regime import MarketRegimeDetector

    from backend.app.core.market_feed_adapter import market_feed_adapter

    if market_feed_adapter.status.running:
        raise HTTPException(status_code=409, detail="Feed is already running")

    try:
        market_feed_adapter.regime_detector = MarketRegimeDetector()
        task = asyncio.create_task(
            market_feed_adapter.start_live_feed(
                symbol=req.symbol,
                timeframes=req.timeframes,
            )
        )
        market_feed_adapter._task = task
        return {
            "success": True,
            "data": {
                "message": f"Live feed started for {req.symbol}",
                "symbol": req.symbol.upper(),
                "timeframes": req.timeframes or ["15m", "1h", "4h", "1d"],
                "poll_interval": req.poll_interval,
            },
        }
    except Exception as e:
        logger.exception("Failed to start feed for %s", req.symbol)
        raise HTTPException(status_code=500, detail=f"Failed to start feed: {e}")


@router.post("/feed/stop")
async def stop_feed():
    """Stop live market data feed."""
    from backend.app.core.market_feed_adapter import market_feed_adapter

    if not market_feed_adapter.status.running:
        raise HTTPException(status_code=409, detail="Feed is not running")

    await market_feed_adapter.stop_live_feed()
    return {"success": True, "data": {"message": "Live feed stopped"}}


@router.get("/health", response_model=dict[str, Any])
async def trading_health():
    """Health check for trading module."""
    return {
        "status": "ok",
        "module": "trading_analyst",
        "version": "1.0.0",
        "live_feed_available": True,
    }
