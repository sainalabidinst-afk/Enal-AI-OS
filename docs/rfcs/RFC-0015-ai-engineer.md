# RFC-0015: Capability Pack AI Engineer

|Bidang|Nilai|
|-------|-------|
|**ID RFC**|RFC-0015|
|**Status**|Draf|
|**Versi**|0.1.0|
|**Penulis**|Tim Inti AI OS Akhir|
|**Target Rilis**|v2.0.0 (fase Platform Professional)|
|**Capability Pack**|AI Engineer|
|**ID Kemampuan**|`ai-engineer`|
|**Kategori**|Kecerdasan Buatan|
|**Target Kualitas**|A+ (≥95)|
|**Target Kematangan**|Level 3 — Siap Produksi|
|**Referensi RFC**|RFC-0015|

---

## Motivasi

AI adalah komponen inti ECP — sistem trading, research, dan orchestration bergantung pada arsitektur AI yang handal. Saat ini:

1. **Tidak ada desain agent terstruktur** — arsitektur agen (single/multi-agent, orchestration) ditentukan ad hoc
2. **Tidak ada konfigurasi RAC terukur** — chunking, embedding, retrieval tidak dioptimalkan
3. **Prompt tidak terstandarisasi** — template prompt dan best practices tidak terdokumentasi
4. **Tidak ada LLMOps terstruktur** — deployment, monitoring, fine-tuning tidak terstandarisasi
5. **Tidak ada evaluasi AI terukur** — akurasi, faithfulness, hallucination rate tidak dievaluasi
6. **Tidak ada estimasi biaya AI** — biaya token dan infrastruktur tidak terprediksi

Capability Pack AI Engineer menjadi otoritas rekayasa AI yang menerjemahkan kebutuhan produk menjadi spesifikasi arsitektur AI yang dapat dieksekusi, dievaluasi, dan dioperasikan secara produksi.

---

## Pernyataan Masalah

Tanpa Capability Pack AI Engineer yang khusus:

- **Agen tidak handal** — arsitektur agen tidak optimal, menyebabkan kegagalan tugas
- **RAG tidak akurat** — retrieval dan generation tidak terkoordinasi
- **Prompt tidak konsisten** — template prompt beragam tanpa standar
- **LLMOps tidak profesional** — deployment, monitoring, dan evaluasi tidak terstandarisasi
- **Biaya AI tidak terprediksi** — biaya token dan infrastruktur melonjak tanpa kendali
- **Evaluasi tidak ada** — metrik akurasi dan faithfulness tidak dievaluasi

## Tujuan

1. **Agent Design** — Merancang arsitektur agent (single/multi-agent, orchestration)
2. **RAG Engine Design** — Merancang konfigurasi RAG (chunking, embedding, vector store)
3. **Prompt Engineering** — Merancang template prompt dan optimization strategies
4. **LLMOps Setup** — Merancang deployment, monitoring, dan fine-tuning pipelines
5. **AI Assessment** — Evaluasi gap dan rekomendasi peningkatan arsitektur AI

### Kriteria Keberhasilan

|Metrik|Target|Nilai|
|--------|--------|-------|
|Akurasi Agent|≥95%|A+|
|Faithfulness RAG|≥92%|A+|
|Halusination Rate|<5%|A+|
|Latensi P95|<500ms|A|
|Skor Kualitas|≥95%|A+|
|Akurasi Estimasi Biaya|±10%|A|
|Kepatuhan|100%|A|
|Konsistensi|≥95%|A+|

---

## Non-Tujuan

1. **Pelatihan model dari nol** — AI Engineer merancang konfigurasi, bukan melatih model dasar
2. **Data labeling** — Persiapan data training adalah tanggung jawab eksternal
3. **Inferensi real-time otomatis** — Desain spesifikasi, bukan menjalankan inference
4. **Penelitian AI baru** — Fokus rekayasa, bukan penelitian
5. **Modifikasi Core** — Semua implementasi berada di dalam Capability Pack

---

## Ruang Lingkup Kapabilitas

### Kapabilitas Inti

