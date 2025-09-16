"""Cloud provider models for Multi-Cloud Provider (MCP) architecture."""
from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Dict, List, Optional, Union
from uuid import UUID

from pydantic import BaseModel, Field


class ProviderType(str, Enum):
    """Supported cloud providers."""
    GITHUB = "github"
    GITLAB = "gitlab"
    BITBUCKET = "bitbucket"
    AZURE_DEVOPS = "azure_devops"
    AWS_CODECOMMIT = "aws_codecommit"
    GENERIC_GIT = "generic_git"


class ProviderConfig(BaseModel):
    """Base configuration for cloud providers."""
    provider_type: ProviderType
    name: str
    description: Optional[str] = None
    enabled: bool = True


class RepositoryReference(BaseModel):
    """Repository reference that is provider-agnostic."""
    provider_type: ProviderType
    provider_id: str
    repository_id: str
    full_name: str
    url: str
    default_branch: str = "main"
    

class PullRequestReference(BaseModel):
    """Pull request reference that is provider-agnostic."""
    provider_type: ProviderType
    provider_id: str
    repository_id: str
    pr_id: str
    number: Optional[int] = None
    title: str
    description: str
    branch_name: str
    status: str
    url: Optional[str] = None


class CloudProvider(ABC):
    """Abstract base class for cloud providers."""
    
    @abstractmethod
    async def get_repository(self, owner: str, repo: str) -> Optional[RepositoryReference]:
        """Get repository by owner/name."""
        pass
    
    @abstractmethod
    async def clone_repository(self, repo_ref: RepositoryReference, target_dir: str, branch: str = None) -> str:
        """Clone repository to target directory."""
        pass
    
    @abstractmethod
    async def create_pull_request(
        self, 
        repo_ref: RepositoryReference,
        title: str,
        description: str,
        source_branch: str,
        target_branch: str,
        draft: bool = True
    ) -> Optional[PullRequestReference]:
        """Create a pull request."""
        pass
    
    @abstractmethod
    async def add_review_comment(
        self,
        pr_ref: PullRequestReference,
        comment: str,
        path: Optional[str] = None,
        line: Optional[int] = None
    ) -> bool:
        """Add a review comment to a pull request."""
        pass
    
    @abstractmethod
    async def update_pull_request_status(
        self,
        pr_ref: PullRequestReference,
        status: str
    ) -> bool:
        """Update pull request status."""
        pass
        
    @abstractmethod
    async def post_review(
        self,
        repo_id: str,
        pr_id: str,
        review: Any
    ) -> bool:
        """Post a review to a pull request."""
        pass