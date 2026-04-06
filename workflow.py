import asyncio
from vector_store import search_vector
import redis

# 🔹 Redis
redis_client = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

# 🔹 Simple keyword (sparse) search
def keyword_search(query):
    docs = [
        "RAG uses retrieval and generation",
        "Redis is used for caching",
        "Qdrant is a vector database",
        "Multi-tenant architecture isolates data",
    ]

    return [doc for doc in docs if query.lower() in doc.lower()]

# 🔹 Hybrid search
def hybrid_search(query, tenant_id):
    dense_results = search_vector(query, tenant_id)
    sparse_results = keyword_search(query)

    # merge + remove duplicates
    combined = list(set(dense_results + sparse_results))
    return combined

# 🔹 Confidence scoring
def confidence_score(results):
    return round(min(len(results) / 5, 1.0), 2)

# 🔹 Main pipeline
async def run_pipeline(query, tenant_id):
    try:
        # 🔹 Cache check
        cache_key = f"{tenant_id}:{query}"
        cached = redis_client.get(cache_key)

        if cached:
            return {
                "results": [f"(cache) {cached}"],
                "confidence": 0.95
            }

        # 🔹 Hybrid retrieval
        results = hybrid_search(query, tenant_id)

        # 🔹 Generation (simple)
        answer = f"RAG answer for '{query}' using context {results}"

        # 🔹 Save cache
        redis_client.set(cache_key, answer)

        return {
            "results": [answer],
            "confidence": confidence_score(results)
        }

    except Exception as e:
        return {
            "results": [f"Error: {str(e)}"],
            "confidence": 0
        }

# 🔹 Multi-query async
async def multi_query_pipeline(query: str, tenant_id: str):
    expanded_queries = [
        query,
        f"{query} example",
        f"{query} use case"
    ]

    tasks = [run_pipeline(q, tenant_id) for q in expanded_queries]
    results = await asyncio.gather(*tasks)

    return results