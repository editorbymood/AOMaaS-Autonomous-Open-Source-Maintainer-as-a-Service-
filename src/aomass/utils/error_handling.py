"""Error handling utilities for AOMaaS."""
from typing import Any, Dict, List, Optional, Type, Union

from fastapi import HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from .logging import get_logger

logger = get_logger(__name__)


class AOMaaSError(Exception):
    """Base exception class for AOMaaS."""
    
    def __init__(
        self, 
        message: str, 
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        error_code: str = "internal_error",
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        self.details = details or {}
        super().__init__(self.message)


class ResourceNotFoundError(AOMaaSError):
    """Exception raised when a requested resource is not found."""
    
    def __init__(self, resource_type: str, resource_id: str, details: Optional[Dict[str, Any]] = None):
        message = f"{resource_type} with ID {resource_id} not found"
        super().__init__(
            message=message,
            status_code=status.HTTP_404_NOT_FOUND,
            error_code="resource_not_found",
            details=details or {"resource_type": resource_type, "resource_id": resource_id}
        )


class ValidationFailedError(AOMaaSError):
    """Exception raised when validation fails."""
    
    def __init__(self, message: str, validation_errors: List[Dict[str, Any]]):
        super().__init__(
            message=message,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            error_code="validation_failed",
            details={"validation_errors": validation_errors}
        )


class AuthenticationError(AOMaaSError):
    """Exception raised when authentication fails."""
    
    def __init__(self, message: str = "Authentication failed", details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            status_code=status.HTTP_401_UNAUTHORIZED,
            error_code="authentication_failed",
            details=details
        )


class AuthorizationError(AOMaaSError):
    """Exception raised when authorization fails."""
    
    def __init__(self, message: str = "Not authorized to perform this action", details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            status_code=status.HTTP_403_FORBIDDEN,
            error_code="authorization_failed",
            details=details
        )


class RateLimitExceededError(AOMaaSError):
    """Exception raised when rate limit is exceeded."""
    
    def __init__(self, message: str = "Rate limit exceeded", retry_after: int = 60, details: Optional[Dict[str, Any]] = None):
        details = details or {}
        details["retry_after"] = retry_after
        super().__init__(
            message=message,
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            error_code="rate_limit_exceeded",
            details=details
        )


class ExternalServiceError(AOMaaSError):
    """Exception raised when an external service fails."""
    
    def __init__(self, service_name: str, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=f"Error from external service {service_name}: {message}",
            status_code=status.HTTP_502_BAD_GATEWAY,
            error_code="external_service_error",
            details=details or {"service_name": service_name}
        )


class TaskError(AOMaaSError):
    """Exception raised when a task fails."""
    
    def __init__(self, task_id: str, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error_code="task_error",
            details=details or {"task_id": task_id}
        )


def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """Handle HTTPException and return a standardized JSON response."""
    logger.warning(
        "HTTP exception", 
        status_code=exc.status_code, 
        detail=exc.detail,
        headers=exc.headers,
        path=request.url.path
    )
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail,
            "type": "http_exception",
            "status_code": exc.status_code
        },
        headers=exc.headers
    )


def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """Handle RequestValidationError and return a standardized JSON response."""
    errors = []
    for error in exc.errors():
        error_info = {
            "loc": error["loc"],
            "msg": error["msg"],
            "type": error["type"]
        }
        errors.append(error_info)
    
    logger.warning(
        "Validation error", 
        errors=errors,
        path=request.url.path,
        body=request.state.body if hasattr(request.state, "body") else None
    )
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": "Validation error",
            "type": "validation_error",
            "errors": errors
        }
    )


def aomass_exception_handler(request: Request, exc: AOMaaSError) -> JSONResponse:
    """Handle AOMaaSError and return a standardized JSON response."""
    logger.error(
        exc.message,
        error_code=exc.error_code,
        status_code=exc.status_code,
        details=exc.details,
        path=request.url.path,
        exception_type=type(exc).__name__
    )
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.message,
            "type": exc.error_code,
            "details": exc.details
        }
    )


def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle any unhandled exception and return a standardized JSON response."""
    logger.exception(
        "Unhandled exception",
        exception_type=type(exc).__name__,
        exception_str=str(exc),
        path=request.url.path
    )
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "An unexpected error occurred",
            "type": "internal_server_error"
        }
    )


def register_exception_handlers(app):
    """Register all exception handlers with the FastAPI app."""
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(AOMaaSError, aomass_exception_handler)
    app.add_exception_handler(Exception, generic_exception_handler)