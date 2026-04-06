from fastapi import FastAPI
from pydantic import BaseModel
from workflow import multi_query_pipeline

app = FastAPI()

# -------------------------------
# 🔹 Request Model
# -------------------------------
class QueryRequest(BaseModel):
    query: str
    tenant_id: str
    role: str


# -------------------------------
# 🔹 Governance Layer
# -------------------------------
def governance_check(query):
    blocked_words = ["hack", "illegal", "attack"]

    for word in blocked_words:
        if word in query.lower():
            return False

    return True


# -------------------------------
# 🔹 Audit Logging
# -------------------------------
def audit_log(request, response):
    log = {
        "query": request.query,
        "tenant": request.tenant_id,
        "response": response,
        "status": "success"
    }

    print("AUDIT LOG:", log)


# -------------------------------
# 🔹 API Endpoint
# -------------------------------
@app.post("/query")
async def query_api(request: QueryRequest):

    # ✅ Governance Check
    if not governance_check(request.query):
        return {
            "error": "Query not allowed (governance blocked)"
        }

    # ✅ Run pipeline (with tenant)
    results = await multi_query_pipeline(request.query, request.tenant_id)
    result = results[0]

    response = {
        "tenant": request.tenant_id,
        "query": request.query,
        "output": result
    }

    # ✅ Audit logging
    audit_log(request, response)

    return response