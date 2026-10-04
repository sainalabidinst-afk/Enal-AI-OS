"""
Tests for Memory Engine Enhancement
====================================
Tests for Episodic Memory, Memory Consolidation, and Cross-session Retrieval.
Also covers persistence-on-restart and TTL enforcement.
"""

import tempfile

import pytest

from backend.app.core.memory_layer import (
    KnowledgeMemory,
    LongTermMemory,
    MemoryManager,
    SessionMemory,
)


class TestKnowledgeMemory:
    """Tests for KnowledgeMemory layer - no Redis dependency."""

    def _get_knowledge_memory_class(self):
        """Load KnowledgeMemory without triggering FastAPI import."""

        return KnowledgeMemory

    @pytest.mark.asyncio
    async def test_knowledge_store_and_retrieve(self):
        KnowledgeMemory = self._get_knowledge_memory_class()  # noqa: N806
        with tempfile.TemporaryDirectory() as tmpdir:
            mem = KnowledgeMemory(base_path=tmpdir)
            await mem.store("k1", {"fact": "knowledge item"})

            result = await mem.retrieve("k1")
            assert result == {"fact": "knowledge item"}

    @pytest.mark.asyncio
    async def test_knowledge_search(self):
        KnowledgeMemory = self._get_knowledge_memory_class()  # noqa: N806
        with tempfile.TemporaryDirectory() as tmpdir:
            mem = KnowledgeMemory(base_path=tmpdir)
            await mem.store("doc1", "This is a Python function")
            await mem.store("doc2", "JavaScript handles async")

            results = await mem.search("python", limit=5)
            assert len(results) >= 1

    @pytest.mark.asyncio
    async def test_knowledge_reload_from_disk(self):
        KnowledgeMemory = self._get_knowledge_memory_class()  # noqa: N806
        with tempfile.TemporaryDirectory() as tmpdir:
            mem1 = KnowledgeMemory(base_path=tmpdir)
            await mem1.store("k-reload", {"fact": "reloaded knowledge"})
            mem2 = KnowledgeMemory(base_path=tmpdir)
            result = await mem2.retrieve("k-reload")
            assert result == {"fact": "reloaded knowledge"}


class TestEpisodicMemory:
    """Tests for EpisodicMemory layer - no Redis dependency."""

    def _get_episodic_memory_class(self):
        """Load EpisodicMemory without triggering FastAPI import."""
        from backend.app.core.memory_layer import EpisodicMemory

        return EpisodicMemory

    @pytest.mark.asyncio
    async def test_episodic_store(self):
        EpisodicMemory = self._get_episodic_memory_class()  # noqa: N806
        with tempfile.TemporaryDirectory() as tmpdir:
            mem = EpisodicMemory(base_path=tmpdir)

            await mem.store(
                "episode-1",
                {
                    "session_id": "session-abc",
                    "event_type": "task_completed",
                    "content": {"result": "success"},
                    "importance": 0.9,
                    "summary": "Task completed successfully",
                },
            )

            result = await mem.retrieve("episode-1")
            assert result is not None
            assert result["event_type"] == "task_completed"

    @pytest.mark.asyncio
    async def test_episodic_search(self):
        EpisodicMemory = self._get_episodic_memory_class()  # noqa: N806
        with tempfile.TemporaryDirectory() as tmpdir:
            mem = EpisodicMemory(base_path=tmpdir)

            await mem.store(
                "e1",
                {
                    "session_id": "s1",
                    "event_type": "error",
                    "content": {"error": "timeout"},
                    "summary": "Connection timeout occurred",
                },
            )

            results = await mem.search("timeout", limit=5)
            assert len(results) >= 1

    @pytest.mark.asyncio
    async def test_episodic_reload_from_disk(self):
        EpisodicMemory = self._get_episodic_memory_class()  # noqa: N806
        with tempfile.TemporaryDirectory() as tmpdir:
            mem1 = EpisodicMemory(base_path=tmpdir)
            await mem1.store(
                "ep-reload-1",
                {
                    "session_id": "sess-a",
                    "event_type": "reload_test",
                    "content": {"check": True},
                    "summary": "Reload persistence test",
                },
            )
            mem2 = EpisodicMemory(base_path=tmpdir)
            result = await mem2.retrieve("ep-reload-1")
            assert result is not None
            assert result["event_type"] == "reload_test"

    @pytest.mark.asyncio
    async def test_episodic_list_keys_pattern(self):
        EpisodicMemory = self._get_episodic_memory_class()  # noqa: N806
        with tempfile.TemporaryDirectory() as tmpdir:
            mem = EpisodicMemory(base_path=tmpdir)
            await mem.store("ep-alpha", {"event_type": "t", "content": {}})
            await mem.store("ep-beta", {"event_type": "t", "content": {}})
            keys = await mem.list_keys(pattern="ep-alpha")
            assert keys == ["ep-alpha"]


