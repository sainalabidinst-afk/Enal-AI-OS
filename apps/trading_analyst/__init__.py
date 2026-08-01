"""
Trading Analyst Reference App
====================================

Demonstrates ECP capabilities for financial market analysis.

Workflow:
User Request
    ↓
Intent Router
    ↓
Capability Graph → trading-*
    ↓
Task Planner
    ↓
Subtasks:
- Market Analysis
- Risk Assessment
- Portfolio Analysis
- Strategy Generation
    ↓
Execution Planner
    ↓
Execution Runtime
    ↓
Trading Worker
    ↓
Trading Engine (full market intelligence pipeline)
    ↓
Result
"""

from typing import Any

from apps.base import BaseReferenceApp
from apps.trading_analyst.engine import trading_engine, TradingEngine


class TradingAnalystApp(BaseReferenceApp):
    name = "trading-analyst"
    version = "1.0.0"
    description = "Market analysis and trading insights powered by ECP"
    category = "finance"
    pipeline = ["perception", "memory", "reasoning", "simulation", "decision", "action"]

    def __init__(self):
        self.engine = trading_engine

    async def run(self, user_input: str, context: dict[str, Any] | None = None) -> dict[str, Any]:
        context = context or {}
        project_id = context.get("project_id", "trading-analyst-default")

        # Parse symbol from user input if possible.
        symbol = context.get("symbol", "BTCUSDT")
        if not symbol and user_input:
            candidate = user_input.strip().upper().replace(" ", "")
            # crude symbol detection: strip common words
            for word in ("ANALISA", "ANALYZE", "ANALISIS", "ANALYSIS", "CARA", "HOW", "TO",
                         "MARKET", "PASAR", "SYMBOL", "PERDAGANGAN", "TRADING"):
                candidate = candidate.replace(word, "")
            if candidate:
                symbol = candidate

        # Run full pipeline.
        market = await self.engine.analyze_market(symbol, use_live_data=False)
        risk = self.engine.assess_risk_from_result(market)
        portfolio = await self.engine.analyze_portfolio()
        strategy = self.engine.generate_strategy_from_result(market)

        return {
            "app": self.name,
            "version": self.version,
            "input": user_input,
            "pipeline": self.pipeline,
            "result": {
                "market": market.to_dict(),
                "risk": risk,
                "portfolio": portfolio,
                "strategy": strategy,
            },
            "metadata": {
                "category": self.category,
                "capabilities_used": [
                    "market-analysis",
                    "risk-assessment",
                    "portfolio-optimization",
                    "strategy-backtesting",
                ],
                "symbol": symbol,
            },
        }


def get_app() -> TradingAnalystApp:
    return TradingAnalystApp()


__all__ = ["TradingAnalystApp", "TradingEngine", "trading_engine", "get_app"]

