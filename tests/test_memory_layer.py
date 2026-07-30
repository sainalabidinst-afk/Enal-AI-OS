"""
Tests for Memory Engine Enhancement
====================================
Tests for Episodic Memory, Memory Consolidation, and Cross-session Retrieval.
"""

import tempfile

import pytest


class TestKnowledgeMemory:
    """Tests for KnowledgeMemory layer - no Redis dependency."""

    def _get_knowledge_memory_class(self):
        """Load KnowledgeMemory without triggering FastAPI import."""
        from backend.app.core.memory_layer import KnowledgeMemory
        return KnowledgeMemory

    @pytest.mark.asyncio
    async def test_knowledge_store_and_retrieve(self):
        KnowledgeMemory = self._get_knowledge_memory_class()
        with tempfile.TemporaryDirectory() as tmpdir:
            mem = KnowledgeMemory(base_path=tmpdir)
            await mem.store("k1", {"fact": "knowledge item"})

            result = await mem.retrieve("k1")
            assert result == {"fact": "knowledge item"}

    @pytest.mark.asyncio
    async def test_knowledge_search(self):
        KnowledgeMemory = self._get_knowledge_memory_class()
        with tempfile.TemporaryDirectory() as tmpdir:
            mem = KnowledgeMemory(base_path=tmpdir)
            await mem.store("doc1", "This is a Python function")
            await mem.store("doc2", "JavaScript handles async")

            results = await mem.search("python", limit=5)
            assert len(results) >= 1


class TestEpisodicMemory:
    """Tests for EpisodicMemory layer - no Redis dependency."""

    def _get_episodic_memory_class(self):
        """Load EpisodicMemory without triggering FastAPI import."""
        from backend.app.core.memory_layer import EpisodicMemory
        return EpisodicMemory

    @pytest.mark.asyncio
    async def test_episodic_store(self):
        EpisodicMemory = self._get_episodic_memory_class()
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
        EpisodicMemory = self._get_episodic_memory_class()
        with tempfile.TemporaryDirectory() as tmpdir:
            mem = EpisodicMemory(base_path=tmpdir)

            await mem.store("e1", {
                "session_id": "s1",
                "event_type": "error",
                "content": {"error": "timeout"},
                "summary": "Connection timeout occurred",
            })

            results = await mem.search("timeout", limit=5)
            assert len(results) >= 1


class TestMemoryManager:
    """Tests for unified MemoryManager."""

    def _get_memory_manager_class(self):
        """Load MemoryManager without triggering FastAPI import."""
        from backend.app.core.memory_layer import EpisodicMemory, KnowledgeMemory, MemoryManager
        return MemoryManager, KnowledgeMemory, EpisodicMemory

    @pytest.mark.asyncio
    async def test_cross_layer_store(self):
        MemoryManager, KnowledgeMemory, EpisodicMemory = self._get_memory_manager_class()
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
        MemoryManager, _, EpisodicMemory = self._get_memory_manager_class()
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = MemoryManager()
            manager._layers["episodic"] = EpisodicMemory(base_path=f"{tmpdir}/episodic")
            manager._layers["working"] = None
            manager._layers["conversation"] = None

            await manager.store("episodic", "ep-1", {
                "session_id": "session-xyz",
                "event_type": "task",
                "content": {"task": "analyze"},
                "summary": "Analysis task",
            })

            results = await manager.cross_session_search("task")
            assert len(results) >= 1
            assert any(r["layer"] == "episodic" for r in results)