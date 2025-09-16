"""Core data models for AOMaaS."""
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Union
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from .providers import ProviderType


class TaskStatus(str, Enum):
    """Task execution status."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class OpportunityType(str, Enum):
    """Types of maintenance opportunities."""
    DEPENDENCY_UPDATE = "dependency_update"
    SECURITY_VULNERABILITY = "security_vulnerability"
    API_MIGRATION = "api_migration"
    CODE_OPTIMIZATION = "code_optimization"
    TEST_COVERAGE = "test_coverage"
    DOCUMENTATION = "documentation"


class Language(str, Enum):
    """Supported programming languages."""
    PYTHON = "python"
    JAVASCRIPT = "javascript"
    TYPESCRIPT = "typescript"
    RUST = "rust"
    GO = "go"
    JAVA = "java"


class Repository(BaseModel):
    """Repository model."""
    id: UUID = Field(default_factory=uuid4)
    owner: str
    name: str
    full_name: str
    url: str
    default_branch: str = "main"
    languages: List[Language] = Field(default_factory=list)
    provider_type: str = ProviderType.GITHUB.value
    provider_id: str = "github"
    provider_specific_data: Dict[str, Any] = Field(default_factory=dict)
    indexed_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class CodeFile(BaseModel):
    """Code file model."""
    id: UUID = Field(default_factory=uuid4)
    repository_id: UUID
    path: str
    language: Language
    content_hash: str
    size: int
    last_modified: datetime
    analyzed_at: Optional[datetime] = None


class Opportunity(BaseModel):
    """Maintenance opportunity model."""
    id: UUID = Field(default_factory=uuid4)
    repository_id: UUID
    type: OpportunityType
    title: str
    description: str
    priority: int = Field(ge=1, le=10)  # 1 = highest, 10 = lowest
    confidence: float = Field(ge=0.0, le=1.0)
    files_affected: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Plan(BaseModel):
    """Implementation plan model."""
    id: UUID = Field(default_factory=uuid4)
    opportunity_id: UUID
    title: str
    description: str
    steps: List[Dict[str, Any]] = Field(default_factory=list)
    estimated_effort: str  # e.g., "low", "medium", "high"
    risks: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Implementation(BaseModel):
    """Implementation result model."""
    id: UUID = Field(default_factory=uuid4)
    plan_id: UUID
    status: TaskStatus = TaskStatus.PENDING
    changes: List[Dict[str, Any]] = Field(default_factory=list)
    tests_passed: Optional[bool] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None


class PullRequest(BaseModel):
    """Pull request model."""
    id: UUID = Field(default_factory=uuid4)
    implementation_id: UUID
    repository_id: UUID
    provider_type: str = ProviderType.GITHUB.value
    provider_id: str = "github"
    provider_pr_id: str
    number: Optional[int] = None
    title: str
    description: str
    branch_name: str
    status: str
    url: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class Review(BaseModel):
    """Code review model."""
    id: UUID = Field(default_factory=uuid4)
    pull_request_id: UUID
    reviewer_id: str
    status: str
    comments: List[Dict[str, Any]] = Field(default_factory=list)
    provider_type: str = ProviderType.GITHUB.value
    provider_id: str = "github"
    provider_review_id: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


# Old PullRequest model replaced by the new one above


class Review(BaseModel):
    """Code review model."""
    id: UUID = Field(default_factory=uuid4)
    pull_request_id: UUID
    reviewer: str  # AI agent name
    status: str  # approved, changes_requested, commented
    comments: List[Dict[str, Any]] = Field(default_factory=list)
    score: float = Field(ge=0.0, le=10.0)
    created_at: datetime = Field(default_factory=datetime.utcnow)
