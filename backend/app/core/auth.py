"""Authentication and authorization dependencies."""
import logging
from typing import Any

from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from backend.app.core.config import settings
from backend.app.core.security_model import Permission, security_model

logger = logging.getLogger(__name__)

security = HTTPBearer(auto_error=False)


async def get_current_user(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> dict[str, Any]:
    if not credentials or not credentials.credentials:
        raise HTTPException(status_code=401, detail="Missing or invalid authorization header")

    token = credentials.credentials
    user_id = f"user:{token}"

    if not settings.SECRET_KEY:
        raise HTTPException(
            status_code=401,
            detail="SECRET_KEY is not configured. Set SECRET_KEY to enable authentication.",
        )

    return {
        "user_id": user_id,
        "token": token,
        "scopes": ["default"],
    }


def require_permission(permission: Permission | str):
    if isinstance(permission, str):
        permission = Permission(permission)
    async def checker(current_user: dict[str, Any] = Depends(get_current_user)) -> dict[str, Any]:
        plugin_id = current_user["user_id"]
        allowed = security_model.check_permission(
            plugin_id=plugin_id,
            permission=permission,
            context={"user_id": current_user["user_id"]},
        )
        if not allowed:
            raise HTTPException(status_code=403, detail=f"Permission denied: {permission.value}")
        return current_user

    return checker
