"""
Translator Expert Engine.
"""

from __future__ import annotations

import logging
import time

from apps.translator_expert.glossary_manager import GlossaryManager
from apps.translator_expert.observability_log import (
    log_translation_complete,
    log_translation_error,
    start_translation_trace,
)
from apps.translator_expert.schemas import (
    GlossaryConfig,
    TranslationReport,
    TranslationRequest,
    TranslationResult,
    TranslationStyle,
)
from apps.translator_expert.translator_engine import TranslationEngine

logger = logging.getLogger(__name__)


class TranslatorExpertEngine:
    """
    Orchestrates the translation pipeline:
        1. Language Detection (auto-detect source if not provided)
        2. Glossary Preprocessing (replace domain terms with tagged placeholders)
        3. Style-Aware Translation (formal/informal, technical/casual)
        4. Glossary Post-Processing (enforce approved target terms)
        5. Confidence & Explainability Scoring
    """

    def __init__(self) -> None:
        self.engine = TranslationEngine()
        self.glossary_manager = GlossaryManager()

    def execute(self, request: TranslationRequest) -> TranslationReport:
        config: GlossaryConfig = request.inputs
        source_lang = request.source_language
        target_lang = request.target_language
        style: TranslationStyle = request.style
        domain_str = config.domain.value

        trace_id, span = start_translation_trace(
            text=request.text,
            source_lang=source_lang or "auto",
            target_lang=target_lang,
            domain=domain_str,
            style=style.value,
        )
        start_time = time.perf_counter()

        try:
            result = self.engine.translate_text(
                text=request.text,
                source_lang=source_lang,
                target_lang=target_lang,
                style=style,
                glossary_config=config,
            )

            if source_lang is None and result.detected_source_language:
                detected_lang = result.detected_source_language
            else:
                detected_lang = source_lang or "en"

            quality_score = self._compute_quality_score(result, config.domain, config.enforce)

            duration_ms = (time.perf_counter() - start_time) * 1000
            throughput = (
                round(len(request.text) / (duration_ms / 1000), 2) if duration_ms > 0 else 0.0
            )

            log_translation_complete(
                span=span,
                result={
                    "source_language": detected_lang,
                    "target_language": target_lang,
                    "domain": domain_str,
                    "style": style.value,
                    "quality_score": quality_score,
                    "confidence": result.confidence,
                    "model_used": result.model_used,
                    "glossary_terms_used": len(result.glossary_terms_used),
                    "text_length": len(request.text),
                    "token_count": len(request.text.split()),
                },
                duration_ms=duration_ms,
            )

            return TranslationReport(
                request_id=request.request_id,
                source_language=detected_lang,
                target_language=target_lang,
                style=style,
                domain=config.domain,
                results=[result],
                metadata={
                    "glossary_enforced": config.enforce,
                    "custom_terms_count": len(config.custom_terms),
                    "detected_language_confidence": result.confidence,
                    "trace_id": trace_id,
                    "latency_ms": round(duration_ms, 2),
                    "throughput_cps": throughput,
                },
                quality_score=quality_score,
                model_version="2.0.0",
            )
        except Exception as exc:
            duration_ms = (time.perf_counter() - start_time) * 1000
            log_translation_error(span, exc, duration_ms)
            raise

    def _compute_quality_score(
        self, result: TranslationResult, domain: str, enforce_glossary: bool
    ) -> float:
        score = result.confidence

        if result.glossary_terms_used and enforce_glossary:
            score += 0.05
        if result.model_used != "rule-based-fallback":
            score += 0.03
        if domain != "general":
            score += 0.02

        return round(min(score, 0.98), 2)


__all__ = ["TranslatorExpertEngine"]
