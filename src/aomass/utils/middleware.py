"""Middleware for AOMaaS."""
import time
from typing import Callable

from fastapi import FastAPI, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from .logging import get_logger

logger = get_logger(__name__)


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Middleware for logging request and response information."""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Process the request, log details, and return the response."""
        request_id = request.headers.get("X-Request-ID", "")
        
        # Store request body for potential error logging
        body = await self._get_request_body(request)
        request.state.body = body
        
        # Log request
        logger.info(
            "Request started",
            request_id=request_id,
            method=request.method,
            path=request.url.path,
            query_params=dict(request.query_params),
            client_host=request.client.host if request.client else None,
            user_agent=request.headers.get("User-Agent"),
        )
        
        # Process request and measure time
        start_time = time.time()
        try:
            response = await call_next(request)
            process_time = time.time() - start_time
            
            # Log successful response
            logger.info(
                "Request completed",
                request_id=request_id,
                method=request.method,
                path=request.url.path,
                status_code=response.status_code,
                process_time_ms=round(process_time * 1000, 2),
            )
            
            # Add processing time header
            response.headers["X-Process-Time"] = str(process_time)
            if request_id:
                response.headers["X-Request-ID"] = request_id
                
            return response
            
        except Exception as e:
            # Log exception (the exception will be handled by exception handlers)
            process_time = time.time() - start_time
            logger.error(
                "Request failed",
                request_id=request_id,
                method=request.method,
                path=request.url.path,
                process_time_ms=round(process_time * 1000, 2),
                exception_type=type(e).__name__,
                exception_str=str(e),
            )
            raise

    async def _get_request_body(self, request: Request) -> str:
        """Get the request body as a string."""
        body = await request.body()
        # FastAPI already handles body reading internally
        # No need to seek as request.body() returns a copy
        return body.decode() if body else ""


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Middleware for rate limiting requests."""

    def __init__(self, app: FastAPI, requests_per_minute: int = 100):
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        self.requests = {}

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Process the request with rate limiting."""
        client_ip = request.client.host if request.client else "unknown"
        current_time = time.time()
        
        # Clean up old requests
        self._clean_old_requests(current_time)
        
        # Check rate limit
        if self._is_rate_limited(client_ip, current_time):
            logger.warning(
                "Rate limit exceeded",
                client_ip=client_ip,
                path=request.url.path,
                method=request.method,
            )
            
            # Return 429 Too Many Requests
            from aomass.utils.error_handling import RateLimitExceededError
            raise RateLimitExceededError()
        
        # Process request
        return await call_next(request)

    def _clean_old_requests(self, current_time: float) -> None:
        """Remove requests older than 1 minute."""
        for ip in list(self.requests.keys()):
            self.requests[ip] = [ts for ts in self.requests[ip] if current_time - ts < 60]
            if not self.requests[ip]:
                del self.requests[ip]

    def _is_rate_limited(self, client_ip: str, current_time: float) -> bool:
        """Check if the client has exceeded the rate limit."""
        if client_ip not in self.requests:
            self.requests[client_ip] = []
        
        self.requests[client_ip].append(current_time)
        
        return len(self.requests[client_ip]) > self.requests_per_minute


def setup_middleware(app: FastAPI) -> None:
    """Set up all middleware for the application."""
    app.add_middleware(RequestLoggingMiddleware)
    app.add_middleware(RateLimitMiddleware)