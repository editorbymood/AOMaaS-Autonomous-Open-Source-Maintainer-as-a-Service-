"""Simple FastAPI app for demonstration."""
from datetime import datetime
from fastapi import FastAPI

app = FastAPI(
    title="AOMaaS",
    description="Autonomous Open-Source Maintainer as a Service",
    version="0.1.0"
)

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "version": "0.1.0",
        "timestamp": datetime.utcnow().isoformat(),
        "message": "AOMaaS is running successfully! 🤖⚡"
    }

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Welcome to AOMaaS - Autonomous Open-Source Maintainer as a Service!",
        "version": "0.1.0",
        "docs": "/docs",
        "health": "/health"
    }

# Mock endpoints for demonstration
@app.post("/api/v1/index")
async def index_repository(repo_data: dict):
    """Mock repository indexing."""
    return {
        "task_id": "123e4567-e89b-12d3-a456-426614174000",
        "status": "pending",
        "message": f"Started indexing repository: {repo_data.get('url', 'unknown')}",
        "repository_id": "456e7890-e89b-12d3-a456-426614174000"
    }

@app.post("/api/v1/mine")
async def mine_opportunities(mine_data: dict):
    """Mock opportunity mining."""
    return {
        "repository_id": mine_data.get("repository_id"),
        "opportunities": [
            {
                "id": "789e0123-e89b-12d3-a456-426614174000",
                "type": "dependency_update",
                "title": "Update FastAPI to latest version",
                "description": "FastAPI 0.116.1 is available with bug fixes and performance improvements",
                "priority": 3,
                "confidence": 0.9,
                "files_affected": ["requirements.txt", "pyproject.toml"]
            },
            {
                "id": "abc1234d-e89b-12d3-a456-426614174000",
                "type": "security_vulnerability",
                "title": "Fix potential SQL injection vulnerability",
                "description": "Raw SQL query construction detected in user input handling",
                "priority": 1,
                "confidence": 0.75,
                "files_affected": ["src/database/queries.py"]
            }
        ],
        "total_count": 2
    }

@app.get("/demo")
async def demo():
    """Demo endpoint showing AOMaaS capabilities."""
    return {
        "message": "AOMaaS Demo - Autonomous Repository Maintenance",
        "capabilities": [
            "🔍 Repository Indexing & Semantic Analysis",
            "⚡ Automated Opportunity Mining", 
            "🤖 AI-Powered Implementation Planning",
            "🛠️ Automated Code Implementation",
            "📝 GitHub PR Creation & Management",
            "🔍 Multi-Agent Code Review"
        ],
        "supported_languages": ["Python", "JavaScript", "TypeScript", "Rust", "Go", "Java"],
        "opportunity_types": [
            "dependency_update",
            "security_vulnerability", 
            "api_migration",
            "code_optimization",
            "test_coverage",
            "documentation"
        ]
    }
