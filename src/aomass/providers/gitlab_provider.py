"""GitLab provider implementation for MCP architecture."""
import os
from pathlib import Path
from typing import Optional

import gitlab
from gitlab.v4.objects import Project as GitlabProject
from gitlab.v4.objects import ProjectMergeRequest as GitlabMergeRequest

from ..config.settings import settings
from ..models.providers import (
    CloudProvider,
    ProviderType,
    RepositoryReference,
    PullRequestReference
)
from ..utils.logging import get_logger

logger = get_logger(__name__)


class GitLabProvider(CloudProvider):
    """GitLab provider implementation."""
    
    def __init__(self, token: Optional[str] = None, url: Optional[str] = None):
        """Initialize GitLab provider with authentication."""
        self.gitlab = None
        self.token = token or settings.gitlab_token
        self.url = url or settings.gitlab_url
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize GitLab client with authentication."""
        if self.token and self.url:
            try:
                self.gitlab = gitlab.Gitlab(url=self.url, private_token=self.token)
                self.gitlab.auth()
                logger.info("GitLab client initialized with token")
            except Exception as e:
                logger.error(f"Failed to initialize GitLab client: {str(e)}")
        else:
            logger.warning("No GitLab authentication configured")
    
    async def get_repository(self, owner: str, repo: str) -> Optional[RepositoryReference]:
        """Get repository by owner/name."""
        if not self.gitlab:
            logger.error("GitLab client not initialized")
            return None
        
        try:
            # In GitLab, the full path is owner/repo
            full_path = f"{owner}/{repo}"
            gitlab_project = self.gitlab.projects.get(full_path)
            
            return RepositoryReference(
                provider_type=ProviderType.GITLAB,
                provider_id="gitlab",
                repository_id=str(gitlab_project.id),
                full_name=gitlab_project.path_with_namespace,
                url=gitlab_project.web_url,
                default_branch=gitlab_project.default_branch
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
        """Create a merge request (GitLab's equivalent of a pull request)."""
        if not self.gitlab:
            logger.error("GitLab client not initialized")
            return None
        
        try:
            # Get the GitLab project
            gitlab_project = self.gitlab.projects.get(repo_ref.repository_id)
            
            # Create the merge request
            mr = gitlab_project.mergerequests.create({
                'title': title,
                'description': description,
                'source_branch': source_branch,
                'target_branch': target_branch,
                'work_in_progress': draft  # GitLab uses work_in_progress for draft MRs
            })
            
            return PullRequestReference(
                provider_type=ProviderType.GITLAB,
                provider_id="gitlab",
                repository_id=str(gitlab_project.id),
                pr_id=str(mr.id),
                number=mr.iid,  # GitLab uses iid for user-facing MR numbers
                title=mr.title,
                description=mr.description,
                branch_name=source_branch,
                status="draft" if draft else "open",
                url=mr.web_url
            )
        except Exception as e:
            logger.error(f"Failed to create merge request for {repo_ref.full_name}", error=str(e))
            return None
    
    async def add_review_comment(
        self,
        pr_ref: PullRequestReference,
        comment: str,
        path: Optional[str] = None,
        line: Optional[int] = None
    ) -> bool:
        """Add a review comment to a merge request."""
        if not self.gitlab:
            logger.error("GitLab client not initialized")
            return False
        
        try:
            # Get the GitLab project and merge request
            gitlab_project = self.gitlab.projects.get(pr_ref.repository_id)
            mr = gitlab_project.mergerequests.get(pr_ref.number)
            
            if path and line:
                # Add a comment to a specific line in a file
                # GitLab requires position data for line comments
                # This is a simplified implementation
                mr.discussions.create({
                    'body': comment,
                    'position': {
                        'base_sha': mr.diff_refs['base_sha'],
                        'head_sha': mr.diff_refs['head_sha'],
                        'start_sha': mr.diff_refs['start_sha'],
                        'position_type': 'text',
                        'new_path': path,
                        'new_line': line
                    }
                })
            else:
                # Add a general comment
                mr.notes.create({'body': comment})
            
            return True
        except Exception as e:
            logger.error(f"Failed to add review comment to MR #{pr_ref.number}", error=str(e))
            return False
    
    async def update_pull_request_status(
        self,
        pr_ref: PullRequestReference,
        status: str
    ) -> bool:
        """Update merge request status."""
        if not self.gitlab:
            logger.error("GitLab client not initialized")
            return False
        
        try:
            # Get the GitLab project and merge request
            gitlab_project = self.gitlab.projects.get(pr_ref.repository_id)
            mr = gitlab_project.mergerequests.get(pr_ref.number)
            
            if status.lower() == "closed":
                mr.state_event = 'close'
                mr.save()
            elif status.lower() == "open":
                mr.state_event = 'reopen'
                mr.save()
            elif status.lower() == "merged" and mr.merge_status == 'can_be_merged':
                mr.merge()
            else:
                logger.warning(f"Unsupported MR status: {status}")
                return False
            
            return True
        except Exception as e:
            logger.error(f"Failed to update MR #{pr_ref.number} status", error=str(e))
            return False
            
    async def post_review(
        self,
        repo_id: str,
        pr_id: str,
        review: object
    ) -> bool:
        """Post a review to a merge request."""
        if not self.gitlab:
            logger.error("GitLab client not initialized")
            return False
        
        try:
            # Parse the repository ID (owner/repo format)
            owner_repo = repo_id
            if '/' not in owner_repo:
                logger.error(f"Invalid repository ID format: {repo_id}")
                return False
                
            # Get the GitLab project
            gitlab_project = self.gitlab.projects.get(owner_repo)
            
            # Get the merge request (convert PR ID to number if needed)
            try:
                mr_number = int(pr_id)
            except ValueError:
                logger.error(f"Invalid MR ID format: {pr_id}")
                return False
                
            mr = gitlab_project.mergerequests.get(mr_number)
            
            # Add a summary comment with the review score
            mr.notes.create({
                'body': f"AI Review - Score: {review.score:.1f}/10\n\nStatus: {review.status}"
            })
            
            # Add individual comments for each review comment
            for comment in review.comments:
                if 'file' in comment and 'line' in comment:
                    # Try to add a line comment if possible
                    try:
                        mr.discussions.create({
                            'body': f"[{comment['agent']}] {comment['comment']} (Severity: {comment['severity']})",
                            'position': {
                                'base_sha': mr.diff_refs['base_sha'],
                                'head_sha': mr.diff_refs['head_sha'],
                                'start_sha': mr.diff_refs['start_sha'],
                                'position_type': 'text',
                                'new_path': comment['file'],
                                'new_line': comment['line']
                            }
                        })
                    except Exception as line_error:
                        # Fall back to a regular comment if line comment fails
                        logger.warning(f"Failed to add line comment, falling back to regular comment: {str(line_error)}")
                        mr.notes.create({
                            'body': f"[{comment['agent']}] File: {comment['file']}, Line: {comment['line']} - {comment['comment']} (Severity: {comment['severity']})"
                        })
                else:
                    # Add a regular comment
                    mr.notes.create({
                        'body': f"[{comment['agent']}] {comment['comment']} (Severity: {comment['severity']})"
                    })
            
            # Update the merge request approval status based on the review status
            if review.status == "approved":
                # In GitLab, we can't directly approve via API without proper permissions
                # Just add a comment indicating approval
                mr.notes.create({
                    'body': "This merge request has been APPROVED by the AI review."
                })
            elif review.status == "changes_requested":
                mr.notes.create({
                    'body': "Changes have been REQUESTED by the AI review."
                })
            
            return True
        except Exception as e:
            logger.error(f"Failed to post review to MR #{pr_id}", error=str(e))
            return False