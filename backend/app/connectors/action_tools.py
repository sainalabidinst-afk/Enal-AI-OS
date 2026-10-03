"""
Action Tool Registration
========================

Registers action connector tools (FileSystem, Email, Calendar, SmartHome)
with the ToolRegistry so they can be invoked by the CognitiveKernel pipeline
and by LLM agent tool-calling.

ADR-024: Action Connector Architecture
"""

from __future__ import annotations

import logging
from typing import Any

from backend.app.connectors.base_action import (
    action_connector_manager,
)
from backend.app.core.tool_registry import Tool

logger = logging.getLogger(__name__)


def _fs_read_file(params: dict[str, Any]) -> dict[str, Any]:
    """Read a file from the local filesystem."""
    import asyncio

    async def _run():
        connector = await action_connector_manager.get_connector("file_system")
        if not connector.connected:
            await connector.connect()
        result = await connector.execute("read_file", params)
        return result.to_dict() if hasattr(result, "to_dict") else result.__dict__

    return asyncio.new_event_loop().run_until_complete(_run())


def _fs_list_directory(params: dict[str, Any]) -> dict[str, Any]:
    """List contents of a directory."""
    import asyncio

    async def _run():
        connector = await action_connector_manager.get_connector("file_system")
        if not connector.connected:
            await connector.connect()
        result = await connector.execute("list_directory", params)
        return result.__dict__

    return asyncio.new_event_loop().run_until_complete(_run())


def _email_send(params: dict[str, Any]) -> dict[str, Any]:
    """Send an email via SMTP or Gmail API."""
    import asyncio

    async def _run():
        connector = await action_connector_manager.get_connector("email")
        if not connector.connected:
            await connector.connect()
        result = await connector.execute("send_email", params)
        return result.__dict__

    return asyncio.new_event_loop().run_until_complete(_run())


def _calendar_create(params: dict[str, Any]) -> dict[str, Any]:
    """Create a calendar event."""
    import asyncio

    async def _run():
        connector = await action_connector_manager.get_connector("calendar")
        if not connector.connected:
            await connector.connect()
        result = await connector.execute("create_event", params)
        return result.__dict__

    return asyncio.new_event_loop().run_until_complete(_run())


def _smarthome_turn_on(params: dict[str, Any]) -> dict[str, Any]:
    """Turn on a smart home device (light, switch, etc.)."""
    import asyncio

    async def _run():
        connector = await action_connector_manager.get_connector("smart_home")
        if not connector.connected:
            await connector.connect()
        result = await connector.execute("turn_on", params)
        return result.__dict__

    return asyncio.new_event_loop().run_until_complete(_run())


