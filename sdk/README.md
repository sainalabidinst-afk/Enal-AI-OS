# SDK Enal Cognitive Platform (ECP)

<!-- DOCUMENT_METADATA_START -->
**Pemilik:** Tim Dokumentasi
**Pemilik Canonical:** Pimpinan Tata Kelola Dokumentasi
**Terakhir Diverifikasi:** 2026-08-02
**Versi:** 1.0.0
**Status:** Aktif
**SSOT:** Ikhtisar proyek
<!-- DOCUMENT_METADATA_END -->

SDK Developer untuk membangun agen, tool, dan workflow di atas ECP.

## Instalasi

```bash
pip install -e .
```

## Status: Platform RC (2026-07-27)
- Runtime: 426 test lulus
- Architecture: 92/100 - Cognitive pipeline terintegrasi

## Quick Start

### Membuat Agent

```python
from enal_ai import Agent, EnalAI

enal = EnalAI()

class MikrotikAgent(Agent):
    name = "mikrotik"
    description = "Mikrotik network configuration"
    capabilities = ["networking", "mikrotik", "firewall"]
    model = "gpt-4o"
    temperature = 0.3

    async def execute(self, task: str, context: dict | None = None) -> str:
        # Your custom logic here
        return f"Configured: {task}"

agent = MikrotikAgent()
result = await agent.run("Configure hotspot with 3 VLANs")
print(result)
```

### Membuat Tool

```python
from enal_ai import Tool

@enal.tool(name="docker_build", description="Build Docker image")
async def docker_build(dockerfile_path: str, image_name: str):
    # Your tool logic
    return {"status": "built", "image": image_name}
```

### Membuat Workflow

```python
from enal_ai import Workflow, WorkflowStep

workflow = Workflow(
    name="erp-build",
    description="Build ERP system",
    steps=[
        WorkflowStep(id="1", name="Requirements", agent="analyst", action="analyze"),
        WorkflowStep(id="2", name="Backend", agent="backend-dev", action="build_backend", depends_on=["1"]),
        WorkflowStep(id="3", name="Frontend", agent="frontend-dev", action="build_frontend", depends_on=["1"]),
        WorkflowStep(id="4", name="Deploy", agent="devops", action="deploy", depends_on=["2", "3"]),
    ],
)

result = await workflow.execute({"project_id": "erp-001"})
```

## Referensi API

### Agent

```python
class Agent:
    config: AgentConfig
    async def execute(self, task: str, context: dict | None = None) -> str
    async def run(self, task: str, context: dict | None = None) -> dict
    def to_dict(self) -> dict
```

### Tool

```python
class Tool:
    config: ToolConfig
    async def invoke(self, parameters: dict) -> dict
    def to_dict(self) -> dict
```

### Workflow

```python
class Workflow:
    config: WorkflowConfig
    async def execute(self, context: dict | None = None) -> dict
    def to_dict(self) -> dict
```

### EnalAI (Titik Masuk SDK)

```python
enal = EnalAI(api_url="http://localhost:8000")

# Register agents
enal.agent("my-agent")(MyAgentClass)

# Register tools
enal.tool("my-tool")(my_tool_function)

# Register workflows
enal.workflow("my-workflow")(MyWorkflowClass)

# List registered
enal.list_agents()
enal.list_tools()
enal.list_workflows()
```

## Kontrak

Semua komponen menerapkan kontrak yang stabil:

- `CapabilityContract` — Kapabilitas Agent
- `ToolContract` — Invokasi Tool
- `ArtifactContract` — Manajemen Artifact
- `MemoryContract` — Operasi Memory
- `WorkflowContract` — Eksekusi Workflow
- `WorldModelContract` — Kueri World Model
- `LearningContract` — Operasi Learning

## Contoh

Lihat direktori `examples/`:
- `custom_agent.py` — Membuat custom agent
- `custom_workflow.py` — Membangun workflow

## Dokumentasi

Lihat direktori `docs/` untuk:
- Getting Started Guide
- Agent Development Guide
- Tool Development Guide
- Workflow Design Guide
- API Reference

