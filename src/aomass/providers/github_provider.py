"""GitHub provider implementation for MCP architecture."""
import os
from pathlib import Path
from typing import Optional

from github import Github
from github.Repository import Repository as GithubRepository
from github.PullRequest import PullRequest as GithubPullRequest

from ..config.settings import settings
from ..models.providers import (
    CloudProvider,
    ProviderType,
    RepositoryReference,
    PullRequestReference
)
from ..utils.logging import get_logger

logger = get_logger(__name__)


class GitHubProvider(CloudProvider):
    """GitHub provider implementation."""
    
    def __init__(self, token: Optional[str] = None, app_id: Optional[str] = None, private_key_path: Optional[str] = None):
        """Initialize GitHub provider with authentication."""
        self.github = None
        self.token = token or settings.github_token
        self.app_id = app_id or settings.github_app_id
        self.private_key_path = private_key_path or settings.github_private_key_path
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize GitHub client with authentication."""
        if self.token:
            self.github = Github(self.token)
            logger.info("GitHub client initialized with token")
        elif self.app_id and self.private_key_path:
            # TODO: Implement GitHub App authentication
            logger.info("GitHub App authentication not implemented yet")
        else:
            logger.warning("No GitHub authentication configured")
    
    async def get_repository(self, owner: str, repo: str) -> Optional[RepositoryReference]:
        """Get repository by owner/name."""
        if not self.github:
            logger.error("GitHub client not initialized")
            return None
        
        try:
            github_repo = self.github.get_repo(f"{owner}/{repo}")
            return RepositoryReference(
                provider_type=ProviderType.GITHUB,
                provider_id="github",
                repository_id=str(github_repo.id),
                full_name=github_repo.full_name,
                url=github_repo.html_url,
                default_branch=github_repo.default_branch
            )
        except Exception as e:
            logger.error(f"Failed to get repository {owner}/{repo}", error=str(e))
            return None
    
    async def clone_repository(self, repo_ref: RepositoryReference, target_dir: str, branch: str = None) -> str:
        """Clone repository to target directory."""
        import git
        
        target_path = Path(target_dir)
        target_path.mkdir(parents=True, exist_ok=True)
        
        clone_url = repo_ref.url
        if self.token:
            # Add token to URL for authentication
            parsed_url = clone_url.split("//")
            clone_url = f"{parsed_url[0]}//oauth2:{self.token}@{parsed_url[1]}"
        
        try:
            repo = git.Repo.clone_from(
                clone_url,
                target_path,
                branch=branch or repo_ref.default_branch
            )
            logger.info(f"Cloned repository {repo_ref.full_name} to {target_dir}")
            return str(target_path)
        except Exception as e:
            logger.error(f"Failed to clone repository {repo_ref.full_name}", error=str(e))
            raise
    
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
        if not self.github:
            logger.error("GitHub client not initialized")
            return None
        
        try:
            github_repo = self.github.get_repo(repo_ref.full_name)
            pr = github_repo.create_pull(
                title=title,
                body=description,
                head=source_branch,
                base=target_branch,
                draft=draft
            )
            
            return PullRequestReference(
                provider_type=ProviderType.GITHUB,
                provider_id="github",
                repository_id=str(github_repo.id),
                pr_id=str(pr.id),
                number=pr.number,
                title=pr.title,
                description=pr.body,
                branch_name=source_branch,
                status="draft" if draft else "open",
                url=pr.html_url
            )
        except Exception as e:
            logger.error(f"Failed to create pull request for {repo_ref.full_name}", error=str(e))
            return None
    
    async def add_review_comment(
        self,
        pr_ref: PullRequestReference,
        comment: str,
        path: Optional[str] = None,
        line: Optional[int] = None
    ) -> bool:
        """Add a review comment to a pull request."""
        if not self.github:
            logger.error("GitHub client not initialized")
            return False
        
        try:
            github_repo = self.github.get_repo(pr_ref.repository_id)
            pr = github_repo.get_pull(pr_ref.number)
            
            if path and line:
                # Add a comment to a specific line
                pr.create_review_comment(body=comment, path=path, line=line)
            else:
                # Add a general comment
                pr.create_issue_comment(comment)
            
            return True
        except Exception as e:
            logger.error(f"Failed to add review comment to PR #{pr_ref.number}", error=str(e))
            return False
    
    async def update_pull_request_status(
        self,
        pr_ref: PullRequestReference,
        status: str
    ) -> bool:
        """Update pull request status."""
        if not self.github:
            logger.error("GitHub client not initialized")
            return False
        
        try:
            github_repo = self.github.get_repo(pr_ref.repository_id)
            pr = github_repo.get_pull(pr_ref.number)
            
            if status.lower() == "closed":
                pr.edit(state="closed")
            elif status.lower() == "open":
                pr.edit(state="open")
            elif status.lower() == "merged" and pr.mergeable:
                pr.merge()
            else:
                logger.warning(f"Unsupported PR status: {status}")
                return False
            
            return True
        except Exception as e:
            logger.error(f"Failed to update PR #{pr_ref.number} status", error=str(e))
            return False
            
    async def post_review(
        self,
        repo_id: str,
        pr_id: str,
        review: object
    ) -> bool:
        """Post a review to a pull request."""
        if not self.github:
            logger.error("GitHub client not initialized")
            return False
        
        try:
            # Parse the repository ID (owner/repo format)
            owner_repo = repo_id
            if '/' not in owner_repo:
                logger.error(f"Invalid repository ID format: {repo_id}")
                return False
                
            # Get the GitHub repository
            github_repo = self.github.get_repo(owner_repo)
            
            # Get the pull request (convert PR ID to number if needed)
            try:
                pr_number = int(pr_id)
            except ValueError:
                logger.error(f"Invalid PR ID format: {pr_id}")
                return False
                
            pr = github_repo.get_pull(pr_number)
            
            # Create a review with comments
            comments = []
            for comment in review.comments:
                if 'file' in comment and 'line' in comment:
                    comments.append({
                        'path': comment['file'],
                        'position': comment['line'],
                        'body': f"[{comment['agent']}] {comment['comment']} (Severity: {comment['severity']})"
                    })
            
            # Determine review state based on status
            review_state = "COMMENT"
            if review.status == "approved":
                review_state = "APPROVE"
            elif review.status == "changes_requested":
                review_state = "REQUEST_CHANGES"
            
            # Submit the review
            pr.create_review(
                body=f"AI Review - Score: {review.score:.1f}/10",
                event=review_state,
                comments=comments
            )
            
            return True
        except Exception as e:
            logger.error(f"Failed to post review to PR #{pr_id}", error=str(e))
            return False