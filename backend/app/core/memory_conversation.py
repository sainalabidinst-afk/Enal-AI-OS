import json
import logging
from typing import Any

import redis.asyncio as aioredis

from backend.app.core.config import settings

logger = logging.getLogger(__name__)


class ConversationMemory:
    """Redis-backed conversation memory with longer TTL."""

    def __init__(self):
        self.redis = aioredis.from_url(settings.REDIS_URL, decode_responses=True)

    async def store(self, key: str, value: Any, ttl: int | None = 86400, session_id: str | None = None, project_id: str | None = None):
        await self.redis.setex(f"conv:{key}", ttl or 86400, json.dumps(value, default=str))

    async def retrieve(self, key: str, session_id: str | None = None, project_id: str | None = None) -> Any | None:
        data = await self.redis.get(f"conv:{key}")
        return json.loads(data) if data else None

    async def search(self, query: str, limit: int = 10, session_id: str | None = None, project_id: str | None = None) -> list[dict]:
        results: list[dict] = []
        count = 0
        async for k in self.redis.scan_iter("conv:*"):
            if count >= limit * 3:
                break
            data = await self.redis.get(k)
            if data:
                val = json.loads(data)
                if query.lower() in str(val).lower():
                    results.append({"key": k, "value": val})
                    if len(results) >= limit:
                        break
            count += 1
        return results

    async def delete(self, key: str) -> bool:
        return bool(await self.redis.delete(f"conv:{key}"))

    async def list_keys(self, pattern: str = "*") -> list[str]:
        keys = []
        async for k in self.redis.scan_iter(f"conv:{pattern}"):
            keys.append(k[5:])
        return keys
