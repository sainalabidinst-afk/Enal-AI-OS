# ADR-026: Voice Interaction Capability Pack

- **Status**: Accepted
- **Date**: 2026-10-02
- **Deciders**: Enal-AI-OS Core Team
- **Related ADRs**: [ADR-023](ADR-023-voice-provider-architecture.md), [ADR-021](ADR-021-translator-expert.md)
- **Related RFCs**: [RFC-0043](RFC-0043-jenny-voice-interface.md)

## Context

The ECP needs a Voice Interaction capability pack that integrates with the existing backend STT/TTS services (stt_service, tts_service) and frontend voice UI. The pack must follow the established ECP pattern with schemas, engine, worker, benchmark, golden tests, and real cases.

## Decision

We will create a `voice_interaction` capability pack at `apps/voice_interaction/` with:

1. **Schemas**: Pydantic models using StrEnum for `VoiceInteractionOperation` and `VoiceLanguage`, BaseModel for requests/responses
2. **Voice Engine**: Delegates to backend `stt_service` and `tts_service` via the runtime facade, with async `process_voice_interaction` orchestrator
3. **Engine**: Synchronous wrapper for ECP pipeline compatibility
4. **Worker**: Agent-adapted execution from cognitive pipeline tasks
5. **Observability**: Structured tracing via the runtime `observability` facade
6. **Benchmark**: 8 dimensions covering STT accuracy, TTS quality, latency, language detection, provider resilience, conversation flow, explainability, and real-time streaming

### Provider Architecture

Follows ADR-023 lazy provider pattern:
- **STT fallback chain**: whisper → openai → web_speech
- **TTS fallback chain**: pyttsx3 → piper → elevenlabs → openai
- No hard dependencies on optional provider packages

### Supported Languages

22 language codes covering global markets:
en, id, es, fr, de, zh, ja, ar, pt, ru, ko, hi, th, vi, tl, nl, it, tr, pl, uk, ca, ms

## Consequences

- Voice operations are traced through the Observability system with `SpanType.AGENT` spans
- Pack integrates with existing backend services at `backend/app/core/stt_service.py` and `backend/app/core/tts_service.py`
- Frontend integration reuses `frontend/services/voice.ts` and `chatgpt-page.tsx` voice UI
- WebSocket streaming endpoint at `/ws/voice` supports real-time transcription
- Benchmark targets Grade A (>= 90% overall score)

## References

- [RFC-0043: Jenny Voice Interface](RFC-0043-jenny-voice-interface.md)
- [ADR-023: Voice Provider Architecture](ADR-023-voice-provider-architecture.md)
- Backend: `backend/app/core/stt_service.py`, `backend/app/core/tts_service.py`, `backend/app/api/voice.py`
- Frontend: `frontend/services/voice.ts`, `frontend/components/chat/chatgpt-page.tsx`
