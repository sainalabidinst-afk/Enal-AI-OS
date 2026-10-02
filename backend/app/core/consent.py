"""
Consent & Safety Manager
========================

Implements user consent request/approve/deny flow with timeout handling
and risk-based action classification for Jenny-like interaction.

ADR-025: Consent & Permission Architecture
"""

from __future__ import annotations

import logging
import uuid
from collections import deque
from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta
from enum import StrEnum
from typing import Any

logger = logging.getLogger(__name__)


class RiskLevel(StrEnum):
    """Risk classification for actions."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class ConsentStatus(StrEnum):
    """Consent request status values."""

    PENDING = "pending"
    APPROVED = "approved"
    DENIED = "denied"
    EXPIRED = "expired"


@dataclass
class ConsentRequest:
    """A request for user consent to perform an action."""

    request_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    session_id: str = ""
    action_type: str = ""
    description: str = ""
    risk_level: RiskLevel = RiskLevel.LOW
    params: dict[str, Any] = field(default_factory=dict)
    connector_type: str = ""
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    timeout_seconds: int = 30
    status: ConsentStatus = ConsentStatus.PENDING
    response_at: datetime | None = None
    responder: str = ""

    @property
    def expires_at(self) -> datetime:
        return self.created_at + timedelta(seconds=self.timeout_seconds)

    @property
    def is_expired(self) -> bool:
        if self.status != ConsentStatus.PENDING:
            return False
        return datetime.now(UTC) >= self.expires_at

    @property
    def is_resolved(self) -> bool:
        return self.status in (
            ConsentStatus.APPROVED,
            ConsentStatus.DENIED,
            ConsentStatus.EXPIRED,
        )

    def approve(self, responder: str = "user") -> None:
        self.status = ConsentStatus.APPROVED
        self.response_at = datetime.now(UTC)
        self.responder = responder
        logger.info(
            "Consent approved: %s (action=%s, risk=%s)",
            self.request_id,
            self.action_type,
            self.risk_level.value,
        )

    def deny(self, responder: str = "user") -> None:
        self.status = ConsentStatus.DENIED
        self.response_at = datetime.now(UTC)
        self.responder = responder
        logger.warning(
            "Consent denied: %s (action=%s, risk=%s)",
            self.request_id,
            self.action_type,
            self.risk_level.value,
        )


# Action definitions for risk classification
LOW_RISK_ACTIONS = frozenset([
    "read_file",
    "list_directory",
    "search_files",
    "file_info",
    "list_events",
    "list_emails",
    "search_emails",
    "read_emails",
    "get_state",
])

MEDIUM_RISK_ACTIONS = frozenset([
    "write_file",
    "delete_file",
    "send_email",
    "create_event",
    "update_event",
    "delete_event",
    "set_brightness",
    "set_temperature",
])

HIGH_RISK_ACTIONS = frozenset([
    "trading",
    "system_config",
    "iot_control",
    "system_restart",
    "factory_reset",
])

# Connector type permissions
SYSTEM_CONNECTORS = frozenset(["file_system", "calendar", "smart_home"])


def classify_risk(
    action_type: str,
    params: dict[str, Any] | None = None,
) -> RiskLevel:
    """Classify an action by risk level.

    Low: read-only operations, knowledge search
    Medium: file write, email send, event creation — requires confirmation
    High: trading, system config, IoT control — requires explicit approval
    """
    params = params or {}

    if action_type in HIGH_RISK_ACTIONS:
        return RiskLevel.HIGH

    if action_type in MEDIUM_RISK_ACTIONS:
        return RiskLevel.MEDIUM

    if action_type in LOW_RISK_ACTIONS:
        return RiskLevel.LOW

    connector = params.get("connector_type", "")
    if connector in SYSTEM_CONNECTORS:
        return RiskLevel.MEDIUM

    # Default: treat unknown actions as medium risk for safety
    logger.warning("Unknown action type '%s' — defaulting to medium risk", action_type)
    return RiskLevel.MEDIUM


class ConsentManager:
    """Manages consent requests with timeout and lifecycle tracking."""

    def __init__(self, default_timeout: int = 30) -> None:
        self._requests: dict[str, ConsentRequest] = {}
        self._history: deque[ConsentRequest] = deque(maxlen=1000)
        self._default_timeout = default_timeout

    def request(
        self,
        action_type: str,
        description: str,
        params: dict[str, Any] | None = None,
        session_id: str = "",
        connector_type: str = "",
        timeout_seconds: int | None = None,
    ) -> ConsentRequest:
        """Create a new consent request.

        Returns the request with status PENDING.
        The caller must check is_resolved and status before proceeding.
        """
        risk = classify_risk(action_type, params)
        request = ConsentRequest(
            session_id=session_id,
            action_type=action_type,
            description=description,
            risk_level=risk,
            params=params or {},
            connector_type=connector_type,
            timeout_seconds=timeout_seconds or self._default_timeout,
        )
        self._requests[request.request_id] = request
        self._history.append(request)

        logger.info(
            "Consent requested: %s (action=%s, risk=%s, timeout=%ss)",
            request.request_id,
            action_type,
            risk.value,
            request.timeout_seconds,
        )
        return request

    def get_request(self, request_id: str) -> ConsentRequest | None:
        """Retrieve a consent request by ID."""
        return self._requests.get(request_id)

    def approve(self, request_id: str, responder: str = "user") -> ConsentRequest | None:
        """Approve a pending consent request."""
        request = self._requests.get(request_id)
        if request is None:
            logger.warning("Consent request not found: %s", request_id)
            return None
        if request.is_resolved:
            logger.warning("Consent request already resolved: %s", request_id)
            return request
        request.approve(responder)
        return request

    def deny(self, request_id: str, responder: str = "user") -> ConsentRequest | None:
        """Deny a pending consent request."""
        request = self._requests.get(request_id)
        if request is None:
            logger.warning("Consent request not found: %s", request_id)
            return None
        if request.is_resolved:
            logger.warning("Consent request already resolved: %s", request_id)
            return request
        request.deny(responder)
        return request

    def check_timeout(self, request_id: str) -> ConsentStatus:
        """Check if a pending request has expired."""
        request = self._requests.get(request_id)
        if request is None:
            return ConsentStatus.PENDING
        if request.is_expired:
            request.status = ConsentStatus.EXPIRED
            request.response_at = datetime.now(UTC)
            logger.warning("Consent expired: %s", request_id)
        return request.status

    def get_pending_count(self) -> int:
        """Count pending (non-expired) requests."""
        count = 0
        for r in self._requests.values():
            if r.status == ConsentStatus.PENDING and not r.is_expired:
                count += 1
        return count

    def get_history(
        self,
        status: ConsentStatus | None = None,
        limit: int = 100,
    ) -> list[ConsentRequest]:
        """Get consent request history, optionally filtered by status."""
        if status:
            return [r for r in self._history if r.status == status][-limit:]
        return list(self._history)[-limit:]

    def cleanup(self) -> int:
        """Remove expired PENDING requests. Returns count removed."""
        expired_ids = [
            rid for rid, r in self._requests.items()
            if r.status == ConsentStatus.PENDING and r.is_expired
        ]
        for rid in expired_ids:
            self._requests[rid].status = ConsentStatus.EXPIRED
            del self._requests[rid]
            logger.info("Cleaned up expired consent: %s", rid)
        return len(expired_ids)


consent_manager = ConsentManager()
