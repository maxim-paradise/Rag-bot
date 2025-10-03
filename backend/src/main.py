"""
Main FastAPI application for ML/AI Backend
Minimal working version
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
try:
    from api.rag_api import router as rag_router
    RAG_AVAILABLE = True
except ImportError:
    RAG_AVAILABLE = False

# Import configuration
try:
    from config.settings import settings
except ImportError:
    # Fallback settings
    class Settings:
        API_HOST = "0.0.0.0"
        API_PORT = 8000
        DEBUG = True
        ENVIRONMENT = "development"
    settings = Settings()

# Import API routers
try:
    from api.sentiment_analysis import router as sentiment_router
    SENTIMENT_AVAILABLE = True
except ImportError:
    SENTIMENT_AVAILABLE = False

# Create FastAPI app
app = FastAPI(
    title="ML/AI Backend Platform",
    description="Minimal ML Backend",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if RAG_AVAILABLE:
    app.include_router(rag_router, prefix="/api/rag", tags=["RAG System"])

# Include API routers
if SENTIMENT_AVAILABLE:
    app.include_router(sentiment_router, prefix="/api/sentiment", tags=["Sentiment Analysis"])

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "ML/AI Backend Platform",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "environment": getattr(settings, 'ENVIRONMENT', 'development'),
        "backend": "active"
    }

@app.get("/api/test")
async def test_endpoint():
    """Simple test endpoint"""
    return {"message": "API работает!", "test": "success"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )