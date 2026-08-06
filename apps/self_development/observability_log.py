"""
Observability log for Self Development.
"""

import logging

logger = logging.getLogger(__name__)


def log_execution(capability_id: str, operation: str, duration_ms: float) -> None:
    """Log capability execution."""
    logger.info("Capability %s executed %s in %.2fms", capability_id, operation, duration_ms)


def log_error(capability_id: str, operation: str, error: Exception) -> None:
    """Log capability error."""
    logger.error("Capability %s failed %s: %s", capability_id, operation, error)
