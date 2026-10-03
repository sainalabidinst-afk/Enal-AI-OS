"""
Telephony integration for voice agents.

Provides inbound/outbound call handling via Twilio or Plivo.
"""

from __future__ import annotations

import logging
from typing import Any

logger = logging.getLogger(__name__)


class TelephonyIntegrationError(Exception):
    """Raised when telephony integration fails."""


class TelephonyIntegration:
    """Telephony integration for voice agents."""

    def __init__(self, provider: str = "twilio") -> None:
        self.provider = provider
        self._active_calls: dict[str, dict[str, Any]] = {}

    async def handle_inbound_call(
        self,
        call_id: str,
        from_number: str,
        to_number: str,
    ) -> dict[str, Any]:
        logger.info("Inbound call %s from %s to %s", call_id, from_number, to_number)
        call = {
            "id": call_id,
            "from": from_number,
            "to": to_number,
            "direction": "inbound",
            "status": "active",
        }
        self._active_calls[call_id] = call
        return call

    async def handle_outbound_call(
        self,
        call_id: str,
        from_number: str,
        to_number: str,
    ) -> dict[str, Any]:
        logger.info("Outbound call %s from %s to %s", call_id, from_number, to_number)
        call = {
            "id": call_id,
            "from": from_number,
            "to": to_number,
            "direction": "outbound",
            "status": "active",
        }
        self._active_calls[call_id] = call
        return call

    async def end_call(self, call_id: str) -> dict[str, Any]:
        call = self._active_calls.get(call_id)
        if not call:
            raise TelephonyIntegrationError(f"Call not found: {call_id}")
        call["status"] = "ended"
        logger.info("Call %s ended", call_id)
        return call

    def get_active_calls(self) -> list[dict[str, Any]]:
        return [call for call in self._active_calls.values() if call["status"] == "active"]


telephony_integration = TelephonyIntegration()
