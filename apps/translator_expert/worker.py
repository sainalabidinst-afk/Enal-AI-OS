"""
Translator Expert Worker.
"""

from __future__ import annotations

import json
from typing import Any

from apps.translator_expert.engine import TranslatorExpertEngine
from apps.translator_expert.schemas import TranslationRequest


class TranslatorExpertWorker:
    """Thin adapter that exposes the Translator Expert engine to agents."""

    def __init__(self) -> None:
        self.engine = TranslatorExpertEngine()

    def execute(self, task: dict[str, Any]) -> dict[str, Any]:
        request = TranslationRequest(**task)
        report = self.engine.execute(request)
        return json.loads(report.model_dump_json())


__all__ = ["TranslatorExpertWorker"]
