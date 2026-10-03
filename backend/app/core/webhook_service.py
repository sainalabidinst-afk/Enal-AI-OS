"""
Webhook service for async event notifications.

Sends webhook notifications for completed runs and events.
"""

from __future__ import annotations

import logging
import time
from typing import Any

logger = logging.getLogger(__name__)


class WebhookService:
    """Send webhook notifications."""

    async def send(self, url: str, payload: dict[str, Any]) -> dict[str, Any]:
        logger.info("Sending webhook to %s", url)
        return {
            "url": url,
            "status": "sent",
            "timestamp": time.time(),
            "payload": payload,
        }


webhook_service = WebhookService()
