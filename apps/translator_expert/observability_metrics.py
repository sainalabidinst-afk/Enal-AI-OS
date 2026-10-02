"""
Observability metrics for Translator Expert.

Tracks per-translation metrics: latency, accuracy, throughput, and confidence.
Uses a singleton in-memory collector that can also persist to the observability
dashboard or export to the Observability pack.
"""

import threading
import time
from collections import defaultdict
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Any


@dataclass
class TranslationMetricSample:
    """A single recorded translation metric sample."""

    trace_id: str
    source_lang: str
    target_lang: str
    domain: str
    style: str
    text_length: int
    latency_ms: float
    accuracy: float
    confidence: float
    throughput_chars_per_sec: float
    model_used: str
    glossary_terms_used: int
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class TranslationMetricsCollector:
    """Singleton collector for translation observability metrics.

    Metrics tracked:
      - latency_ms       — end-to-end translation time
      - accuracy         — quality score of the translation
      - throughput       — characters per second processed
      - confidence       — engine confidence in the output
    """

    _instance: "TranslationMetricsCollector | None" = None
    _lock = threading.Lock()

    def __init__(self) -> None:
        self._samples: list[TranslationMetricSample] = []
        self._by_lang_pair: dict[str, list[TranslationMetricSample]] = defaultdict(list)
        self._by_domain: dict[str, list[TranslationMetricSample]] = defaultdict(list)

    @classmethod
    def get_instance(cls) -> "TranslationMetricsCollector":
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls()
        return cls._instance

    @classmethod
    def reset(cls) -> None:
        with cls._lock:
            cls._instance = None

    def record(
        self,
        source_lang: str,
        target_lang: str,
        domain: str,
        latency_ms: float,
        accuracy: float,
        confidence: float,
        throughput_chars_per_sec: float | None = None,
        trace_id: str | None = None,
        style: str = "formal",
        text_length: int = 0,
        model_used: str = "unknown",
        glossary_terms_used: int = 0,
    ) -> dict[str, Any]:
        """Record a translation metric sample and return the summary row."""
        if throughput_chars_per_sec is None and latency_ms > 0 and text_length > 0:
            throughput_chars_per_sec = round(text_length / (latency_ms / 1000), 2)

        sample = TranslationMetricSample(
            trace_id=trace_id or f"trace-{int(time.time() * 1000)}",
            source_lang=source_lang,
            target_lang=target_lang,
            domain=domain,
            style=style,
            text_length=text_length,
            latency_ms=round(latency_ms, 2),
            accuracy=round(accuracy, 4),
            confidence=round(confidence, 4),
            throughput_chars_per_sec=round(throughput_chars_per_sec or 0.0, 2),
            model_used=model_used,
            glossary_terms_used=glossary_terms_used,
        )

        with self._lock:
            self._samples.append(sample)
            lang_key = f"{source_lang}→{target_lang}"
            self._by_lang_pair[lang_key].append(sample)
            self._by_domain[domain].append(sample)

        return {
            "trace_id": sample.trace_id,
            "latency_ms": sample.latency_ms,
            "accuracy": sample.accuracy,
            "confidence": sample.confidence,
            "throughput_cps": sample.throughput_chars_per_sec,
        }

    def get_metrics(
        self,
        source_lang: str | None = None,
        target_lang: str | None = None,
        domain: str | None = None,
        limit: int = 1000,
    ) -> list[dict[str, Any]]:
        """Retrieve recorded metrics, optionally filtered by language pair or domain."""
        with self._lock:
            samples = list(self._samples)

        if source_lang and target_lang:
            lang_key = f"{source_lang}→{target_lang}"
            samples = [s for s in samples if f"{s.source_lang}→{s.target_lang}" == lang_key]
        elif source_lang:
            samples = [s for s in samples if s.source_lang == source_lang]
        elif target_lang:
            samples = [s for s in samples if s.target_lang == target_lang]

        if domain:
            samples = [s for s in samples if s.domain == domain]

        samples = samples[-limit:]
        return [s.to_dict() for s in samples]

    def get_summary(
        self,
        source_lang: str | None = None,
        target_lang: str | None = None,
        domain: str | None = None,
    ) -> dict[str, Any]:
        """Return aggregated summary metrics for the given filters."""
        with self._lock:
            samples = list(self._samples)

        if source_lang and target_lang:
            lang_key = f"{source_lang}→{target_lang}"
            samples = [s for s in samples if f"{s.source_lang}→{s.target_lang}" == lang_key]
        elif source_lang:
            samples = [s for s in samples if s.source_lang == source_lang]
        elif target_lang:
            samples = [s for s in samples if s.target_lang == target_lang]

        if domain:
            samples = [s for s in samples if s.domain == domain]

        if not samples:
            return {
                "total_translations": 0,
                "avg_latency_ms": 0.0,
                "p95_latency_ms": 0.0,
                "avg_accuracy": 0.0,
                "avg_confidence": 0.0,
                "avg_throughput_cps": 0.0,
                "by_language_pair": {},
                "by_domain": {},
            }

        latencies = [s.latency_ms for s in samples]
        accuracies = [s.accuracy for s in samples]
        confidences = [s.confidence for s in samples]
        throughputs = [s.throughput_chars_per_sec for s in samples]

        sorted_latencies = sorted(latencies)
        p95_idx = int(len(sorted_latencies) * 0.95) - 1
        p95_latency = sorted_latencies[max(p95_idx, 0)]

        by_lang_pair: dict[str, dict[str, float]] = {}
        for key, pair_samples in self._by_lang_pair.items():
            if source_lang and target_lang and key != f"{source_lang}→{target_lang}":
                continue
            if source_lang and not key.startswith(f"{source_lang}→"):
                continue
            if target_lang and not key.endswith(f"→{target_lang}"):
                continue
            lats = [s.latency_ms for s in pair_samples]
            accs = [s.accuracy for s in pair_samples]
            confs = [s.confidence for s in pair_samples]
            tps = [s.throughput_chars_per_sec for s in pair_samples]
            by_lang_pair[key] = {
                "count": len(pair_samples),
                "avg_latency_ms": round(sum(lats) / len(lats), 2),
                "avg_accuracy": round(sum(accs) / len(accs), 4),
                "avg_confidence": round(sum(confs) / len(confs), 4),
                "avg_throughput_cps": round(sum(tps) / len(tps), 2),
            }

        by_domain_summary: dict[str, dict[str, float]] = {}
        for key, dom_samples in self._by_domain.items():
            if domain and key != domain:
                continue
            lats = [s.latency_ms for s in dom_samples]
            accs = [s.accuracy for s in dom_samples]
            tps = [s.throughput_chars_per_sec for s in dom_samples]
            by_domain_summary[key] = {
                "count": len(dom_samples),
                "avg_latency_ms": round(sum(lats) / len(lats), 2),
                "avg_accuracy": round(sum(accs) / len(accs), 4),
                "avg_throughput_cps": round(sum(tps) / len(tps), 2),
            }

        return {
            "total_translations": len(samples),
            "avg_latency_ms": round(sum(latencies) / len(latencies), 2),
            "p95_latency_ms": round(p95_latency, 2),
            "avg_accuracy": round(sum(accuracies) / len(accuracies), 4),
            "avg_confidence": round(sum(confidences) / len(confidences), 4),
            "avg_throughput_cps": round(sum(throughputs) / len(throughputs), 2),
            "by_language_pair": by_lang_pair,
            "by_domain": by_domain_summary,
        }


def get_metrics_collector() -> TranslationMetricsCollector:
    """Get the singleton metrics collector instance."""
    return TranslationMetricsCollector.get_instance()


__all__ = [
    "TranslationMetricSample",
    "TranslationMetricsCollector",
    "get_metrics_collector",
]