|Kapabilitas|Deskripsi|Masukan|Keluaran|
|-----------|-------------|--------|---------|
|Desain Agent|Merancang arsitektur agent dengan tool dan orchestration|Kebutuhan tugas, domain|AgentSpec|
|Desain RAG Engine|Merancang konfigurasi RAG|Korpus dokumen, kebutuhan retrieval|RAGConfig|
|Prompt Engineering|Merancang template prompt dan optimization|Tugas, variabel, format output|PromptTemplate|
|LLMOps Setup|Merancang deployment, monitoring, fine-tuning|Target lingkungan, anggaran|DeploymentConfig, MonitoringConfig|
|Penilaian AI|Evaluasi gap dan rekomendasi arsitektur AI|Spesifikasi saat ini dan target|Laporan assessment|

### Di Luar Cakupan

- Pelatihan model fundamental dari nol
- Pengumpulan dan labeling dataset
- Eksekusi inference real-time
- Penelitian AI baru
- Modifikasi kontrak Core

---

## Kontrak Publik

### Kontrak Masukan: Permintaan Rekayasa AI

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

### Kontrak Keluaran: Laporan Rekayasa AI

```json
{
  "request_id": "uuid",
  "operation": "string",
  "agent_spec": {
    "name": "string",
    "architecture": "single_agent",
    "orchestration": "sequential",
    "llm_provider": "openai",
    "model": "gpt-4o",
    "temperature": 0.7,
    "tools": [{"name": "web_search", "description": "string"}],
    "system_prompt": "string",
    "guardrails": ["string"],
    "context_window": 128000
  },
  "rag_config": {
    "strategy": "chunked",
    "chunk_size": 512,
    "chunk_overlap": 50,
    "embedding_model": "text-embedding-3-small",
    "vector_store": "pinecone",
    "top_k": 5,
    "rerank_enabled": true
  },
  "prompt_templates": [
    {
      "name": "rag_assistant",
      "template": "string",
      "variables": ["context", "query"],
      "expected_output_format": "text"
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

### Catatan Pengalaman (Memori Pengalaman)

```json
{
  "record_id": "uuid",
  "request_id": "uuid",
  "timestamp": "ISO 8601",
  "operation": "string",
  "agent_type": "string",
  "accuracy_achieved": 0.92,
  "latency_p95_ms": 450,
  "cost_monthly_usd": 150.0,
  "outcome": "accepted | partially_accepted | rejected | revised"
}
```

---

## Titik Integrasi (Grafik Kapabilitas)

```
Trading Analyst / Research Assistant / Code Engineer
    │
    │  provides AI requirements (accuracy, latency, cost)
    ▼
AI Engineer Engine
    │
    │  ┌─────────────────────────────────────────────────────┐
    │  │ 1. Agent Design (architecture, tools, orchestration) │
    │  │ 2. RAG Engine Design (chunking, embedding, retrieval)│
    │  │ 3. Prompt Engineering (templates, optimization)      │
    │  │ 4. LLMOps Setup (deployment, monitoring, eval)       │
    │  │ 5. AI Assessment → Experience Memory                  │
    │  └─────────────────────────────────────────────────────┘
    │
    │  produces AI architecture specification
    ▼
Execution Runtime
    │
    │  routes to consumer Capability Packs
    ▼
DevOps Assistant (deployment)
    │
    │  consumes spec for IaC / container orchestration
    ▼
