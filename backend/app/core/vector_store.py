import logging
from backend.app.core.config import settings
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

logger = logging.getLogger(__name__)


class VectorStore:
    def __init__(self):
        self.client = QdrantClient(url=settings.QDRANT_URL, api_key=settings.QDRANT_API_KEY or None)
        self.collection_name = "enal_ai_os_docs"
        self.embedding_model = settings.DEFAULT_EMBEDDING_MODEL
        self._init_collection()

    def _init_collection(self):
        try:
            self.client.get_collection(self.collection_name)
        except Exception:
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
            )

    def embed(self, text: str) -> list[float]:
        from litellm import embedding
        response = embedding(model=self.embedding_model, input=text)
        return response.data[0]["embedding"]

    def index(self, documents: list[dict]):
        points = []
        for i, doc in enumerate(documents):
            vector = self.embed(doc["content"])
            points.append(PointStruct(
                id=i,
                vector=vector,
                payload={"content": doc["content"], "metadata": doc.get("metadata", {})},
            ))
        self.client.upsert(collection_name=self.collection_name, points=points)

    def search(self, query: str, limit: int = 5) -> list[dict]:
        query_vector = self.embed(query)
        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            limit=limit,
        )
        return [{"content": r.payload["content"], "score": r.score} for r in results]


vector_store = VectorStore()
