"""Integration tests for GitHub provider implementation."""
import asyncio
import os
import pytest
from uuid import uuid4

from aomass.models.providers import ProviderType, RepositoryReference
from aomass.providers.factory import ProviderFactory


@pytest.mark.asyncio
async def test_github_provider_initialization():
    """Test GitHub provider initialization."""
    # Get GitHub provider from factory
    provider_factory = ProviderFactory()
    github_provider = provider_factory.get_provider(ProviderType.GITHUB)
    
    # Verify provider is initialized
    assert github_provider is not None
    assert github_provider.github is not None


@pytest.mark.asyncio
async def test_get_repository():
    """Test getting repository information."""
    # Skip test if GitHub token is not set
    if not os.environ.get("GITHUB_TOKEN"):
        pytest.skip("GITHUB_TOKEN environment variable not set")
    
    # Get GitHub provider
    provider_factory = ProviderFactory()
    github_provider = provider_factory.get_provider(ProviderType.GITHUB)
    
    # Get repository information for a public repository
    repo_ref = await github_provider.get_repository("aomass", "aomass")
    
    # Verify repository information
    assert repo_ref is not None
    assert repo_ref.provider_type == ProviderType.GITHUB
    assert repo_ref.full_name == "aomass/aomass"
    assert repo_ref.url.startswith("https://github.com/")
    assert repo_ref.default_branch is not None


@pytest.mark.asyncio
async def test_clone_repository():
    """Test cloning a repository."""
    # Skip test if GitHub token is not set
    if not os.environ.get("GITHUB_TOKEN"):
        pytest.skip("GITHUB_TOKEN environment variable not set")
    
    # Get GitHub provider
    provider_factory = ProviderFactory()
    github_provider = provider_factory.get_provider(ProviderType.GITHUB)
    
    # Get repository information for a public repository
    repo_ref = await github_provider.get_repository("aomass", "aomass")
    assert repo_ref is not None
    
    # Create a temporary directory for cloning
    temp_dir = f"/tmp/aomass-test-{uuid4()}"
    
    try:
        # Clone the repository
        clone_path = await github_provider.clone_repository(repo_ref, temp_dir)
        
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
    asyncio.run(test_github_provider_initialization())
    asyncio.run(test_get_repository())
    asyncio.run(test_clone_repository())
    print("All tests passed!")