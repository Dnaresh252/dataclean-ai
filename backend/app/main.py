"""
Main FastAPI application entry point.
This is where our API starts.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from app.api.routes import clean, auth  # Add auth
# Import routes (FIXED PATH)
from app.api.routes import clean

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app instance
app = FastAPI(
    title="DataClean.AI API",
    description="AI-powered data cleaning service",
    version="0.1.0"
)

# CORS middleware (allow frontend to make requests)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: Restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(clean.router, prefix="/api/v1", tags=["cleaning"])
app.include_router(auth.router, prefix="/api/v1/auth", tags=["authentication"]) 
@app.get("/")
def read_root():
    """
    Root endpoint - API info.
    """
    return {
        "message": "DataClean.AI API is running!",
        "version": "0.1.0",
        "status": "healthy",
        "docs": "/docs",
        "endpoints": {
            "analyze": "/api/v1/analyze",
            "clean": "/api/v1/clean",
            "health": "/api/v1/health"
        }
    }

@app.on_event("startup")
async def startup_event():
    """
    Run on application startup.
    Load ML models here.
    """
    logger.info("🚀 Starting DataClean.AI API...")
    
    # ML models are loaded when ml_service is first imported
    # This happens automatically in clean.py
    
    logger.info("✅ API started successfully!")

@app.on_event("shutdown")
async def shutdown_event():
    """
    Run on application shutdown.
    Cleanup resources.
    """
    logger.info("👋 Shutting down DataClean.AI API...")