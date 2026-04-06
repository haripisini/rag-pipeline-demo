import asyncio
import redis
from vector_store import search_vector

# -------------------------------
# 🔹 Redis Setup
# -------------------------------
redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)


# -------------------------------
# 🔹 Knowledge Graph (simple)
# -------------------------------
knowledge_graph = {
    "rag": ["retrieval", "generation"],
    "redis": ["cache", "fast"],
    "qdrant": ["vector db", "search"],
}


# -------------------------------
# 🔹 Main Pipeline
# -------------------------------
async def run_pipeline(query: str, tenant_id: str):

    cache_key = f"{tenant_id}:{query}"

    # ✅ Check cache
    cached = redis_client.get(cache_key)
    if cached:
        return {
            "results": [f"(cache) {cached}"],
            "confidence": 0.95
        }

    # ✅ Vector Retrieval (Qdrant)
    context = search_vector(query)

    # ✅ Knowledge Graph enrichment
    graph_context = knowledge_graph.get(query.lower(), [])

    # ✅ Combine context
    full_context = context + graph_context

    # ✅ Generate response
    result = f"RAG answer for '{query}' using context {full_context}"

    # ✅ Store in cache
    redis_client.set(cache_key, result)

    return {
        "results": [result],
        "confidence": 0.90
    }


# -------------------------------
# 🔹 Multi Query (Async)
# -------------------------------
async def multi_query_pipeline(query: str, tenant_id: str):

    expanded_queries = [
        query,
        f"{query} example",
        f"{query} use case"
    ]

    tasks = [run_pipeline(q, tenant_id) for q in expanded_queries]

    results = await asyncio.gather(*tasks)

    return results