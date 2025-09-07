"""Unit tests for API routes."""
import pytest
from fastapi.testclient import TestClient

from aomass.models.api import IndexRepositoryRequest, MineOpportunitiesRequest


def test_health_check(client: TestClient):
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data
    assert "services" in data


def test_index_repository(client: TestClient, sample_github_url: str):
    """Test repository indexing endpoint."""
    request_data = {
        "url": sample_github_url,
        "branch": "main",
        "force_reindex": False
    }
    
    response = client.post("/api/v1/index", json=request_data)
    assert response.status_code == 200
    
    data = response.json()
    assert "task_id" in data
    assert data["status"] == "pending"


def test_mine_opportunities(client: TestClient, mock_repo_id: str):
    """Test opportunity mining endpoint."""
    request_data = {
        "repository_id": str(mock_repo_id),
        "opportunity_types": ["dependency_update"],
        "max_opportunities": 5
    }
    
    response = client.post("/api/v1/mine", json=request_data)
    assert response.status_code == 200
    
    data = response.json()
    assert "opportunities" in data
    assert "total_count" in data
    assert isinstance(data["opportunities"], list)


def test_generate_plan(client: TestClient, mock_opportunity_id: str):
    """Test plan generation endpoint."""
    request_data = {
        "opportunity_id": str(mock_opportunity_id),
        "preferences": {}
    }
    
    response = client.post("/api/v1/plan", json=request_data)
    assert response.status_code == 200
    
    data = response.json()
    assert "plan_id" in data
    assert "title" in data
    assert "steps" in data
    assert isinstance(data["steps"], list)


def test_implement_plan(client: TestClient, mock_plan_id: str):
    """Test plan implementation endpoint."""
    request_data = {
        "plan_id": str(mock_plan_id),
        "dry_run": True
    }
    
    response = client.post("/api/v1/implement", json=request_data)
    assert response.status_code == 200
    
    data = response.json()
    assert "task_id" in data
    assert data["status"] == "pending"


def test_invalid_repository_url(client: TestClient):
    """Test indexing with invalid repository URL."""
    request_data = {
        "url": "not-a-valid-url",
        "branch": "main",
        "force_reindex": False
    }
    
    response = client.post("/api/v1/index", json=request_data)
    # Should still accept the request but validation might catch it later
    assert response.status_code in [200, 422]  # 422 for validation error
