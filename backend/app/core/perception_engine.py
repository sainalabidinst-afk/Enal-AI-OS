import logging
from dataclasses import dataclass, field
from typing import Any

logger = logging.getLogger(__name__)

# ─── Perception Types ──

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

# ─── Perception Engine ──

class PerceptionEngine:
    """Process and extract meaning from various input sources."""

    def __init__(self):
        self._processors: dict[str, Any] = {}

    async def process(self, perception_input: PerceptionInput) -> PerceptionResult:
        """Process input and extract entities/intents."""
        result = PerceptionResult(source=perception_input.source)

        if perception_input.content_type == "text/plain":
            result = await self._process_text(perception_input.content, result)
        elif perception_input.content_type.startswith("image/"):
            result = await self._process_image(perception_input.content, result)
        elif perception_input.content_type == "application/json":
            result = await self._process_json(perception_input.content, result)

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

    async def _process_json(self, content: str | bytes, result: PerceptionResult) -> PerceptionResult:
        """Extract from JSON structure."""
        import json
        try:
            data = json.loads(content) if isinstance(content, str) else json.loads(content.decode())
            result.entities = list(data.keys())[:10]
            result.extracted_data = data
            result.confidence = 0.9
        except Exception as e:
            logger.warning("Failed to parse JSON: %s", e)
            result.confidence = 0.1
        return result

    def _infer_intents(self, text: str) -> list[str]:
        """Infer intents from text keywords."""
        intents = []
        patterns = {
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
        positive = ["good", "great", "excellent", "positive", "success"]
        negative = ["bad", "poor", "fail", "error", "negative"]
        score = 0
        text_lower = text.lower()
        for p in positive:
            if p in text_lower:
                score += 1
        for n in negative:
            if n in text_lower:
                score -= 1
        return max(-1, min(1, score / max(1, len(text.split()))))

# ─── Singleton ──

perception_engine = PerceptionEngine()