"""Provider factory for MCP architecture."""
from typing import Dict, Optional, Type

from ..config.settings import settings
from ..models.providers import CloudProvider, ProviderType
from .github_provider import GitHubProvider
from .gitlab_provider import GitLabProvider
from ..utils.logging import get_logger

logger = get_logger(__name__)


class ProviderFactory:
    """Factory for creating and managing cloud providers."""
    
    _providers: Dict[ProviderType, Type[CloudProvider]] = {
        ProviderType.GITHUB: GitHubProvider,
        ProviderType.GITLAB: GitLabProvider,
    }
    
    _instances: Dict[ProviderType, CloudProvider] = {}
    
    @classmethod
    def register_provider(cls, provider_type: ProviderType, provider_class: Type[CloudProvider]) -> None:
        """Register a new provider type."""
        cls._providers[provider_type] = provider_class
        logger.info(f"Registered provider: {provider_type}")
    
    @classmethod
    def get_provider(cls, provider_type: ProviderType) -> Optional[CloudProvider]:
        """Get or create a provider instance."""
        if provider_type not in cls._providers:
            logger.error(f"Provider type not supported: {provider_type}")
            return None
        
        if provider_type not in cls._instances:
            provider_class = cls._providers[provider_type]
            
            if provider_type == ProviderType.GITHUB:
                cls._instances[provider_type] = provider_class(
                    token=settings.github_token,
                    app_id=settings.github_app_id,
                    private_key_path=settings.github_private_key_path
                )
            elif provider_type == ProviderType.GITLAB:
                cls._instances[provider_type] = provider_class(
                    token=settings.gitlab_token,
                    url=settings.gitlab_url
                )
            # Add other provider initializations here
            
            logger.info(f"Created provider instance: {provider_type}")
        
        return cls._instances[provider_type]
    
    @classmethod
    def get_default_provider(cls) -> Optional[CloudProvider]:
        """Get the default provider (GitHub)."""
        return cls.get_provider(ProviderType.GITHUB)