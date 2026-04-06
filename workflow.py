import asyncio
import random
import redis

# -------------------------------
# Redis Connection (Caching Layer)
# -------------------------------
redis_client = redis.Redis(host="localhost", port=6379, decode_responses=True)


# -------------------------------
# Knowledge Graph (Simple Mock)
# -------------------------------
KNOWLEDGE_GRAPH = {
    "RAG": ["retrieval", "generation"],
    "Databricks": ["spark", "big data"],
    "AWS": ["cloud", "ETL"]
}


def get_graph_context(query: str):
    return KNOWLEDGE_GRAPH.get(query, [])


# -------------------------------
# Core Pipeline (Single Query)
# -------------------------------
async def run_pipeline(query: str):
    # 1. Check cache first
    cached_result = redis_client.get(query)
    if cached_result:
        return {
            "results": [f"(cache) {cached_result}"],
            "confidence": 0.95
        }

    try:
        # 2. Simulate processing delay
        await asyncio.sleep(1)

        # 3. Get graph context
        context = get_graph_context(query)

        # 4. Generate response
        answer = f"Answer for '{query}' using context {context}"

        result = {
            "results": [answer],
            "confidence": round(random.uniform(0.75, 0.9), 2)
        }

        # 5. Store in cache
        redis_client.set(query, answer)

        return result

    except Exception as e:
        # 6. Fallback handling (important for production)
        return {
            "results": ["Fallback response due to system issue"],
            "confidence": 0.5
        }


# -------------------------------
# Multi Query (Async Execution)
# -------------------------------
async def multi_query_pipeline(query: str):
    # simulate query expansion
    expanded_queries = [
        query,
        f"{query} example",
        f"{query} use case"
    ]

    tasks = [run_pipeline(q) for q in expanded_queries]

    results = await asyncio.gather(*tasks)

    return results