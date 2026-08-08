from fastapi import APIRouter, HTTPException

from backend.app.core.distributed_runtime import NodeCapability, distributed_runtime
from backend.app.core.plugin_marketplace import PluginManifest, PluginStatus, plugin_marketplace
from backend.app.studio.ai_studio import ai_studio

router = APIRouter()


@router.get("/studio/traces/{trace_id}")
async def studio_get_trace(trace_id: str):
    return await ai_studio.get_trace(trace_id)


@router.get("/studio/metrics")
async def studio_get_metrics(agent: str | None = None):
    return await ai_studio.get_metrics(agent=agent)


@router.get("/studio/artifacts/{project_id}")
async def studio_get_artifacts(project_id: str):
    return await ai_studio.get_artifacts(project_id)


@router.get("/studio/graph/{project_id}")
async def studio_get_graph(project_id: str):
    return await ai_studio.get_graph(project_id)


@router.get("/studio/memory")
async def studio_get_memory(layer: str, query: str, limit: int = 10):
    return await ai_studio.get_memory(layer, query, limit)


@router.get("/studio/reputation")
async def studio_get_reputation():
    return await ai_studio.get_reputation()


@router.get("/studio/cognitive/services")
async def studio_get_cognitive_services():
    return await ai_studio.get_cognitive_services()


@router.get("/studio/cognitive/pipelines")
async def studio_get_pipeline_presets():
    return await ai_studio.get_pipeline_presets()


@router.get("/studio/cognitive/meta/metrics")
async def studio_get_meta_metrics():
    return await ai_studio.get_meta_metrics()


@router.get("/studio/export/{project_id}")
async def studio_export_project(project_id: str):
    return await ai_studio.export_project(project_id)


@router.post("/marketplace/publish")
async def marketplace_publish(
    plugin_id: str,
    name: str,
    version: str,
    description: str,
    author: str,
    category: str,
    tags: list[str] | None = None,
    permissions: list[str] | None = None,
):
    manifest = PluginManifest(
        id=plugin_id,
        name=name,
        version=version,
        description=description,
        author=author,
        category=category,
        tags=tags or [],
        permissions=permissions or [],
    )
    await plugin_marketplace.publish(manifest)
    return {"published": True, "plugin_id": plugin_id}


@router.get("/marketplace/plugins")
async def marketplace_list_plugins(category: str | None = None, status: str | None = None):
    plugin_status = PluginStatus(status) if status else None
    plugins = plugin_marketplace.list_plugins(category=category, status=plugin_status)
    return [
        {
            "id": p.id,
            "name": p.name,
            "version": p.version,
            "description": p.description,
            "downloads": p.downloads,
            "rating": p.rating,
        }
        for p in plugins
    ]


@router.get("/marketplace/plugins/search")
async def marketplace_search(query: str):
    plugins = plugin_marketplace.search(query)
    return [
        {
            "id": p.id,
            "name": p.name,
            "version": p.version,
            "description": p.description,
        }
        for p in plugins
    ]


@router.post("/marketplace/install/{plugin_id}")
async def marketplace_install(plugin_id: str):
    success = await plugin_marketplace.install(plugin_id)
    return {"installed": success, "plugin_id": plugin_id}


@router.post("/marketplace/uninstall/{plugin_id}")
async def marketplace_uninstall(plugin_id: str):
    success = await plugin_marketplace.uninstall(plugin_id)
    return {"uninstalled": success, "plugin_id": plugin_id}


@router.get("/marketplace/installed")
async def marketplace_installed():
    return {"installed": plugin_marketplace.get_installed()}


@router.post("/distributed/nodes")
async def distributed_register_node(name: str, capabilities: list[str]):
    caps = [NodeCapability(c) for c in capabilities if c in [e.value for e in NodeCapability]]
    node_id = await distributed_runtime.register_node(name, caps)
    return {"node_id": node_id, "name": name}


@router.get("/distributed/cluster")
async def distributed_cluster_status():
    return await distributed_runtime.get_cluster_status()


@router.get("/distributed/nodes/{node_id}")
async def distributed_get_node(node_id: str):
    node = await distributed_runtime.get_node(node_id)
    if not node:
        raise HTTPException(status_code=404, detail="Node not found")
    return {
        "id": node.id,
        "name": node.name,
        "capabilities": [c.value for c in node.capabilities],
        "status": node.status.value,
    }
