from fastapi import APIRouter
from backend.app.core.model_gateway import model_gateway

router = APIRouter()


@router.get("/health")
async def model_health(provider: str | None = None):
    if provider:
        return await model_gateway.health_check(provider)
    providers = {}
    for p in list(model_gateway._providers.keys()):
        providers[p] = await model_gateway.health_check(p)
    return providers


@router.get("/providers")
async def list_providers():
    return model_gateway.get_status()


@router.post("/route")
async def route_model(task_type: str, capability: str, context: dict | None = None):
    return await model_gateway.route(task_type, capability, context)