Trading Analyst / Research Assistant (consumers)
```

### Templat Tugas

|Tugas|Subtugas|
|------|----------|
|Rekayasa AI|Kebutuhan → Desain Agent / RAG / Prompt / LLMOps → Evaluasi → Rekomendasi|

---

## Capability Pack Konsumen

|Capability Pack Konsumen|Kasus Penggunaan|
|--------------------------|----------|
|**Analis Perdagangan**|Mengonsumsi spesifikasi agent untuk trading AI|
|**Asisten Riset**|Mengonsumsi konfigurasi RAG untuk research pipeline|
|**Insinyur Kode**|Mengonsumsi template prompt untuk code generation|
|**Decision Intelligence**|Mengonsumsi evaluasi model untuk keputusan AI|
|**Asisten DevOps**|Mengonsumsi konfigurasi deployment untuk provisioning AI|

---

## Ketergantungan

### Dependensi Internal (Kontrak Bersama)

1. **Execution Runtime** — Tugas perutean dan orkestrasi (sesuai ADR-002)
2. **Experience Memory** — Persistensi catatan desain dan evaluasi (sesuai ADR-011)
3. **Kontrak Bersama** — Definisi Task/Intent dan skema hasil (sesuai ADR-006)

### Pengetahuan Eksternal

1. **LangChain / LlamaIndex** — Framework agent dan RAG
2. **OpenAI / Anthropic API** — Referensi provider LLM
3. **CIS AI Benchmark** — Baseline keamanan AI
4. **MLOps Best Practices** — Deployment dan monitoring
5. **Prompt Engineering Guide** — Best practices prompt design

### Tidak Ada Perubahan Inti yang Diperlukan

Semua implementasi berada di dalam Capability Pack AI Engineer:

```
apps/
└── ai_engineer/
    ├── engine.py               # Domain Engine (per ADR-004)
    ├── worker.py               # Thin adapter (per ADR-003)
    ├── schemas.py              # Public contracts
    ├── agent_designer.py       # Agent architecture design
    ├── rag_engine.py           # RAG configuration design
    ├── prompt_engineer.py      # Prompt template design
    └── llmops_manager.py       # Deployment and monitoring setup
```

**Dampak ADR:** Tidak ada. Tidak diperlukan modifikasi Core, Runtime, Kernel, atau kontrak bersama.

---

## Spesifikasi Benchmark

### Kerangka Benchmark

|Dimensi|Definisi|Pengukuran|Target|
|-----------|------------|-------------|--------|
|**Akurasi Agent**|% tugas diselesaikan dengan benar|Evaluasi ground truth|≥95%|
|**Faithfulness RAG**|% jawaban didukung oleh konteks|Ground truth evaluation|≥92%|
|**Halusination Rate**|% jawaban yang tidak didukung konteks|Ground truth evaluation|<5%|
|**Latensi P95**|Waktu respons pada persentil ke-95|Metrik produksi|<500ms|
|**Skor Kualitas**|Skor kualitas keseluruhan|Tinjau ahli|≥95%|
|**Akurasi Estimasi Biaya**|Prediksi vs aktual|Perbandingan biaya aktual|±10%|
|**Kepatuhan**|% kontrol kepatuhan lulus|Checklist kepatuhan|≥95%|
|**Konsistensi**|Input yang menghasilkan spec yang sama|Varian di 10 run <5%|≥95%|

### Kumpulan Data Benchmark

- **100 skenario AI engineering** yang mencakup:
  - Single-agent task completion
  - Multi-agent collaboration
  - RAG dengan berbagai strategi
  - Prompt optimization
  - LLMOps setup (deployment, monitoring, fine-tuning)

---

## Spesifikasi Golden Test

| # |Skenario|Hasil yang diharapkan|Kriteria Penerimaan|
|---|----------|-----------------|---------------------|
|1|Desain agent untuk tugas complex|AgentSpec dengan tools dan orchestration yang tepat|≥95% kelengkapan|
|2|Desain RAG untuk korpus besar|RAGConfig dengan chunking dan retrieval optimal|≥92% faithfulness|
|3|Prompt engineering untuk code generation|PromptTemplate dengan variabel yang benar|≥90% kegunaan|
|4|LLMOps setup untuk produksi|DeploymentConfig dengan scaling dan monitoring|≥90% kelengkapan|
|5|Multi-agent orchestration design|AgentSpec dengan orchestration pattern yang benar|≥90% kelengkapan|
|6|RAG dengan reranking|RAGConfig dengan rerank model yang tepat|≥92% faithfulness|
|7|Fine-tuning pipeline design|FineTuningConfig dengan metrics yang tepat|≥90% kelengkapan|
|8|Monitoring setup untuk LLM|MonitoringConfig dengan alert thresholds yang tepat|100% kontrol|
|9|AI assessment gap analysis|Gap teridentifikasi dengan prioritas|≥90% cakupan|
|10|Cost estimation for AI system|Estimasi biaya token dan infrastruktur|±10% akurasi|

### Kriteria Penerimaan Golden Test

- Semua 10 skenario lulus pada ≥90% dari kriteria penerimaan
- Tingkat kelulusan Golden Test AI Engineer keseluruhan ≥90%
- Evaluasi model divalidasi dengan ground truth
- Estimasi biaya diverifikasi dengan data pasar

---

## Persyaratan Kasus Nyata

### Direktori Kasus Nyata

`real_cases/ai_engineer/` harus berisi minimal 3 kasus demonstrasi (untuk RFC):

|Urutannya|Jumlah Minimal|
|-------------|---------------|
|Desain agent untuk RAG chatbot|1|
|Desain orchestration multi-agent|1|
|LLMOps setup untuk fine-tuning|1|

### Struktur Kasus Nyata

```
real_cases/ai_engineer/<case_id>/
├── input/
│   ├── requirements.json    # AI requirements and constraints
│   └── constraints.md       # Technical and business constraints
├── output/
│   ├── agent_design.json    # Generated agent spec
│   ├── rag_config.json      # RAG configuration
│   ├── prompt_templates.jsonl # Generated prompt templates
│   └── deployment_config.yaml # Deployment configuration
└── evaluation.md            # Ground truth, expert review, lessons learned
```

---

## Definisi Selesai

```text
Definition of Done — AI Engineer Capability Pack

