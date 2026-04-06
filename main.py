from fastapi import FastAPI
from pydantic import BaseModel
from workflow import multi_query_pipeline

app = FastAPI()

# Request model
class QueryRequest(BaseModel):
    query: str
    tenant_id: str
    role: str

# Dummy audit log
def audit_log(request):
    print(f"Audit log: {request.query}")

# Dummy tenant filter
def filter_by_tenant(query, tenant_id):
    return []

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