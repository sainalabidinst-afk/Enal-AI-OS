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
Trading Engine
    ↓
Result
"""

from typing import Any
from apps.base import BaseReferenceApp
from apps.trading_analyst.engine import trading_engine


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

        market = await self.engine.analyze_market(project_id)
        risk = await self.engine.assess_risk(project_id)
        portfolio = await self.engine.analyze_portfolio()
        strategy = await self.engine.generate_strategy(project_id)

        return {
            "app": self.name,
            "version": self.version,
            "input": user_input,
            "pipeline": self.pipeline,
            "result": {
                "market": market,
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
            },
        }


def get_app() -> TradingAnalystApp:
    return TradingAnalystApp()
