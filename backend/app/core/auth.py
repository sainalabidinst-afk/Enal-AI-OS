"""Authentication and authorization dependencies."""
import logging
from typing import Any

from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

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
    try:
        from backend.app.api.auth import _decode_token
        token_data = _decode_token(token)
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=401, detail="Invalid or expired token") from exc

    return {
        "user_id": token_data.username,
        "token": token,
        "scopes": token_data.permissions or ["default"],
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
