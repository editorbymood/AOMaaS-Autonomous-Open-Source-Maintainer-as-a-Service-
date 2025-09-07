"""Main FastAPI application."""
from contextlib import asynccontextmanager
from datetime import datetime

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from aomass.config.settings import settings
from aomass.models.api import HealthResponse
from aomass.api.routes import router as api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup
    print(f"Starting {settings.app_name} v{settings.app_version}")
    
    # Initialize services here
    # await initialize_services()
    
    yield
    
    # Shutdown
    print("Shutting down...")
    # await cleanup_services()


def create_app() -> FastAPI:
    """Create FastAPI application."""
    app = FastAPI(
        title=settings.app_name,
        description="Autonomous Open-Source Maintainer as a Service",
        version=settings.app_version,
        debug=settings.debug,
        lifespan=lifespan,
    )
    
    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include API routes
    app.include_router(api_router, prefix="/api/v1")
    
    @app.get("/health", response_model=HealthResponse)
    async def health_check():
        """Health check endpoint."""
        return HealthResponse(
            status="healthy",
            version=settings.app_version,
            timestamp=datetime.utcnow().isoformat(),
            services={
                "api": "healthy",
                "database": "healthy",  # TODO: actual health checks
                "redis": "healthy",
                "qdrant": "healthy",
                "minio": "healthy",
            }
        )
    
    @app.exception_handler(Exception)
    async def global_exception_handler(request, exc):
        """Global exception handler."""
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error", "type": type(exc).__name__}
        )
    
    return app


# Create app instance
app = create_app()
