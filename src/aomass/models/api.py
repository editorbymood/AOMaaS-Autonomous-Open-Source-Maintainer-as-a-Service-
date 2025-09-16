"""API request and response models."""
from typing import Any, Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel, Field, HttpUrl

from .core import Language, OpportunityType, TaskStatus
from .providers import ProviderType


# Request Models
class IndexRepositoryRequest(BaseModel):
    """Request to index a repository."""
    url: HttpUrl
    provider_type: Optional[str] = None
    branch: Optional[str] = None
    force_reindex: bool = False


class MineOpportunitiesRequest(BaseModel):
    """Request to mine opportunities."""
    repository_id: UUID
    opportunity_types: List[OpportunityType] = Field(default_factory=list)
    languages: List[Language] = Field(default_factory=list)
    max_opportunities: int = Field(default=10, ge=1, le=100)


class GeneratePlanRequest(BaseModel):
    """Request to generate implementation plan."""
    opportunity_id: UUID
    preferences: Dict[str, Any] = Field(default_factory=dict)


class ImplementPlanRequest(BaseModel):
    """Request to implement a plan."""
    plan_id: UUID
    dry_run: bool = False


class CreatePRRequest(BaseModel):
    """Request to create pull request."""
    implementation_id: UUID
    title: Optional[str] = None
    description: Optional[str] = None
    draft: bool = True
    provider_type: Optional[ProviderType] = None  # If None, uses default provider


class ReviewPRRequest(BaseModel):
    """Request to review pull request."""
    pull_request_id: UUID
    reviewers: List[str] = Field(default_factory=list)  # AI agent names


# Response Models
class TaskResponse(BaseModel):
    """Generic task response."""
    task_id: str
    status: TaskStatus
    message: str = "Task submitted"


class IndexResponse(TaskResponse):
    """Repository indexing response."""
    repository_id: Optional[UUID] = None


class OpportunitiesResponse(BaseModel):
    """Opportunities mining response."""
    repository_id: UUID
    opportunities: List[Dict[str, Any]]
    total_count: int


class PlanResponse(BaseModel):
    """Plan generation response."""
    plan_id: UUID
    title: str
    description: str
    steps: List[Dict[str, Any]]
    estimated_effort: str
    risks: List[str]


class ImplementationResponse(TaskResponse):
    """Implementation response."""
    implementation_id: Optional[UUID] = None
    changes_count: Optional[int] = None


class PRResponse(BaseModel):
    """Pull request response."""
    pr_id: UUID
    provider_type: ProviderType
    provider_pr_number: Optional[str] = None
    url: Optional[str] = None
    status: str


class ReviewResponse(BaseModel):
    """Review response."""
    review_id: UUID
    provider_type: str
    provider_id: str
    provider_review_id: Optional[str] = None
    status: str
    score: float
    comments_count: int


class HealthResponse(BaseModel):
    """Health check response."""
    status: str = "healthy"
    version: str
    timestamp: str
    services: Dict[str, str] = Field(default_factory=dict)