def register_action_tools():
    """Register all action connector tools with the ToolRegistry.

    Called once during application startup.
    """
    from backend.app.core.tool_registry import tool_registry

    tools = [
        Tool(
            name="read_file",
            description=(
                "Read a text file from the local filesystem. "
                "Use this to open documents, configs, or any readable file."
            ),
            category="action",
            agent="jenny",
            capabilities=["file-io", "read"],
            permissions=["action.execute", "file.read"],
            parameters={
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Relative path to the file"},
                },
                "required": ["path"],
            },
            input_schema={
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Relative path to the file"},
                },
                "required": ["path"],
            },
            output_schema={
                "type": "object",
                "properties": {
                    "path": {"type": "string"},
                    "content": {"type": "string"},
                    "size_bytes": {"type": "integer"},
                    "modified_at": {"type": "string"},
                },
            },
            handler=_fs_read_file,
            requires_confirmation=False,
        ),
        Tool(
            name="list_directory",
            description="List contents of a directory on the local filesystem.",
            category="action",
            agent="jenny",
            capabilities=["file-io", "list"],
            permissions=["action.execute", "file.read"],
            parameters={
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Relative directory path"},
                },
                "required": ["path"],
            },
            input_schema={
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Relative directory path"},
                },
                "required": ["path"],
            },
            output_schema={
                "type": "object",
                "properties": {
                    "path": {"type": "string"},
                    "entries": {"type": "array"},
                },
            },
            handler=_fs_list_directory,
            requires_confirmation=False,
        ),
        Tool(
            name="send_email",
            description=(
                "Send an email via SMTP or Gmail API. Requires 'to' and 'subject' parameters."
            ),
            category="action",
            agent="jenny",
            capabilities=["email", "communication"],
            permissions=["action.execute", "email.send"],
            parameters={
                "type": "object",
                "properties": {
                    "to": {"type": "string", "description": "Recipient email address"},
                    "subject": {"type": "string", "description": "Email subject"},
                    "body": {"type": "string", "description": "Email body content"},
                    "cc": {"type": "string", "description": "CC recipient(s)"},
                    "bcc": {"type": "string", "description": "BCC recipient(s)"},
                },
                "required": ["to", "subject"],
            },
            input_schema={
                "type": "object",
                "properties": {
                    "to": {"type": "string"},
                    "subject": {"type": "string"},
                    "body": {"type": "string"},
                    "cc": {"type": "string"},
                    "bcc": {"type": "string"},
                },
                "required": ["to", "subject"],
            },
            output_schema={
                "type": "object",
                "properties": {
                    "to": {"type": "string"},
                    "subject": {"type": "string"},
                    "sent": {"type": "boolean"},
                    "timestamp": {"type": "string"},
                },
            },
            handler=_email_send,
            requires_confirmation=True,
        ),
        Tool(
            name="create_calendar_event",
            description="Create a calendar event. Requires 'summary' and 'start' parameters.",
            category="action",
            agent="jenny",
            capabilities=["calendar", "scheduling"],
            permissions=["action.execute", "calendar.write"],
            parameters={
                "type": "object",
                "properties": {
                    "summary": {"type": "string", "description": "Event title"},
                    "start": {"type": "string", "description": "Start time (ISO 8601)"},
                    "end": {"type": "string", "description": "End time (ISO 8601)"},
                    "description": {"type": "string"},
                    "attendees": {"type": "array", "items": {"type": "string"}},
                    "location": {"type": "string"},
                },
                "required": ["summary", "start"],
            },
            input_schema={
                "type": "object",
                "properties": {
                    "summary": {"type": "string"},
                    "start": {"type": "string"},
                    "end": {"type": "string"},
                    "description": {"type": "string"},
                    "attendees": {"type": "array", "items": {"type": "string"}},
                    "location": {"type": "string"},
                },
                "required": ["summary", "start"],
            },
            output_schema={
                "type": "object",
                "properties": {
                    "event_id": {"type": "string"},
                    "summary": {"type": "string"},
                    "sent": {"type": "boolean"},
                },
            },
            handler=_calendar_create,
            requires_confirmation=True,
        ),
        Tool(
            name="smarthome_control",
            description=(
                "Control a smart home device (turn on/off, set brightness, set temperature)."
            ),
            category="action",
            agent="jenny",
            capabilities=["iot", "smarthome"],
            permissions=["action.execute", "iot.control"],
            parameters={
                "type": "object",
                "properties": {
                    "entity_id": {
                        "type": "string",
                        "description": "Device entity ID (e.g. light.living_room)",
                    },
                    "topic": {"type": "string", "description": "MQTT topic"},
                    "action": {
                        "type": "string",
                        "description": (
                            "Action: turn_on, turn_off, set_brightness, set_temperature"
                        ),
                    },
                    "brightness": {"type": "integer", "minimum": 0, "maximum": 100},
                    "temperature": {"type": "number"},
                },
                "required": ["action"],
            },
            input_schema={
                "type": "object",
                "properties": {
                    "entity_id": {"type": "string"},
                    "topic": {"type": "string"},
                    "action": {"type": "string"},
                    "brightness": {"type": "integer"},
                    "temperature": {"type": "number"},
                },
                "required": ["action"],
            },
            output_schema={
                "type": "object",
                "properties": {
                    "entity_id": {"type": "string"},
                    "success": {"type": "boolean"},
                },
            },
            handler=lambda params: params,
            requires_confirmation=True,
        ),
    ]

    registered = 0
    for tool in tools:
        tool_registry = tool_registry or None
        from backend.app.core.tool_registry import tool_registry as _reg

        _reg.register(tool)
        registered += 1
        logger.info("Registered action tool: %s", tool.name)

    logger.info("Registered %d action tools", registered)
    return registered
