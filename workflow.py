import asyncio
import redis
from vector_store import search_vector

# -------------------------------
# 🔹 Redis Setup
# -------------------------------
redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)


# -------------------------------
# 🔹 Knowledge Graph
# -------------------------------
knowledge_graph = {
    "rag": ["retrieval", "generation"],
    "redis": ["cache", "fast"],
    "qdrant": ["vector db", "search"],
}


# -------------------------------
# 🔹 Keyword Search (Sparse)
# -------------------------------
def keyword_search(query):
    docs = [
        "RAG uses retrieval and generation",
        "Redis is used for caching",
        "Qdrant is a vector database",
        "Multi-tenant architecture isolates data"
    ]

    results = []

    for doc in docs:
        if query.lower() in doc.lower():
            results.append(doc)

    return results


# -------------------------------
# 🔹 Main Pipeline
# -------------------------------
async def run_pipeline(query: str, tenant_id: str):

    try:
        cache_key = f"{tenant_id}:{query}"

        # ✅ Cache check
        cached = redis_client.get(cache_key)
        if cached:
            return {
                "results": [f"(cache) {cached}"],
                "confidence": 0.95
            }

        # ✅ Normalize query
        clean_query = query.lower().strip()

        # 🔥 Hybrid Search (Dense + Sparse)
        vector_results = search_vector(clean_query)
        keyword_results = keyword_search(clean_query)

        # ✅ Combine + remove duplicates
        context = list(set(vector_results + keyword_results))

        # ✅ Knowledge Graph enrichment
        graph_context = knowledge_graph.get(clean_query, [])

        # ✅ Final context
        full_context = context + graph_context

        # ✅ Generate response
        result = f"RAG answer for '{query}' using context {full_context}"

        # ✅ Store in cache
        redis_client.set(cache_key, result)

        return {
            "results": [result],
            "confidence": 0.90
        }

    except Exception as e:
        return {
            "results": [f"Error: {str(e)}"],
            "confidence": 0.0
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