"""
Tests for backend/app/core/event_bus.py — RFC-0001 StableEventBus
with Pydantic validation and in-memory mode.
"""

import pytest

from backend.app.core.event_bus import StableEventBus
from backend.app.core.schemas import Event, EventPriority


class TestStableEventBus:
    @pytest.fixture
    def bus(self):
        return StableEventBus(use_redis=False)

    @pytest.mark.asyncio
    async def test_publish_and_subscribe(self, bus):
        received = []

        async def handler(event):
            received.append(event)

        bus.subscribe("test.event", handler)
        ev = Event(event_type="test.event", payload={"msg": "hello"})
        envelope_id = await bus.publish(ev)

        assert len(envelope_id) > 0
        assert len(received) == 1
        assert received[0].payload["msg"] == "hello"

    @pytest.mark.asyncio
    async def test_publish_dict_validates_pydantic(self, bus):
        received = []

        async def handler(event):
            received.append(event)

        bus.subscribe("test.dict", handler)
        await bus.publish({"event_type": "test.dict", "payload": {"x": 1}})

        assert len(received) == 1
        assert received[0].event_type == "test.dict"

    @pytest.mark.asyncio
    async def test_publish_invalid_payload_raises(self, bus):
        from pydantic import ValidationError

        with pytest.raises((ValidationError, ValueError, TypeError)):
            await bus.publish({"payload": {"x": 1}})

    @pytest.mark.asyncio
    async def test_handler_error_is_isolated(self, bus):
        received = []

        async def bad_handler(event):
            raise ValueError("handler error")

        async def good_handler(event):
            received.append(event)

        bus.subscribe("test.error", bad_handler)
        bus.subscribe("test.error", good_handler)
        await bus.publish(Event(event_type="test.error", payload={"key": "val"}))

        assert len(received) == 1

    @pytest.mark.asyncio
    async def test_trace_id_propagation(self, bus):
        received = []

        async def handler(event):
            received.append(event)

        bus.subscribe("test.trace", handler)
        ev = Event(
            event_type="test.trace",
            payload={"data": "value"},
            trace_id="trace-abc",
            correlation_id="corr-def",
        )
        await bus.publish(ev)

        assert received[0].trace_id == "trace-abc"
        assert received[0].correlation_id == "corr-def"

    @pytest.mark.asyncio
    async def test_get_events_by_type(self, bus):
        await bus.publish(Event(event_type="type.a", payload={}))
        await bus.publish(Event(event_type="type.b", payload={}))
        await bus.publish(Event(event_type="type.a", payload={}))

        events_a = bus.get_events(event_type="type.a")
        assert len(events_a) == 2

    @pytest.mark.asyncio
    async def test_get_events_by_trace_id(self, bus):
        await bus.publish(Event(event_type="test", payload={}, trace_id="trace-1"))
        await bus.publish(Event(event_type="test", payload={}, trace_id="trace-1"))
        await bus.publish(Event(event_type="test", payload={}, trace_id="trace-2"))

        events = bus.get_events(trace_id="trace-1")
        assert len(events) == 2
        assert all(e.trace_id == "trace-1" for e in events)

    @pytest.mark.asyncio
    async def test_event_log_records_all(self, bus):
        for i in range(5):
            await bus.publish(Event(event_type="test.log", payload={"i": i}))

        assert len(bus.event_log) == 5

    def test_unsubscribe(self, bus):
        async def handler(event):
            pass

        bus.subscribe("test.unsub", handler)
        assert len(bus.subscribers("test.unsub")) == 1
        bus.unsubscribe("test.unsub", handler)
        assert len(bus.subscribers("test.unsub")) == 0

    def test_clear(self, bus):
        async def handler(event):
            pass

        bus.subscribe("test.clear", handler)
        bus.clear()
        assert len(bus.subscribers("test.clear")) == 0
        assert len(bus.event_log) == 0

    @pytest.mark.asyncio
    async def test_event_priority(self, bus):
        ev = Event(
            event_type="priority.test",
            payload={},
            priority=EventPriority.HIGH,
        )
        await bus.publish(ev)
        events = bus.get_events(event_type="priority.test")
        assert events[0].priority == EventPriority.HIGH
