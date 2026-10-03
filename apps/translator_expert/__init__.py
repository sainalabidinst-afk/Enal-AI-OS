"""
Translator Expert — __init__.py
"""

from typing import Any

from apps.base import BaseReferenceApp
from apps.translator_expert.engine import TranslatorExpertEngine
from apps.translator_expert.glossary_manager import GlossaryManager
from apps.translator_expert.glossary_plugin import (
    GlossaryPluginData,
    GlossaryPluginRegistry,
    glossary_plugin_registry,
    load_glossary_from_file,
    persist_glossary_to_file,
)
from apps.translator_expert.schemas import (
    DomainGlossary,
    GlossaryConfig,
    GlossaryEntry,
    SupportedLanguage,
    TranslationReport,
    TranslationRequest,
    TranslationResult,
    TranslationStyle,
    TranslatorExpertRecord,
)
from apps.translator_expert.worker import TranslatorExpertWorker


class TranslatorExpertApp(BaseReferenceApp):
    name = "translator-expert"
    version = "1.0.0"
    description = (
        "Multilingual translation with domain context, style control, and glossary enforcement"  # noqa: E501
    )
    category = "language"
    pipeline = ["perception", "memory", "reasoning", "planning", "decision", "action"]

    def __init__(self) -> None:
        self.worker = TranslatorExpertWorker()

    async def run(self, user_input: str, context: dict[str, Any] | None = None) -> dict[str, Any]:
        task = dict(context or {})
        task.setdefault("user_input", user_input)
        return self.worker.execute(task)


def get_app() -> "TranslatorExpertApp":
    return TranslatorExpertApp()


__all__ = [
    "TranslatorExpertApp",
    "get_app",
    "TranslatorExpertEngine",
    "TranslatorExpertWorker",
    "TranslationRequest",
    "TranslationReport",
    "TranslationResult",
    "TranslationStyle",
    "DomainGlossary",
    "SupportedLanguage",
    "GlossaryConfig",
    "GlossaryEntry",
    "TranslatorExpertRecord",
    "GlossaryManager",
    "GlossaryPluginData",
    "GlossaryPluginRegistry",
    "glossary_plugin_registry",
    "persist_glossary_to_file",
    "load_glossary_from_file",
]
