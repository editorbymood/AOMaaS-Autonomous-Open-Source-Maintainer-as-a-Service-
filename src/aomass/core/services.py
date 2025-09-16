"""Core services initialization and management."""
import asyncio
from typing import Dict, Any

from ..config.settings import settings
from ..providers.factory import ProviderFactory

# Global service instances
_services = {}


async def initialize_services():
    """Initialize all required services for the application."""
    global _services
    
    print("Initializing services...")
    
    # Initialize provider factory
    _services["provider_factory"] = ProviderFactory()
    
    # Initialize other services as needed
    # Example: database, cache, etc.
    
    print("Services initialized successfully")


async def get_services_health() -> Dict[str, str]:
    """Get health status of all services.
    
    Returns:
        Dict[str, str]: Dictionary of service names and their health status.
    """
    health_statuses = {}
    
    # Check provider factory health
    if "provider_factory" in _services:
        health_statuses["provider_factory"] = "healthy"
    
    # Add other service health checks as needed
    # Example: database, cache, etc.
    
    return health_statuses


def get_service(service_name: str) -> Any:
    """Get a service instance by name.
    
    Args:
        service_name: Name of the service to retrieve.
        
    Returns:
        Any: The service instance.
        
    Raises:
        KeyError: If the service is not found.
    """
    if service_name not in _services:
        raise KeyError(f"Service '{service_name}' not found")
    
    return _services[service_name]


def get_provider_factory() -> ProviderFactory:
    """Get the provider factory instance.
    
    Returns:
        ProviderFactory: The provider factory instance.
        
    Raises:
        RuntimeError: If the provider factory is not initialized.
    """
    try:
        return get_service("provider_factory")
    except KeyError:
        raise RuntimeError("Provider factory not initialized")