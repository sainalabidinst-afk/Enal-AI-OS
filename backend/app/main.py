import logging

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

from .api import (
    a2a_mcp,
    actions,
    artifact,
    attachments,
    auth,
    benchmark,
    blueprints,
    bulk_evaluation,
    capability_discovery,
    capability_execution,
    capability_lifecycle,
    chat,
    ecosystem,
    end_to_end,
    execution,
    governance,
    guardrails,
    health,
    integration,
    marketplace,
    model_gateway,
    notifications,
    orchestrator_v2,
    phase3,
    self_development,
    telemetry,
    trading,
    voice,
    workspace,
)
from .api import (
    consent as consent_api,
)
from .core.config import settings

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

        from backend.app.core.config import settings

        if getattr(settings, "TESTING", False):
            return await call_next(request)
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
        if request.url.path in (
            "/",
            "/docs",
            "/openapi.json",
            "/redoc",
            "/health",
            "/api/v1/auth/login",
            "/api/v1/metrics",
            "/api/v1/capabilities",
        ):
            return await call_next(request)

        auth = request.headers.get("Authorization")
        if not auth or not auth.startswith("Bearer "):
            from fastapi.responses import JSONResponse

            return JSONResponse(
                status_code=401, content={"detail": "Missing or invalid authorization header"}
            )  # noqa: E501

        token = auth.split(" ", 1)[1]
        try:
            from backend.app.api.auth import _decode_token

            _decode_token(token)
        except HTTPException:
            from fastapi.responses import JSONResponse

            return JSONResponse(status_code=401, content={"detail": "Invalid or expired token"})
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
app.include_router(auth.router, prefix=settings.API_V1_STR, tags=["auth"])
app.include_router(chat.router, prefix=settings.API_V1_STR, tags=["chat"])
app.include_router(orchestrator_v2.router, prefix=settings.API_V1_STR, tags=["orchestrator-v2"])
app.include_router(phase3.router, prefix=settings.API_V1_STR, tags=["phase3"])
app.include_router(ecosystem.router, prefix=settings.API_V1_STR, tags=["ecosystem"])
app.include_router(
    capability_discovery.router, prefix=settings.API_V1_STR, tags=["capability-discovery"]
)  # noqa: E501
app.include_router(
    capability_execution.router, prefix=settings.API_V1_STR, tags=["capability-execution"]
)  # noqa: E501
app.include_router(
    capability_lifecycle.router, prefix=settings.API_V1_STR, tags=["capability-lifecycle"]
)  # noqa: E501
app.include_router(execution.router, prefix=settings.API_V1_STR, tags=["execution"])
app.include_router(workspace.router, prefix=settings.API_V1_STR, tags=["workspace"])
app.include_router(artifact.router, prefix=settings.API_V1_STR, tags=["artifact"])
app.include_router(model_gateway.router, prefix=settings.API_V1_STR, tags=["models"])
app.include_router(notifications.router, prefix=settings.API_V1_STR, tags=["notifications"])
app.include_router(attachments.router, prefix=settings.API_V1_STR, tags=["attachments"])
app.include_router(voice.router, prefix=settings.API_V1_STR, tags=["voice"])
app.include_router(actions.router, prefix=settings.API_V1_STR, tags=["actions"])
app.include_router(consent_api.router, prefix=settings.API_V1_STR, tags=["consent"])
app.include_router(telemetry.router, prefix=settings.API_V1_STR, tags=["telemetry"])
app.include_router(benchmark.router, prefix=settings.API_V1_STR, tags=["benchmark"])
app.include_router(trading.router, prefix=settings.API_V1_STR, tags=["trading"])
app.include_router(self_development.router, prefix=settings.API_V1_STR, tags=["self-development"])
app.include_router(integration.router, prefix=settings.API_V1_STR, tags=["integration"])
app.include_router(blueprints.router, prefix=settings.API_V1_STR, tags=["blueprints"])
app.include_router(guardrails.router, prefix=settings.API_V1_STR, tags=["guardrails"])
app.include_router(governance.router, prefix=settings.API_V1_STR, tags=["governance"])
app.include_router(marketplace.router, prefix=settings.API_V1_STR, tags=["marketplace"])
app.include_router(a2a_mcp.router, prefix=settings.API_V1_STR, tags=["a2a-mcp"])
app.include_router(bulk_evaluation.router, prefix=settings.API_V1_STR, tags=["bulk-evaluation"])
app.include_router(end_to_end.router, prefix=settings.API_V1_STR, tags=["end-to-end"])


@app.on_event("startup")
async def register_action_tools_startup():
    """Register action connector tools with ToolRegistry on startup."""
    try:
        from backend.app.connectors.action_tools import register_action_tools

        count = register_action_tools()
        logger.info("Registered %d action tools on startup", count)
    except Exception as e:
        logger.warning("Failed to register action tools on startup: %s", e)


@app.get("/")
async def root():
    return {"message": "Welcome to Enal AI OS", "docs": "/docs", "version": settings.VERSION}