class TestMemoryManager:
    """Tests for unified MemoryManager."""

    def _get_memory_manager_class(self):
        """Load MemoryManager without triggering FastAPI import."""
        from backend.app.core.memory_layer import EpisodicMemory, MemoryManager

        return MemoryManager, KnowledgeMemory, EpisodicMemory

    @pytest.mark.asyncio
    async def test_cross_layer_store(self):
        MemoryManager, KnowledgeMemory, EpisodicMemory = self._get_memory_manager_class()  # noqa: N806
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = MemoryManager()
            manager._layers["knowledge"] = KnowledgeMemory(base_path=f"{tmpdir}/know")
            manager._layers["episodic"] = EpisodicMemory(base_path=f"{tmpdir}/episodic")

            await manager.store("knowledge", "fact-1", {"knowledge": "item"})
            await manager.store("episodic", "ep-1", {"event_type": "test", "content": {}})

            know_result = await manager.retrieve("knowledge", "fact-1")
            assert know_result == {"knowledge": "item"}

            episodic_result = await manager.retrieve("episodic", "ep-1")
            assert episodic_result is not None

    @pytest.mark.asyncio
    async def test_cross_session_search(self):
        MemoryManager, _, EpisodicMemory = self._get_memory_manager_class()  # noqa: N806
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = MemoryManager()
            manager._layers["episodic"] = EpisodicMemory(base_path=f"{tmpdir}/episodic")
            manager._layers["working"] = None
            manager._layers["conversation"] = None

            await manager.store(
                "episodic",
                "ep-1",
                {
                    "session_id": "session-xyz",
                    "event_type": "task",
                    "content": {"task": "analyze"},
                    "summary": "Analysis task",
                },
            )

            results = await manager.cross_session_search("task")
            assert len(results) >= 1
            assert any(r["layer"] == "episodic" for r in results)

    @pytest.mark.asyncio
    async def test_session_reload_from_disk(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            mem1 = SessionMemory(base_path=tmpdir)
            await mem1.store("sess-key", {"data": "session-value"}, session_id="sess-1")
            mem2 = SessionMemory(base_path=tmpdir)
            result = await mem2.retrieve("sess-key", session_id="sess-1")
            assert result == {"data": "session-value"}

    @pytest.mark.asyncio
    async def test_session_list_keys_pattern(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            mem = SessionMemory(base_path=tmpdir)
            await mem.store("key-a", "val-a", session_id="s1")
            await mem.store("key-b", "val-b", session_id="s1")
            keys = await mem.list_keys(pattern="key-a", session_id="s1")
            assert keys == ["key-a"]

    @pytest.mark.asyncio
    async def test_longterm_ttl_expiry(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            mem = LongTermMemory(base_path=tmpdir)
            await mem.store("lt-key", {"info": "temp"}, ttl=0)
            result = await mem.retrieve("lt-key")
            assert result is None

    @pytest.mark.asyncio
    async def test_longterm_reload_from_disk(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            mem1 = LongTermMemory(base_path=tmpdir)
            await mem1.store("lt-reload", {"info": "persisted"})
            mem2 = LongTermMemory(base_path=tmpdir)
            result = await mem2.retrieve("lt-reload")
            assert result == {"info": "persisted"}

    @pytest.mark.asyncio
    async def test_manager_delete_with_session_id(self):
        manager = MemoryManager()
        manager._layers["session"] = SessionMemory()
        with tempfile.TemporaryDirectory() as tmpdir:
            manager._layers["session"] = SessionMemory(base_path=tmpdir)
            await manager.store("session", "m-key", {"v": 1}, session_id="sess-mgr")
            deleted = await manager.delete("session", "m-key", session_id="sess-mgr")
            assert deleted is True
            result = await manager.retrieve("session", "m-key", session_id="sess-mgr")
            assert result is None
