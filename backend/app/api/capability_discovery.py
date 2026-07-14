from fastapi import APIRouter
from apps.organization.capability_graph import capability_graph
from apps.society.intent_router import intent_router
import logging

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/capabilities")
async def list_capabilities():
    nodes = [capability_graph.get_capability_node(cap_id) for cap_id in capability_graph.get_all_capabilities()]
    capabilities = []
    for node in nodes:
        if node is None:
            continue
        related = capability_graph.get_related_capabilities(node.capability_id)
        capabilities.append({
            "id": node.capability_id,
            "name": node.name,
            "description": node.description,
            "skills": node.required_skills,
            "dependencies": node.dependencies,
            "complexity": node.estimated_complexity,
            "tags": node.tags,
            "related_capabilities": related,
        })
    domains = []
    for domain, pack in intent_router._capability_packs.items():
        domains.append({
            "domain": domain.value,
            "capabilities": pack.capabilities,
            "workers": pack.workers,
            "description": pack.description,
        })
    return {
        "capabilities": capabilities,
        "domains": domains,
    }


@router.get("/capabilities/{capability_id}")
async def get_capability(capability_id: str):
    node = capability_graph.get_capability_node(capability_id)
    if node is None:
        return {"error": f"Capability '{capability_id}' not found"}
    related = capability_graph.get_related_capabilities(capability_id)
    subtasks = capability_graph.get_subtask_templates(domain=node.tags[0]) if node.tags else []
    return {
        "id": node.capability_id,
        "name": node.name,
        "description": node.description,
        "skills": node.required_skills,
        "dependencies": node.dependencies,
        "complexity": node.estimated_complexity,
        "tags": node.tags,
        "related_capabilities": related,
        "subtask_templates": [
            {
                "id": t.subtask_id,
                "name": t.name,
                "description": t.description,
                "required_skills": t.required_skills,
                "produces_artifact": t.produces_artifact,
                "estimated_duration_minutes": t.estimated_duration_minutes,
                "priority": t.priority,
            }
            for t in subtasks
        ],
    }
