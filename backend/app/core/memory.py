import json
import logging

import redis.asyncio as aioredis

from backend.app.core.config import settings

logger = logging.getLogger(__name__)


class ConversationStore:
    def __init__(self):
        self.redis = aioredis.from_url(
            settings.REDIS_URL,
            encoding="utf-8",
            decode_responses=True,
        )

    async def get_conversation(self, conversation_id: str) -> list[dict]:
        key = f"conversation:{conversation_id}"
        data = await self.redis.get(key)
        if not data:
            return []
        return json.loads(data)

    async def append_message(self, conversation_id: str, message: dict):
        key = f"conversation:{conversation_id}"
        messages = await self.get_conversation(conversation_id)
        messages.append(message)
        await self.redis.setex(key, 86400, json.dumps(messages))

    async def clear_conversation(self, conversation_id: str):
        key = f"conversation:{conversation_id}"
        await self.redis.delete(key)


conversation_store = ConversationStore()
