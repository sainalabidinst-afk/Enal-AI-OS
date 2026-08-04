import json
import logging
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import redis.asyncio as aioredis

from backend.app.core.config import settings

logger = logging.getLogger(__name__)


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


class MemoryLayer(ABC):
    @abstractmethod
    async def store(self, key: str, value: Any, ttl: int | None = None, session_id: str | None = None, project_id: str | None = None):
        raise NotImplementedError

    @abstractmethod
    async def retrieve(self, key: str, session_id: str | None = None, project_id: str | None = None) -> Any | None:
        raise NotImplementedError

    @abstractmethod
    async def search(self, query: str, limit: int = 10, session_id: str | None = None, project_id: str | None = None) -> list[dict]:
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


from backend.app.core.memory_working import WorkingMemory
from backend.app.core.memory_conversation import ConversationMemory
from backend.app.core.memory_knowledge import KnowledgeMemory
from backend.app.core.memory_longterm import LongTermMemory
from backend.app.core.memory_episodic import EpisodicMemory
from backend.app.core.memory_session import SessionMemory
from backend.app.core.memory_project import ProjectMemory


class MemoryManager:
    def __init__(self):
        self._layers: dict[str, MemoryLayer] = {
            "working": WorkingMemory(),
            "conversation": ConversationMemory(),
            "knowledge": KnowledgeMemory(),
            "longterm": LongTermMemory(),
            "episodic": EpisodicMemory(),
            "session": SessionMemory(),
            "project": ProjectMemory(),
        }

    async def get_session_context(self, session_id: str, query: str | None = None) -> dict[str, Any]:
        context: dict[str, Any] = {"session_id": session_id, "entries": [], "summary": ""}
        session_results = await self._layers["session"].search("", limit=100, session_id=session_id)
        context["entries"] = session_results
        if query:
            context["entries"] = [e for e in session_results if query.lower() in str(e.get("value", "")).lower()]
        return context

    async def get_project_context(self, project_id: str, query: str | None = None) -> dict[str, Any]:
        context: dict[str, Any] = {"project_id": project_id, "entries": [], "summary": ""}
        proj_results = await self._layers["project"].search("", limit=100, project_id=project_id)
        context["entries"] = proj_results
        if query:
            context["entries"] = [e for e in proj_results if query.lower() in str(e.get("value", "")).lower()]
        return context

    async def rank_memories(self, candidates: list[dict], importance_factor: float = 1.0) -> list[dict]:
        scored: list[dict] = []
        now = time.time()
        for c in candidates:
            scores: list[float] = []
            ts = c.get("timestamp", now)
            recency_val = max(0.1, 1.0 - (now - ts) / 86400)
            scores.append(recency_val)
            imp = float(c.get("importance", 0.5))
            scores.append(imp * importance_factor)
            c["rank_score"] = sum(scores) / len(scores) if scores else 0
            scored.append(c)
        return sorted(scored, key=lambda x: x.get("rank_score", 0), reverse=True)

    async def compress_memory(self, layer: str, threshold: int = 50) -> str | None:
        keys = await self._layers[layer].list_keys() if layer in self._layers else []
        if len(keys) > threshold:
            block = await self.consolidate(layer, "", max_entries=threshold)
            if block:
                await self.store("longterm", block.block_id, block.consolidated_content)
                for k in block.source_ids:
                    await self._layers[layer].delete(k)
                return block.block_id
        return None

    async def store(self, layer: str, key: str, value: Any, ttl: int | None = None, session_id: str | None = None, project_id: str | None = None):
        mem = self._layers.get(layer)
        if not mem:
            return
        await mem.store(key, value, ttl, session_id=session_id, project_id=project_id)
        logger.info(f"Stored in {layer} memory: {key}")

    async def retrieve(self, layer: str, key: str, session_id: str | None = None, project_id: str | None = None) -> Any | None:
        mem = self._layers.get(layer)
        if not mem:
            return None
        return await mem.retrieve(key, session_id=session_id, project_id=project_id)

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
        import uuid

        from backend.app.core.model_router import model_router

        mem = self._layers.get(layer)
        if not mem:
            return None

        keys = await mem.list_keys()
        keys = keys[:max_entries]
        entries: list[dict] = []
        for k in keys:
            v = await mem.retrieve(k)
            if v:
                entries.append({"key": k, "value": v})

        if not entries:
            return None

        prompt = f"Summarize the key points from these {len(entries)} memory entries: {json.dumps(entries[:20])}"
        response = await model_router.acomplete(
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
        results: list[dict] = []
        for layer_name, mem in self._layers.items():
            if mem is None:
                continue
            layer_results = await mem.search(query, limit=5)
            for r in layer_results:
                r["layer"] = layer_name
                if session_pattern:
                    if isinstance(r.get("value"), dict):
                        session_id_val = r["value"].get("session_id", "")
                        if session_pattern not in session_id_val:
                            continue
                results.append(r)
        return results


memory_manager = MemoryManager()
