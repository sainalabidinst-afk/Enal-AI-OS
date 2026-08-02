"""
Data Models for Market Intelligence
====================================

TradingContext   — Raw market data from provider
MarketData      — Processed data with indicators
Evidence        — Structured evidence (facts only)
AnalysisMetadata — Audit trail
AnalysisResult  — Final structured output
"""

from dataclasses import dataclass, field
from typing import Any
from enum import Enum


class Bias(str, Enum):
    BULLISH = "bullish"
    BEARISH = "bearish"
    NEUTRAL = "neutral"


class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Timeframe(str, Enum):
    M1 = "1m"
    M5 = "5m"
    M15 = "15m"
    M30 = "30m"
    H1 = "1h"
    H4 = "4h"
    D1 = "1d"
    W1 = "1w"


@dataclass
class OHLCV:
    """Single candlestick."""
    timestamp: int
    open: float
    high: float
    low: float
    close: float
    volume: float

    def __post_init__(self):
        for attr in ('open', 'high', 'low', 'close', 'volume'):
            val = getattr(self, attr)
            if isinstance(val, (int, float)) and val < 0:
                raise ValueError(f"{attr} cannot be negative: {val}")


@dataclass
class TradingContext:
    """Raw market data from provider."""
    symbol: str
    exchange: str = "binance"
    timeframes: dict[str, list[OHLCV]] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class MarketData:
    """Processed market data with computed indicators."""
    symbol: str
    timeframe: str
    ohlcv: list[OHLCV]
    indicators: dict[str, float | str | bool] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class MarketEvidence:
    """A single evidence item (fact, not decision)."""
    id: str
    type: str          # e.g., "market_structure", "trend", "volume", "volatility", "session"
    description: str   # Human-readable, e.g., "Higher High formed on 1h"
    timeframe: str
    strength: float    # 0.0 - 1.0 (how strong this evidence is)
    direction: str     # "bullish" | "bearish" | "neutral"
    source: str        # e.g., "analyzer.trend", "indicators.ema"
    confidence: float = 0.0  # How reliable this evidence is (0-1)

    def __post_init__(self):
        self.strength = max(0.0, min(1.0, self.strength))
        self.confidence = max(0.0, min(1.0, self.confidence))


# TODO(v2): remove compatibility alias after all modules migrate to MarketEvidence.
Evidence = MarketEvidence


@dataclass
class AnalysisMetadata:
    """Metadata for reproducibility and audit."""
    symbol: str = ""
    exchange: str = "binance"
    timeframes: list[str] = field(default_factory=list)
    generated_at: str = ""
    data_source: str = ""
    analysis_version: str = "1.0.0"
    latency_ms: float = 0.0
    raw_data_points: int = 0


@dataclass
class AnalysisResult:
    """Final structured output from the Market Intelligence Engine."""
    symbol: str
    bias: Bias = Bias.NEUTRAL
    confidence: float = 0.0        # 0.0 - 1.0
    evidence: list[MarketEvidence] = field(default_factory=list)
    risk_level: RiskLevel = RiskLevel.MEDIUM
    counter_scenario: str = ""
    suggested_strategy: str = ""
    summary: str = ""
    reasoning_steps: list[str] = field(default_factory=list)
    metadata: AnalysisMetadata = field(default_factory=AnalysisMetadata)
    raw: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "symbol": self.symbol,
            "bias": self.bias.value,
            "confidence": round(self.confidence * 100),
            "evidence": [
                {
                    "id": e.id,
                    "type": e.type,
                    "description": e.description,
                    "timeframe": e.timeframe,
                    "strength": round(e.strength, 2),
                    "direction": e.direction,
                    "source": e.source,
                    "confidence": round(e.confidence, 2),
                }
                for e in self.evidence
            ],
            "risk_level": self.risk_level.value,
            "counter_scenario": self.counter_scenario,
            "suggested_strategy": self.suggested_strategy,
            "summary": self.summary,
            "reasoning_steps": self.reasoning_steps,
            "metadata": {
                "symbol": self.metadata.symbol,
                "exchange": self.metadata.exchange,
                "timeframes": self.metadata.timeframes,
                "generated_at": self.metadata.generated_at,
                "data_source": self.metadata.data_source,
                "analysis_version": self.metadata.analysis_version,
                "latency_ms": round(self.metadata.latency_ms, 2),
                "raw_data_points": self.metadata.raw_data_points,
            },
            "raw": self.raw,
        }

