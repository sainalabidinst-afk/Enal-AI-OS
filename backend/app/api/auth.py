import hmac
import secrets
from datetime import UTC, datetime, timedelta

import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from pydantic import BaseModel, Field

from backend.app.core.config import settings
from backend.app.core.passwords import hash_password, verify_password

router = APIRouter(prefix="/auth", tags=["auth"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int = 3600


class AuthUser(BaseModel):
    username: str
    roles: list[str] = Field(default_factory=list)
    permissions: list[str] = Field(default_factory=list)


class TokenData(BaseModel):
    username: str
    roles: list[str] = Field(default_factory=list)
    permissions: list[str] = Field(default_factory=list)


_DUMMY_PASSWORD_HASH = hash_password(secrets.token_urlsafe(32))


def _create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(UTC) + (
        expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")


def _decode_token(token: str) -> TokenData:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        username = payload.get("sub")
        if not isinstance(username, str) or not username:
            raise InvalidTokenError("Missing subject")
        account = settings.AUTH_ACCOUNT
        if not hmac.compare_digest(username.encode(), account.username.encode()):
            raise InvalidTokenError("Unknown account")
        roles = payload.get("roles", [])
        permissions = payload.get("permissions", [])
        if (
            not isinstance(roles, list)
            or not all(isinstance(role, str) for role in roles)
            or not isinstance(permissions, list)
            or not all(isinstance(permission, str) for permission in permissions)
            or not set(roles).issubset(account.roles)
            or not set(permissions).issubset(account.permissions)
        ):
            raise InvalidTokenError("Token permissions are no longer valid")
        return TokenData(username=username, roles=roles, permissions=permissions)
    except InvalidTokenError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc


def get_current_user(token: str = Depends(oauth2_scheme)) -> AuthUser:
    token_data = _decode_token(token)
    return AuthUser(
        username=token_data.username,
        roles=token_data.roles,
        permissions=token_data.permissions,
    )


@router.post("/login", response_model=LoginResponse)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if not settings.SECRET_KEY:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="SECRET_KEY is not configured on the server.",
        )
    username = form_data.username or ""
    password = form_data.password or ""
    account = settings.AUTH_ACCOUNT
    if not account.username or not account.password_hash:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Authentication is not configured on the server.",
        )
    username_matches = hmac.compare_digest(username.encode(), account.username.encode())
    password_hash = account.password_hash if username_matches else _DUMMY_PASSWORD_HASH
    password_matches = verify_password(password, password_hash)
    if not username_matches or not password_matches:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = _create_access_token(
        data={
            "sub": account.username,
            "roles": account.roles,
            "permissions": account.permissions,
        }
    )
    return LoginResponse(
        access_token=token,
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )


@router.get("/me", response_model=AuthUser)
async def get_me(current_user: AuthUser = Depends(get_current_user)):
    return current_user


@router.post("/logout")
async def logout(current_user: AuthUser = Depends(get_current_user)):
    return {"detail": "Logged out successfully"}
