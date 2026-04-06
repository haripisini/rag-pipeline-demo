from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
from qdrant_client.models import Filter, FieldCondition, MatchValue
from sentence_transformers import SentenceTransformer
import uuid

# 🔹 Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# 🔹 Connect Qdrant (in-memory)
client = QdrantClient(":memory:")

COLLECTION_NAME = "rag_collection"

# 🔹 Create collection
client.recreate_collection(
    collection_name=COLLECTION_NAME,
    vectors_config=VectorParams(size=384, distance=Distance.COSINE),
)

# 🔹 Sample documents
documents = [
    {"text": "RAG uses retrieval and generation", "tenant": "t1", "type": "ai", "version": "v1"},
    {"text": "Redis is used for caching", "tenant": "t1", "type": "db", "version": "v1"},
    {"text": "Qdrant is a vector database", "tenant": "t2", "type": "db", "version": "v1"},
    {"text": "Multi-tenant architecture isolates data", "tenant": "t2", "type": "arch", "version": "v1"},
]

# 🔹 Insert data
points = []

for doc in documents:
    vector = model.encode(doc["text"]).tolist()

    points.append(
        PointStruct(
            id=str(uuid.uuid4()),
            vector=vector,
            payload={
                "text": doc["text"],
                "tenant": doc["tenant"],
                "type": doc["type"],
                "version": doc["version"]
            }
        )
    )

client.upsert(
    collection_name=COLLECTION_NAME,
    points=points
)

# 🔹 Search with proper filter
def search_vector(query, tenant_id):
    query_vector = model.encode(query).tolist()

    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=2,
        query_filter=Filter(
            must=[
                FieldCondition(
                    key="tenant",
                    match=MatchValue(value=tenant_id)
                )
            ]
        )
    )

    return [point.payload["text"] for point in results.points]