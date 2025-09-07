"""GitHub integration utilities."""
from typing import Optional, Dict, Any
import os
from pathlib import Path

from github import Github
from github.Repository import Repository as GithubRepository
from github.PullRequest import PullRequest as GithubPullRequest

from aomass.config.settings import settings
from aomass.utils.logging import get_logger

logger = get_logger(__name__)


class GitHubClient:
    """GitHub API client wrapper."""
    
    def __init__(self):
        self.github = None
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize GitHub client with authentication."""
        if settings.github_token:
            self.github = Github(settings.github_token)
            logger.info("GitHub client initialized with token")
        elif settings.github_app_id and settings.github_private_key_path:
            # TODO: Implement GitHub App authentication
            logger.info("GitHub App authentication not implemented yet")
        else:
            logger.warning("No GitHub authentication configured")
    
    def get_repository(self, owner: str, repo: str) -> Optional[GithubRepository]:
        """Get repository by owner/name."""
        if not self.github:
            logger.error("GitHub client not initialized")
            return None
        
        try:
            return self.github.get_repo(f"{owner}/{repo}")
        except Exception as e:
            logger.error(f"Failed to get repository {owner}/{repo}", error=str(e))
            return None
    
    def create_pull_request(
        self,
        repo: GithubRepository,
        title: str,
        body: str,
        head_branch: str,
        base_branch: str = "main",
        draft: bool = True
    ) -> Optional[GithubPullRequest]:
        """Create a pull request."""
        try:
            pr = repo.create_pull(
                title=title,
                body=body,
                head=head_branch,
                base=base_branch,
                draft=draft
            )
            logger.info(f"Created PR #{pr.number}: {title}")
            return pr
        except Exception as e:
            logger.error(f"Failed to create PR", error=str(e))
            return None
    
    def create_branch(
        self, 
        repo: GithubRepository, 
        branch_name: str, 
        source_branch: str = "main"
    ) -> bool:
        """Create a new branch."""
        try:
            source_sha = repo.get_branch(source_branch).commit.sha
            repo.create_git_ref(ref=f"refs/heads/{branch_name}", sha=source_sha)
            logger.info(f"Created branch {branch_name}")
            return True
        except Exception as e:
            logger.error(f"Failed to create branch {branch_name}", error=str(e))
            return False
    
    def update_file(
        self,
        repo: GithubRepository,
        file_path: str,
        content: str,
        commit_message: str,
        branch: str
    ) -> bool:
        """Update a file in the repository."""
        try:
            # Check if file exists
            try:
                file_content = repo.get_contents(file_path, ref=branch)
                # Update existing file
                repo.update_file(
                    path=file_path,
                    message=commit_message,
                    content=content,
                    sha=file_content.sha,
                    branch=branch
                )
            except:
                # Create new file
                repo.create_file(
                    path=file_path,
                    message=commit_message,
                    content=content,
                    branch=branch
                )
            
            logger.info(f"Updated file {file_path} in branch {branch}")
            return True
        except Exception as e:
            logger.error(f"Failed to update file {file_path}", error=str(e))
            return False
    
    def add_pr_comment(self, pr: GithubPullRequest, comment: str) -> bool:
        """Add a comment to a pull request."""
        try:
            pr.create_issue_comment(comment)
            logger.info(f"Added comment to PR #{pr.number}")
            return True
        except Exception as e:
            logger.error(f"Failed to add PR comment", error=str(e))
            return False
    
    def request_review(self, pr: GithubPullRequest, reviewers: list) -> bool:
        """Request review from users."""
        try:
            pr.create_review_request(reviewers=reviewers)
            logger.info(f"Requested review from {reviewers}")
            return True
        except Exception as e:
            logger.error(f"Failed to request review", error=str(e))
            return False


# Global GitHub client instance
github_client = GitHubClient()
