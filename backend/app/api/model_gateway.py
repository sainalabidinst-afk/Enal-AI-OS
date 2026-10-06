from fastapi import APIRouter
from pydantic import BaseModel

from backend.app.core.model_gateway import model_gateway

router = APIRouter(prefix="/models")


class ModelRouteRequest(BaseModel):
    taskType: str = ""
    capability: str = ""
    context: dict | None = None


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
    return await model_gateway.get_status()


@router.post("/route")
async def route_model(payload: ModelRouteRequest):
    return await model_gateway.route(
        task_type=payload.taskType,
        capability=payload.capability,
        context=payload.context,
    )
