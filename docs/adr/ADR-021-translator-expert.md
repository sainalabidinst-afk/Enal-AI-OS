# ADR-015: Translator Engine Architecture

|Bidang|Nilai|
|-------|-------|
|**ID ADR**|ADR-015|
|**Status**|Accepted|
|**Date**|2026-10-02|
|**Decision Maker**|Platform Architecture Board|
|**Related RFC**|RFC-0039|

## Context

The Translator Expert capability pack needs to provide high-quality multilingual translation with domain context, style control, and glossary enforcement. The engine must work both with and without heavy ML dependencies (transformers, torch, langdetect) installed, since CI/CD environments may not have GPU or model access.

## Decision

1. **Translation Engine**: Use HuggingFace `MarianMT` (Helsinki-NLP) / `M2M-100` as the baseline engine, imported lazily via `__getattr__` to avoid hard dependencies.
2. **Fallback Strategy**: When ML libraries are unavailable, fall back to rule-based translation with glossary lookup and idiomatic phrase replacement.
3. **Language Detection**: Use `langdetect` (lazy import) with a heuristic fallback for common languages (en, id, es, zh).
4. **Glossary Enforcement**: Pre-processing replaces source terms with tagged tokens; post-processing replaces them with approved glossary terms in the target language.
5. **Style Control**: Style prefix prompts are prepended to the source text before translation (formal/informal/technical/casual).
6. **Full integration with `useExecutionStore`**: All translation artifacts, logs, and timeline entries are recorded through the execution store for full observability.

## Alternatives Considered

- **Google Translate API**: Rejected — vendor lock-in, cost per request, external dependency.
- **In-house seq2seq model**: Rejected — high training cost, requires large multilingual corpus.
- **OpenAI translation**: Rejected — external API dependency, cost, rate limits.
- **Static rule-based only**: Rejected — insufficient for natural language fluency (used only as fallback).

## Consequences

- Translator Expert becomes a new pack in `apps/translator_expert/`
- CI/CD pipeline adds matrix testing for translation scenarios
- Governance checks remain enforced (boundary, ADR verification)
- No external API dependencies — all inference can run locally when models are available
- Rule-based fallback ensures the pack always produces deterministic output

## Cross-Capability Proof

- Documentation Engineer consumes glossary for terminology consistency (provider → consumer)
- Legal Advisor consumes legal document translation (consumer → provider)
- Finance Analyst consumes financial report translation (consumer → provider)
- Research Assistant consumes multilingual literature synthesis (consumer → provider)
