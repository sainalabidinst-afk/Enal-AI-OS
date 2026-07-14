from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health():
    return {"status": "ok", "service": "enal-ai-os", "version": "0.1.0"}


@router.get("/agents")
async def list_agents():
    return {
        "agents": [
            {"name": "planner", "role": "Plans and decomposes tasks"},
            {"name": "coding-agent", "role": "Writes and reviews code"},
            {"name": "research-agent", "role": "Gathers information"},
            {"name": "data-agent", "role": "Handles databases and data"},
            {"name": "ui-agent", "role": "Designs and builds UIs"},
            {"name": "trading-agent", "role": "Analyzes markets and trades"},
            {"name": "network-agent", "role": "Configures networking"},
            {"name": "writer-agent", "role": "Creates documentation"},
            {"name": "qa-agent", "role": "Tests and validates"},
            {"name": "security-agent", "role": "Audits security"},
            {"name": "reviewer", "role": "Reviews and merges results"},
        ]
    }
