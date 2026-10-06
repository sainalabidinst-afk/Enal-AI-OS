from __future__ import annotations

import logging
from typing import Any

from fastapi import APIRouter, HTTPException

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/settings/api-keys")
async def list_api_keys() -> dict[str, Any]:
    return {"keys": []}


@router.post("/settings/api-keys")
async def create_api_key(payload: dict[str, Any]) -> dict[str, Any]:
    name = payload.get("name", "")
    scope = payload.get("scope", "")
    return {"id": "key-new", "name": name, "scope": scope, "created_at": ""}


@router.delete("/settings/api-keys/{key_id}")
async def delete_api_key(key_id: str) -> dict[str, Any]:
    return {"deleted": key_id}


@router.get("/search")
async def search(q: str = "") -> dict[str, Any]:
    return {"query": q, "results": []}
