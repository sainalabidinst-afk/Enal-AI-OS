"""
Trading API Endpoints
=====================

Endpoints:
- POST /api/v1/trading/analyze — Full market analysis
- GET  /api/v1/trading/regime/live — Real-time market regime detection
- GET  /api/v1/trading/feed/status — Live feed connection status
- GET  /api/v1/trading/feed/stream — SSE stream of regime + feed status
- POST /api/v1/trading/feed/start — Start live market data feed
- POST /api/v1/trading/feed/stop — Stop live market data feed
- GET  /api/v1/trading/health — Health check
"""

import asyncio
import json
import logging
import time
from collections.abc import AsyncIterator
from typing import Any

from fastapi import APIRouter, HTTPException, Query, Request
from fastapi.responses import StreamingResponse
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


def _ensure_regime_detector(adapter) -> None:
    """Attach the regime detector to the shared feed adapter when absent."""
    from apps.trading_analyst.market_regime import MarketRegimeDetector

    if adapter.regime_detector is None:
        adapter.regime_detector = MarketRegimeDetector()


def _feed_status_payload(adapter) -> dict[str, Any]:
    status = adapter.status
    return {
        "running": status.running,
        "symbol": status.symbol,
        "timeframes": status.timeframes,
        "last_update": status.last_update,
        "error_count": status.error_count,
        "fallback_active": status.fallback_active,
        "metadata": status.metadata,
    }


@router.get("/regime/live")
async def get_live_regime(
    symbol: str = Query(..., min_length=2, max_length=20),
    lookback: int = Query(20, ge=5, le=200),
):
    """
    Get real-time market regime detection for a symbol.

    Delegates to the market feed adapter so HTTP polling and the SSE stream
    share one detection path.
    """
    from backend.app.core.market_feed_adapter import market_feed_adapter

    try:
        _ensure_regime_detector(market_feed_adapter)
        result = await market_feed_adapter.get_latest_regime(
            symbol.upper().strip(), lookback=lookback
        )
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

    return {"success": True, "data": _feed_status_payload(market_feed_adapter)}


@router.get("/feed/stream")
async def stream_feed(
    request: Request,
    symbol: str = Query("BTCUSDT", min_length=2, max_length=20),
    interval: float = Query(5.0, ge=1.0, le=60.0),
    lookback: int = Query(20, ge=5, le=200),
):
    """
    Stream market regime detections and feed status as Server-Sent Events.

    Emits an initial `snapshot` event, then a `tick` event every interval.
    Heartbeat comments keep intermediaries from closing the connection.
    """
    from backend.app.core.market_feed_adapter import market_feed_adapter

    _ensure_regime_detector(market_feed_adapter)
    pair = symbol.upper().strip()

    async def event_generator() -> AsyncIterator[str]:
        index = 0
        while True:
            if await request.is_disconnected():
                break
            regime = await market_feed_adapter.get_latest_regime(pair, lookback=lookback)
            payload = {
                "success": True,
                "data": {
                    "symbol": pair,
                    "regime": regime,
                    "feed": _feed_status_payload(market_feed_adapter),
                    "sequence": index,
                    "emitted_at": time.time(),
                },
            }
            event = "snapshot" if index == 0 else "tick"
            yield f"event: {event}\ndata: {json.dumps(payload)}\n\n"
            index += 1
            await asyncio.sleep(interval)

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


@router.post("/feed/start")
async def start_feed(req: FeedStartRequest):
    """Start live market data feed for a symbol."""
    from backend.app.core.market_feed_adapter import FeedStatus, market_feed_adapter

    if market_feed_adapter.status.running:
        raise HTTPException(status_code=409, detail="Feed is already running")

    try:
        _ensure_regime_detector(market_feed_adapter)
        market_feed_adapter.poll_interval = req.poll_interval
        market_feed_adapter.status = FeedStatus(
            running=True,
            symbol=req.symbol.upper().strip(),
            timeframes=req.timeframes or ["15m", "1h", "4h", "1d"],
            last_update=time.time(),
        )
        task = asyncio.create_task(
            market_feed_adapter.start_live_feed(
                symbol=req.symbol.upper().strip(),
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
