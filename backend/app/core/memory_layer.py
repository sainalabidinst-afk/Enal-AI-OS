import logging
from abc import ABC, abstractmethod
from typing import Any
from pathlib import Path
from backend.app.core.config import settings
import redis.asyncio as aioredis
import json

logger = logging.getLogger(__name__)


class MemoryLayer(ABC):
    @abstractmethod
    async def store(self, key: str, value: Any, ttl: int | None = None):
        raise NotImplementedError

    @abstractmethod
    async def retrieve(self, key: str) -> Any | None:
        raise NotImplementedError

    @abstractmethod
    async def search(self, query: str, limit: int = 10) -> list[dict]:
        raise NotImplementedError


class WorkingMemory(MemoryLayer):
    def __init__(self):
        self.redis = aioredis.from_url(settings.REDIS_URL, decode_responses=True)

    async def store(self, key: str, value: Any, ttl: int | None = 3600):
        await self.redis.setex(f"wm:{key}", ttl or 3600, json.dumps(value))

    async def retrieve(self, key: str) -> Any | None:
        data = await self.redis.get(f"wm:{key}")
        return json.loads(data) if data else None

    async def search(self, query: str, limit: int = 10) -> list[dict]:
        keys = await self.redis.keys("wm:*")
        results = []
        for k in keys[:limit]:
            data = await self.redis.get(k)
            if data:
                results.append({"key": k, "value": json.loads(data)})
        return results


class ConversationMemory(MemoryLayer):
    def __init__(self):
        self.redis = aioredis.from_url(settings.REDIS_URL, decode_responses=True)

    async def store(self, key: str, value: Any, ttl: int | None = None):
        await self.redis.setex(f"cm:{key}", ttl or 86400 * 30, json.dumps(value))

    async def retrieve(self, key: str) -> Any | None:
        data = await self.redis.get(f"cm:{key}")
        return json.loads(data) if data else None

    async def search(self, query: str, limit: int = 10) -> list[dict]:
        keys = await self.redis.keys("cm:*")
        results = []
        for k in keys[:limit]:
            data = await self.redis.get(k)
            if data:
                results.append({"key": k, "value": json.loads(data)})
        return results


class KnowledgeMemory(MemoryLayer):
    def __init__(self):
        from backend.app.core.vector_store import vector_store
        self.vector_store = vector_store

    async def store(self, key: str, value: Any, ttl: int | None = None):
        await self.vector_store.index([{"content": json.dumps(value), "metadata": {"key": key}}])

    async def retrieve(self, key: str) -> Any | None:
        results = await self.vector_store.search(key, limit=1)
        if results:
            return json.loads(results[0]["content"])
        return None

    async def search(self, query: str, limit: int = 10) -> list[dict]:
        return await self.vector_store.search(query, limit=limit)


class LongTermMemory(MemoryLayer):
    def __init__(self, base_path: str = "./workspace/memory"):
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)

    async def store(self, key: str, value: Any, ttl: int | None = None):
        path = self.base_path / f"{key}.json"
        path.write_text(json.dumps(value, indent=2))

    async def retrieve(self, key: str) -> Any | None:
        path = self.base_path / f"{key}.json"
        if path.exists():
            return json.loads(path.read_text())
        return None

    async def search(self, query: str, limit: int = 10) -> list[dict]:
        results = []
        for path in self.base_path.glob("*.json"):
            if len(results) >= limit:
                break
            content = json.loads(path.read_text())
            results.append({"key": path.stem, "value": content})
        return results


class MemoryManager:
    def __init__(self):
        self.working = WorkingMemory()
        self.conversation = ConversationMemory()
        self.knowledge = KnowledgeMemory()
        self.long_term = LongTermMemory()

    async def store(self, layer: str, key: str, value: Any, ttl: int | None = None):
        layer_map = {
            "working": self.working,
            "conversation": self.conversation,
            "knowledge": self.knowledge,
            "long_term": self.long_term,
        }
        mem = layer_map.get(layer)
        if mem:
            await mem.store(key, value, ttl)
        else:
            raise ValueError(f"Unknown memory layer: {layer}")

    async def retrieve(self, layer: str, key: str) -> Any | None:
        layer_map = {
            "working": self.working,
            "conversation": self.conversation,
            "knowledge": self.knowledge,
            "long_term": self.long_term,
        }
        mem = layer_map.get(layer)
        return await mem.retrieve(key) if mem else None

    async def search(self, layer: str, query: str, limit: int = 10) -> list[dict]:
        layer_map = {
            "working": self.working,
            "conversation": self.conversation,
            "knowledge": self.knowledge,
            "long_term": self.long_term,
        }
        mem = layer_map.get(layer)
        return await mem.search(query, limit=limit) if mem else []


memory_manager = MemoryManager()
