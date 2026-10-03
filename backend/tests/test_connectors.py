"""Tests for action connectors (FileSystem, Email, Calendar, SmartHome)."""

import asyncio
import tempfile
from datetime import UTC, datetime
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from backend.app.connectors.base_action import (
    ActionConnectorError,
    ActionRequest,
    ActionResult,
    action_connector_manager,
)


def _run(coro):
    """Run an async coroutine synchronously for testing."""
    return asyncio.new_event_loop().run_until_complete(coro)


class TestFileSystemConnector:
    """Tests for FileSystemConnector."""

    def test_init(self):
        """FileSystemConnector initializes with a base path."""
        from backend.app.connectors.file_system import FileSystemConnector

        connector = FileSystemConnector(base_path="/tmp/test_ecp")
        assert connector.connector_type.value == "file_system"
        assert connector._base_path == "/tmp/test_ecp"
        assert connector.connected

    def test_list_actions(self):
        """FileSystemConnector exposes expected actions."""
        from backend.app.connectors.file_system import FileSystemConnector

        connector = FileSystemConnector(base_path="/tmp/test_ecp")
        actions = _run(connector.list_actions())
        assert "read_file" in actions
        assert "write_file" in actions
        assert "list_directory" in actions
        assert "search_files" in actions
        assert "delete_file" in actions
        assert "file_info" in actions

    def test_read_file_success(self):
        """read_file returns file content when file exists."""
        from backend.app.connectors.file_system import FileSystemConnector

        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "test.txt"
            test_file.write_text("Hello, Jenny!")

            connector = FileSystemConnector(base_path=tmpdir)
            params = {"path": "test.txt"}
            result = _run(connector.execute("read_file", params))

            assert result.success
            assert result.data["content"] == "Hello, Jenny!"
            assert result.action == "read_file"
            assert result.connector == "file_system"

    def test_read_file_failure(self):
        """read_file raises ActionConnectorError when file not found."""
        from backend.app.connectors.file_system import FileSystemConnector

        with tempfile.TemporaryDirectory() as tmpdir:
            connector = FileSystemConnector(base_path=tmpdir)
            result = _run(connector.execute("read_file", {"path": "nonexistent.txt"}))
            assert not result.success
            assert "errno" in result.error.lower() or "no such file" in result.error.lower()


class TestEmailConnector:
    """Tests for EmailConnector."""

    def test_init(self):
        """EmailConnector initializes with config."""
        from backend.app.connectors.email import EmailConnector

        connector = EmailConnector(
            smtp_host="smtp.test.com",
            smtp_port=587,
            smtp_user="test@test.com",
            smtp_password="secret",
        )
        assert connector.connector_type.value == "email"
        assert connector._smtp_host == "smtp.test.com"
        assert not connector.connected

    def test_list_actions(self):
        """EmailConnector exposes expected actions."""
        from backend.app.connectors.email import EmailConnector

        connector = EmailConnector(smtp_host="smtp.test.com")
        actions = _run(connector.list_actions())
        assert "send_email" in actions
        assert "read_emails" in actions
        assert "list_emails" in actions
        assert "search_emails" in actions

    @patch("backend.app.connectors.email.smtplib.SMTP")
    def test_send_email_success(self, mock_smtp_class):
        """send_email succeeds via SMTP."""
        from backend.app.connectors.email import EmailConnector

        mock_server = MagicMock()
        mock_smtp_class.return_value = mock_server

        connector = EmailConnector(
            smtp_host="smtp.test.com",
            smtp_port=587,
            smtp_user="test@test.com",
            smtp_password="secret",
        )
        result = _run(
            connector.execute(
                "send_email",
                {"to": "recipient@test.com", "subject": "Test", "body": "..."},
            )
        )

        assert result.success
        assert result.data["to"] == "recipient@test.com"
        assert result.data["subject"] == "Test"
        assert result.data["sent"] is True
        mock_server.send_message.assert_called_once()

    def test_send_email_requires_to(self):
        """send_email fails without 'to' parameter."""
        from backend.app.connectors.email import EmailConnector

        connector = EmailConnector(smtp_host="smtp.test.com")
        result = _run(connector.execute("send_email", {"subject": "x"}))
        assert not result.success
        assert "to" in result.error.lower()


class TestCalendarConnector:
    """Tests for CalendarConnector."""

    def test_init(self):
        """CalendarConnector initializes with Google config."""
        from backend.app.connectors.calendar import CalendarConnector

        connector = CalendarConnector(google_access_token="token123")
        assert connector.connector_type.value == "calendar"
        assert connector._calendar_id == "primary"
        assert connector.connected

    def test_init_no_config(self):
        """CalendarConnector without config is not connected."""
        from backend.app.connectors.calendar import CalendarConnector

        connector = CalendarConnector()
        assert not connector.connected

    def test_list_actions(self):
        """CalendarConnector exposes expected actions."""
        from backend.app.connectors.calendar import CalendarConnector

        connector = CalendarConnector(google_access_token="token")
        actions = _run(connector.list_actions())
        assert "create_event" in actions
        assert "list_events" in actions
        assert "update_event" in actions
        assert "delete_event" in actions

    def test_list_events_stub(self):
        """list_events returns empty list in stub mode."""
        from backend.app.connectors.calendar import CalendarConnector

        connector = CalendarConnector()
        result = _run(connector.execute("list_events", {}))
        assert result.success
        assert result.data["count"] == 0
        assert result.data["events"] == []

    def test_create_event_failure(self):
        """create_event fails without required params."""
        from backend.app.connectors.calendar import CalendarConnector

        connector = CalendarConnector()
        result = _run(connector.execute("create_event", {}))
        assert not result.success