Functional
- [ ] Agent Design generates AgentSpec with tools, orchestration, guardrails
- [ ] RAG Engine Design generates RAGConfig with chunking and retrieval
- [ ] Prompt Engineering generates PromptTemplate with variables
- [ ] LLMOps Setup generates DeploymentConfig, MonitoringConfig, FineTuningConfig
- [ ] AI Assessment produces gap analysis and recommendations

Benchmark
- [ ] Agent Accuracy ≥ 95%
- [ ] RAG Faithfulness ≥ 92%
- [ ] Hallucination Rate < 5%
- [ ] Latency P95 < 500ms
- [ ] Quality Score ≥ 95%
- [ ] Cost Accuracy ±10%
- [ ] Compliance ≥ 95%
- [ ] Consistency ≥ 95%

Golden Tests
- [ ] All 10 pack golden test scenarios pass at ≥90%

Real Cases
- [ ] ≥ 3 sample cases in real_cases/ai_engineer/
- [ ] Evaluation notes recorded for each case

Documentation
- [ ] docs/capabilities/ai-engineer.md
- [ ] API reference / contract (this RFC + schemas.py)
- [ ] Real case evaluation summary published

SDK
- [ ] Pack accessible via SDK without Core changes
- [ ] AI Engineer callable via Execution Runtime

Performance
- [ ] Latency P95 < 3000ms for standard AI engineering design

Security
- [ ] No known P0/P1 security issues
- [ ] Generated specs do not expose API keys or credentials

