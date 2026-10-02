"""
Translator Expert — Core Translation Engine module.

Provides language detection and multilingual translation using
HuggingFace MarianMT/M2M-100 models (lazy import). Falls back to
rule-based translation when ML libraries are not available.
"""

from __future__ import annotations

import logging
import re
from typing import Any

from apps.translator_expert.glossary_manager import GlossaryManager
from apps.translator_expert.schemas import (
    GlossaryConfig,
    TranslationResult,
    TranslationStyle,
)

logger = logging.getLogger(__name__)


class TranslationEngine:
    """
    Core translation engine with lazy-loaded HuggingFace models.

    - Language detection via lazy `langdetect` import
    - Translation via lazy `transformers` pipeline (MarianMT/M2M-100)
    - Rule-based fallback when ML libraries unavailable
    """

    STYLE_PREFIXES: dict[TranslationStyle, str] = {
        TranslationStyle.formal: "[formal]",
        TranslationStyle.casual: "[casual]",
        TranslationStyle.technical: "[technical]",
        TranslationStyle.creative: "[creative]",
    }

    IDIOM_MAP: dict[str, dict[str, str]] = {
        "en→id": {
            "break the ice": "memulai dengan santai",
            "piece of cake": "mudah seperti makan kue",
            "hit the books": "membuka buku",
            "under the weather": "kurang enek",
            "cost an arm and a leg": "mahal seperti lengan dan kaki",
            "bite the bullet": "menanggungnya",
        },
        "id→en": {
            "jalan terus": "straight ahead",
            "kuda hitam": "white elephant",
            "makan kubur": "underutilized",
        },
        "en→es": {
            "break the ice": "romper el hielo",
            "piece of cake": "un pastel",
            "hit the books": "estudiar",
            "under the weather": "mal de por medio",
            "cost an arm and a leg": "costar un brazo y una pierna",
            "bite the bullet": "muerde la bala",
        },
        "en→zh": {
            "break the ice": "打破僵局",
            "piece of cake": "小菜一碟",
            "hit the books": "用功学习",
            "under the weather": "身体不适",
            "cost an arm and a leg": "贵得人尽锤折",
        },
    }

    RULE_BASED_MAP: dict[str, dict[str, str]] = {
        "en→id": {
            "hello": "halo",
            "world": "dunia",
            "good morning": "selamat pagi",
            "good afternoon": "selamat siang",
            "good evening": "selamat malam",
            "thank you": "terima kasih",
            "please": "silakan",
            "excuse me": "maaf",
            "how are you": "bagaimana kabar Anda",
            "goodbye": "selamat taslim",
            "congratulations": "selamat",
            "welcome": "selamat datang",
            "yes": "ya",
            "no": "tidak",
            "sorry": "maaf",
            "help": "bantuan",
        },
        "id→en": {
            "halo": "hello",
            "terima kasih": "thank you",
            "selamat pagi": "good morning",
            "selamat siang": "good afternoon",
            "selamat malam": "good evening",
            "selamat taslim": "goodbye",
            "bagaimana kabar Anda": "how are you",
            "tolong": "please",
            "maaf": "sorry",
            "ya": "yes",
            "tidak": "no",
        },
        "en→es": {
            "hello": "hola",
            "world": "mundo",
            "good morning": "buenos días",
            "good afternoon": "buenas tardes",
            "good evening": "buenas noches",
            "thank you": "gracias",
            "please": "por favor",
            "excuse me": "disculpe",
            "how are you": "¿cómo estás?",
            "goodbye": "adiós",
            "congratulations": "felicidades",
            "welcome": "bienvenido",
            "yes": "sí",
            "no": "no",
            "sorry": "lo siento",
            "help": "ayuda",
        },
        "en→zh": {
            "hello": "你好",
            "world": "世界",
            "good morning": "早上好",
            "good afternoon": "下午好",
            "good evening": "晚上好",
            "thank you": "谢谢",
            "please": "请",
            "excuse me": "对不起",
            "how are you": "你好吗",
            "goodbye": "再见",
            "congratulations": "恭喜",
            "welcome": "欢迎",
            "yes": "是",
            "no": "不是",
            "sorry": "对不起",
        },
    }

    def __init__(self) -> None:
        self.glossary_manager = GlossaryManager()
        self._model_cache: dict[str, Any] = {}

    def detect_language(self, text: str) -> tuple[str, float]:
        """Detect the language of the input text."""
        try:
            from langdetect import detect, detect_langs  # type: ignore[import-untyped]

            lang = detect(text)
            langs = detect_langs(text)
            confidence = float(langs[0].prob) if langs else 0.8
            return self._normalize_lang(lang), confidence
        except ImportError:
            return self._heuristic_detect(text)
        except Exception:
            logger.warning("Language detection failed, using heuristic")
            return self._heuristic_detect(text)

    def _normalize_lang(self, lang: str) -> str:
        """Normalize language codes to supported short forms."""
        lang_map = {
            "eng": "en",
            "ind": "id",
            "spa": "es",
            "zho": "zh",
            "fra": "fr",
            "deu": "de",
            "jpn": "ja",
        }
        return lang_map.get(lang[:3], lang[:2])

    def _heuristic_detect(self, text: str) -> tuple[str, float]:
        """Fallback language detection using word-pattern heuristics."""
        text_lower = text.lower()
        scores: dict[str, float] = {"en": 0, "id": 0, "es": 0, "zh": 0}

        if re.search(r"[\u4e00-\u9fff]", text):
            scores["zh"] = 0.9
        if text_lower.count("the") > 0.5:
            scores["en"] += 0.3
        words = set(re.findall(r"[a-z]+", text_lower))
        if any(w in words for w in ["dan", "yang", "di", "ke", "dari"]):
            scores["id"] += 0.2
        if any(w in words for w in ["el", "la", "de", "que", "con"]):
            scores["es"] += 0.15
        if any(w in words for w in ["the", "and", "is", "of", "to"]):
            scores["en"] += 0.2

        best_lang = max(scores, key=lambda k: scores[k])
        confidence = max(scores.values()) if scores else 0.0
        if confidence == 0:
            return "en", 0.5
        return best_lang, min(confidence + 0.3, 0.95)

    def translate_with_model(
        self,
        text: str,
        source_lang: str,
        target_lang: str,
        style: TranslationStyle,
        glossary_config: GlossaryConfig,
    ) -> TranslationResult:
        """Translate using HuggingFace MarianMT/M2M-100 (lazy import)."""
        model_name = self._get_model_name(source_lang, target_lang)

        try:
            from transformers import pipeline  # type: ignore[import-untyped]

            if model_name not in self._model_cache:
                self._model_cache[model_name] = pipeline(
                    "translation",
                    model=model_name,
                )

            model = self._model_cache[model_name]

            preprocessed, prep_terms = self.glossary_manager.apply_preprocessing(
                text, glossary_config, source_lang, target_lang
            )

            style_prefix = self.STYLE_PREFIXES.get(style, "")
            model_input = f"{style_prefix} {preprocessed}" if style_prefix else preprocessed

            result = model(model_input, max_length=max(len(model_input) * 3, 512))
            raw_translation = result[0]["translation_text"]

            postprocessed, post_terms = self.glossary_manager.apply_postprocessing(
                raw_translation, glossary_config, source_lang, target_lang
            )

            all_terms = list(set(prep_terms + post_terms))
            confidence = 0.92 if all_terms else 0.88

            return TranslationResult(
                translated_text=postprocessed,
                confidence=round(confidence, 2),
                glossary_terms_used=all_terms,
                style_applied=style,
                model_used=model_name,
            )
        except ImportError:
            logger.info("transformers not available; using rule-based fallback")
            return self._rule_based_translate(
                text, source_lang, target_lang, style, glossary_config
            )
        except Exception as e:
            logger.warning(f"Model translation failed ({e}); using rule-based fallback")
            return self._rule_based_translate(
                text, source_lang, target_lang, style, glossary_config
            )

    def _rule_based_translate(
        self,
        text: str,
        source_lang: str,
        target_lang: str,
        style: TranslationStyle,
        glossary_config: GlossaryConfig,
    ) -> TranslationResult:
        """Fallback rule-based translation when no ML model is available."""
        lang_pair = f"{source_lang}→{target_lang}"

        preprocessed, prep_terms = self.glossary_manager.apply_preprocessing(
            text, glossary_config, source_lang, target_lang
        )

        rule_map = self.RULE_BASED_MAP.get(lang_pair, {})
        idiom_map = self.IDIOM_MAP.get(lang_pair, {})

        processed = preprocessed
        for idiom, replacement in sorted(idiom_map.items(), key=lambda x: len(x[0]), reverse=True):
            if idiom in processed:
                processed = processed.replace(idiom, f"__IDIOM_{replacement}__")

        words = processed.split()
        translated_words: list[str] = []
        for w in words:
            if w.startswith("[") and w.endswith("]"):
                translated_words.append(w)
                continue
            cleaned = w.strip(".,!?;:\"'()[]")
            matched = False
            if cleaned.lower() in rule_map:
                replacement = rule_map[cleaned.lower()]
                if cleaned[0].isupper():
                    replacement = replacement.capitalize()
                translated_words.append(replacement)
                matched = True
            if not matched:
                if "__IDIOM_" in w:
                    translated_words.append(w.replace("__IDIOM_", "").replace("__", ""))
                else:
                    translated_words.append(w)

        raw_translation = " ".join(translated_words)

        postprocessed, post_terms = self.glossary_manager.apply_postprocessing(
            raw_translation, glossary_config, source_lang, target_lang
        )

        all_terms = list(set(prep_terms + post_terms))
        confidence = 0.85

        if style == TranslationStyle.technical:
            confidence += 0.10
        elif style == TranslationStyle.formal:
            confidence += 0.05

        return TranslationResult(
            translated_text=postprocessed,
            confidence=round(min(confidence, 0.90), 2),
            glossary_terms_used=all_terms,
            style_applied=style,
            model_used="rule-based-fallback",
        )

    def _get_model_name(self, source_lang: str, target_lang: str) -> str:
        """Get the HuggingFace model name for a language pair."""
        return f"Helsinki-NLP/opus-mt-{source_lang}-{target_lang}"

    def translate_text(
        self,
        text: str,
        source_lang: str | None,
        target_lang: str,
        style: TranslationStyle,
        glossary_config: GlossaryConfig,
    ) -> TranslationResult:
        """Translate a single text string, auto-detecting source language if needed."""
        if source_lang:
            detected_lang = source_lang
            detected_confidence = 0.95
        else:
            detected_lang, detected_confidence = self.detect_language(text)

        if detected_lang == target_lang:
            return TranslationResult(
                translated_text=text,
                detected_source_language=detected_lang,
                confidence=round(detected_confidence, 2),
                glossary_terms_used=[],
                style_applied=style,
                model_used="passthrough",
            )

        return self.translate_with_model(
            text, detected_lang, target_lang, style, glossary_config
        ) if detected_lang != target_lang else TranslationResult(
            translated_text=text,
            detected_source_language=detected_lang,
            confidence=round(detected_confidence, 2),
            glossary_terms_used=[],
            style_applied=style,
            model_used="passthrough",
        )


__all__ = ["TranslationEngine"]
