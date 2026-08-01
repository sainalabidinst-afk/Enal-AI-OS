"""
Trading Engine
==============

Full-pipeline trading engine for the Trading Analyst Reference App.

Integrates all market intelligence analyzers into a single analysis pipeline:

- MarketAnalyzer        -> market_structure, trend, volume, volatility
- WyckoffAnalyzer       -> accumulation, distribution, composite operator
- SMCAnalyzer           -> FVG, order blocks, liquidity sweeps, premium/discount
- ElliottWaveAnalyzer   -> impulse/corrective waves, ending diagonal
- VolumeProfileAnalyzer -> POC, value area, HVN/LVN, profile shape
- PsychologyAnalyzer    -> sentiment extremes, FOMO, volume psychology
- MacroAnalyzer         -> policy rate, inflation, economic health, risk sentiment
- DerivativesAnalyzer   -> IV, put/call, skew, futures basis, COT, max pain

Pipeline:
    TradingContext
        |
    MarketAnalyzer (4 core categories)
        |
    Domain Analyzers (Wyckoff, SMC, Elliott Wave, Volume Profile, Psychology,
                      Macro, Derivatives)
        |
    EvidenceBuilder (cross-timeframe boost, deduplication, normalization)
        |
    ConfidenceScorer (weighted 35/25/20/10/10)
        |
    MarketSummaryGenerator -> AnalysisResult
"""

import logging
import random
import time
from typing import Any

from apps.trading_analyst.market_intelligence.models import (
    OHLCV,
    AnalysisResult,
    TradingContext,
    MarketEvidence,
    Bias,
)
from apps.trading_analyst.market_intelligence.analyzer import MarketAnalyzer
from apps.trading_analyst.market_intelligence.wyckoff import WyckoffAnalyzer
from apps.trading_analyst.market_intelligence.smc import SMCAnalyzer
from apps.trading_analyst.market_intelligence.elliott_wave import ElliottWaveAnalyzer
from apps.trading_analyst.market_intelligence.volume_profile import VolumeProfileAnalyzer
from apps.trading_analyst.market_intelligence.psychology import PsychologyAnalyzer
from apps.trading_analyst.market_intelligence.macro_analyzer import MacroAnalyzer
from apps.trading_analyst.market_intelligence.derivatives import DerivativesAnalyzer
from apps.trading_analyst.market_intelligence.summary import MarketSummaryGenerator
from apps.trading_analyst.market_intelligence import indicators as ind

logger = logging.getLogger(__name__)

DEFAULT_TIMEFRAMES = ["15m", "1h", "4h", "1d"]

# Maximum number of FVG evidence items per timeframe (noise reduction).
FVG_CAP_PER_TIMEFRAME = 8


