# RFC-0049: Voice Agent Enhancements

<!-- DOCUMENT_METADATA_START -->
**Pemilik:** Tim Frontend Platform
**Canonical Owner:** Lead Platform Engineer
**Terakhir Diverifikasi:** 2026-10-03
**Versi:** 1.0.0
**Status:** Draft → Proposed
**SSOT:** Rancangan voice agent enhancements: telephony inbound/outbound, STT/TTS providers, latency monitoring, dan voice-specific observability
<!-- DOCUMENT_METADATA_END -->

## Abstrak

RFC ini mendefinisikan enhancements untuk Voice Agent di ECP, mencakup telephony integration (inbound/outbound calls), multi-provider STT/TTS, latency monitoring (TTFS, P50/P90/P99), dan voice-specific observability.

## Konteks

ECP sudah memiliki VoiceAgent skeleton (RFC-0043), tetapi belum memiliki:
1. Telephony integration untuk inbound/outbound calls
2. Multi-provider STT/TTS (Whisper, Deepgram, ElevenLabs, Azure)
3. Latency monitoring untuk voice pipeline
4. Voice-specific guardrails

## Keputusan

### 1. Telephony Integration

**Provider:** Twilio (default) atau Plivo
**Features:**
- Inbound call handling
- Outbound dialing
- Call status tracking
- Active calls management

### 2. STT Service

**Providers:**
| Provider | Condition | Lazy Import |
|----------|-----------|-------------|
| `whisper` | Whisper server (HTTP API) | `aiohttp` |
| `deepgram` | Deepgram API | `aiohttp` |
| `google` | Google Speech-to-Text | `google-cloud-speech` |

### 3. TTS Service

**Providers:**
| Provider | Condition | Lazy Import |
|----------|-----------|-------------|
| `elevenlabs` | ElevenLabs API | `aiohttp` |
| `azure` | Azure Cognitive Services | `aiohttp` |
| `openai` | OpenAI TTS API | `openai` |

### 4. Latency Monitor

Track metrics:
- TTFS (Time To First Sound)
- STT latency (P50/P90/P99)
- LLM latency (P50/P90/P99)
- TTS latency (P50/P90/P99)
- Total latency (P50/P90/P99)

### 5. Voice Agent Runtime

Pipeline: STT → LLM → TTS
- Record latency per stage
- Apply guardrails to input/output
- Return structured result dengan latency metrics

### 6. Frontend Route

`/builder/voice` — `VoiceAgentBuilderPage` rendering `VoiceAgentBuilder`

## Implementasi

### Frontend Components

- `VoiceAgentBuilder.tsx` — Voice-specific agent config
- Call UI dengan recording controls
- Call history view

### Backend Modules

- `backend/app/core/stt_service.py` — STTService
- `backend/app/core/tts_service.py` — TTSService
- `backend/app/core/telephony_integration.py` — TelephonyIntegration
- `backend/app/core/latency_monitor.py` — LatencyMonitor
- `backend/app/core/voice_agent_runtime.py` — VoiceAgentRuntime

## Dependencies

- RFC-0046: Visual Builder Foundation
- RFC-0047: Visual Agent Builder
- RFC-0050: Guardrails & Safety

## Testing

- TypeScript: 0 errors
- Ruff: 0 errors
- Mypy: 0 errors

## References

- RFC-0043: Jenny Voice Interface
- SimplAI Voice Agents: https://simplai.ai/docs/voice-agents/
