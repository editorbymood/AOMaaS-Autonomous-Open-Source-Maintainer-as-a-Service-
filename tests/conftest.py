"""Pytest configuration and fixtures."""
import pytest
import asyncio
from pathlib import Path
from uuid import uuid4

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from aomass.api.main import app
from aomass.config.settings import settings


@pytest.fixture
def client():
    """FastAPI test client."""
    return TestClient(app)


@pytest.fixture
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def mock_repo_id():
    """Mock repository ID for tests."""
    return uuid4()


@pytest.fixture
def mock_opportunity_id():
    """Mock opportunity ID for tests."""
    return uuid4()


@pytest.fixture
def mock_plan_id():
    """Mock plan ID for tests."""
    return uuid4()


@pytest.fixture
def sample_github_url():
    """Sample GitHub repository URL."""
    return "https://github.com/octocat/Hello-World"


@pytest.fixture
def temp_repo_dir(tmp_path):
    """Temporary directory for repository cloning."""
    repo_dir = tmp_path / "test_repo"
    repo_dir.mkdir()
    return repo_dir
