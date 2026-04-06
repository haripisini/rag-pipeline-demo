import asyncio
import random
import redis

# Redis connection
redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)

# Knowledge Graph
GRAPH = {
    "RAG": ["retrieval", "generation"],
    "Databricks": ["spark", "big data"]
}

def get_graph_context(query):
    return GRAPH.get(query, [])

# -------------------------------
# Main Pipeline
# -------------------------------
async def run_pipeline(query: str):

    # ✅ 1. Check Redis cache
    cached = redis_client.get(query)
    if cached:
        return {
            "results": [f"(cache) {cached}"],
            "confidence": 0.95
        }

    # ✅ 2. Get context
    context = get_graph_context(query)

    # ✅ 3. Generate answer
    answer = f"{query} uses retrieval + generation"

    # ✅ 4. Store in Redis
    redis_client.set(query, answer)

    return {
        "results": [answer],
        "confidence": round(random.uniform(0.7, 0.95), 2)
    }


# -------------------------------
# Multi Query (Async)
# -------------------------------
async def multi_query_pipeline(query: str):

    expanded_queries = [
        query,
        f"{query} example",
        f"{query} use case"
    ]

    tasks = [run_pipeline(q) for q in expanded_queries]

    results = await asyncio.gather(*tasks)

    return results