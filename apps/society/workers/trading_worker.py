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
import re
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
        if "market" in lowered or "analysis" in lowered or "analyze" in lowered or "analisa" in lowered or "analisis" in lowered:
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
        symbol = self._resolve_symbol(subtask_data, context)
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
        symbol = self._resolve_symbol(subtask_data, context)
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
        symbol = self._resolve_symbol(subtask_data, context)
        try:
            result = await self._app.engine.generate_strategy(symbol)
            return {
                "subtask_id": subtask_data.get("subtask_id", subtask_data.get("id", "")),
                "status": "completed",
                "result": result,
            }
        except Exception as exc:
            return {"subtask_id": subtask_data.get("subtask_id", subtask_data.get("id", "")), "status": "failed", "error": str(exc)}

    @staticmethod
    def _resolve_symbol(subtask_data: dict[str, Any], context: dict[str, Any]) -> str:
        task_context = context.get("task", {})
        raw_text = (
            task_context.get("intent")
            or task_context.get("description")
            or subtask_data.get("description")
            or subtask_data.get("name")
            or "BTCUSDT"
        )
        return TradingWorker._extract_symbol(str(raw_text))

    @staticmethod
    def _extract_symbol(intent: str) -> str:
        tickers = re.findall(r"\b[A-Z]{4,5}\b", intent or "")
        return tickers[0] if tickers else (intent or "BTCUSDT")


trading_worker = TradingWorker()
