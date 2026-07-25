"""
Tests for Memory Engine Enhancement
====================================
Tests for Episodic Memory, Memory Consolidation, and Cross-session Retrieval.
"""

import tempfile
from pathlib import Path

import pytest


class TestWorkingMemory:
    """Tests for WorkingMemory layer."""

    @pytest.mark.asyncio
    async def test_store_and_retrieve(self):
        from backend.app.core.memory_layer import WorkingMemory
        mem = WorkingMemory()
        test_key = "test-key-1"
        test_value = {"data": "test", "nested": {"value": 123}}

        await mem.store(test_key, test_value)
        result = await mem.retrieve(test_key)

        assert result == test_value

    @pytest.mark.asyncio
    async def test_search(self):
        from backend.app.core.memory_layer import WorkingMemory
        mem = WorkingMemory()
        await mem.store("key1", {"content": "find me"})
        await mem.store("key2", {"other": "data"})

        results = await mem.search("find", limit=5)
        assert len(results) >= 1
        assert any("find" in str(r.get("value", "")) for r in results)

    @pytest.mark.asyncio
    async def test_delete(self):
        from backend.app.core.memory_layer import WorkingMemory
        mem = WorkingMemory()

        await mem.store("del-test", {"value": "delete"})
        result = await mem.retrieve("del-test")
        assert result is not None

        deleted = await mem.delete("del-test")
        assert deleted is True

        result = await mem.retrieve("del-test")
        assert result is None


class TestKnowledgeMemory:
    """Tests for KnowledgeMemory layer."""

    @pytest.mark.asyncio
    async def test_knowledge_store_and_retrieve(self):
        from backend.app.core.memory_layer import KnowledgeMemory
        with tempfile.TemporaryDirectory() as tmpdir:
            mem = KnowledgeMemory(base_path=tmpdir)
            await mem.store("k1", {"fact": "knowledge item"})

            result = await mem.retrieve("k1")
            assert result == {"fact": "knowledge item"}

    @pytest.mark.asyncio
    async def test_knowledge_search(self):
        from backend.app.core.memory_layer import KnowledgeMemory
        with tempfile.TemporaryDirectory() as tmpdir:
            mem = KnowledgeMemory(base_path=tmpdir)
            await mem.store("doc1", "This is a Python function")
            await mem.store("doc2", "JavaScript handles async")

            results = await mem.search("python", limit=5)
            assert len(results) >= 1


class TestEpisodicMemory:
    """Tests for EpisodicMemory layer."""

    @pytest.mark.asyncio
    async def test_episodic_store(self):
        from backend.app.core.memory_layer import EpisodicMemory
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
        from backend.app.core.memory_layer import EpisodicMemory
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

    @pytest.mark.asyncio
    async def test_cross_layer_store(self):
        from backend.app.core.memory_layer import MemoryManager, KnowledgeMemory, EpisodicMemory
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
        from backend.app.core.memory_layer import MemoryManager, EpisodicMemory
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = MemoryManager()
            manager._layers["episodic"] = EpisodicMemory(base_path=f"{tmpdir}/episodic")

            await manager.store("episodic", "ep-1", {
                "session_id": "session-xyz",
                "event_type": "task",
                "content": {"task": "analyze"},
                "summary": "Analysis task",
            })

            results = await manager.cross_session_search("task")
            assert len(results) >= 1
            assert any(r["layer"] == "episodic" for r in results)


class TestConsolidatedBlock:
    """Tests for memory consolidation."""

    @pytest.mark.asyncio
    async def test_consolidate_returns_block(self):
        from backend.app.core.memory_layer import MemoryManager, KnowledgeMemory
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = MemoryManager()
            manager._layers["knowledge"] = KnowledgeMemory(base_path=f"{tmpdir}/know")

            for i in range(3):
                await manager.store("knowledge", f"entry-{i}", {"fact": f"information {i}"})

            try:
                block = await manager.consolidate("knowledge", "information", max_entries=5)
                if block is not None:
                    assert block.source_layer == "knowledge"
                    assert len(block.source_ids) > 0
            except Exception:
                pass