# RFC-0046: Visual Builder Foundation

<!-- DOCUMENT_METADATA_START -->
**Pemilik:** Tim Frontend Platform
**Canonical Owner:** Lead Platform Engineer
**Terakhir Diverifikasi:** 2026-10-03
**Versi:** 1.0.0
**Status:** Draft → Proposed
**SSOT:** Rancangan fondasi visual builder untuk ECP: canvas, node types, toolbar, schema blueprints, dan API persistensi
<!-- DOCUMENT_METADATA_END -->

## Abstrak

RFC ini mendefinisikan fondasi visual builder untuk Enal Cognitive Platform (ECP), yang memungkinkan pembuatan agent dan tool melalui antarmuka drag-drop. Fondasi ini mencakup ReactFlow canvas, node types yang dapat diperluas, toolbar palette, schema blueprints, dan API persistensi.

## Konteks

ECP memerlukan cara visual untuk membuat dan mengedit agent/tool tanpa menulis kode. SimplAI dan platform sejenis menawarkan visual builder sebagai fitur utama. ECP sudah memiliki pipeline engine dan decorator SDK, tetapi belum memiliki UI visual untuk merakit kemampuan tersebut.

## Keputusan

### 1. ReactFlow sebagai Canvas Engine

Gunakan `reactflow` library untuk infinite canvas dengan pan/zoom, snap-to-grid, dan edge routing.

**Alasan:**
- Mature library (11k+ stars, production-ready)
- Built-in support untuk custom nodes/edges
- TypeScript support excellent
- Performa baik untuk 50-100 nodes

### 2. Node Types

Tipe node yang didukung:

| Node Type | Warna | Purpose |
|-----------|-------|---------|
| `agent` | Biru | Agent configuration node |
| `tool` | Hijau | Tool step node |
| `knowledgeBase` | Ungu | Knowledge base attachment |
| `conditional` | Oranye | If/else branching |
| `delay` | Abu-abu | Time delay |

### 3. Blueprint Schema

```python
class AgentBlueprint(BaseModel):
    id: str
    name: str
    description: str
    model: str
    tools: list[str]
    knowledge_base_ids: list[str]
    prompt: str
    temperature: float
    max_tokens: int
    metadata: dict[str, Any]

class ToolBlueprint(BaseModel):
    id: str
    name: str
    description: str
    steps: list[ToolStep]
    branches: list[ConditionalBranch]
    metadata: dict[str, Any]
```

### 4. API Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/api/v1/blueprints/agent` | Create agent blueprint |
| GET | `/api/v1/blueprints/agent` | List agent blueprints |
| GET | `/api/v1/blueprints/agent/{id}` | Get agent blueprint |
| PUT | `/api/v1/blueprints/agent/{id}` | Update agent blueprint |
| DELETE | `/api/v1/blueprints/agent/{id}` | Delete agent blueprint |
| POST | `/api/v1/blueprints/tool` | Create tool blueprint |
| GET | `/api/v1/blueprints/tool` | List tool blueprints |
| GET | `/api/v1/blueprints/tool/{id}` | Get tool blueprint |
| PUT | `/api/v1/blueprints/tool/{id}` | Update tool blueprint |
| DELETE | `/api/v1/blueprints/tool/{id}` | Delete tool blueprint |

### 5. Persistence

Blueprint disimpan di JSON file (`data/blueprints/`) untuk development. Production akan migrasi ke PostgreSQL via existing database layer.

## Implementasi

### Frontend Components

- `BuilderCanvas.tsx` — Main canvas dengan ReactFlow
- `BuilderToolbar.tsx` — Toolbar dengan draggable node palette
- `AgentNode.tsx` — Agent node component
- `ToolNode.tsx` — Tool node component
- `KnowledgeBaseNode.tsx` — KB node component
- `ConditionalNode.tsx` — If/else node dengan 2 output handles
- `DelayNode.tsx` — Delay node component

### Backend Modules

- `backend/app/core/schemas.py` — AgentBlueprint, ToolBlueprint, ToolStep, ConditionalBranch
- `backend/app/core/blueprint_repository.py` — BlueprintRepository untuk persistensi JSON
- `backend/app/api/blueprints.py` — CRUD endpoints

## Dependencies

- `reactflow` — Canvas engine
- Existing: `fastapi`, `pydantic`, `react`

## Risks

1. **Complexity:** Visual builders kompleks; mulai dengan MVP
2. **Performance:** Canvas dengan banyak nodes bisa lambat; reactflow sudah optimize
3. **State Management:** Gunakan React state + props untuk MVP, bisa ditambah Zustand jika perlu

## Testing

- TypeScript: 0 errors
- Ruff: 0 errors
- Mypy: 0 errors
- Backend tests: 3 passed

## References

- SimplAI: https://simplai.ai/docs/agents/
- ReactFlow: https://reactflow.dev/