Regression
- [ ] No regression in existing Capability Pack benchmark dimensions
```

---

## Risiko

|Risiko|Dampak|Kemungkinan|Mitigasi|
|------|--------|------------|------------|
|Arsitektur agent tidak sesuai kebutuhan|Tinggi — kegagalan tugas|Tinggi|Evaluasi multi-metrik; validasi ahli; ground truth testing|
|RAG menghasilkan halusinasi|Tinggi — output tidak dapat dipercaya|Sedang|Ground truth evaluation; reranking; faithfulness threshold|
|Estimasi biaya token tidak akurat|Sedang — kejutan anggaran|Tinggi|Data pasar aktual; kalibrasi berkala|
|Prompt tidak optimal|Sedang — akurasi rendah|Tinggi|A/B testing; evaluasi otomatis; prompt optimization|
|Fine-tuning overfit|Sedang — generalisasi buruk|Sedang|Validation split; early stopping; eval metrics|
|Deployment tidak skalabel|Tinggi — bottleneck produksi|Sedang|Load testing; autoscaling config; rate limiting|

---

## Dampak ADR

**Apakah ini memerlukan perubahan Core?** Tidak.

AI Engineer adalah **Capability Pack baru** yang mengikuti pola yang sudah ada:

- **ADR-001 (Core Pipeline Freeze):** Tidak ada perubahan Core. Semua logika di `apps/ai_engineer/`.
- **ADR-002 (Capability Pack Kemerdekaan):** AI Engineer berkomunikasi dengan paket lain melalui tugas Execution Runtime dan kontrak bersama saja.
- **ADR-003 (Pekerja = Hanya Adaptor):** Pekerja tipis merutekan tugas ke Mesin Domain.
- **ADR-004 (Logika Bisnis Milik Mesin Domain):** Semua logika rekayasa AI berada di `apps/ai_engineer/engine.py`.
- **ADR-005 (Human Approval Required):** Semua spesifikasi AI memerlukan persetujuan manusia sebelum deployment.
- **ADR-006 (Capability Contract v1 Frozen):** Menggunakan kontrak bersama yang ada.
- **ADR-007 (Batas Percakapan):** AI Engineer dipanggil melalui Execution Runtime.

**ADR yang diperlukan:** Tidak ada. Ini adalah Capability Pack baru, bukan modifikasi Core.

---

## Peluncuran Rencana

### Fase 1: Prototipe (RFC → Eksperimental)

**Durasi:** 5 minggu

- [ ] Membuat struktur paket `apps/ai_engineer/`
- [x] Mengimplementasikan Agent Designer
- [x] Mengimplementasikan RAG Engine
- [x] Mengimplementasikan Prompt Engineer
- [x] Mengimplementasikan LLMOps Manager
- [x] Mendefinisikan kontrak publik (AI Request, AI Report)
- [x] Mengimplementasikan adaptor Worker tipis
- [x] Membuat 10 skenario Golden Test
- [x] Integrasi: Trading Analyst ← AI Engineer (spesifikasi agent)
- [ ] **Gerbang:** 10 Golden Test lulus pada ≥80%

### Fase 2: Kapabilitas Lengkap (Eksperimental → Stabil)

**Durasi:** 8 minggu

- [ ] Menyempurnakan semua desainer dengan knowledge expansion
- [x] Memperluas Golden Test menjadi 10 skenario penuh
- [x] Mencatat kasus nyata dalam `real_cases/ai_engineer/`
- [x] **Benchmark:** 100 skenario, ≥95% kualitas
- [x] **Integrasi:** Research Assistant mengonsumsi RAG config
- [x] **Integrasi:** Code Engineer mengonsumsi prompt templates
- **Gerbang:** Semua 10 Golden Test lulus pada ≥90%; Benchmark ≥95%

### Fase 3: Ekosistem (Stabil → Bersertifikat)

**Durasi:** 6 minggu

- [ ] Keempat paket konsumen terintegrasi
- [x] Desain divalidasi melalui deployment di staging
- [ ] **Benchmark:** ≥95% di semua dimensi berkelanjutan
- [ ] **Kasus Nyata:** ≥20 kasus dengan ≥90% adopsi hilir
- **Gerbang:** Audit kelulusan independen; Benchmark ≥95% berkelanjutan

---

## Peningkatan di Masa Depan

### Fase 2 (Pasca-Rilis v2.0.0)

1. **Multi-Modal Agent Design** — Agenta yang memproses teks, gambar, audio
2. **Advanced RAG** — Graph RAG, agentic RAG dengan tool use
3. **AI Observability** — LangSmith, Phoenix integration untuk tracing
4. **Prompt Versioning** — Version control dan A/B testing untuk prompt

### Fase 3 (Perusahaan)

1. **AI Safety & Alignment** — Guardrails, Constitutional AI, red-teaming
2. **Federated Learning** — Training terdistribusi tanpa data central
3. **AI Governance** — Audit trail, model card, compliance reporting
4. **Edge AI Optimization** — Model compression, quantization untuk edge
