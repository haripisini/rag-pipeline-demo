# 🚀 RAG Pipeline - Production Design

## 📌 Overview

This project demonstrates a scalable, production-ready RAG (Retrieval-Augmented Generation) pipeline.

It includes modern backend design patterns such as:
- Multi-tenant architecture
- Vector search using Qdrant
- Redis caching
- Async query processing
- Governance and audit logging

---

## 🏗️ Architecture

Refer to the architecture diagram:

docs/rag-architecture.png

---

## ⚙️ Features

### ✅ Core Features
- Multi-tenant data isolation
- Metadata-aware query handling
- Async multi-query pipeline
- Confidence scoring

### 🔥 Advanced Features
- Qdrant vector database (Dense embeddings)
- Semantic search using Sentence Transformers
- Redis caching for faster responses
- Governance layer (query validation & blocking)
- Audit logging (request/response tracking)

### 🚀 Optimization Features
- Query expansion (multi-query execution)
- Context enrichment (knowledge graph)
- Partial retrieval handling
- Scalable pipeline design

---

## 🧠 Tech Stack

- Backend: FastAPI
- Vector DB: Qdrant (in-memory)
- Cache: Redis
- Embeddings: Sentence Transformers
- Language: Python
- Async Processing: asyncio

---

## 📂 Project Structure

rag-pipeline-demo/

├── main.py  
├── workflow.py  
├── vector_store.py  
├── run.py  
├── README.md  
├── .gitignore  

└── docs/  
  └── rag-architecture.png  

---

## 🔄 How It Works

1. User sends query via API  
2. Governance layer validates input  
3. Query expansion creates multiple variations  
4. Vector search (Qdrant) retrieves relevant context  
5. Knowledge graph enriches context  
6. Response is generated  
7. Redis caches result for faster future access  
8. Audit logs are recorded  

---

## 🧪 API Usage

### Endpoint:
POST /query

### Sample Request:

{
  "query": "rag",
  "tenant_id": "t1",
  "role": "user"
}

### Sample Response:

{
  "tenant": "t1",
  "query": "rag",
  "output": {
    "results": [
      "RAG answer for 'rag' using context [...]"
    ],
    "confidence": 0.90
  }
}

---

## ⚡ Running Locally

### 1. Install dependencies
pip install fastapi uvicorn redis qdrant-client sentence-transformers

### 2. Start Redis
redis-server

### 3. Run application
python -m uvicorn main:app --reload

### 4. Open Swagger UI
http://127.0.0.1:8000/docs

---

## 📊 Production Capabilities

- Scalable RAG architecture  
- Efficient retrieval using dense embeddings  
- Low-latency responses via Redis caching  
- Secure and governed query handling  
- Async processing for high throughput  

---

## 🚀 Future Enhancements

- Hybrid search (Dense + Sparse retrieval)  
- Qdrant cloud deployment  
- Advanced ranking algorithms  
- Document versioning  
- Kafka-based streaming pipelines  

---

## 👨‍💻 Author

Hari Pisini

---

## ⭐ Summary

This project showcases a real-world production-ready RAG pipeline with modern backend practices.

Suitable for:
- AI-powered applications  
- Enterprise search systems  
- Knowledge assistants  
- Scalable data platforms  