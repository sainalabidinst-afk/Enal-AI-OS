from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import chat, health, orchestrator_v2, phase3, ecosystem, capability_discovery, execution, workspace, artifact, model_gateway, notifications, attachments, telemetry, benchmark, trading
from .core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="AI Operating System - Multi-Agent AI Platform",
)

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


@app.get("/")
async def root():
    return {"message": "Welcome to Enal AI OS", "docs": "/docs", "version": settings.VERSION}
