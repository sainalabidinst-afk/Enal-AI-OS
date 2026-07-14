from datetime import datetime
from typing import Optional, Dict, Any, List
from collections import defaultdict
import asyncio


class NotificationService:
    def __init__(self) -> None:
        self._notifications: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
        self._lock = asyncio.Lock()

    async def send(self, recipient: str, message: str, channel: str = "websocket", metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        async with self._lock:
            entry = {
                "id": __import__("uuid").uuid4().hex,
                "recipient": recipient,
                "channel": channel,
                "message": message,
                "timestamp": datetime.utcnow().isoformat(),
                "metadata": metadata or {},
                "read": False,
            }
            self._notifications[recipient].append(entry)
            return entry

    async def get_notifications(self, recipient: str, limit: int = 50) -> List[Dict[str, Any]]:
        return self._notifications.get(recipient, [])[-limit:]

    async def mark_read(self, recipient: str, notification_id: str) -> bool:
        for n in self._notifications.get(recipient, []):
            if n["id"] == notification_id:
                n["read"] = True
                return True
        return False


notification_service = NotificationService()
