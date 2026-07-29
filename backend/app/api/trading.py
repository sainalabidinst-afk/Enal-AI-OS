"""
Trading API Endpoint
====================

POST /api/v1/trading/analyze

Accepts a symbol and optional parameters, returns structured market analysis.
"""

import logging
import time
from typing import Any
from pydantic import BaseModel, Field

from fastapi import APIRouter, HTTPException

from apps.trading_analyst.market_intelligence.provider import build_trading_context, DEFAULT_TIMEFRAMES
from apps.trading_analyst.market_intelligence.analyzer import MarketAnalyzer
from apps.trading_analyst.market_intelligence.summary import MarketSummaryGenerator

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/trading", tags=["trading"])


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


@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze_market(req: AnalyzeRequest):
    """
    Analyze market conditions for a given symbol.

    Returns structured analysis with evidence, confidence scores, and summary.
    Does NOT return trading signals (BUY/SELL).
    """
    start = time.monotonic()

    try:
        symbol = req.symbol.upper().strip()
        timeframes = req.timeframes or DEFAULT_TIMEFRAMES

        # Step 1: Fetch market data
        ctx = await build_trading_context(symbol, timeframes, req.exchange)
        if not ctx.timeframes:
            raise HTTPException(
                status_code=502,
                detail=f"Failed to fetch market data for {symbol}. Check symbol and try again.",
            )

        latency_ms = (time.monotonic() - start) * 1000

        # Step 2: Analyze
        analyzer = MarketAnalyzer()
        raw_evidence = await analyzer.analyze(ctx)
        analyzed_timeframes = analyzer.get_analyzed_timeframes()

        if not analyzed_timeframes:
            raise HTTPException(
                status_code=422,
                detail=f"Insufficient data to analyze {symbol}. Need at least 20 candles per timeframe.",
            )

        # Step 3: Generate summary
        generator = MarketSummaryGenerator()
        result = generator.generate(
            raw_evidence=raw_evidence,
            timeframes=analyzed_timeframes,
            symbol=symbol,
            exchange=req.exchange,
            latency_ms=latency_ms,
        )

        # Step 4: Return
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


@router.get("/health", response_model=dict[str, Any])
async def trading_health():
    """Health check for trading module."""
    return {
        "status": "ok",
        "module": "trading_analyst",
        "version": "1.0.0",
    }
