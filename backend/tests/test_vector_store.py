import sys

import pytest


def fake_embedding(model, input):
    return type("Resp", (), {"data": [{"embedding": [0.1, 0.2, 0.3]}]})()


class TestVectorStore:
    def test_embed_calls_litellm(self, monkeypatch):
        fake_litellm = type("module", (), {"embedding": staticmethod(fake_embedding)})()
        monkeypatch.setitem(sys.modules, "litellm", fake_litellm)
        import importlib
        import backend.app.core.vector_store as vs_module
        importlib.reload(vs_module)
        store = vs_module.VectorStore.__new__(vs_module.VectorStore)
        store.embedding_model = "test-model"
        embedding = store.embed("hello")
        assert embedding == [0.1, 0.2, 0.3]

    def test_index_embeds_and_upserts(self, monkeypatch):
        class FakePoint:
            def __init__(self, id, vector, payload):
                self.id = id
                self.vector = vector
                self.payload = payload

        class FakeClient:
            def __init__(self, *args, **kwargs):
                self.upserted = []

            def get_collection(self, name):
                raise Exception("not found")

            def create_collection(self, **kwargs):
                pass

            def upsert(self, collection_name, points):
                self.upserted.append(points)

        fake_qdrant = type("module", (), {
            "QdrantClient": FakeClient,
            "Distance": type("Distance", (), {"COSINE": "COSINE"}),
            "PointStruct": FakePoint,
            "VectorParams": lambda *args, **kwargs: None,
        })()
        fake_litellm = type("module", (), {"embedding": staticmethod(fake_embedding)})()
        monkeypatch.setitem(sys.modules, "qdrant_client", fake_qdrant)
        monkeypatch.setitem(sys.modules, "qdrant_client.models", fake_qdrant)
        monkeypatch.setitem(sys.modules, "litellm", fake_litellm)
        import importlib
        import backend.app.core.vector_store as vs_module
        importlib.reload(vs_module)
        store = vs_module.VectorStore()
        store.index([{"content": "doc1", "metadata": {"source": "test"}}])
        assert len(store.client.upserted) == 1
        assert len(store.client.upserted[0]) == 1
        assert store.client.upserted[0][0].payload["content"] == "doc1"

    def test_search_returns_results(self, monkeypatch):
        class FakeResult:
            def __init__(self, payload, score):
                self.payload = payload
                self.score = score

        class FakeClient:
            def __init__(self, *args, **kwargs):
                pass

            def get_collection(self, name):
                pass

            def search(self, collection_name, query_vector, limit):
                return [FakeResult({"content": "result1"}, 0.95)]

        fake_qdrant = type("module", (), {"QdrantClient": FakeClient})()
        fake_litellm = type("module", (), {"embedding": staticmethod(fake_embedding)})()
        monkeypatch.setitem(sys.modules, "qdrant_client", fake_qdrant)
        monkeypatch.setitem(sys.modules, "litellm", fake_litellm)
        import importlib
        import backend.app.core.vector_store as vs_module
        importlib.reload(vs_module)
        store = vs_module.VectorStore()
        results = store.search("query", limit=1)
        assert len(results) == 1
        assert results[0]["content"] == "result1"
        assert results[0]["score"] == 0.95
