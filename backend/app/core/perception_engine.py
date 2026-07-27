"""Perception Engine - Process and extract meaning from various input sources."""
import logging
from dataclasses import dataclass, field
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class PerceptionInput:
    """Input to the perception engine."""
    source: str
    content: str | bytes
    content_type: str = "text/plain"
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class PerceptionResult:
    """Result from perception processing."""
    source: str
    entities: list[str] = field(default_factory=list)
    intents: list[str] = field(default_factory=list)
    sentiment: float = 0.0
    confidence: float = 0.0
    extracted_data: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)


class PerceptionEngine:
    """Process and extract meaning from various input sources."""

    def __init__(self) -> None:
        self._processors: dict[str, Any] = {}

    async def process(self, perception_input: PerceptionInput) -> PerceptionResult:
        """Process input and extract entities/intents."""
        result = PerceptionResult(source=perception_input.source)
        content = perception_input.content

        if perception_input.content_type == "text/plain":
            text_content = content if isinstance(content, str) else content.decode("utf-8", errors="ignore")
            result = await self._process_text(text_content, result)
        elif perception_input.content_type.startswith("image/"):
            bytes_content = content if isinstance(content, bytes) else content.encode("utf-8")
            result = await self._process_image(bytes_content, result)
        elif perception_input.content_type == "application/json":
            text_content = content if isinstance(content, str) else content.decode("utf-8", errors="ignore")
            result = await self._process_json(text_content, result)

        result.metadata.update(perception_input.metadata)
        return result

    async def _process_text(self, content: str, result: PerceptionResult) -> PerceptionResult:
        """Extract entities and intents from text."""
        words = content.lower().split()
        result.entities = [w for w in words if len(w) > 3]
        result.intents = self._infer_intents(content)
        result.sentiment = self._analyze_sentiment(content)
        result.confidence = 0.8
        return result

    async def _process_image(self, content: bytes, result: PerceptionResult) -> PerceptionResult:
        """Placeholder for image processing."""
        result.entities = ["image_detected"]
        result.intents = ["analyze_image"]
        result.confidence = 0.5
        return result

    async def _process_json(self, content: str, result: PerceptionResult) -> PerceptionResult:
        """Extract from JSON structure."""
        import json
        try:
            data = json.loads(content)
            result.entities = list(data.keys())[:10]
            result.extracted_data = data
            result.confidence = 0.9
        except Exception as e:
            logger.warning("Failed to parse JSON: %s", e)
            result.confidence = 0.1
        return result

    def _infer_intents(self, text: str) -> list[str]:
        """Infer intents from text keywords."""
        intents: list[str] = []
        patterns: dict[str, list[str]] = {
            "search": ["find", "search", "look", "seek"],
            "create": ["make", "create", "build", "generate"],
            "analyze": ["analyze", "examine", "study", "review"],
            "execute": ["run", "execute", "start", "launch"],
        }
        text_lower = text.lower()
        for intent, keywords in patterns.items():
            if any(kw in text_lower for kw in keywords):
                intents.append(intent)
        return intents if intents else ["general"]

    def _analyze_sentiment(self, text: str) -> float:
        """Simple sentiment analysis (-1 to 1)."""
        positive: list[str] = ["good", "great", "excellent", "positive", "success"]
        negative: list[str] = ["bad", "poor", "fail", "error", "negative"]
        score = 0.0
        text_lower = text.lower()
        for p in positive:
            if p in text_lower:
                score += 1.0
        for n in negative:
            if n in text_lower:
                score -= 1.0
        word_count = max(1, len(text.split()))
        return max(-1.0, min(1.0, score / word_count))


# ─── Singleton ──

perception_engine = PerceptionEngine()
