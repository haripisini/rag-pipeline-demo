# vector_store.py

from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
from sentence_transformers import SentenceTransformer
import uuid

# 🔹 Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# 🔹 Connect Qdrant (local memory)
client = QdrantClient(":memory:")

COLLECTION_NAME = "rag_collection"

# 🔹 Create collection
client.recreate_collection(
    collection_name=COLLECTION_NAME,
    vectors_config=VectorParams(size=384, distance=Distance.COSINE),
)

# 🔹 Sample data
documents = [
    "RAG uses retrieval and generation",
    "Redis is used for caching",
    "Qdrant is a vector database",
    "Multi-tenant architecture isolates data",
]

# 🔹 Insert data
points = []

for doc in documents:
    vector = model.encode(doc).tolist()
    points.append(
        PointStruct(
            id=str(uuid.uuid4()),
            vector=vector,
            payload={"text": doc}
        )
    )

client.upsert(
    collection_name=COLLECTION_NAME,
    points=points
)


# 🔹 Search function
def search_vector(query):
    query_vector = model.encode(query).tolist()

    results = client.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_vector,
        limit=2
    )

    return [r.payload["text"] for r in results]