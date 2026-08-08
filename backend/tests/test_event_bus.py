import pytest

from backend.app.core.event_bus import EventBus


class FakeRedis:
    def __init__(self):
        self.streams = {}
        self.groups = {}
        self.messages = {}

    async def xadd(self, stream, payload):
        msg_id = f"msg-{len(self.messages)}"
        self.messages.setdefault(stream, []).append((msg_id, payload))
        return msg_id

    async def xgroup_create(self, stream, group, id, mkstream=False):
        self.groups.setdefault(stream, []).append(group)

    async def xreadgroup(self, group, consumer, streams, count=10, block=5000):
        results = []
        for stream_name in streams:
            if stream_name in self.messages:
                results.append((stream_name, self.messages[stream_name][:count]))
        return results

    async def xack(self, stream, group, message_id):
        pass


class FakeEvent:
    def __init__(self, event_type, payload, source="system", target="*", timestamp=None, correlation_id=None, metadata=None):
        self.event_type = event_type
        self.payload = payload
        self.source = source
        self.target = target
        self.timestamp = timestamp or __import__("datetime").datetime.now(__import__("datetime").timezone.utc)
        self.correlation_id = correlation_id
        self.metadata = metadata or {}


class TestEventBus:
    @pytest.fixture
    def bus(self, monkeypatch):
        import backend.app.core.event_bus as eb_module
        fake_redis = FakeRedis()
        monkeypatch.setattr(eb_module.EventBus, "redis", property(lambda self: fake_redis))
        bus = EventBus()
        bus._redis = fake_redis
        return bus

    async def test_subscribe_adds_handler(self, bus):
        async def handler(event):
            pass

        bus.subscribe("test", handler)
        assert "test" in bus._subscribers
        assert handler in bus._subscribers["test"]

    async def test_publish_returns_envelope_id(self, bus):
        async def handler(event):
            pass

        bus.subscribe("test", handler)
        event = FakeEvent("test", {"key": "value"})
        envelope_id = await bus.publish(event)
        assert envelope_id is not None
        assert len(envelope_id) > 0

    async def test_publish_calls_handlers(self, bus):
        called = []

        async def handler(event):
            called.append(event)

        bus.subscribe("test", handler)
        event = FakeEvent("test", {"key": "value"})
        await bus.publish(event)
        assert len(called) == 1
        assert called[0].payload == {"key": "value"}

    async def test_publish_handles_handler_error(self, bus):
        async def bad_handler(event):
            raise ValueError("fail")

        async def good_handler(event):
            pass

        bus.subscribe("test", bad_handler)
        bus.subscribe("test", good_handler)
        event = FakeEvent("test", {"key": "value"})
        envelope_id = await bus.publish(event)
        assert envelope_id is not None

    def test_stream_name(self, bus):
        stream = bus._stream_name("test")
        assert stream == "enal:events:test"

    def test_redis_property_creates_client_when_none(self, monkeypatch):
        import backend.app.core.event_bus as eb_module
        from unittest.mock import MagicMock

        bus = EventBus()
        bus._redis = None
        fake_redis = MagicMock()
        mock_redis_cls = MagicMock()
        mock_redis_cls.from_url.return_value = fake_redis
        monkeypatch.setattr(eb_module, "Redis", mock_redis_cls)
        monkeypatch.setattr(eb_module.settings, "REDIS_URL", "redis://localhost:6379/0")
        redis = bus.redis
        assert redis is fake_redis
        assert bus._redis is fake_redis
        mock_redis_cls.from_url.assert_called_once_with(
            "redis://localhost:6379/0",
            encoding="utf-8",
            decode_responses=True,
        )
