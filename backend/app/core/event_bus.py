import json
import logging
import uuid
from collections.abc import Awaitable, Callable
from datetime import UTC, datetime

from redis.asyncio import Redis

from backend.app.core.config import settings
from backend.app.core.events import Event, EventEnvelope

logger = logging.getLogger(__name__)


class EventBus:
    def __init__(self):
        self._subscribers: dict[str, list[Callable[[Event], Awaitable[None]]]] = {}
        self._stream_prefix = "enal:events"
        self._redis: Redis | None = None

    @property
    def redis(self):
        if self._redis is None:
            self._redis = Redis.from_url(
                settings.REDIS_URL,
                encoding="utf-8",
                decode_responses=True,
            )
        return self._redis

    def _stream_name(self, event_type: str) -> str:
        return f"{self._stream_prefix}:{event_type}"

    async def publish(self, event: Event) -> str:
        stream = self._stream_name(event.event_type)
        envelope = EventEnvelope(event=event, stream=stream, id=str(uuid.uuid4()))
        payload = {
            "id": envelope.id,
            "source": event.source,
            "target": event.target,
            "timestamp": event.timestamp.isoformat(),
            "correlation_id": event.correlation_id or "",
            "data": json.dumps(event.payload),
            "metadata": json.dumps(event.metadata),
        }
        await self.redis.xadd(stream, payload)
        for handler in self._subscribers.get(event.event_type, []):
            try:
                await handler(event)
            except Exception as e:
                logger.error(f"Event handler error: {e}")
        return envelope.id or ""

    def subscribe(self, event_type: str, handler: Callable[[Event], Awaitable[None]]):
        self._subscribers.setdefault(event_type, []).append(handler)

    async def consume(self, event_type: str, group: str = "workers", consumer: str = "worker-1"):
        stream = self._stream_name(event_type)
        try:
            await self.redis.xgroup_create(stream, group, id="0", mkstream=True)
        except Exception:
            pass
        while True:
            results = await self.redis.xreadgroup(
                group, consumer, {stream: ">"}, count=10, block=5000
            )
            for stream_name, messages in results:
                for message_id, data in messages:
                    event = Event(
                        event_type=event_type,
                        payload=json.loads(data.get("data", "{}")),
                        source=data.get("source", "system"),
                        target=data.get("target", "*"),
                        timestamp=datetime.fromisoformat(data.get("timestamp", datetime.now(UTC).isoformat())),
                        correlation_id=data.get("correlation_id") or None,
                        metadata=json.loads(data.get("metadata", "{}")),
                    )
                    for handler in self._subscribers.get(event_type, []):
                        try:
                            await handler(event)
                        except Exception as e:
                            logger.error(f"Event handler error: {e}")
                    await self.redis.xack(stream, group, message_id)


event_bus = EventBus()

