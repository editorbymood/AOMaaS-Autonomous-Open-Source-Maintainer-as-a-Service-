"""Logging configuration for AOMaaS."""
import logging
import sys
from pathlib import Path

import structlog
from rich.logging import RichHandler

from aomass.config.settings import settings


def setup_logging() -> None:
    """Set up structured logging with Rich formatting."""
    
    # Create logs directory
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Configure standard library logging
    logging.basicConfig(
        level=getattr(logging, settings.log_level.upper()),
        format="%(message)s",
        handlers=[
            RichHandler(rich_tracebacks=True),
            logging.FileHandler(log_dir / "aomass.log")
        ]
    )
    
    # Configure structlog
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
            structlog.processors.TimeStamper(fmt="ISO"),
            structlog.dev.ConsoleRenderer() if settings.debug else structlog.processors.JSONRenderer()
        ],
        wrapper_class=structlog.make_filtering_bound_logger(
            getattr(logging, settings.log_level.upper())
        ),
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )


def get_logger(name: str = None) -> structlog.BoundLogger:
    """Get a configured logger instance."""
    return structlog.get_logger(name)
