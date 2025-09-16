# Multi-Cloud Provider (MCP) Architecture

## Overview

The Multi-Cloud Provider (MCP) architecture enables AOMASS to work with multiple cloud-based Git providers, including GitHub, GitLab, Bitbucket, Azure DevOps, and AWS CodeCommit. This document outlines the architecture, components, and how to extend it for additional providers.

> **Note:** Our MCP architecture is distinct from GitHub's MCP Server (github-mcp-server). While GitHub's MCP Server focuses on connecting AI tools to GitHub's platform via natural language interactions, our implementation is a provider-agnostic abstraction layer that allows AOMaaS to work with multiple cloud providers through a unified programmatic API.

## Architecture Components

### Provider Abstraction Layer

The provider abstraction layer consists of:

1. **Provider Models** (`models/providers.py`)
   - `ProviderType` enum: Defines supported provider types
   - `RepositoryReference`: Provider-agnostic repository reference
   - `PullRequestReference`: Provider-agnostic pull request reference
   - `CloudProvider` abstract base class: Defines the interface for all providers

2. **Provider Factory** (`providers/factory.py`)
   - Manages provider registration and instantiation
   - Creates provider instances with appropriate configuration
   - Provides a default provider based on settings

3. **Provider Implementations**
   - `GitHubProvider` (`providers/github_provider.py`)
   - `GitLabProvider` (`providers/gitlab_provider.py`)
   - Additional providers can be added following the same pattern

### Configuration

The MCP architecture is configured in `config/settings.py` with the following settings:

```python
# Cloud Providers
default_provider: str = "github"  # Default provider to use

# GitHub Configuration
github_token: Optional[str] = None
github_app_id: Optional[str] = None
github_private_key_path: Optional[str] = None

# GitLab Configuration
gitlab_token: Optional[str] = None
gitlab_url: str = "https://gitlab.com"

# Additional provider configurations...
```

## Core Services Integration

The following services have been updated to use the provider abstraction:

1. **Indexer Service** (`services/indexer.py`)
   - Uses provider factory to get appropriate provider
   - Handles repository cloning through provider interface

2. **PR Manager Service** (`services/pr_manager.py`)
   - Creates pull requests through provider interface
   - Updates pull request status across different providers

3. **Reviewer Service** (`services/reviewer.py`)
   - Posts reviews to pull requests through provider interface
   - Handles provider-specific review formats

## API Integration

The API has been updated to support MCP operations:

1. **API Models** (`models/api.py`)
   - `IndexRepositoryRequest` includes `provider_type` field
   - `PRResponse` and `ReviewResponse` use provider-agnostic fields

2. **API Routes** (`api/routes.py`)
   - Updated to pass provider information to services

## Data Models

Core data models have been updated to support MCP:

1. **Repository Model** (`models/core.py`)
   - Added `provider_type` and `provider_id` fields

2. **PullRequest Model** (`models/core.py`)
   - Replaced GitHub-specific fields with provider-agnostic fields
   - Added `provider_type`, `provider_id`, and `provider_pr_id`

## Adding a New Provider

To add a new provider:

1. **Create Provider Implementation**
   - Create a new file in `providers/` directory (e.g., `bitbucket_provider.py`)
   - Implement the `CloudProvider` abstract base class
   - Implement all required methods

2. **Update Provider Factory**
   - Register the new provider in `ProviderFactory._providers`
   - Add initialization logic in `get_provider` method

3. **Update Settings**
   - Add configuration options in `config/settings.py`

## Usage Examples

### Indexing a Repository

```python
from aomass.models.providers import ProviderType
from aomass.services.indexer import IndexerService

indexer = IndexerService()
await indexer.index_repository(
    url="https://github.com/owner/repo",
    provider_type=ProviderType.GITHUB,
    branch="main"
)
```

### Creating a Pull Request

```python
from aomass.models.providers import ProviderType
from aomass.services.pr_manager import PRManagerService

pr_manager = PRManagerService()
await pr_manager.create_pull_request(
    implementation_id=implementation_id,
    title="Fix security vulnerability",
    description="This PR fixes a security vulnerability in the authentication system.",
    provider_type=ProviderType.GITLAB
)
```

## Testing

Each provider implementation should be tested with:

1. Unit tests for provider-specific logic
2. Integration tests for end-to-end workflows
3. Mock tests for API interactions

See the test directory for examples.