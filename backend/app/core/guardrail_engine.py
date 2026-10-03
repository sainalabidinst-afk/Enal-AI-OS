"""
Guardrail engine for validating agent/tool inputs and outputs.

Provides validators for PII, toxic language, prompt injection,
bias, logic, competitor mentions, gibberish, and reading level.
"""

from __future__ import annotations

import logging
import re
from enum import StrEnum
from typing import Any

logger = logging.getLogger(__name__)


class CorrectiveAction(StrEnum):
    FIX = "fix"
    NOOP = "noop"
    EXCEPTION = "exception"


class GuardrailResult:
    def __init__(
        self,
        guardrail: str,
        triggered: bool,
        action: CorrectiveAction,
        details: str = "",
        modified_content: str = "",
    ) -> None:
        self.guardrail = guardrail
        self.triggered = triggered
        self.action = action
        self.details = details
        self.modified_content = modified_content


class BaseGuardrail:
    name: str = "base"
    action: CorrectiveAction = CorrectiveAction.NOOP

    def check(self, content: str, context: dict[str, Any] | None = None) -> GuardrailResult:
        raise NotImplementedError


class PIIGuardrail(BaseGuardrail):
    name = "pii"

    _patterns = [
        (r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", "email"),
        (r"\b\d{3}[-.]?\d{3}[-.]?\d{4}\b", "phone"),
        (r"\b\d{3}-\d{2}-\d{4}\b", "ssn"),
        (r"\b\d{4}[-\s]\d{4}[-\s]\d{4}[-\s]\d{4}\b", "credit_card"),
    ]

    def check(self, content: str, context: dict[str, Any] | None = None) -> GuardrailResult:
        for pattern, pii_type in self._patterns:
            if re.search(pattern, content):
                return GuardrailResult(
                    guardrail=self.name,
                    triggered=True,
                    action=self.action,
                    details=f"Detected {pii_type}",
                    modified_content=re.sub(pattern, "[REDACTED]", content),
                )
        return GuardrailResult(guardrail=self.name, triggered=False, action=self.action)


class ToxicLanguageGuardrail(BaseGuardrail):
    name = "toxic_language"

    _words = {"badword1", "badword2", "badword3"}

    def check(self, content: str, context: dict[str, Any] | None = None) -> GuardrailResult:
        lower = content.lower()
        found = [w for w in self._words if w in lower]
        if found:
            return GuardrailResult(
                guardrail=self.name,
                triggered=True,
                action=self.action,
                details=f"Toxic words: {', '.join(found)}",
                modified_content="",
            )
        return GuardrailResult(guardrail=self.name, triggered=False, action=self.action)


class PromptInjectionGuardrail(BaseGuardrail):
    name = "prompt_injection"

    _patterns = [
        r"ignore previous instructions",
        r"ignore all previous",
        r"disregard all",
        r"forget everything",
        r"you are now",
        r"new instructions",
    ]

    def check(self, content: str, context: dict[str, Any] | None = None) -> GuardrailResult:
        lower = content.lower()
        for pattern in self._patterns:
            if re.search(pattern, lower):
                return GuardrailResult(
                    guardrail=self.name,
                    triggered=True,
                    action=CorrectiveAction.EXCEPTION,
                    details=f"Prompt injection detected: {pattern}",
                )
        return GuardrailResult(guardrail=self.name, triggered=False, action=self.action)


class BiasCheckGuardrail(BaseGuardrail):
    name = "bias_check"

    _biased_terms = ["biased_term1", "biased_term2"]

    def check(self, content: str, context: dict[str, Any] | None = None) -> GuardrailResult:
        lower = content.lower()
        found = [t for t in self._biased_terms if t in lower]
        if found:
            return GuardrailResult(
                guardrail=self.name,
                triggered=True,
                action=self.action,
                details=f"Biased terms: {', '.join(found)}",
            )
        return GuardrailResult(guardrail=self.name, triggered=False, action=self.action)


class LogicCheckGuardrail(BaseGuardrail):
    name = "logic_check"

    def check(self, content: str, context: dict[str, Any] | None = None) -> GuardrailResult:
        if "contradiction" in content.lower() or "impossible" in content.lower():
            return GuardrailResult(
                guardrail=self.name,
                triggered=True,
                action=self.action,
                details="Logical inconsistency detected",
            )
        return GuardrailResult(guardrail=self.name, triggered=False, action=self.action)


class CompetitorCheckGuardrail(BaseGuardrail):
    name = "competitor_check"

    _competitors = ["competitor1", "competitor2"]

    def check(self, content: str, context: dict[str, Any] | None = None) -> GuardrailResult:
        lower = content.lower()
        found = [c for c in self._competitors if c in lower]
        if found:
            return GuardrailResult(
                guardrail=self.name,
                triggered=True,
                action=self.action,
                details=f"Competitor mentions: {', '.join(found)}",
            )
        return GuardrailResult(guardrail=self.name, triggered=False, action=self.action)


class GibberishGuardrail(BaseGuardrail):
    name = "gibberish"

    def check(self, content: str, context: dict[str, Any] | None = None) -> GuardrailResult:
        words = content.split()
        if len(words) > 10 and len(set(words)) / len(words) < 0.3:
            return GuardrailResult(
                guardrail=self.name,
                triggered=True,
                action=self.action,
                details="Gibberish detected: low vocabulary diversity",
            )
        return GuardrailResult(guardrail=self.name, triggered=False, action=self.action)


class ReadingLevelGuardrail(BaseGuardrail):
    name = "reading_level"

    def check(self, content: str, context: dict[str, Any] | None = None) -> GuardrailResult:
        avg_word_length = sum(len(w) for w in content.split()) / max(len(content.split()), 1)
        if avg_word_length > 15:
            return GuardrailResult(
                guardrail=self.name,
                triggered=True,
                action=self.action,
                details=f"Reading level too high: avg word length {avg_word_length:.1f}",
            )
        return GuardrailResult(guardrail=self.name, triggered=False, action=self.action)


class GuardrailEngine:
    """Run guardrail checks against content."""

    def __init__(self) -> None:
        self._guardrails: list[BaseGuardrail] = [
            PIIGuardrail(),
            ToxicLanguageGuardrail(),
            PromptInjectionGuardrail(),
            BiasCheckGuardrail(),
            LogicCheckGuardrail(),
            CompetitorCheckGuardrail(),
            GibberishGuardrail(),
            ReadingLevelGuardrail(),
        ]

    def check(
        self,
        content: str,
        enabled: dict[str, bool],
        context: dict[str, Any] | None = None,
    ) -> list[GuardrailResult]:
        results = []
        for guardrail in self._guardrails:
            if enabled.get(guardrail.name, False):
                results.append(guardrail.check(content, context))
        return results

    def apply_corrective_action(self, result: GuardrailResult, original_content: str) -> str:
        if not result.triggered:
            return original_content
        if result.action == CorrectiveAction.FIX:
            return result.modified_content or original_content
        if result.action == CorrectiveAction.EXCEPTION:
            raise ValueError(f"Guardrail {result.guardrail} triggered: {result.details}")
        return original_content


guardrail_engine = GuardrailEngine()
