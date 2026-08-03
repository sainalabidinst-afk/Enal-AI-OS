from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

from backend.app.core.config import settings

import jwt
from jwt.exceptions import InvalidTokenError
from datetime import datetime, timedelta, timezone

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
    roles: list[str] = []
    permissions: list[str] = []


class TokenData(BaseModel):
    username: str
    roles: list[str] = []
    permissions: list[str] = []


def _create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")


def _decode_token(token: str) -> TokenData:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        username = payload.get("sub")
        if username is None:
            raise InvalidTokenError("Missing subject")
        return TokenData(
            username=username,
            roles=payload.get("roles", []),
            permissions=payload.get("permissions", []),
        )
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
    if not username or not password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username and password are required.",
        )
    token = _create_access_token(
        data={
            "sub": username,
            "roles": ["default"],
            "permissions": ["default"],
        }
    )
    return LoginResponse(access_token=token)


@router.get("/me", response_model=AuthUser)
async def get_me(current_user: AuthUser = Depends(get_current_user)):
    return current_user


@router.post("/logout")
async def logout(current_user: AuthUser = Depends(get_current_user)):
    return {"detail": "Logged out successfully"}
