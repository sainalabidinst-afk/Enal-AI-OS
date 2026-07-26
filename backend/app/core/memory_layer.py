import logging
import time
import hashlib
import json
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from pathlib import Path
from backend.app.core.config import settings
import redis.asyncio as aioredis

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Core Dataclasses
# ---------------------------------------------------------------------------

@dataclass
class EpisodicMemoryEntry:
    """A single episode / event stored in episodic memory."""
    episode_id: str
    session_id: str
    timestamp: float
    event_type: str
    content: dict[str, Any]
    tags: list[str] = field(default_factory=list)
    importance: float = 0.5
    summary: str = ""


@dataclass
class ConsolidatedBlock:
    """Result of compressing several related memories into one."""
    block_id: str
    source_ids: list[str]
    consolidated_content: dict[str, Any]
    summary: str
    importance: float
    source_layer: str
    created_at: float


# ---------------------------------------------------------------------------
# Abstract Layer
# ---------------------------------------------------------------------------

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

    @abstractmethod
    async def delete(self, key: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def list_keys(self, pattern: str = "*") -> list[str]:
        raise NotImplementedError

    async def count(self) -> int:
        keys = await self.list_keys()
        return len(keys)


# ---------------------------------------------------------------------------
# Working Memory (short-lived, Redis, 1-hour TTL)
# ---------------------------------------------------------------------------

class WorkingMemory(MemoryLayer):
    def __init__(self):
        self.redis = aioredis.from_url(settings.REDIS_URL, decode_responses=True)

    async def store(self, key: str, value: Any, ttl: int | None = 3600):
        await self.redis.setex(f"wm:{key}", ttl or 3600, json.dumps(value, default=str))

    async def retrieve(self, key: str) -> Any | None:
        data = await self.redis.get(f"wm:{key}")
        return json.loads(data) if data else None

    async def search(self, query: str, limit: int = 10) -> list[dict]:
        keys = await self.redis.keys("wm:*")
        results = []
        for k in keys[:limit * 3]:
            data = await self.redis.get(k)
            if data:
                val = json.loads(data)
                if query.lower() in str(val).lower():
                    results.append({"key": k, "value": val})
                    if len(results) >= limit:
                        break
        return results

    async def delete(self, key: str) -> bool:
        return bool(await self.redis.delete(f"wm:{key}"))

    async def list_keys(self, pattern: str = "*") -> list[str]:
        keys = await self.redis.keys(f"wm:{pattern}")
        return [k[3:] for k in keys]  # Remove wm: prefix


# ---------------------------------------------------------------------------
# Conversation Memory (Redis-backed with longer TTL)
# ---------------------------------------------------------------------------

class ConversationMemory(MemoryLayer):
    def __init__(self):
        self.redis = aioredis.from_url(settings.REDIS_URL, decode_responses=True)

    async def store(self, key: str, value: Any, ttl: int | None = 86400):
        await self.redis.setex(f"conv:{key}", ttl or 86400, json.dumps(value, default=str))

    async def retrieve(self, key: str) -> Any | None:
        data = await self.redis.get(f"conv:{key}")
        return json.loads(data) if data else None

    async def search(self, query: str, limit: int = 10) -> list[dict]:
        keys = await self.redis.keys("conv:*")
        results = []
        for k in keys[:limit * 3]:
            data = await self.redis.get(k)
            if data:
                val = json.loads(data)
                if query.lower() in str(val).lower():
                    results.append({"key": k, "value": val})
                    if len(results) >= limit:
                        break
        return results

    async def delete(self, key: str) -> bool:
        return bool(await self.redis.delete(f"conv:{key}"))

    async def list_keys(self, pattern: str = "*") -> list[str]:
        keys = await self.redis.keys(f"conv:{pattern}")
        return [k[5:] for k in keys]  # Remove conv: prefix


# ---------------------------------------------------------------------------
# Knowledge Memory (Vector store, FAISS-like)
# ---------------------------------------------------------------------------

class KnowledgeMemory(MemoryLayer):
    def __init__(self, base_path: str = "./workspace/memory/knowledge"):
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)
        self._index: dict[str, list[str]] = {}  # Simple keyword index

    async def store(self, key: str, value: Any, ttl: int | None = None):
        path = self.base_path / f"{key}.json"
        data = {"key": key, "value": value, "updated_at": time.time()}
        path.write_text(json.dumps(data, default=str))
        # Update index
        content = str(value).lower()
        words = [w for w in content.split() if len(w) > 3]
        self._index[key] = words

    async def retrieve(self, key: str) -> Any | None:
        path = self.base_path / f"{key}.json"
        if not path.exists():
            return None
        data = json.loads(path.read_text())
        return data.get("value")

    async def search(self, query: str, limit: int = 10) -> list[dict]:
        query_lower = query.lower()
        results = []
        for path in self.base_path.glob("*.json"):
            data = json.loads(path.read_text())
            score = sum(1 for w in data.get("value", "").lower().split() if query_lower in w)
            if score > 0:
                results.append({"key": data["key"], "value": data["value"], "score": score})
        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:limit]

    async def delete(self, key: str) -> bool:
        path = self.base_path / f"{key}.json"
        if path.exists():
            path.unlink()
            return True
        return False

    async def list_keys(self, pattern: str = "*") -> list[str]:
        return [p.stem for p in self.base_path.glob(f"{pattern}.json")]


# ---------------------------------------------------------------------------
# Long-term Memory (Persistent, compressed)
# ---------------------------------------------------------------------------

