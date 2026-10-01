# RFC-0024: Cross-Domain Knowledge Graph Generator

|Bidang|Nilai|
|-------|-------|
|**ID RFC**|RFC-0024|
|**Status**|Draft|
|**Versi**|0.1.0|
|**Penulis**|Tim Inti AI OS Akhir|
|**Target Rilis**|v2.1.0 (Fase Keunggulan Kemampuan +)|
|**Capability Pack**|Cross-Domain Graph|
|**ID Kemampuan**|`cross-domain-graph`|
|**Kategori**|Pengetahuan / Cognitive|
|**Target Kualitas**|A+ (≥95)
|**Target Kematangan**|Level 4 — Domain Expert (L4)|
|**Referensi RFC**|RFC-0024; berelasi dengan RFC-0015 (AI Engineer), RFC-0011 (System Architect)|

---

## Ringkasan

Capability Pack Cross-Domain Knowledge Graph Generator ("The Connector") secara otomatis memindai semua lapisan Memory (Knowledge, Episodic, Project, Long-term) dan memetakan hubungan entitas lintas domain dalam bentuk Graph Database. Sistem ini mengubah ECP dari sistem retrieval menjadi sistem koneksi antar-disiplin ilmu.

---

## Motivasi

Saat ini, ECP memiliki banyak Memory (Knowledge, Episodic, Project) yang tersebar di 7 lapisan berbeda:

- **Working Memory** — konteks percakapan saat ini
- **Conversation Memory** — riwayat percakapan
- **Knowledge Memory** — pengetahuan domain yang terstruktur
- **Episodic Memory** — pengalaman proyek sebelumnya
- **Long-term Memory** — konsolidasi pengetahuan
- **Session Memory** — konteks sesi
- **Project Memory** — artefak dan memori proyek

Namun, koneksi antar pengetahuan ini masih perlu dilakukan secara manual melalui prompting. Jika pengguna bertanya soal "Marketing Digital," sistem hanya menarik dari Knowledge Base Marketing. Dengan modul ini, sistem dapat mengatakan:

> "Berdasarkan data Episodic Memory (proyek kuartal lalu) yang berkaitan dengan 'Budgeting' dan Knowledge Base tentang 'Tren Konsumen X', saya sarankan fokus ke strategi pemasaran A karena ada korelasi Y."

Tanpa modul ini, kemampuan lintas-domain tetap terbatas — pengetahuan tidak dapat saling terhubung secara otomatis.

---

## Pernyataan Masalah

| Aspek | Keterbatasan Saat Ini | Dampak |
|-------|---------------------|--------|
| Cross-memory search | `cross_session_search` hanya pencarian linear | Hubungan antar memori tidak terdeteksi |
| Knowledge Graph | `knowledge/graph.py` hanya untuk Knowledge Memory | Tidak menghubungkan Knowledge, Episodic, Project |
| Semantic Graph | `semantic_graph.py` hanya untuk workspace/project | Tidak lintas domain atau memori |
| Entitas lintas domain | Tidak ada mekanisme entitas-resolver lintas memori | Duplikasi dan kontradiksi tidak terdeteksi |
| Korelasi otomatis | Harus dilakukan manual via prompt | Keandalan dan coverage rendah |

---

## Tujuan

1. **Memory Layer Scanning** — Memindai semua 7 lapisan memory untuk entitas dan relasi
2. **Cross-Domain Entity Resolution** — Mengidentifikasi entitas yang sama di berbagai domain/memori
3. **Graph Database Generation** — Membangun dan memelihara struktur graph node-edge
4. **Cross-Domain Relationship Discovery** — Mendeteksi korelasi, ketergantungan, dan kontradiksi
5. **Inference Engine** — Menjawab pertanyaan lintas domain berdasarkan graph
6. **Explainability** — Menyajikan jejak hubungan entitas ke pengguna

### Kriteria Keberhasilan

| Metrik | Target | Nilai |
|--------|--------|-------|
| Entitas yang terdeteksi | Minimum entitas unik di semua lapisan | ≥50 entitas |
| Resolusi lintas domain | Akurasi identifikasi entitas yang sama | ≥90% |
| Relasi yang ditemukan | Relasi yang valid terdeteksi | ≥80% presisi |
| Inferensi jawaban | Pertanyaan lintas domain berhasil dijawab | ≥85% |
| Update graph | Latency pembaharuan graph setelah memori berubah | < 30 detik |
| Explainability | Jejak hubungan entitas | ≥95% |

---

## Non-Tujuan

