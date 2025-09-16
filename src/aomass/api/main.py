"""Main FastAPI application."""
from contextlib import asynccontextmanager
from datetime import datetime

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import os
from pathlib import Path

# Use relative imports
from ..utils.error_handling import register_exception_handlers
from ..utils.logging import setup_logging
from ..utils.middleware import setup_middleware
from ..config.settings import settings
from ..models.api import HealthResponse
from .routes import router as api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup
    print(f"Starting {settings.app_name} v{settings.app_version}")
    
    # Initialize services here
    from ..core.services import initialize_services
    await initialize_services()
    
    yield
    
    # Shutdown
    print("Shutting down...")
    # await cleanup_services()


def create_app() -> FastAPI:
    """Create FastAPI application."""
    # Set up logging first
    setup_logging()
    
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
    
    # Static files
    project_root = Path(os.path.abspath(__file__)).parent.parent.parent.parent
    static_dir = project_root / "static"
    templates_dir = project_root / "templates"
    
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")
    templates = Jinja2Templates(directory=str(templates_dir))
    
    # Include API routes
    app.include_router(api_router, prefix="/api/v1")
    
    # Set up middleware
    setup_middleware(app)
    
    # Register exception handlers
    register_exception_handlers(app)
    
    # Root route for landing page
    @app.get("/")
    async def root(request):
        return templates.TemplateResponse("index.html", {"request": request})
        
    # Demo page route
    @app.get("/demo")
    async def demo_page(request):
        return templates.TemplateResponse("demo.html", {"request": request})
    
    @app.get("/health", response_model=HealthResponse)
    async def health_check():
        """Health check endpoint."""
        # Perform actual health checks
        services_status = {
            "api": "healthy"
        }
        
        # Add service statuses if they exist
        try:
            from ..core.services import get_services_health
            services_status.update(await get_services_health())
        except Exception as e:
            print(f"Error getting service health: {e}")
        
        return HealthResponse(
            status="healthy",
            version=settings.app_version,
            timestamp=datetime.utcnow().isoformat(),
            services=services_status
        )
    
    # Custom exception handlers are now registered through register_exception_handlers
    
    return app


# Create app instance
app = create_app()
