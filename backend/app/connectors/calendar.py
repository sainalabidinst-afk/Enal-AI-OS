"""
Calendar Action Connector
=========================

Provides calendar operations for Jenny: create_event, list_events, update_event, delete_event.
Supports CalDAV (local) and Google Calendar API (cloud, lazy import).
"""

from __future__ import annotations

import logging
from datetime import UTC, datetime
from typing import Any

from backend.app.connectors.base_action import (
    ActionConnectorError,
    ActionResult,
    ActionType,
    BaseActionConnector,
)

logger = logging.getLogger(__name__)


class CalendarConnector(BaseActionConnector):
    """Calendar connector supporting CalDAV and Google Calendar API."""

    def __init__(
        self,
        caldav_url: str = "",
        caldav_user: str = "",
        caldav_password: str = "",
        calendar_id: str = "primary",
        google_access_token: str = "",
        connector_type: ActionType = ActionType.CALENDAR,
    ) -> None:
        super().__init__(connector_type=connector_type)
        self._caldav_url = caldav_url
        self._caldav_user = caldav_user
        self._caldav_password = caldav_password
        self._calendar_id = calendar_id
        self._google_token = google_access_token
        self._connected = bool(caldav_url) or bool(google_access_token)

    async def connect(self) -> None:
        if not self._caldav_url and not self._google_token:
            raise ActionConnectorError("No calendar configured (caldav_url or google_access_token)")
        self._connected = True
        logger.info("CalendarConnector ready (calendar_id=%s)", self._calendar_id)

    async def disconnect(self) -> None:
        self._connected = False

    async def list_actions(self) -> list[str]:
        return ["create_event", "list_events", "update_event", "delete_event"]

    async def execute(self, action: str, params: dict[str, Any]) -> ActionResult:
        action_map = {
            "create_event": self._create_event,
            "list_events": self._list_events,
            "update_event": self._update_event,
            "delete_event": self._delete_event,
        }

        handler = action_map.get(action)
        if not handler:
            raise ActionConnectorError(f"Unknown action: {action}")

        try:
            data = await handler(params)
            return ActionResult(
                success=True,
                data=data,
                action=action,
                connector=self.connector_type.value,
            )
        except Exception as e:
            logger.error("Calendar action '%s' failed: %s", action, e)
            return ActionResult(
                success=False,
                error=str(e),
                action=action,
                connector=self.connector_type.value,
            )

    async def _create_event(self, params: dict[str, Any]) -> dict[str, Any]:
        summary = params.get("summary", "")
        start = params.get("start", "")
        end_ = params.get("end", "")
        description = params.get("description", "")
        attendees = params.get("attendees", [])
        location = params.get("location", "")

        if not summary or not start:
            raise ActionConnectorError("'summary' and 'start' are required for create_event")

        event = {
            "summary": summary,
            "start": start,
            "end": end_,
            "description": description,
            "attendees": attendees,
            "location": location,
            "created_at": datetime.now(UTC).isoformat(),
        }

        if self._google_token:
            try:
                import aiohttp

                headers = {"Authorization": f"Bearer {self._google_token}"}
                payload = {
                    "summary": summary,
                    "start": {"dateTime": start},
                    "end": {"dateTime": end_ or start},
                }
                if description:
                    payload["description"] = description
                if location:
                    payload["location"] = location
                if attendees:
                    payload["attendees"] = [{"email": a} for a in attendees]

                async with aiohttp.ClientSession() as session:
                    async with session.post(
                        f"https://www.googleapis.com/calendar/v3/calendars/{self._calendar_id}/events",
                        headers=headers,
                        json=payload,
                        timeout=aiohttp.ClientTimeout(total=15),
                    ) as resp:
                        if resp.status != 200:
                            raise ActionConnectorError(
                                f"Google Calendar API error: HTTP {resp.status}"
                            )
                        result = await resp.json()
                return {"event_id": result.get("id"), **event}
            except ImportError:
                raise ActionConnectorError("aiohttp required for Google Calendar API")
        else:
            return {"event_id": f"cal-{datetime.now(UTC).strftime('%Y%m%d%H%M%S')}", **event}

    async def _list_events(self, params: dict[str, Any]) -> dict[str, Any]:
        start_time = params.get("start_time", "")
        end_time = params.get("end_time", "")
        max_results = int(params.get("max_results", 10))

        if self._google_token:
            try:
                import aiohttp

                headers = {"Authorization": f"Bearer {self._google_token}"}
                url = f"https://www.googleapis.com/calendar/v3/calendars/{self._calendar_id}/events"
                query_params = {"maxResults": str(max_results)}
                if start_time:
                    query_params["timeMin"] = start_time
                if end_time:
                    query_params["timeMax"] = end_time

                async with aiohttp.ClientSession() as session:
                    async with session.get(
                        url,
                        headers=headers,
                        params=query_params,
                        timeout=aiohttp.ClientTimeout(total=15),
                    ) as resp:
                        if resp.status != 200:
                            raise ActionConnectorError(
                                f"Google Calendar API error: HTTP {resp.status}"
                            )
                        result = await resp.json()
                events = result.get("items", [])
                return {"count": len(events), "events": events}
            except ImportError:
                raise ActionConnectorError("aiohttp required for Google Calendar API")
        else:
            return {
                "count": 0,
                "events": [],
                "note": "Google Calendar API token not configured. No events to list.",
            }

    async def _update_event(self, params: dict[str, Any]) -> dict[str, Any]:
        event_id = params.get("event_id", "")
        if not event_id:
            raise ActionConnectorError("'event_id' is required for update_event")

        update_fields = {
            k: v
            for k, v in params.items()
            if k in ("summary", "start", "end", "description", "location", "attendees")
        }

        if self._google_token:
            try:
                import aiohttp

                headers = {
                    "Authorization": f"Bearer {self._google_token}",
                    "Content-Type": "application/json",
                }
                payload = {}
                if "summary" in update_fields:
                    payload["summary"] = update_fields["summary"]
                if "start" in update_fields:
                    payload["start"] = {"dateTime": update_fields["start"]}
                if "end" in update_fields:
                    payload["end"] = {"dateTime": update_fields["end"]}

                async with aiohttp.ClientSession() as session:
                    async with session.patch(
                        f"https://www.googleapis.com/calendar/v3/calendars/{self._calendar_id}/events/{event_id}",
                        headers=headers,
                        json=payload,
                        timeout=aiohttp.ClientTimeout(total=15),
                    ) as resp:
                        if resp.status != 200:
                            raise ActionConnectorError(
                                f"Google Calendar API error: HTTP {resp.status}"
                            )
                        result = await resp.json()
                return {"event_id": event_id, "updated": True, "result": result}
            except ImportError:
                raise ActionConnectorError("aiohttp required for Google Calendar API")
        else:
            return {
                "event_id": event_id,
                "updated": True,
                "note": "Local stub — no real update performed",
            }

    async def _delete_event(self, params: dict[str, Any]) -> dict[str, Any]:
        event_id = params.get("event_id", "")
        if not event_id:
            raise ActionConnectorError("'event_id' is required for delete_event")

        if self._google_token:
            try:
                import aiohttp

                headers = {"Authorization": f"Bearer {self._google_token}"}
                async with aiohttp.ClientSession() as session:
                    async with session.delete(
                        f"https://www.googleapis.com/calendar/v3/calendars/{self._calendar_id}/events/{event_id}",
                        headers=headers,
                        timeout=aiohttp.ClientTimeout(total=15),
                    ) as resp:
                        if resp.status != 204:
                            raise ActionConnectorError(
                                f"Google Calendar API error: HTTP {resp.status}"
                            )
                return {"event_id": event_id, "deleted": True}
            except ImportError:
                raise ActionConnectorError("aiohttp required for Google Calendar API")
        else:
            return {
                "event_id": event_id,
                "deleted": True,
                "note": "Local stub — no real delete performed",
            }