class TestSmartHomeConnector:
    """Tests for SmartHomeConnector."""

    def test_init(self):
        """SmartHomeConnector initializes with HA config."""
        from backend.app.connectors.smarthome import SmartHomeConnector

        connector = SmartHomeConnector(ha_url="http://ha:8123", ha_token="token")
        assert connector.connector_type.value == "smart_home"
        assert connector._ha_url == "http://ha:8123"
        assert connector.connected

    def test_init_stub(self):
        """SmartHomeConnector without config is stub mode."""
        from backend.app.connectors.smarthome import SmartHomeConnector

        connector = SmartHomeConnector()
        assert not connector.connected

    def test_list_actions(self):
        """SmartHomeConnector exposes expected actions."""
        from backend.app.connectors.smarthome import SmartHomeConnector

        connector = SmartHomeConnector()
        actions = _run(connector.list_actions())
        assert "turn_on" in actions
        assert "turn_off" in actions
        assert "set_brightness" in actions
        assert "set_temperature" in actions
        assert "get_state" in actions

    def test_turn_on_stub(self):
        """turn_on succeeds in stub mode with entity_id."""
        from backend.app.connectors.smarthome import SmartHomeConnector

        connector = SmartHomeConnector()
        connector._connected = True

        result = _run(connector.execute("turn_on", {"entity_id": "light.test"}))
        assert result.success
        assert result.data["entity_id"] == "light.test"
        assert result.data["state"] == "on"

    def test_turn_off_stub(self):
        """turn_off succeeds in stub mode with entity_id."""
        from backend.app.connectors.smarthome import SmartHomeConnector

        connector = SmartHomeConnector()
        connector._connected = True

        result = _run(connector.execute("turn_off", {"entity_id": "light.test"}))
        assert result.success
        assert result.data["entity_id"] == "light.test"
        assert result.data["state"] == "off"

    def test_turn_on_requires_entity_or_topic(self):
        """turn_on fails without entity_id or topic."""
        from backend.app.connectors.smarthome import SmartHomeConnector

        connector = SmartHomeConnector()
        connector._connected = True

        result = _run(connector.execute("turn_on", {}))
        assert not result.success


class TestActionConnectorManager:
    """Tests for ActionConnectorManager singleton."""

    def test_singleton(self):
        """action_connector_manager is a singleton instance."""
        assert action_connector_manager is not None
        assert hasattr(action_connector_manager, "get_connector")

    def test_register_and_get(self):
        """Can register and retrieve a connector."""
        from backend.app.connectors.file_system import FileSystemConnector

        fs = FileSystemConnector(base_path="/tmp/test")
        action_connector_manager.register("file_system", fs)
        retrieved = _run(action_connector_manager.get_connector("file_system"))
        assert retrieved.connector_type.value == "file_system"

    def test_unknown_connector_raises(self):
        """Getting unknown connector raises ActionConnectorError."""
        with pytest.raises(ActionConnectorError):
            _run(action_connector_manager.get_connector("nonexistent"))


class TestActionResult:
    """Tests for ActionResult dataclass."""

    def test_success_result(self):
        """ActionResult.success creates a success result."""
        result = ActionResult(
            success=True,
            action="read_file",
            connector="file_system",
            data={"content": "hello"},
            executed_at=datetime.now(UTC),
        )
        assert result.success
        assert result.action == "read_file"
        assert result.connector == "file_system"
        assert result.data["content"] == "hello"

    def test_failure_result(self):
        """ActionResult with failure stores error message."""
        result = ActionResult(
            success=False,
            action="read_file",
            connector="file_system",
            error="File not found",
            executed_at=datetime.now(UTC),
        )
        assert not result.success
        assert result.error == "File not found"

    def test_default_fields(self):
        """ActionResult defaults are empty dicts and current timestamp."""
        result = ActionResult(success=True, action="test", connector="test")
        assert result.data == {}
        assert result.error is None
        assert result.metadata == {}
        assert result.executed_at is not None


class TestActionRequest:
    """Tests for ActionRequest dataclass."""

    def test_create_request(self):
        """ActionRequest stores request details."""
        request = ActionRequest(
            action="read_file",
            params={"path": "test.txt"},
            connector="file_system",
            requester="janny",
        )
        assert request.action == "read_file"
        assert request.connector == "file_system"
        assert request.params["path"] == "test.txt"
        assert request.requester == "janny"

    def test_request_defaults(self):
        """ActionRequest has sensible defaults."""
        request = ActionRequest(action="test", connector="test")
        assert request.params == {}
        assert request.connector == "test"
        assert request.requester == "janny"
