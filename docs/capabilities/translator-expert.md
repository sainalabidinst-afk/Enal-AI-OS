# Translator Expert Capability Pack

**Version:** 1.0.0  
**Target Grade:** A (≥90%)  
**Status:** Implemented  
**Phase:** Platform Enterprise (Phase 7)  
**RFC:** [RFC-0039](docs/rfcs/RFC-0039-translator-expert.md)  
**ADR:** [ADR-015](docs/adr/ADR-015-translator-expert.md)  

## Ringkasan

Translator Expert Capability Pack menyediakan penerjemahan lintas bahasa yang akurat dengan dukungan konteks domain, kontrol gaya, dan penegakan glossary. Pack ini mendukung language detection otomatis, translation engine multi-bahasa (English, Indonesian, Spanish, Mandarin, dll.), contextual adaptation untuk idiom dan istilah teknis, style control (formal/informal, technical/casual), dan glossary integration untuk domain finance, legal, medical, dan technical.

## Kemampuan Inti

1. **Language Detection** — otomatis mendeteksi bahasa sumber dengan confidence score (langdetect atau heuristic fallback)
2. **Multilingual Translation** — mendukung 10+ pasang bahasa dengan MarianMT/M2M-100 (lazy import)
3. **Contextual Adaptation** — idiom, istilah teknis, dan keanekaragaman budaya
4. **Style Control** — formal/informal, technical/casual — dikonfigurasi per request
5. **Glossary Enforcement** — glossary domain (finance, legal, medical, technical) diterapkan pre/post-processing

## Supported Languages

| Code | Language |
|------|----------|
| en | English |
| id | Indonesian |
| es | Spanish |
| zh | Chinese (Simplified) |
| fr | French |
| de | German |
| ja | Japanese |
| ar | Arabic |
| pt | Portuguese |
| ru | Russian |

## Supported Domains

| Domain | Glossary Terms (approx.) | Use Cases |
|--------|--------------------------|-----------|
| finance | 40+ | Financial reports, investment docs, trading analysis |
| legal | 40+ | Contracts, compliance docs, legal correspondence |
| medical | 30+ | Medical guidelines, patient info, clinical docs |
| technical | 30+ | Technical documentation, API docs, code comments |
| general | 0 | General text, chat, casual content |

## Architecture

```
Translator Expert Pipeline:
  1. Language Detection (lazy langdetect)
  2. Glossary Preprocessing (tagged placeholders)
  3. Style-Aware Translation (MarianMT/M2M-100 or rule-based fallback)
  4. Glossary Post-Processing (enforce approved target terms)
  5. Confidence & Explainability Scoring
```

### Lazy Import Pattern

Translation model imports (`transformers`, `langdetect`, `torch`) are **lazy-loaded** to maintain a lightweight runtime facade. When ML libraries are unavailable, the engine falls back to rule-based translation with glossary enforcement.

## Integration

- **Konsumsi dari**: Legal Advisor (legal document translation), Finance Analyst (financial report translation), Research Assistant (multilingual literature synthesis), HSE Specialist (technical safety docs)
- **Digunakan oleh**: Documentation Engineer (glossary & terminology), Code Engineer (i18n docs)

## Benchmark

- 10 scenarios across 6 dimensions:
  1. **Translation Accuracy** — correctness of translations
  2. **Context Adaptation** — idiom & cultural context handling
  3. **Style Control** — formal/informal/technical/casual register
  4. **Glossary Enforcement** — domain term consistency
  5. **Latency Performance** — response time < 2500ms
  6. **Explainability** — confidence scoring & glossary tracking

- Overall score: A (≥90%)
- 10 golden test JSON files in `golden_tests/translator_expert/`
- Benchmark dashboard: `benchmarks/dashboards/translator_expert_dashboard.html`

## Real Cases

10 real cases in `real_cases/translator_expert/` covering:
- Legal contract translation (EN→ID)
- Medical guideline translation (EN→ES)
- Technical documentation translation (EN→ZH)
- Financial report translation (ID→EN)
- Idiomatic phrase translation (ES→EN)
- Formal vs. informal tone adaptation
- Multi-sentence context preservation
- Finance glossary enforcement
- Real-time chat translation
- Latency & accuracy benchmark

## Changelog

- **2026-10-02**: Initial implementation (RFC-0039, ADR-015)
  - `apps/translator_expert/` pack with engine, schemas, worker, glossary_manager, translator_engine
  - Lazy-loaded HuggingFace MarianMT/M2M-100 + rule-based fallback
  - 10 golden test scenarios
  - 10 real cases
  - Benchmark with 6 dimensions
  - Domain glossaries: finance, legal, medical, technical
  - Frontend integration: `translation_pipeline.tsx`