class TradingEngine:
    """
    Orchestrates the full market analysis pipeline.

    Each public method is async for consistency with the data provider layer.

    Usage::

        engine = TradingEngine()
        result = await engine.analyze_market("BTCUSDT")
        result.to_dict()  # JSON-serializable output
    """

    def __init__(self) -> None:
        self.analyzer = MarketAnalyzer()
        self.wyckoff = WyckoffAnalyzer()
        self.smc = SMCAnalyzer()
        self.elliott = ElliottWaveAnalyzer()
        self.volume_profile = VolumeProfileAnalyzer()
        self.psychology = PsychologyAnalyzer()
        self.macro = MacroAnalyzer()
        self.derivatives = DerivativesAnalyzer()
        self.summary = MarketSummaryGenerator()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    async def analyze_market(
        self,
        symbol: str,
        timeframes: list[str] | None = None,
        exchange: str = "binance",
        use_live_data: bool = True,
        macro_data: dict[str, Any] | None = None,
        derivatives_data: dict[str, Any] | None = None,
    ) -> AnalysisResult:
        """
        Run the full market analysis pipeline for a symbol.

        Args:
            symbol: Trading pair, e.g. "BTCUSDT" or project id for fallback.
            timeframes: List of timeframes to analyze. Defaults to
                        ["15m", "1h", "4h", "1d"].
            exchange: Exchange label.
            use_live_data: If True, try to fetch live data from the provider.
                           If False or network unavailable, fall back to a
                           deterministic synthetic context.
            macro_data: Optional dict of macro indicators.
            derivatives_data: Optional dict of derivatives data.

        Returns:
            AnalysisResult with bias, confidence, evidence, and summary.
        """
        tf_list = timeframes or DEFAULT_TIMEFRAMES
        started = time.monotonic()

        # 1. Build trading context (live or synthetic).
        ctx = await self._build_context(symbol, tf_list, exchange, use_live_data)

        # 2. Run core + domain analyzers.
        raw_evidence = await self._run_all_analyzers(ctx, macro_data, derivatives_data)

        # 3. Build final analysis result.
        latency_ms = (time.monotonic() - started) * 1000.0
        result = self.summary.generate(
            raw_evidence=raw_evidence,
            timeframes=self.analyzer.get_analyzed_timeframes(),
            symbol=symbol.upper(),
            exchange=exchange,
            latency_ms=latency_ms,
        )

        # 4. Attach raw analyzer output for auditability.
        result.raw["analyzers"] = {
            "market_analyzer": self._evidence_counts(raw_evidence),
            "domain": {
                "wyckoff": self._count_evidence_type(raw_evidence, "wyckoff"),
                "smc": self._count_evidence_type(raw_evidence, "smc"),
                "elliott_wave": self._count_evidence_type(raw_evidence, "elliott_wave"),
                "volume_profile": self._count_evidence_type(raw_evidence, "volume_profile"),
                "psychology": self._count_evidence_type(raw_evidence, "psychology"),
                "macro": self._count_evidence_type(raw_evidence, "macro"),
                "derivatives": self._count_evidence_type(raw_evidence, "derivatives"),
            },
        }
        return result

    async def analyze_full(
        self,
        symbol: str,
        timeframes: list[str] | None = None,
        exchange: str = "binance",
        use_live_data: bool = True,
        macro_data: dict[str, Any] | None = None,
        derivatives_data: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """
        Run the full pipeline and return a rich dict for the reference app.

        Includes market analysis, risk assessment, portfolio snapshot, and
        strategy suggestion alongside the evidence-based AnalysisResult.
        """
        result = await self.analyze_market(
            symbol=symbol,
            timeframes=timeframes,
            exchange=exchange,
            use_live_data=use_live_data,
            macro_data=macro_data,
            derivatives_data=derivatives_data,
        )
        risk = self.assess_risk_from_result(result)
        strategy = self.generate_strategy_from_result(result)

        return {
            "symbol": result.symbol,
            "bias": result.bias.value,
            "confidence": round(result.confidence * 100),
            "risk_level": result.risk_level.value,
            "market": result.to_dict(),
            "risk_assessment": risk,
            "strategy": strategy,
            "timeframes_analyzed": self.analyzer.get_analyzed_timeframes(),
        }

    # ------------------------------------------------------------------
    # Lightweight helpers (kept for backward compatibility with v1 app)
    # ------------------------------------------------------------------

    async def assess_risk(self, symbol: str, position_size: float = 1000.0) -> dict[str, Any]:
        """Provide a risk assessment. Uses live data when available."""
        result = await self.analyze_market(symbol, use_live_data=True)
        risk = self.assess_risk_from_result(result)
        risk["position_size"] = position_size
        return risk

    async def analyze_portfolio(self) -> dict[str, Any]:
        """Snapshot portfolio analysis. Returns a conservative default."""
        return {
            "total_value": 0.0,
            "positions": 0,
            "diversification": "unknown",
            "exposure": {},
            "note": "Portfolio analysis requires user-supplied holdings.",
        }

    async def generate_strategy(
        self, symbol: str, risk_tolerance: str = "medium"
    ) -> dict[str, Any]:
        """Generate a strategy suggestion informed by the pipeline output."""
        result = await self.analyze_market(symbol, use_live_data=True)
        strategy = self.generate_strategy_from_result(result)
        strategy["risk_tolerance"] = risk_tolerance
        return strategy

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    async def _build_context(
        self,
        symbol: str,
        timeframes: list[str],
        exchange: str,
        use_live_data: bool,
    ) -> TradingContext:
        """Build a TradingContext, falling back to synthetic data if needed."""
        if use_live_data:
            try:
                from apps.trading_analyst.market_intelligence.provider import (
                    build_trading_context,
                )

                ctx = await build_trading_context(symbol, timeframes, exchange)
                # Keep only timeframes that actually returned data.
                if any(ctx.timeframes.values()):
                    return ctx
                logger.warning("Live data empty for %s; using synthetic context.", symbol)
            except Exception as exc:  # pragma: no cover - network boundary
                logger.warning("Live data unavailable for %s: %s", symbol, exc)

        return self._build_synthetic_context(symbol, timeframes, exchange)

    def _build_synthetic_context(
        self, symbol: str, timeframes: list[str], exchange: str
    ) -> TradingContext:
        """
        Build a deterministic synthetic context for offline testing.

        Generates realistic market phases so every analyzer has structure
        to detect:

        1. 60% -- ranging / consolidation (stable volume, small candles)
        2. 25% -- trend up with increasing volume (triggers trend, Wyckoff
                 markup, volume conviction)
        3. 15% -- volatility expansion (volume spike, larger candles,
                 triggers psychology, volatility, volume-spike evidence)

        Seeded so results are reproducible.
        """
        rng = random.Random(42)
        timeframes_out: dict[str, list[OHLCV]] = {}

        base_candles = {
            "15m": 120, "30m": 120, "1h": 120, "4h": 120, "1d": 120, "1w": 120,
        }
        for tf in timeframes:
            n = base_candles.get(tf, 100)
            candles: list[OHLCV] = []
            price = 100.0
            ts = 1_700_000_000
            step = 60 * ({"m": 1, "h": 60, "d": 1440}.get(tf[-1], 60)
                         * int("".join(c for c in tf if c.isdigit()) or 1))

            range_end = int(n * 0.60)
            trend_end = int(n * 0.85)
            base_vol = 1500.0

            for i in range(n):
                o = price
                if i < range_end:
                    shock = rng.gauss(0, 0.004)
                    drift = 0.0002
                    vol_mult = rng.uniform(0.9, 1.1)
                elif i < trend_end:
                    shock = rng.gauss(0, 0.006)
                    drift = 0.003
                    vol_mult = rng.uniform(1.1, 1.6)
                else:
                    shock = rng.gauss(0, 0.014)
                    drift = 0.004
                    vol_mult = rng.uniform(1.8, 3.0)

                c = max(o * (1 + drift + shock), 0.5)
                h = max(o, c) * (1 + abs(rng.gauss(0, 0.004 * (1.8 if i >= trend_end else 1.0))))
                l = min(o, c) * (1 - abs(rng.gauss(0, 0.004 * (1.8 if i >= trend_end else 1.0))))
                v = base_vol * vol_mult * (2.5 if i >= trend_end else 1.0)
                candles.append(
                    OHLCV(
                        timestamp=ts + i * step,
                        open=round(o, 2),
                        high=round(h, 2),
                        low=round(l, 2),
                        close=round(c, 2),
                        volume=round(v, 2),
                    )
                )
                price = c
            timeframes_out[tf] = candles

        return TradingContext(
            symbol=symbol.upper(),
            exchange=exchange,
            timeframes=timeframes_out,
            metadata={"source": "synthetic", "seeded": True},
        )

    async def _run_all_analyzers(
        self,
        ctx: TradingContext,
        macro_data: dict[str, Any] | None,
        derivatives_data: dict[str, Any] | None,
    ) -> dict[str, list[MarketEvidence]]:
        """
        Run every analyzer across all timeframes and aggregate raw evidence.

        The returned dict is keyed by evidence *type* (which the
        EvidenceBuilder / ConfidenceScorer consume).
        """
        raw: dict[str, list[MarketEvidence]] = {}
        for tf, ohlcv in ctx.timeframes.items():
            if not ohlcv or len(ohlcv) < 20:
                logger.debug("Skipping %s: insufficient data", tf)
                continue

            # Core market analyzer (4 categories).
            from apps.trading_analyst.market_intelligence.models import TradingContext as _TC

            mini = _TC(symbol=ctx.symbol, exchange=ctx.exchange, timeframes={tf: ohlcv})
            core_categories = await self.analyzer.analyze(mini)
            self._append_categories(raw, core_categories)

            # Wyckoff.
            for ev in self.wyckoff.analyze(ohlcv, tf):
                self._append(raw, ev)

            # SMC / ICT -- cap FVG per timeframe to reduce noise.
            smc_evidence = self.smc.analyze(ohlcv, tf)
            fvg_seen = 0
            for ev in smc_evidence:
                if ev.type == "smc_fvg":
                    if fvg_seen >= FVG_CAP_PER_TIMEFRAME:
                        continue
                    fvg_seen += 1
                self._append(raw, ev)

            # Elliott Wave.
            for ev in self.elliott.analyze(ohlcv, tf):
                self._append(raw, ev)

            # Volume Profile.
            for ev in self.volume_profile.analyze(ohlcv, tf):
                self._append(raw, ev)

            # Psychology (needs RSI).
            closes = [c.close for c in ohlcv]
            rsi_vals = ind.compute_rsi(closes)
            rsi = rsi_vals[-1] if rsi_vals else 50.0
            for ev in self.psychology.analyze(ohlcv, rsi, tf):
                self._append(raw, ev)

        # Macro (single evaluation, not per-timeframe).
        if macro_data and isinstance(macro_data, dict):
            for ev in self.macro.analyze(macro_data):
                self._append(raw, ev)

        # Derivatives (single evaluation).
        if derivatives_data and isinstance(derivatives_data, dict):
            for ev in self.derivatives.analyze(derivatives_data):
                self._append(raw, ev)

        return raw

    # ------------------------------------------------------------------
    # Small helpers
    # ------------------------------------------------------------------

    def _append(self, raw: dict[str, list[MarketEvidence]], ev: MarketEvidence) -> None:
        """Append a single evidence item keyed by its type."""
        raw.setdefault(ev.type, []).append(ev)

    def _append_categories(
        self, raw: dict[str, list[MarketEvidence]], categories: dict[str, list[MarketEvidence]]
    ) -> None:
        """Merge analyzer categories into the raw evidence dict."""
        for cat, ev_list in categories.items():
            raw.setdefault(cat, []).extend(ev_list)

    def _count_evidence_type(
        self, raw: dict[str, list[MarketEvidence]], prefix: str
    ) -> int:
        """Count evidence items whose type starts with a prefix."""
        return sum(
            1 for ev_list in raw.values() for ev in ev_list if ev.type.startswith(prefix)
        )

    def _evidence_counts(self, raw: dict[str, list[MarketEvidence]]) -> dict[str, int]:
        """Return {category: count} for the raw evidence dict."""
        return {cat: len(ev_list) for cat, ev_list in sorted(raw.items())}

    def assess_risk_from_result(self, result: AnalysisResult) -> dict[str, Any]:
        """Derive a risk assessment from an AnalysisResult."""
        risk_level = result.risk_level.value
        return {
            "symbol": result.symbol,
            "bias": result.bias.value,
            "confidence": round(result.confidence * 100),
            "risk_level": risk_level,
            "max_drawdown": 0.15 if risk_level == "high" else 0.10,
            "var_95": 0.05 if risk_level == "high" else 0.03,
            "note": "Heuristic risk estimate derived from evidence confidence and contradiction.",
        }

    def generate_strategy_from_result(self, result: AnalysisResult) -> dict[str, Any]:
        """Derive a strategy suggestion from an AnalysisResult."""
        if result.bias == Bias.NEUTRAL:
            return {
                "symbol": result.symbol,
                "strategy": "wait",
                "entry": None,
                "exit": None,
                "stop_loss": None,
                "confidence": round(result.confidence * 100),
                "rationale": "Market is neutral; await directional breakout.",
            }
        bias = result.bias.value
        confidence = round(result.confidence * 100)
        risk = result.risk_level.value
        return {
            "symbol": result.symbol,
            "strategy": "momentum" if bias == "bullish" else "counter-trend-watch",
            "entry": f"pullback toward {bias} bias key level",
            "exit": f"{bias} target at measured move",
            "stop_loss": "below recent swing" if bias == "bullish" else "above recent swing",
            "confidence": confidence,
            "rationale": (
                f"{confidence}% confidence {bias} bias with {risk} risk. "
                f"Align with the {bias} trend; respect the counter scenario."
            ),
        }


trading_engine = TradingEngine()