1. **Mengganti Knowledge Graph yang ada** — Ini adalah layer di atas graph yang ada, bukan penggantian
2. **Modifikasi Core** — Semua implementasi di dalam Capability Pack
3. **Real-time streaming** — Graph diperbarui secara periodik, bukan real-time konstan
4. **Mengganti pencarian vektor** — Tetap menggunakan pencarian yang ada; graph adalah layer interpretasi

---

## Ruang Lingkup Kapabilitas

### Kapabilitas Inti

| Kapabilitas | Deskripsi | Masukan | Keluaran |
|-------------|-----------|---------|---------|
| Memory Scanner | Memindai semua lapisan memory untuk entitas | Memory layer names, scan interval | ExtractedEntities |
| Entity Resolver | Mengidentifikasi entitas duplikat di domain berbeda | ExtractedEntities | ResolvedEntityGraph |
| Edge Extractor | Mengekstrak relasi antar entitas | ResolvedEntityGraph | GraphEdges |
| Graph Builder | Membangun dan memelihara struktur graph | ResolvedEntityGraph, GraphEdges | CrossDomainGraph |
| Inference Engine | Menjawab pertanyaan berdasarkan graph | User query, graph context | InferenceResult |
| Relationship Explorer | Menjelajah dan menjelaskan hubungan | Entity ID, depth limit | RelationshipPath |

---

## Kontrak Publik

### Kontrak Masukan: GraphQueryRequest

```json
{
  "request_id": "uuid",
  "query": "string — natural language cross-domain question",
  "source_domains": ["trading", "network", "code"],
  "target_memory_layers": ["knowledge", "episodic", "project", "longterm"],
  "max_depth": 3,
  "include_explanations": true
}
```

### Kontrak Keluaran: GraphQueryResult

```json
{
  "request_id": "uuid",
  "answer": "string — synthesized cross-domain answer",
  "entities_discovered": [{"id": "string", "name": "string", "domain": "string", "layer": "string"}],
  "relationships": [{"source": "entity_id", "target": "entity_id", "relation": "string", "confidence": 0.0}],
  "explanation": {
    "reasoning_chain": ["string"],
    "evidence_sources": [{"layer": "string", "entity_id": "string"}],
    "correlation_found": "string"
  },
  "confidence": 0.0,
  "graph_snapshot": {"nodes": [], "edges": []}
}
```

---

## Titik Integrasi

### Cognitive Pipeline Integration

Cross-Domain Graph dapat dipanggil sebagai tugas:

```json
{
  "domain": "knowledge",
  "intent": "Discover cross-domain relationships for: [user query]",
  "payload": {"query": "...", "source_domains": [...]
}
```

### Memory Layer Integration

Berinteraksi dengan `memory_manager` melalui kontrak MemoryContract (ADR-004 / REF-001):

```python
# Scan semua lapisan memory
for layer in ["knowledge", "episodic", "project", "longterm", "session", "conversation"]:
    entries = await memory_manager.search(layer, query, limit=100)
    entities = entity_extractor.extract(entries)
```

---

## Ketergantungan

### Dependensi Internal (Kontrak Bersama)

1. **Memory Manager** — Akses ke semua lapisan memory (ADR-010, ADR-011)
2. **Knowledge Graph** — Struktur graph dasar dari `backend.app.core.knowledge`
3. **Model Router** — LLM untuk entity extraction dan relationship inference
4. **Execution Runtime** — Task routing (ADR-002)

### Tidak Ada Perubahan Inti yang Diperlukan

```text
apps/
└── cross_domain_graph/
    ├── __init__.py              # App class + factory
    ├── engine.py                # Domain Engine
    ├── worker.py                # Thin adapter
    ├── schemas.py               # Public contracts
    ├── memory_scanner.py        # Scans all memory layers
    ├── entity_resolver.py       # Cross-domain entity resolution
    ├── edge_extractor.py        # Relationship extraction
    ├── graph_builder.py         # Graph construction & maintenance
    ├── inference_engine.py      # Cross-domain Q&A
    └── relationship_explorer.py # Path traversal & explanation
```

**Dampak ADR:** Tidak ada. Capability Pack baru, tidak memodifikasi Core.

---

## Spesifikasi Benchmark

| Dimensi | Definisi | Target |
|---------|----------|--------|
| Coverage | Entitas yang terdeteksi | ≥50 entitas |
| Entity Resolution Accuracy | Akurasi entitas yang sama | ≥90% |
| Edge Precision | Relasi valid yang terdeteksi | ≥80% |
| Inference Accuracy | Jawaban pertanyaan lintas domain | ≥85% |
| Graph Update Latency | Waktu update setelah memori berubah | < 30 detik |
| Explainability | Jejak hubungan | ≥95% |

