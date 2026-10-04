"""
Webhook service for async event notifications.

Sends webhook notifications for completed runs and events.
"""

from __future__ import annotations

import logging
import time
from typing import Any

import httpx

logger = logging.getLogger(__name__)


class WebhookService:
    """Send webhook notifications via real HTTP requests."""

    async def send(self, url: str, payload: dict[str, Any]) -> dict[str, Any]:
        logger.info("Sending webhook to %s", url)
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(url, json=payload)
                response.raise_for_status()
                return {
                    "url": url,
                    "status": "sent",
                    "http_status": response.status_code,
                    "timestamp": time.time(),
                    "payload": payload,
                }
        except Exception as exc:
            logger.error("Webhook delivery to %s failed: %s", url, exc)
            return {
                "url": url,
                "status": "failed",
                "error": str(exc),
                "timestamp": time.time(),
                "payload": payload,
            }


webhook_service = WebhookService()
