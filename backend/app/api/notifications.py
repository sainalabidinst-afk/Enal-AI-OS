from fastapi import APIRouter, HTTPException
from backend.app.core.notification_service import notification_service

router = APIRouter()


@router.post("/notifications")
async def send_notification(recipient: str, message: str, channel: str = "websocket", metadata: dict | None = None):
    entry = await notification_service.send(recipient, message, channel=channel, metadata=metadata)
    return entry


@router.get("/notifications/{recipient}")
async def get_notifications(recipient: str, limit: int = 50):
    return {"recipient": recipient, "notifications": await notification_service.get_notifications(recipient, limit)}


@router.patch("/notifications/{recipient}/read/{notification_id}")
async def mark_notification_read(recipient: str, notification_id: str):
    ok = await notification_service.mark_read(recipient, notification_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Notification not found")
    return {"read": True}
