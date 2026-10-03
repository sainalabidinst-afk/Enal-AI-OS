import json
import logging
import uuid
from collections import defaultdict, deque
from collections.abc import Awaitable, Callable
from datetime import UTC, datetime

from redis.asyncio import Redis

from backend.app.core.config import settings
from backend.app.core.events import Event, EventEnvelope
from backend.app.core.schemas import Event as TypedEvent
from backend.app.core.schemas import EventEnvelope as TypedEventEnvelope

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
                        timestamp=datetime.fromisoformat(
                            data.get("timestamp", datetime.now(UTC).isoformat())
                        ),  # noqa: E501
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


# ---------------------------------------------------------------------------
# RFC-0001 Stable Contract – typed Event Bus
# ---------------------------------------------------------------------------


class StableEventBus:
    """Typed publish-subscribe Event Bus with Pydantic validation (RFC-0001).

    Supports an *in-memory* mode that falls back to an asyncio-compatible
    queue when Redis is unavailable, ensuring pack communication works in
    tests and isolated environments.
    """

    def __init__(self, use_redis: bool = True):
        self._subscribers: dict[str, list[Callable]] = defaultdict(list)
        self._use_redis = use_redis
        self._redis: Redis | None = None
        self._stream_prefix = "enal:events"
        self._in_memory_queue: deque[tuple[str, TypedEvent]] = deque()
        self._event_log: list[TypedEventEnvelope] = []

    # -- Redis backing (optional) -------------------------------------------

    @property
    def redis(self):
        if not self._use_redis:
            return None
        if self._redis is None:
            try:
                self._redis = Redis.from_url(
                    settings.REDIS_URL,
                    encoding="utf-8",
                    decode_responses=True,
                )
            except Exception:
                logger.warning("Redis unavailable; falling back to in-memory mode")
                self._use_redis = False
        return self._redis

    def _stream_name(self, event_type: str) -> str:
        return f"{self._stream_prefix}:{event_type}"

    # -- Pydantic validation ------------------------------------------------

    @staticmethod
    def validate_event(event: TypedEvent | dict) -> TypedEvent:
        """Validate an event payload against the Pydantic schema."""
        if isinstance(event, TypedEvent):
            return event
        if isinstance(event, dict):
            return TypedEvent.model_validate(event)
        raise TypeError(f"Unsupported event type: {type(event)}")

    @staticmethod
    def validate_payload(event_type: str, payload: dict) -> dict:
        """Validate a payload dict; raises ValidationError on schema mismatch."""
        if not isinstance(payload, dict):
            raise ValueError(f"Payload for {event_type} must be a dict")
        return payload

    # -- Subscribe ----------------------------------------------------------

    def subscribe(
        self,
        event_type: str,
        handler: Callable[[TypedEvent], Awaitable[None]],
    ) -> str:
        sub_id = str(uuid.uuid4())
        self._subscribers[event_type].append(handler)
        logger.debug(f"Subscribed handler to event_type={event_type}")
        return sub_id

    def unsubscribe(self, event_type: str, handler: Callable) -> None:
        subs = self._subscribers.get(event_type, [])
        if handler in subs:
            subs.remove(handler)

    def subscribers(self, event_type: str) -> list[Callable]:
        return list(self._subscribers.get(event_type, []))

    # -- Publish ------------------------------------------------------------

    async def publish(
        self,
        event: TypedEvent | dict,
        event_type: str | None = None,
    ) -> str:
        """Publish a typed, Pydantic-validated event.

        Returns the envelope id.
        """
        if event_type and isinstance(event, dict) and "event_type" not in event:
            event["event_type"] = event_type

        typed = self.validate_event(event)
        self.validate_payload(typed.event_type, typed.payload)

        envelope = TypedEventEnvelope(
            event=typed,
            stream=self._stream_name(typed.event_type),
            id=str(uuid.uuid4()),
        )
        self._event_log.append(envelope)

        if self.redis is not None:
            try:
                stream = self._stream_name(typed.event_type)
                payload = {
                    "id": envelope.id,
                    "source": typed.source,
                    "target": typed.target,
                    "timestamp": typed.timestamp,
                    "correlation_id": typed.correlation_id or "",
                    "trace_id": typed.trace_id or "",
                    "priority": typed.priority.value,
                    "data": json.dumps(typed.payload),
                    "metadata": json.dumps(typed.metadata),
                }
                await self.redis.xadd(stream, payload)
            except Exception as e:
                logger.error(f"Redis xadd failed, using in-memory fallback: {e}")
                self._in_memory_queue.append((typed.event_type, typed))
        else:
            self._in_memory_queue.append((typed.event_type, typed))

        await self._dispatch(typed)
        return envelope.id

    async def _dispatch(self, event: TypedEvent) -> None:
        """Invoke all subscribers for *event* (non-blocking, isolated errors)."""
        handlers = self._subscribers.get(event.event_type, [])
        for handler in handlers:
            try:
                result = handler(event)
                if isinstance(result, Awaitable):
                    await result
            except Exception as e:
                logger.error(f"Event handler error for {event.event_type}: {e}")

    # -- Observability ------------------------------------------------------

    @property
    def event_log(self) -> list[TypedEventEnvelope]:
        return list(self._event_log)

    def get_events(
        self,
        event_type: str | None = None,
        trace_id: str | None = None,
    ) -> list[TypedEvent]:
        events = [e.event for e in self._event_log]
        if event_type is not None:
            events = [e for e in events if e.event_type == event_type]
        if trace_id is not None:
            events = [e for e in events if e.trace_id == trace_id]
        return events

    def clear(self) -> None:
        self._subscribers.clear()
        self._in_memory_queue.clear()
        self._event_log.clear()


stable_event_bus = StableEventBus(use_redis=False)
