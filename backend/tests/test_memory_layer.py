import time

import pytest

from backend.app.core.memory_layer import MemoryManager


class FakeMemory:
    def __init__(self, store_result=None, retrieve_result=None, search_result=None, list_keys_result=None, delete_result=None):
        self._store_result = store_result
        self._retrieve_result = retrieve_result
        self._search_result = search_result or []
        self._list_keys_result = list_keys_result or []
        self._delete_result = delete_result or False
        self.stored = []

    async def store(self, key, value, ttl=None, session_id=None, project_id=None):
        self.stored.append((key, value))

    async def retrieve(self, key, session_id=None, project_id=None):
        return self._retrieve_result

    async def search(self, query, limit=10, session_id=None, project_id=None):
        return self._search_result

    async def delete(self, key):
        return self._delete_result

    async def list_keys(self, pattern="*"):
        return self._list_keys_result


class TestMemoryManager:
    @pytest.fixture
    def manager(self):
        mgr = MemoryManager()
        return mgr

    async def test_get_session_context_empty(self, manager):
        manager._layers["session"] = FakeMemory(search_result=[])
        context = await manager.get_session_context("sess-1")
        assert context["session_id"] == "sess-1"
        assert context["entries"] == []

    async def test_get_session_context_with_query(self, manager):
        manager._layers["session"] = FakeMemory(search_result=[
            {"value": "hello world"},
            {"value": "foo bar"},
        ])
        context = await manager.get_session_context("sess-1", query="hello")
        assert len(context["entries"]) == 1
        assert context["entries"][0]["value"] == "hello world"

    async def test_get_project_context_empty(self, manager):
        manager._layers["project"] = FakeMemory(search_result=[])
        context = await manager.get_project_context("proj-1")
        assert context["project_id"] == "proj-1"
        assert context["entries"] == []

    async def test_rank_memories_sorts_by_rank_score(self, manager):
        now = time.time()
        candidates = [
            {"timestamp": now - 100, "importance": 0.9},
            {"timestamp": now - 1000, "importance": 0.5},
        ]
        ranked = await manager.rank_memories(candidates)
        assert ranked[0]["rank_score"] >= ranked[1]["rank_score"]

    async def test_rank_memories_with_importance_factor(self, manager):
        now = time.time()
        candidates = [
            {"timestamp": now, "importance": 0.5},
        ]
        ranked = await manager.rank_memories(candidates, importance_factor=2.0)
        assert "rank_score" in ranked[0]

    async def test_store_unknown_layer_returns_none(self, manager):
        result = await manager.store("unknown", "key", "value")
        assert result is None

    async def test_retrieve_unknown_layer_returns_none(self, manager):
        result = await manager.retrieve("unknown", "key")
        assert result is None

    async def test_search_unknown_layer_returns_empty(self, manager):
        result = await manager.search("unknown", "query")
        assert result == []

    async def test_delete_unknown_layer_returns_false(self, manager):
        result = await manager.delete("unknown", "key")
        assert result is False

    async def test_list_keys_unknown_layer_returns_empty(self, manager):
        result = await manager.list_keys("unknown")
        assert result == []

    async def test_cross_session_search(self, manager):
        for layer in manager._layers:
            manager._layers[layer] = FakeMemory(search_result=[{"value": {"session_id": "s1", "text": "a"}}])
        results = await manager.cross_session_search("query")
        assert len(results) == len(manager._layers)

    async def test_cross_session_search_with_pattern(self, manager):
        for layer in manager._layers:
            manager._layers[layer] = FakeMemory(search_result=[
                {"value": {"session_id": "s1", "text": "a"}},
                {"value": {"session_id": "s2", "text": "b"}},
            ])
        results = await manager.cross_session_search("query", session_pattern="s1")
        assert len(results) == len(manager._layers)
