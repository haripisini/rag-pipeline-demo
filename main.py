from fastapi import FastAPI
from pydantic import BaseModel
from workflow import multi_query_pipeline

app = FastAPI()

# Request model
class QueryRequest(BaseModel):
    query: str
    tenant_id: str
    role: str

# Dummy data (for metadata filtering)
DATA = [
    {"text": "AWS Glue is ETL service", "tenant_id": "t1"},
    {"text": "Databricks used for big data", "tenant_id": "t2"},
    {"text": "RAG uses retrieval + generation", "tenant_id": "t1"}
]

# Metadata filtering
def filter_by_tenant(query, tenant_id):
    results = []
    for item in DATA:
        if item["tenant_id"] == tenant_id and query.lower() in item["text"].lower():
            results.append(item["text"])
    return results

# Audit logging
def audit_log(request):
    print(f"Audit log: {request.query}")

# API endpoint
@app.post("/query")
async def query_api(request: QueryRequest):

    audit_log(request)

    filtered = filter_by_tenant(request.query, request.tenant_id)

    results = await multi_query_pipeline(request.query)
    result = results[0]

    if filtered:
        result["results"] = filtered

    return {
        "tenant": request.tenant_id,
        "query": request.query,
        "output": result
    }