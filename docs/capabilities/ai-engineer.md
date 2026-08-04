# AI Engineer — Spesifikasi Capability

**Versi:** 1.0.0
**Status:** Draft (RFC-0015)
**Target Kualitas:** A+ (≥95)

---

## 1. Tujuan

AI Engineer adalah **otoritas rekayasa AI** untuk ECP — Capability Pack yang menerjemahkan kebutuhan produk (akurasi, latensi, biaya) menjadi spesifikasi arsitektur AI yang dapat dieksekusi, dievaluasi, dan dioperasikan secara produksi untuk agent, RAG, prompt engineering, dan LLMOps.

Capability Pack ini merancang arsitektur agent, konfigurasi RAG, template prompt, dan setup LLMOps — **tanpa memodifikasi Core**.

---

## 2. Ruang Lingkup

### Dalam Ruang Lingkup
- **Agent Design** — Arsitektur single/multi-agent, orchestration, tool specification
- **RAG Engine Design** — Chunking strategies, embedding models, vector stores, reranking
- **Prompt Engineering** — Template design, chain-of-thought, optimization strategies
- **LLMOps Setup** — Deployment configuration, monitoring, fine-tuning pipelines, evaluation
- **AI Assessment** — Gap analysis dan rekomendasi arsitektur AI
- **Evaluation Frameworks** — Accuracy, faithfulness, hallucination rate, latency metrics
- **Cost Estimation** — Biaya token dan infrastruktur AI
- **Guardrails & Safety** — Konfigurasi guardrail untuk output yang aman

### Di Luar Cakupan
- Pelatihan model fundamental dari nol
- Pengumpulan dan labeling dataset
- Eksekusi inference real-time
- Penelitian AI baru (paper, algoritma)
- Modifikasi kontrak Core

---

## 3. Kontrak

### Input: AIEngineerRequest
```json
{
  "request_id": "uuid",
  "operation": "agent_design | rag_engine_design | prompt_engineering | llmops_setup | ai_assessment",
  "business_context": {
    "domain": "trading | research | healthcare",
    "project_name": "string",
    "description": "string"
  },
  "quality_attributes": {
    "accuracy_target": "95%",
    "latency_target": "< 500ms",
    "availability_target": "99.9%",
    "cost_per_1k_tokens": 0.01
  },
  "output_format": "json | markdown | yaml",
  "inputs": {
    "architecture": "single_agent | multi_agent | hierarchical | swarm | pipeline",
    "orchestration": "sequential | concurrent | conditional | human_in_loop | reflection",
    "llm_provider": "openai | anthropic | google | mistral | local",
    "model": "gpt-4o",
    "rag_strategy": "naive | chunked | hybrid | graph | agentic",
    "task_type": "general | code | analysis | rag | agentic"
  }
}
```

### Output: AIEngineerReport
```json
{
  "request_id": "uuid",
  "operation": "string",
  "agent_spec": {
    "name": "trading-agent",
    "architecture": "multi_agent",
    "orchestration": "sequential",
    "llm_provider": "openai",
    "model": "gpt-4o",
    "temperature": 0.3,
    "tools": [{"name": "web_search", "description": "Search web"}],
    "system_prompt": "string",
    "guardrails": ["string"],
    "context_window": 128000
  },
  "rag_config": {
    "strategy": "hybrid",
    "chunk_size": 512,
    "embedding_model": "text-embedding-3-small",
    "vector_store": "pinecone",
    "top_k": 5,
    "rerank_enabled": true
  },
  "prompt_templates": [
    {
      "name": "analysis_assistant",
      "template": "string",
      "variables": ["analysis_type", "data"],
      "expected_output_format": "json"
    }
  ],
  "deployment_config": {
    "environment": "production",
    "scaling_min": 3,
    "scaling_max": 20,
    "gpu_enabled": false,
    "rate_limit_rpm": 100
  },
  "monitoring_config": {
    "metrics_enabled": true,
    "tracing_enabled": true,
    "alert_on_latency_p95": "1000ms"
  },
  "evaluation_results": {
    "accuracy": 0.92,
    "faithfulness": 0.88,
    "hallucination_rate": 0.05
  },
  "cost_estimate": {"total_monthly": 150.0},
  "recommendations": ["string"],
  "quality_score": 0.95,
  "explanation": "string"
}
```

---

## 4. Operasi

| Operasi | Deskripsi | Input | Output |
|-----------|-------------|--------|---------|
| `agent_design` | Desain arsitektur agent | Kebutuhan tugas, domain, tools | AgentSpec |
| `rag_engine_design` | Desain konfigurasi RAG | Korpus dokumen, kebutuhan retrieval | RAGConfig |
| `prompt_engineering` | Desain template prompt | Tugas, variabel, format output | PromptTemplate |
| `llmops_setup` | Setup deployment, monitoring, fine-tuning | Target lingkungan, anggaran | DeploymentConfig, MonitoringConfig |
| `ai_assessment` | Penilaian arsitektur AI | Current state, target state | Laporan gap + rekomendasi |

---

## 5. Modul Designer

| Modul | Tanggung Jawab |
|--------|----------------|
| `agent_designer.py` | Desain arsitektur agent, tools, orchestration |
| `rag_engine.py` | Desain konfigurasi RAG, chunking, embedding, retrieval |
| `prompt_engineer.py` | Desain template prompt, chain-of-thought, optimization |
| `llmops_manager.py` | Desain deployment, monitoring, fine-tuning pipelines |

---

## 6. Dimensi Benchmark

| Dimensi | Target | Grade |
|-----------|--------|-------|
| Agent Accuracy | ≥95% | A+ |
| RAG Faithfulness | ≥92% | A+ |
| Hallucination Rate | <5% | A+ |
| Latency P95 | <500ms | A |
| Quality Score | ≥95% | A+ |
| Cost Accuracy | ±10% | A |
| Compliance | ≥95% | A |
| Consistency | ≥95% | A+ |

---

## 7. Dependensi

- **apps/base.py** — Definisi model dasar
- **apps/ai_engineer/schemas.py** — Kontrak publik
- **apps/ai_engineer/engine.py** — Domain engine
- **apps/ai_engineer/worker.py** — Adaptor tipis (ADR-003)

---

## 8. Contoh Penggunaan

```python
from apps.ai_engineer.engine import AIEngineerEngine
from apps.ai_engineer.schemas import AIEngineerRequest, OperationType, BusinessContext

engine = AIEngineerEngine()
request = AIEngineerRequest(
    operation=OperationType.agent_design,
    business_context=BusinessContext(domain="trading", project_name="market-agent"),
    inputs={"architecture": "multi_agent", "orchestration": "sequential", "llm_provider": "openai"},
)
report = engine.design(request)
print(f"Agent: {report.agent_spec.name}")
print(f"Architecture: {report.agent_spec.architecture.value}")
print(f"Quality score: {report.quality_score:.0%}")
```
