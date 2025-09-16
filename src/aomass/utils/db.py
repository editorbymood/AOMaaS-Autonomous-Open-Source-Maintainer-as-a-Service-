"""Database utilities for AOMaaS."""
from contextlib import asynccontextmanager
from typing import AsyncGenerator, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from aomass.utils.logging import get_logger

logger = get_logger(__name__)


@asynccontextmanager
async def transaction(session: AsyncSession) -> AsyncGenerator[AsyncSession, None]:
    """Context manager for database transactions with error handling.
    
    Usage:
        async with transaction(session) as tx_session:
            # Perform database operations
            tx_session.add(some_model)
    """
    # Start a nested transaction (savepoint)
    async with session.begin():
        try:
            # Yield the session for use within the context
            yield session
            # Transaction will be committed automatically when exiting the context
            # if no exceptions are raised
            logger.debug("Transaction committed successfully")
        except Exception as e:
            # Transaction will be rolled back automatically when an exception occurs
            logger.error(
                "Transaction rolled back due to error",
                exception_type=type(e).__name__,
                exception_str=str(e)
            )
            # Re-raise the exception for higher-level handling
            raise


async def execute_with_retry(
    session: AsyncSession,
    operation,
    max_retries: int = 3,
    retry_delay: float = 0.5
):
    """Execute a database operation with retry logic for transient errors.
    
    Args:
        session: The database session
        operation: A callable that performs the database operation
        max_retries: Maximum number of retry attempts
        retry_delay: Delay between retries in seconds
        
    Returns:
        The result of the operation
    """
    import asyncio
    from sqlalchemy.exc import DBAPIError, OperationalError
    
    retries = 0
    last_error = None
    
    while retries <= max_retries:
        try:
            async with transaction(session) as tx_session:
                result = await operation(tx_session)
                return result
        except (OperationalError, DBAPIError) as e:
            # Only retry on specific database errors that might be transient
            if "deadlock" in str(e).lower() or "connection" in str(e).lower():
                retries += 1
                if retries <= max_retries:
                    logger.warning(
                        f"Database operation failed, retrying ({retries}/{max_retries})",
                        error=str(e)
                    )
                    await asyncio.sleep(retry_delay * retries)  # Exponential backoff
                    continue
            
            # For other database errors, don't retry
            last_error = e
            break
        except Exception as e:
            # Don't retry on non-database errors
            last_error = e
            break
    
    # If we got here, all retries failed or a non-retryable error occurred
    logger.error(
        "Database operation failed after retries",
        max_retries=max_retries,
        exception_type=type(last_error).__name__,
        exception_str=str(last_error)
    )
    raise last_error