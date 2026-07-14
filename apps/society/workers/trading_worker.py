"""
Trading Worker
==============

Worker implementation for the Trading domain.
Executes subtasks using TradingAnalystApp.

Exposes capabilities through the ECP pipeline:
- market analysis
- risk assessment
- portfolio analysis
- strategy generation
"""

import logging
from typing import Any

from apps.trading_analyst import get_app

logger = logging.getLogger(__name__)


def _normalize_subtask(subtask: Any) -> dict[str, Any]:
    if isinstance(subtask, dict):
        return subtask
    if hasattr(subtask, "__dict__"):
        return subtask.__dict__
    return {}


class TradingWorker:
    """Worker that executes trading subtasks."""

    def __init__(self):
        self._app = get_app()

    async def execute(self, subtask: Any, context: dict[str, Any]) -> dict[str, Any]:
        subtask_data = _normalize_subtask(subtask)
        name = subtask_data.get("name", "")
        required_skills = subtask_data.get("required_skills", [])
        subtask_id = subtask_data.get("id", subtask_data.get("subtask_id", ""))

        lowered = name.lower()
        if "market" in lowered or "analysis" in lowered or "analyze" in lowered:
            return await self._handle_market(subtask_data, context)
        if "risk" in lowered or "assess" in lowered:
            return await self._handle_risk(subtask_data, context)
        if "portfolio" in lowered or "portfolio" in lowered or "allocation" in lowered:
            return await self._handle_portfolio(subtask_data, context)
        if "strategy" in lowered or "backtest" in lowered or "generation" in lowered:
            return await self._handle_strategy(subtask_data, context)
        return {
            "subtask_id": subtask_id,
            "status": "completed",
            "result": f"Trading subtask executed: {name}",
            "required_skills": required_skills,
        }

    async def _handle_market(self, subtask_data: dict[str, Any], context: dict[str, Any]) -> dict[str, Any]:
        task_context = context.get("task", {})
        symbol = task_context.get("intent", "BTCUSDT")
        try:
            result = await self._app.engine.analyze_market(symbol)
            return {
                "subtask_id": subtask_data.get("subtask_id", subtask_data.get("id", "")),
                "status": "completed",
                "result": result,
            }
        except Exception as exc:
            return {"subtask_id": subtask_data.get("subtask_id", subtask_data.get("id", "")), "status": "failed", "error": str(exc)}

    async def _handle_risk(self, subtask_data: dict[str, Any], context: dict[str, Any]) -> dict[str, Any]:
        task_context = context.get("task", {})
        symbol = task_context.get("intent", "BTCUSDT")
        try:
            result = await self._app.engine.assess_risk(symbol)
            return {
                "subtask_id": subtask_data.get("subtask_id", subtask_data.get("id", "")),
                "status": "completed",
                "result": result,
            }
        except Exception as exc:
            return {"subtask_id": subtask_data.get("subtask_id", subtask_data.get("id", "")), "status": "failed", "error": str(exc)}

    async def _handle_portfolio(self, subtask_data: dict[str, Any], context: dict[str, Any]) -> dict[str, Any]:
        try:
            result = await self._app.engine.analyze_portfolio()
            return {
                "subtask_id": subtask_data.get("subtask_id", subtask_data.get("id", "")),
                "status": "completed",
                "result": result,
            }
        except Exception as exc:
            return {"subtask_id": subtask_data.get("subtask_id", subtask_data.get("id", "")), "status": "failed", "error": str(exc)}

    async def _handle_strategy(self, subtask_data: dict[str, Any], context: dict[str, Any]) -> dict[str, Any]:
        task_context = context.get("task", {})
        symbol = task_context.get("intent", "BTCUSDT")
        try:
            result = await self._app.engine.generate_strategy(symbol)
            return {
                "subtask_id": subtask_data.get("subtask_id", subtask_data.get("id", "")),
                "status": "completed",
                "result": result,
            }
        except Exception as exc:
            return {"subtask_id": subtask_data.get("subtask_id", subtask_data.get("id", "")), "status": "failed", "error": str(exc)}


trading_worker = TradingWorker()
