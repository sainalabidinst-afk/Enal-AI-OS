# Voice Interaction Capability Pack

**Version:** 3.1.0  
**Target Grade:** A (≥90%)  
**Status:** Implemented  
**Phase:** Jenny-like Interaction (Q4.1–Q4.3)  
**RFC:** [RFC-0043](docs/rfcs/RFC-0043-jenny-voice-interface.md)  
**ADR:** [ADR-026](docs/adr/ADR-026-voice-interaction-capability-pack.md)  

## Ringkasan

Voice Interaction (Jenny-like Interaction) menyediakan antarmuka suara end-to-end:
speech-to-text (STT) → natural language understanding (NLU) → cognitive pipeline →
action connectors → text-to-speech (TTS). Pack ini mengintegrasikan VoiceAgent,
Action Connector Framework, dan Consent Manager untuk interaksi suara yang
aman dan nyaman.

## Arsitektur 3-Fase

1. **Q4.1 — Voice Interface**: STT/TTS service layer, Voice API, frontend voice bridge
2. **Q4.2 — Action Connectors**: FileSystem, Email, Calendar, SmartHome connectors dengan
   ToolRegistry integration
3. **Q4.3 — Observability & Safety**: Consent Manager, anomaly detection, risk-based
   action classification, safety audit

## Knowledge

- **STT**: Whisper.cpp (local), Web Speech API (browser fallback), OpenAI Whisper (cloud)
- **TTS**: Piper (local), browser speechSynthesis (fallback), ElevenLabs (cloud premium)
- **NLU**: Intent classification via LLM prompt + keyword fallback
- **Dialogue Manager**: Multi-turn state tracking via conversation memory
- **Connectors**: FileSystem, Email (SMTP/IMAP + Gmail API), Calendar (CalDAV + Google Calendar API), SmartHome (MQTT + Home Assistant API)
- **Consent**: Risk-based classification (low/medium/high) dengan auto-approval, UI confirmation, atau explicit approval + timeout

## Integration

- **Konsumsi dari**: Cognitive Kernel, Adaptive Runtime, Memory, ToolRegistry, ConnectorManager
- **Digunakan oleh**: Chat interface (chatgpt-page.tsx), capability execution, real-time status

## Benchmark

- 10 scenarios across 6 dimensions (STT accuracy, NLU accuracy, TTS quality, latency,
  action success rate, consent flow)
- Overall score: A (≥90%)
- Dashboard: `benchmarks/dashboards/voice_interaction_dashboard.html`

## Real Cases

10 real cases in `real_cases/voice_interaction/`

## Changelog

- **2026-10-02**: Initial implementation (RFC-0043, ADR-026)
  - STT/TTS service layer (stt_service.py, tts_service.py)
  - Voice API (backend/app/api/voice.py)
  - Frontend voice bridge (frontend/services/voice.ts)
  - 4 action connectors (FileSystem, Email, Calendar, SmartHome)
  - Consent Manager & anomaly detection
  - 50+ safety tests, 512 total tests passing
