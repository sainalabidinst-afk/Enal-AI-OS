# RFC-0041: Capability Pack Translator Expert

|Bidang|Nilai|
|-------|-------|
|**ID RFC**|RFC-0041|
|**Status**|Diterima|
|**Versi**|0.1.0|
|**Penulis**|Tim Inti AI OS Akhir|
|**Target Rilis**|v2.3.0 (Platform Enterprise)|
|**Capability Pack**|Translator Expert|
|**ID Kemampuan**|`translator-expert`|
|**Kategori**|Language|
|**Target Kualitas**|A (≥90)|
|**Referensi RFC**|RFC-0016 (Documentation Engineer) — glossary & terminology; RFC-0008 (Security Engineer) — secure handling|

---

## Motivasi

Organisasi global memerlukan penerjemahan lintas bahasa yang akurat, berkonteks domain, dan konsisten dengan gaya serta istilah khusus. Penerjemahan sembarangan (machine translation mentah) seringkali:

1. **Kehilangan konteks domain** — istilah teknis keuangan, hukum, atau medis disalahartikan.
2. **Gaya tidak konsisten** — formal vs. informal tidak terkontrol.
3. **Glossary tidak terpenuhi** — istilah kunci dikaitas ganti dengan terjemahan yang berbeda.
4. **Idiom salah** — frasa idiomatik diterjemahkan harf-harfi.

Translator Expert menyediakan penerjemahan berkualitas tinggi dengan dukungan:
- Language detection otomatis
- Translation engine multi-bahasa (English, Indonesian, Spanish, Mandarin, dll.)
- Contextual adaptation (idiom, istilah teknis)
- Style control (formal/informal, technical/casual)
- Glossary integration (finance, legal, medical)

---

## Tujuan

1. **Language Detection** — otomatis mendeteksi bahasa sumber dengan confidence score
2. **Multi-Language Translation** — mendukung 10+ pasang bahasa dengan MarianMT/M2M-100
3. **Contextual Adaptation** — idiom, istilah teknis, dan keanekaragaman budaya
4. **Style Control** — formal/informal, technical/casual — dikonfigurasi per request
5. **Glossary Enforcement** — glossary domain (finance, legal, medical) diterapkan pre/post-processing

---

## Knowledge Expansion

- [x] Language Detection: fastText, langdetect, polyglot — confidence scoring
- [x] Translation Models: MarianMT (Helsinki-NLP), M2M-100, NLLB
- [x] Idiomatic Expressions: phrase-based replacement, context-aware disambiguation
- [x] Technical Domain Terminology: finance, legal, medical, engineering glossaries
- [x] Style Transfer: formal ↔ informal, technical ↔ casual tone adaptation
- [x] Glossary Management: domain-specific term databases, versioning, fuzzy matching
- [x] Post-editing: terminology enforcement, fluency post-processing

---

## Arsitektur

```
Translator Expert Pipeline:
  1. Language Detection (lazy langdetect)
  2. Glossary Lookup & Preprocessing
  3. Style-Aware Prompting
  4. Translation Engine (lazy MarianMT/M2M-100)
  5. Glossary Enforcement (post-processing)
  6. Confidence & Explainability Scoring
```

### Komponen

| Komponen | File | Deskripsi |
|---|---|---|
| Translator Engine | `apps/translator_expert/translator_engine.py` | Core translation module — lazy import HuggingFace/MarianMT |
| Glossary Manager | `apps/translator_expert/glossary_manager.py` | Domain glossary management & enforcement |
| Engine | `apps/translator_expert/engine.py` | Orchestration pipeline |
| Worker | `apps/translator_expert/worker.py` | Adapter for agent access |
| Schemas | `apps/translator_expert/schemas.py` | Typed contracts |

### Lazy Import Pattern

Translation model imports (transformers, langdetect, torch) are **lazy-loaded** via `__getattr__` in the translator engine, matching the pattern used in `backend/app/runtime/__init__.py`. This ensures:
- Runtime facade tetap ringan
- Tidak ada hard dependency pada paket ML
- Fallback ke rule-based translation jika model tidak tersedia

---

## Integration

- [x] Documentation Engineer — glossary & terminology consistency
- [x] Legal Advisor — legal document translation (EN ↔ ID, EN ↔ ES)
- [x] Finance Analyst — financial report translation (ID ↔ EN)
- [x] HSE Specialist — technical safety documentation translation
- [x] Research Assistant — multilingual literature synthesis
- [x] Code Engineer — API documentation translation untuk internationalization

---

## Benchmark & Governance

- 10 benchmark scenarios across 6 dimensions
- 10 golden test JSON files
- 10 real cases in `real_cases/translator_expert/`
- Benchmark dashboard: `benchmarks/dashboards/translator_expert_dashboard.html`
- Governance checks pass (package boundary, capability first rule)

---

## Timeline

| Milestone | Target |
|---|---|
| RFC Draft | 2026-10-02 |
| ADR-021 | 2026-10-02 |
| Pack Implementation | 2026-10-02 |
| Golden Tests | 2026-10-02 |
| Benchmark | 2026-10-02 |
| Documentation | 2026-10-02 |
| CI Registration | 2026-10-02 |

---

## Risiko

| Risiko | Mitigasi |
|---|---|
| Model dependencies tidak tersedia | Lazy import + rule-based fallback |
| Akurasi terjemahan domain spesifik rendah | Glossary enforcement pipeline |
| Latency tinggi untuk dokumen panjang | Chunking & batch processing |
| Idiom / konteks budaya salah | Pre-processing idiom dictionary |
