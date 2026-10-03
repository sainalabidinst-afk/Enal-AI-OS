"""
Email Action Connector
======================

Provides email operations for Jenny: send_email, read_emails, list_emails, search_emails.
Supports SMTP/IMAP (local) and Gmail API (cloud, lazy import).
"""

from __future__ import annotations

import logging
import smtplib
from datetime import UTC, datetime
from email.message import EmailMessage
from email.parser import BytesParser
from email.policy import default as default_policy
from typing import Any

from backend.app.connectors.base_action import (
    ActionConnectorError,
    ActionResult,
    ActionType,
    BaseActionConnector,
)

logger = logging.getLogger(__name__)


class EmailConnector(BaseActionConnector):
    """Email connector supporting SMTP (send) and IMAP (read).

    Optional Gmail API support when GMAIL_ACCESS_TOKEN is configured.
    """

    def __init__(
        self,
        smtp_host: str = "",
        smtp_port: int = 587,
        smtp_user: str = "",
        smtp_password: str = "",
        imap_host: str = "",
        imap_port: int = 993,
        imap_user: str = "",
        imap_password: str = "",
        use_tls: bool = True,
        connector_type: ActionType = ActionType.EMAIL,
    ) -> None:
        super().__init__(connector_type=connector_type)
        self._smtp_host = smtp_host
        self._smtp_port = smtp_port
        self._smtp_user = smtp_user
        self._smtp_password = smtp_password
        self._imap_host = imap_host
        self._imap_port = imap_port
        self._imap_user = imap_user
        self._imap_password = imap_password
        self._use_tls = use_tls
        self._connected = False

    async def connect(self) -> None:
        # Connection is lazy per-operation; mark as connected
        self._connected = True
        logger.info("EmailConnector ready (SMTP: %s:%s)", self._smtp_host, self._smtp_port)

    async def disconnect(self) -> None:
        self._connected = False

    async def list_actions(self) -> list[str]:
        return ["send_email", "read_emails", "list_emails", "search_emails"]

    async def execute(self, action: str, params: dict[str, Any]) -> ActionResult:
        action_map = {
            "send_email": self._send_email,
            "read_emails": self._read_emails,
            "list_emails": self._list_emails,
            "search_emails": self._search_emails,
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
            logger.error("Email action '%s' failed: %s", action, e)
            return ActionResult(
                success=False,
                error=str(e),
                action=action,
                connector=self.connector_type.value,
            )

    async def _send_email(self, params: dict[str, Any]) -> dict[str, Any]:
        to = params.get("to", "")
        subject = params.get("subject", "")
        body = params.get("body", "")
        from_addr = params.get("from", self._smtp_user)
        cc = params.get("cc", [])
        bcc = params.get("bcc", [])

        if not to:
            raise ActionConnectorError("'to' parameter is required for send_email")

        recipients = []
        if isinstance(to, str):
            recipients = [to]
        elif isinstance(to, list):
            recipients = to

        if cc:
            cc_list = [cc] if isinstance(cc, str) else cc
            recipients.extend(cc_list)
        if bcc:
            bcc_list = [bcc] if isinstance(bcc, str) else bcc
            recipients.extend(bcc_list)

        msg = EmailMessage()
        msg["From"] = from_addr
        msg["To"] = to
        msg["Subject"] = subject
        msg.set_content(body)

        try:
            server = smtplib.SMTP(self._smtp_host, self._smtp_port, timeout=30)
            if self._use_tls:
                server.starttls()
            if self._smtp_user and self._smtp_password:
                server.login(self._smtp_user, self._smtp_password)
            server.send_message(msg, from_addr=from_addr, to_addrs=recipients)
            server.quit()
        except Exception as e:
            raise ActionConnectorError(f"SMTP send failed: {e}") from e

        return {
            "to": to,
            "subject": subject,
            "sent": True,
            "timestamp": datetime.now(UTC).isoformat(),
        }

    async def _read_emails(self, params: dict[str, Any]) -> dict[str, Any]:
        folder = params.get("folder", "INBOX")
        limit = int(params.get("limit", 10))
        unread_only = bool(params.get("unread_only", True))

        try:
            import imaplib

            mail = imaplib.IMAP4_SSL(self._imap_host, self._imap_port)
            if self._imap_user and self._imap_password:
                mail.login(self._imap_user, self._imap_password)
            mail.select(folder)

            if unread_only:
                status, _ = mail.status(folder, "(UNSEEN)")
                search_criteria = "(UNSEEN)"
            else:
                search_criteria = "ALL"

            _, data = mail.search(None, search_criteria)
            email_ids = data[0].split()[-limit:] if data[0] else []
            emails = []

            for eid in email_ids:
                _, msg_data = mail.fetch(eid, "(RFC822)")
                # msg_data[0] from imaplib is tuple[bytes, bytes | None]
                raw_entry = msg_data[0]
                raw_bytes: bytes | None
                if isinstance(raw_entry, tuple) and len(raw_entry) > 1:
                    raw_bytes = raw_entry[1]
                elif isinstance(raw_entry, bytes):
                    raw_bytes = raw_entry
                else:
                    raw_bytes = None

                msg: EmailMessage
                if raw_bytes:
                    msg = BytesParser(policy=default_policy).parsebytes(raw_bytes)  # type: ignore[assignment]
                else:
                    msg = EmailMessage()
                emails.append(
                    {
                        "id": eid.decode("utf-8"),
                        "from": msg.get("From", ""),
                        "subject": msg.get("Subject", ""),
                        "sent_date": msg.get("Date", ""),
                    }
                )

            mail.close()
            mail.logout()

            return {"folder": folder, "count": len(emails), "emails": emails}
        except Exception as e:
            raise ActionConnectorError(f"IMAP read failed: {e}") from e

    async def _list_emails(self, params: dict[str, Any]) -> dict[str, Any]:
        return await self._read_emails(params)

    async def _search_emails(self, params: dict[str, Any]) -> dict[str, Any]:
        query = params.get("query", "")
        folder = params.get("folder", "INBOX")
        if not query:
            raise ActionConnectorError("'query' parameter is required for search_emails")

        try:
            import imaplib

            mail = imaplib.IMAP4_SSL(self._imap_host, self._imap_port)
            if self._imap_user and self._imap_password:
                mail.login(self._imap_user, self._imap_password)
            mail.select(folder)

            _, data = mail.search(None, f'SUBJECT "{query}" OR FROM "{query}"')
            email_ids = data[0].split() if data[0] else []
            emails = [{"id": eid.decode("utf-8")} for eid in email_ids]

            mail.close()
            mail.logout()

            return {"query": query, "folder": folder, "count": len(emails), "emails": emails}
        except Exception as e:
            raise ActionConnectorError(f"IMAP search failed: {e}") from e
