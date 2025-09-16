"""Integration tests for GitLab provider implementation."""
import asyncio
import os
import pytest
from uuid import uuid4

from aomass.models.providers import ProviderType, RepositoryReference
from aomass.providers.factory import ProviderFactory


@pytest.mark.asyncio
async def test_gitlab_provider_initialization():
    """Test GitLab provider initialization."""
    # Skip test if GitLab token is not set
    if not os.environ.get("GITLAB_TOKEN"):
        pytest.skip("GITLAB_TOKEN environment variable not set")
    
    # Get GitLab provider from factory
    provider_factory = ProviderFactory()
    gitlab_provider = provider_factory.get_provider(ProviderType.GITLAB)
    
    # Verify provider is initialized
    assert gitlab_provider is not None
    assert gitlab_provider.gitlab is not None


@pytest.mark.asyncio
async def test_get_repository():
    """Test getting repository information."""
    # Skip test if GitLab token is not set
    if not os.environ.get("GITLAB_TOKEN"):
        pytest.skip("GITLAB_TOKEN environment variable not set")
    
    # Get GitLab provider
    provider_factory = ProviderFactory()
    gitlab_provider = provider_factory.get_provider(ProviderType.GITLAB)
    
    # Get repository information for a public repository
    # Replace with an actual GitLab repository you have access to
    repo_ref = await gitlab_provider.get_repository("gitlab-org", "gitlab-runner")
    
    # Verify repository information
    assert repo_ref is not None
    assert repo_ref.provider_type == ProviderType.GITLAB
    assert repo_ref.full_name == "gitlab-org/gitlab-runner"
    assert repo_ref.url.startswith("https://gitlab.com/")
    assert repo_ref.default_branch is not None


@pytest.mark.asyncio
async def test_clone_repository():
    """Test cloning a repository."""
    # Skip test if GitLab token is not set
    if not os.environ.get("GITLAB_TOKEN"):
        pytest.skip("GITLAB_TOKEN environment variable not set")
    
    # Get GitLab provider
    provider_factory = ProviderFactory()
    gitlab_provider = provider_factory.get_provider(ProviderType.GITLAB)
    
    # Get repository information for a public repository
    repo_ref = await gitlab_provider.get_repository("gitlab-org", "gitlab-runner")
    assert repo_ref is not None
    
    # Create a temporary directory for cloning
    temp_dir = f"/tmp/aomass-test-{uuid4()}"
    
    try:
        # Clone the repository
        clone_path = await gitlab_provider.clone_repository(repo_ref, temp_dir)
        
        # Verify the repository was cloned
        assert os.path.exists(clone_path)
        assert os.path.exists(os.path.join(clone_path, ".git"))
    finally:
        # Clean up the temporary directory
        if os.path.exists(temp_dir):
            import shutil
            shutil.rmtree(temp_dir)


# Run the tests if executed directly
if __name__ == "__main__":
    asyncio.run(test_gitlab_provider_initialization())
    asyncio.run(test_get_repository())
    asyncio.run(test_clone_repository())
    print("All tests passed!")