class LongTermMemory(MemoryLayer):
    def __init__(self, base_path: str = "./workspace/memory/longterm"):
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)

    async def store(self, key: str, value: Any, ttl: int | None = None):
        path = self.base_path / f"{key}.json"
        data = {"key": key, "value": value, "created_at": time.time()}
        path.write_text(json.dumps(data, default=str))

    async def retrieve(self, key: str) -> Any | None:
        path = self.base_path / f"{key}.json"
        if not path.exists():
            return None
        data = json.loads(path.read_text())
        return data.get("value")

    async def search(self, query: str, limit: int = 10) -> list[dict]:
        results = []
        query_lower = query.lower()
        for path in self.base_path.glob("*.json"):
            data = json.loads(path.read_text())
            content = str(data.get("value", ""))
            if query_lower in content.lower():
                results.append({"key": data["key"], "value": data["value"]})
            if len(results) >= limit:
                break
        return results

    async def delete(self, key: str) -> bool:
        path = self.base_path / f"{key}.json"
        if path.exists():
            path.unlink()
            return True
        return False

    async def list_keys(self, pattern: str = "*") -> list[str]:
        return [p.stem for p in self.base_path.glob(f"{pattern}.json")]


# ---------------------------------------------------------------------------
# Episodic Memory (Events + Timeline)
# ---------------------------------------------------------------------------

class EpisodicMemory(MemoryLayer):
    def __init__(self, base_path: str = "./workspace/memory/episodic"):
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)
        self._episodes: dict[str, EpisodicMemoryEntry] = {}

    async def store(self, key: str, value: Any, ttl: int | None = None):
        if isinstance(value, dict) and "event_type" in value:
            entry = EpisodicMemoryEntry(
                episode_id=key,
                session_id=value.get("session_id", "default"),
                timestamp=time.time(),
                event_type=value.get("event_type", "generic"),
                content=value.get("content", {}),
                tags=value.get("tags", []),
                importance=value.get("importance", 0.5),
                summary=value.get("summary", ""),
            )
            self._episodes[key] = entry
            self._persist(entry)

    async def retrieve(self, key: str) -> Any | None:
        return self._episodes.get(key).__dict__ if key in self._episodes else None

    async def search(self, query: str, limit: int = 10) -> list[dict]:
        results = []
        query_lower = query.lower()
        for entry in self._episodes.values():
            if query_lower in entry.event_type.lower() or query_lower in entry.summary.lower():
                results.append({"key": entry.episode_id, "value": entry.__dict__})
            if len(results) >= limit:
                break
        return results

    async def delete(self, key: str) -> bool:
        if key in self._episodes:
            del self._episodes[key]
            (self.base_path / f"{key}.json").unlink(missing_ok=True)
            return True
        return False

    async def list_keys(self, pattern: str = "*") -> list[str]:
        return list(self._episodes.keys())

    def _persist(self, entry: EpisodicMemoryEntry):
        path = self.base_path / f"{entry.episode_id}.json"
        path.write_text(json.dumps(entry.__dict__, default=str))


# ---------------------------------------------------------------------------
# Memory Manager (Unified Interface)
# ---------------------------------------------------------------------------

class MemoryManager:
    def __init__(self):
        self._layers: dict[str, MemoryLayer] = {
            "working": WorkingMemory(),
            "conversation": ConversationMemory(),
            "knowledge": KnowledgeMemory(),
            "longterm": LongTermMemory(),
            "episodic": EpisodicMemory(),
        }

    async def store(self, layer: str, key: str, value: Any, ttl: int | None = None):
        mem = self._layers.get(layer)
        if mem:
            await mem.store(key, value, ttl)
            logger.info(f"Stored in {layer} memory: {key}")

    async def retrieve(self, layer: str, key: str) -> Any | None:
        mem = self._layers.get(layer)
        if mem:
            return await mem.retrieve(key)
        return None

    async def search(self, layer: str, query: str, limit: int = 10) -> list[dict]:
        mem = self._layers.get(layer)
        if mem:
            return await mem.search(query, limit)
        return []

    async def delete(self, layer: str, key: str) -> bool:
        mem = self._layers.get(layer)
        if mem:
            return await mem.delete(key)
        return False

    async def list_keys(self, layer: str, pattern: str = "*") -> list[str]:
        mem = self._layers.get(layer)
        if mem:
            return await mem.list_keys(pattern)
        return []

    async def consolidate(self, layer: str, query: str, max_entries: int = 100) -> ConsolidatedBlock | None:
        """Compress related memories into consolidated block."""
        from backend.app.core.model_router import model_router
        import uuid

        mem = self._layers.get(layer)
        if not mem:
            return None

        keys = await mem.list_keys()[:max_entries]
        entries = []
        for k in keys:
            v = await mem.retrieve(k)
            if v:
                entries.append({"key": k, "value": v})

        if not entries:
            return None

        # Generate summary via LLM
        prompt = f"Summarize the key points from these {len(entries)} memory entries: {json.dumps(entries[:20])}"
        response = model_router.complete(
            [{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=1024,
        )
        summary = response.choices[0].message.content if response else "Consolidated summary"

        block = ConsolidatedBlock(
            block_id=f"consolidated-{uuid.uuid4().hex[:8]}",
            source_ids=[e["key"] for e in entries],
            consolidated_content={"entries": entries},
            summary=summary,
            importance=0.7,
            source_layer=layer,
            created_at=time.time(),
        )
        return block

    async def cross_session_search(self, query: str, session_pattern: str | None = None) -> list[dict]:
        """Search across all memory layers, optionally filtering by session."""
        results = []
        for layer_name, mem in self._layers.items():
            if mem is None:
                continue
            layer_results = await mem.search(query, limit=5)
            for r in layer_results:
                r["layer"] = layer_name
                if session_pattern:
                    if isinstance(r.get("value"), dict):
                        session_id = r["value"].get("session_id", "")
                        if session_pattern not in session_id:
                            continue
                results.append(r)
        return results


memory_manager = MemoryManager()