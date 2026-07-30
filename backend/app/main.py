from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

from .api import (
    artifact,
    attachments,
    benchmark,
    capability_discovery,
    chat,
    ecosystem,
    execution,
    health,
    integration,
    model_gateway,
    notifications,
    orchestrator_v2,
    phase3,
    telemetry,
    trading,
    workspace,
)
from .core.config import settings

import logging

logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="AI Operating System - Multi-Agent AI Platform",
)


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Content-Security-Policy"] = "default-src 'self'; frame-ancestors 'none'"
        response.headers["Referrer-Policy"] = "no-referrer"
        response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
        return response


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, max_requests: int = 100, window_seconds: int = 60):
        super().__init__(app)
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._requests: dict[str, list[float]] = {}

    async def dispatch(self, request: Request, call_next):
        import time
        client_ip = request.client.host if request.client else "unknown"
        now = time.time()
        window_start = now - self.window_seconds
        requests = [t for t in self._requests.get(client_ip, []) if t > window_start]
        if len(requests) >= self.max_requests:
            from fastapi.responses import JSONResponse
            return JSONResponse(status_code=429, content={"detail": "Too many requests"})
        requests.append(now)
        self._requests[client_ip] = requests
        return await call_next(request)


class AuthenticationMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path in ("/", "/docs", "/openapi.json", "/redoc", "/health"):
            return await call_next(request)

        if not settings.SECRET_KEY:
            from fastapi.responses import JSONResponse
            return JSONResponse(
                status_code=401,
                content={"detail": "SECRET_KEY is not configured. Set SECRET_KEY to enable authentication."},
            )

        auth = request.headers.get("Authorization")
        if not auth or not auth.startswith("Bearer "):
            from fastapi.responses import JSONResponse
            return JSONResponse(status_code=401, content={"detail": "Missing or invalid authorization header"})
        return await call_next(request)


class AuditLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        import time
        start = time.perf_counter()
        response = await call_next(request)
        elapsed_ms = (time.perf_counter() - start) * 1000

        user = request.headers.get("Authorization", "anonymous")
        logger.info(
            "audit %s %s status=%d duration=%.2fms user=%s",
            request.method,
            request.url.path,
            response.status_code,
            elapsed_ms,
            user[:20] if user else "anonymous",
        )
        return response


app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(RateLimitMiddleware, max_requests=100, window_seconds=60)
app.add_middleware(AuthenticationMiddleware)
app.add_middleware(AuditLoggingMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    allow_headers=["*"],
)

app.include_router(health.router, tags=["health"])
app.include_router(chat.router, prefix=settings.API_V1_STR, tags=["chat"])
app.include_router(orchestrator_v2.router, prefix=settings.API_V1_STR, tags=["orchestrator-v2"])
app.include_router(phase3.router, prefix=settings.API_V1_STR, tags=["phase3"])
app.include_router(ecosystem.router, prefix=settings.API_V1_STR, tags=["ecosystem"])
app.include_router(capability_discovery.router, prefix=settings.API_V1_STR, tags=["capability-discovery"])
app.include_router(execution.router, prefix=settings.API_V1_STR, tags=["execution"])
app.include_router(workspace.router, prefix=settings.API_V1_STR, tags=["workspace"])
app.include_router(artifact.router, prefix=settings.API_V1_STR, tags=["artifact"])
app.include_router(model_gateway.router, prefix=settings.API_V1_STR, tags=["models"])
app.include_router(notifications.router, prefix=settings.API_V1_STR, tags=["notifications"])
app.include_router(attachments.router, prefix=settings.API_V1_STR, tags=["attachments"])
app.include_router(telemetry.router, prefix=settings.API_V1_STR, tags=["telemetry"])
app.include_router(benchmark.router, prefix=settings.API_V1_STR, tags=["benchmark"])
app.include_router(trading.router, prefix=settings.API_V1_STR, tags=["trading"])
app.include_router(integration.router, prefix=settings.API_V1_STR, tags=["integration"])


@app.get("/")
async def root():
    return {"message": "Welcome to Enal AI OS", "docs": "/docs", "version": settings.VERSION}
