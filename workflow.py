import asyncio
import random

# Knowledge Graph
GRAPH = {
    "RAG": ["retrieval", "generation"],
    "Databricks": ["spark", "big data"]
}

def get_graph_context(query):
    return GRAPH.get(query, [])

# Main pipeline
async def run_pipeline(query):
    context = get_graph_context(query)

    return {
        "results": [f"Answer for {query}", f"Context: {context}"],
        "confidence": round(random.uniform(0.7, 0.95), 2)
    }

# Multi-query async
async def multi_query_pipeline(query):
    queries = [query, query + " example", query + " use case"]

    tasks = [run_pipeline(q) for q in queries]

    results = await asyncio.gather(*tasks)

    return results