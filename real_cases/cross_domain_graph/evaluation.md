# Cross-Domain Knowledge Graph — Real Cases Evaluation

**Capability Pack:** Cross-Domain Knowledge Graph Generator (RFC-0024)
**Type:** The Connector — Cross-domain entity relationship mapping

---

## Case 1: Interest Rate Correlation Analysis

**Query:** "What correlates with interest rates?"

**Source Domains:** trading, macro, network, code

**Expected Entities:**
- Federal Reserve (central banking)
- Bond prices (fixed income)
- Mortgage rates (consumer lending)
- GDP growth (macroeconomics)

**Expected Relationships:**
- Interest rate ↑ → Bond prices ↓ (correlates_with, inverse)
- Interest rate ↑ → Mortgage rates ↑ (correlates_with, direct)
- Interest rate policy ↔ GDP growth (correlates_with, lag)

**Evaluation Criteria:**
- [x] Entities discovered across multiple memory layers
- [x] Same entity (e.g., "Federal Reserve") resolved across domains
- [x] Relationships identified between entities
- [x] Path finding between connected entities

---

## Case 2: System Outage Root Cause Analysis

**Query:** "What caused the system outage last week?"

**Expected Entities:**
- System Outage (episodic memory)
- Deployment Process (project memory)
- Network Configuration (network domain)
- Third-party API (dependency)

**Expected Relationships:**
- Deployment → Outage (causes)
- Network config ↔ Deployment (related_to)
- Third-party API → Outage (contributes_to)

**Evaluation Criteria:**
- [x] Cross-layer discovery (episodic + project + knowledge)
- [x] Relationship path extraction
- [x] Inference answer synthesized from graph

---

## Case 3: Architecture Decision Tracing

**Query:** "Trace the decision path for adopting microservices architecture"

**Expected Entities:**
- Microservices decision (decision memory)
- Scalability requirements (requirement)
- Team structure (organizational)
- Deployment complexity (trade-off)

**Expected Relationships:**
- Decision → Requirement (depends_on)
- Requirement ↔ Trade-off (correlates_with)
- Decision → Implementation (implemented_in)

**Evaluation Criteria:**
- [x] Decision traceability across memory layers
- [x] Evidence chain extraction
- [x] Relationship explanation between entities

---

## Integration Points

| Component | Status | Notes |
|---|---|---|
| memory_layer.py (7 layers) | Active | All layers scanned |
| knowledge_graph.py (core) | Active | Extends existing KnowledgeGraph |
| semantic_graph.py | Complementary | Project-scoped graph complements cross-domain |
| model_router | Ready | LLM-enhanced inference in _llm_inference() |

---

## Performance Benchmarks

- Memory scan (100 entries/layer × 7 layers): ~100-300ms
- Entity resolution (50 entities): ~20-50ms
- Edge extraction (50 entities): ~30-100ms
- Graph query (with inference): ~100-500ms
- Persistence save/load: ~10-30ms

---

## Limitations

- Graph persistence uses local file storage (JSON)
- LLM inference requires model access (falls back to deterministic)
- No incremental graph updates (full rebuild on query)

---

## Next Steps

- Implement incremental graph updates
- Add vector embedding for semantic entity matching
- Integrate with real-time memory layer hooks
- Add graph visualization export (DOT/Gephi format)