---

## Definisi Selesai

```text
Definition of Done — Cross-Domain Knowledge Graph Capability Pack

Functional
- [ ] Memory Scanner: scans all 7 memory layers
- [ ] Entity Resolver: cross-domain entity resolution with ≥90% accuracy
- [ ] Edge Extractor: relationship extraction (causation, correlation, dependency)
- [ ] Graph Builder: persistent graph with add/update/delete
- [ ] Inference Engine: cross-domain Q&A with explanation
- [ ] Relationship Explorer: path traversal and explanation

Benchmark
- [ ] Entity resolution ≥ 90%
- [ ] Edge precision ≥ 80%
- [ ] Inference accuracy ≥ 85%
- [ ] Graph update latency < 30 seconds

Golden Tests
- [ ] 10 skenario golden test lulus pada ≥90%
- [ ] Single-domain entity extraction
- [ ] Cross-domain entity resolution
- [ ] Relationship extraction from evidence
- [ ] Cross-domain Q&A inference
- [ ] Graph persistence and update
- [ ] Circular dependency detection

Real Cases
- [ ] ≥5 real cases in real_cases/cross_domain_graph/
- [ ] Cases involving multiple capability pack domains

Documentation
- [ ] docs/capabilities/cross-domain-graph.md
- [ ] API reference / contract
- [ ] Integration guide
```

---

## Linimana

### Fase 1: Prototipe (RFC → Eksperimental)

**Durasi:** 3 minggu

- [ ] Struktur paket `apps/cross_domain_graph/`
- [ ] Memory Scanner untuk 3 lapisan (knowledge, episodic, project)
- [ ] Entity Resolver (basic name + description matching)
- [ ] Edge Extractor (keyword/LLM-based relationship)
- [ ] Graph Builder (in-memory + persistence)
- [ ] 5 skenario golden test dasar
- [ ] **Gerbang:** 5/5 golden test lulus ≥80%

### Fase 2: Kapabilitas Lengkap (Eksperimental → Stabil)

**Durasi:** 4 minggu

- [ ] Memory Scanner untuk semua 7 lapisan
- [ ] Entity Resolver dengan embedding similarity
- [ ] Edge Extractor dengan LLM inference
- [ ] Inference Engine untuk cross-domain Q&A
- [ ] Relationship Explorer dengan path traversal
- [ ] 10 skenario golden test lengkap
- [ ] ≥10 real cases
- [ ] **Gerbang:** Semua golden test lulus ≥90%; Benchmark ≥90%

### Fase 3: Ekosistem (Stabil → Bersertifikat)

**Durasi:** 6 minggu

- [ ] Integration dengan Decision Intelligence, Trading Analyst, System Architect
- [ ] Real-time graph update (event-driven)
- [ ] Visualisasi graph (export to JSON for frontend)
- [ ] Audit independen
- [ ] **Gerbang:** RFC, Benchmark ≥90%, Golden Test 100%, Real Cases ≥10

---

## Risiko

|Risiko|Dampak|Kemungkinan|Mitigasi|
|------|------|-----------|--------|
|Entity resolution false positives|Hubungan yang salah|Medium|Confidence threshold, user review|
|Graph ukuran besar|Memory dan latency|Medium|Pagination, lazy loading, TTL|
|Relationship extraction noise|False positives|High|Confidence scoring, precision filtering|
|Memory layer coupling|Tight coupling|Low|Gunakan kontrak bersama, tidak import langsung|
|Performance pada scan penuh|Latency tinggi|Medium|Incremental scan, caching|

---

## Dampak ADR

**Apakah ini memerlukan perubahan Core?** Tidak.

Cross-Domain Knowledge Graph adalah Capability Pack baru:

- **ADR-001 (Core Pipeline Freeze):** Tidak ada perubahan Core.
- **ADR-002 (Capability Pack Independence):** Berkomunikasi melalui Execution Runtime dan kontrak bersama.
- **ADR-003 (Worker = Adapter):** Worker tipis.
- **ADR-004 (Domain Engine Owns Business Logic):** Logika di `engine.py`.
- **ADR-005 (Human Approval Required):** Graph adalah alat bantu; keputusan akhir memerlukan persetujuan.
- **ADR-006 (Capability Contract v1):** Menggunakan kontrak yang ada.
- **ADR-007 (Conversation Boundary):** Dipanggil melalui Execution Runtime.
- **ADR-008 (Core Change Requires Cross-Capability Proof):** Tidak ada perubahan Core.

**ADR yang diperlukan:** Tidak ada. Ini adalah Capability Pack baru.
