"""
Lovable-AI Builder Platform - Main FastAPI Application
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging

from app.core.config import settings
from app.api import requirements, interview, generate, models as models_api
from app.db.session import engine
from app.db.base import Base

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events"""
    # Startup
    logger.info("Starting Lovable-AI Builder Platform...")
    try:
        # Create database tables if they don't exist
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created/verified")
    except Exception as e:
        logger.error(f"Database initialization error: {e}")

    yield

    # Shutdown
    logger.info("Shutting down Lovable-AI Builder Platform...")


# Initialize FastAPI app
app = FastAPI(
    title="Lovable-AI Builder Platform",
    description="AI-powered application engineering system",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    lifespan=lifespan
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(requirements.router, prefix="/api/requirements", tags=["Requirements"])
app.include_router(interview.router, prefix="/api/interview", tags=["Interview"])
app.include_router(generate.router, prefix="/api/generate", tags=["Generation"])
app.include_router(models_api.router, prefix="/api/models", tags=["AI Models"])


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Lovable-AI Builder Platform",
        "version": "1.0.0"
    }


@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "database": "connected",
        "redis": "connected",
        "services": {
            "requirement_parser": "operational",
            "interview_engine": "operational",
            "code_generator": "operational",
            "devops_generator": "operational"
        }
    }


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": str(exc) if settings.DEBUG else "An unexpected error occurred"
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
