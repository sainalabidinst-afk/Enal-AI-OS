"""
Kafka Event Bus — distributed message streaming via Apache Kafka.

Provides an alternative to the Redis-based EventBus, with support for:
- Producer with async message publishing
- Consumer with group-based message consumption
- Topic management (auto-create topics)
- Integration with the existing Event/Envelope model

ADR-003: Thin adapter over aiokafka.
ADR-004: Topic naming and partitioning strategies are configured here,
         but business-level routing logic lives in domain services.

Configuration:
    Set KAFKA_BOOTSTRAP_SERVERS in environment or .env file.
    Default: localhost:9092
"""

from __future__ import annotations

import json
import logging
import uuid
from collections.abc import Awaitable, Callable
from datetime import UTC, datetime
from typing import Any

from backend.app.core.config import settings
from backend.app.core.events import Event

logger = logging.getLogger(__name__)

_DEFAULT_TOPIC_PREFIX = "enal"


class KafkaEventBus:
    """
    Kafka-backed event bus.

    Falls back gracefully when Kafka is not available — messages are
    logged and stored in an in-memory buffer for development/testing.
    """

    def __init__(
        self,
        bootstrap_servers: str | None = None,
        topic_prefix: str = _DEFAULT_TOPIC_PREFIX,
    ) -> None:
        self._bootstrap_servers = bootstrap_servers or settings.KAFKA_BOOTSTRAP_SERVERS
        self._topic_prefix = topic_prefix
        self._producer: Any | None = None
        self._subscribers: dict[str, list[Callable[[Event], Awaitable[None]]]] = {}
        self._in_memory_buffer: list[dict[str, Any]] = []
        self._available = False

    def _topic_name(self, event_type: str) -> str:
        safe_type = event_type.replace(":", ".").replace("/", ".")
        return f"{self._topic_prefix}.{safe_type}"

    @property
    def available(self) -> bool:
        if not self._available:
            self._check_availability()
        return self._available

    def _check_availability(self) -> None:
        try:
            from aiokafka import AIOKafkaProducer

            self._producer = AIOKafkaProducer(
                bootstrap_servers=self._bootstrap_servers,
                value_serializer=lambda v: json.dumps(v).encode("utf-8"),
            )
            self._available = True
        except Exception as e:
            logger.warning(f"Kafka not available ({e}), using in-memory fallback")
            self._available = False

    async def start_producer(self) -> None:
        if not self.available:
            logger.debug("Kafka not available; producer will use in-memory buffer")
            return
        try:
            from aiokafka import AIOKafkaProducer

            self._producer = AIOKafkaProducer(
                bootstrap_servers=self._bootstrap_servers,
                value_serializer=lambda v: json.dumps(v).encode("utf-8"),
            )
            await self._producer.start()
            logger.info("Kafka producer started")
        except Exception as e:
            logger.warning(f"Failed to start Kafka producer: {e}")
            self._available = False

    async def stop_producer(self) -> None:
        if self._producer:
            try:
                await self._producer.stop()
            except Exception:
                pass
            self._producer = None

    async def publish(self, event: Event) -> str:
        """
        Publish an event to Kafka.

        Returns the Kafka message ID (or a synthetic ID if in-memory fallback).
        """
        topic = self._topic_name(event.event_type)
        message_id = str(uuid.uuid4())

        payload = {
            "id": message_id,
            "event_type": event.event_type,
            "source": event.source,
            "target": event.target,
            "timestamp": event.timestamp.isoformat(),
            "correlation_id": event.correlation_id or "",
            "payload": event.payload,
            "metadata": event.metadata,
        }

        if self.available and self._producer:
            try:
                await self._producer.send_and_wait(topic, payload)
                logger.debug(f"Published event to {topic}: {event.event_type}")
                return message_id
            except Exception as e:
                logger.warning(f"Kafka publish failed ({e}), falling back to buffer")
                self._in_memory_buffer.append(payload)
        else:
            self._in_memory_buffer.append(payload)
            if len(self._in_memory_buffer) > 10000:
                self._in_memory_buffer = self._in_memory_buffer[-1000:]

        return message_id

    def subscribe(self, event_type: str, handler: Callable[[Event], Awaitable[None]]) -> None:
        self._subscribers.setdefault(event_type, []).append(handler)

    async def consume(
        self,
        event_type: str,
        group: str = "workers",
        bootstrap_servers: str | None = None,
    ) -> None:
        """
        Consume events from a Kafka topic using a consumer group.

        This is a long-running consumer that processes events indefinitely.
        """
        if not self.available:
            logger.debug("Kafka not available; consume is a no-op")
            return

        from aiokafka import AIOKafkaConsumer

        topic = self._topic_name(event_type)
        servers = bootstrap_servers or self._bootstrap_servers

        consumer = AIOKafkaConsumer(
            topic,
            bootstrap_servers=servers,
            group_id=group,
            auto_offset_reset="earliest",
            value_deserializer=lambda v: json.loads(v.decode("utf-8")),
        )
        await consumer.start()
        logger.info(f"Kafka consumer started for topic '{topic}' (group='{group}')")

        try:
            async for msg in consumer:
                try:
                    data = msg.value
                    event = Event(
                        event_type=data["event_type"],
                        payload=data.get("payload", {}),
                        source=data.get("source", "system"),
                        target=data.get("target", "*"),
                        timestamp=datetime.fromisoformat(
                            data.get("timestamp", datetime.now(UTC).isoformat())
                        ),  # noqa: E501
                        correlation_id=data.get("correlation_id") or None,
                        metadata=data.get("metadata", {}),
                    )
                    for handler in self._subscribers.get(event_type, []):
                        try:
                            await handler(event)
                        except Exception as e:
                            logger.error(f"Consumer handler error: {e}")
                except Exception as e:
                    logger.error(f"Kafka message processing error: {e}")
        finally:
            await consumer.stop()

    def get_buffer(self) -> list[dict[str, Any]]:
        """Return the in-memory buffer (used when Kafka is unavailable)."""
        return list(self._in_memory_buffer)

    def clear_buffer(self) -> None:
        """Clear the in-memory buffer."""
        self._in_memory_buffer.clear()


kafka_event_bus = KafkaEventBus()
