import time
import json
import logging
from fastapi import FastAPI, Request
from ikea_recommender.app.api.v1.recommendation import router as recommendation_router
from ikea_recommender.app.api.v1.feedback import router as feedback_router
from ikea_recommender.app.core.config import settings

# Configure Structured Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ikea_recommender")

import uuid

# Configure Structured Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ikea_recommender")

app = FastAPI(title=settings.PROJECT_NAME, version="1.0.0")

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    # Distributed Tracing: Assign a unique ID to every request
    request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
    
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Process-Time"] = str(process_time)
    
    log_data = {
        "request_id": request_id,
        "method": request.method,
        "path": request.url.path,
        "status_code": response.status_code,
        "duration_ms": round(process_time * 1000, 2),
    }
    logger.info(json.dumps(log_data))
    return response

# Health & Readiness Probes
@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "healthy", "timestamp": time.time()}

@app.get("/ready", tags=["Health"])
def readiness_check():
    return {"status": "ready"}

@app.get("/")
async def root():
    return {
        "message": f"{settings.PROJECT_NAME} Semantic Recommender API",
        "version": "1.0.0",
        "features": [
            "Vector Search (Vertex AI)", 
            "Cross-Encoder Reranking", 
            "Knowledge Graph Hybrid retrieval", 
            "RL Feedback Loop"
        ],
        "compliance": "Ingka Elite Standard"
    }

# Include routers
app.include_router(recommendation_router, prefix=settings.API_V1_STR)
app.include_router(feedback_router, prefix=settings.API_V1_STR)
