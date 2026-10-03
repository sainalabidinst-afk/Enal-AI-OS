# RFC-0043: Jenny Voice Interface

<!-- DOCUMENT_METADATA_START -->
**Pemilik:** Tim Arsitektur Suara
**Canonical Owner:** Lead Platform Engineer
**Terakhir Diverifikasi:** 2026-10-02
**Versi:** 1.0.0
**Status:** Draft → Proposed
**SSOT:** Rancangan layanan STT/TTS, API endpoints, dan frontend voice bridge untuk interaksi suara ala Jenny
<!-- DOCUMENT_METADATA_END -->

## Abstrak

RFC ini mendefinisikan rancangan layanan Speech-to-Text (STT) dan Text-to-Speech (TTS) untuk Enal Cognitive Platform (ECP), yang memungkinkan interaksi suara ala "Jenny". Arsitektur ini memperluas skeleton `VoiceAgent` yang ada di `backend/app/core/voice_vision_agent.py` dengan implementasi provider yang sebenarnya, API endpoints, dan integrasi frontend.

## Konteks

Sejak v1.0.0-dev, ECP memiliki skeleton `VoiceAgent` dan `VisionAgent` di `backend/app/core/voice_vision_agent.py` yang masih `raise NotImplementedError`. Frontend (`frontend/components/chat/chatgpt-page.tsx`) sudah memiliki UI mic/speak tapi hanya menggunakan Web Speech API (browser-only), tidak terhubung ke backend.

Untuk interaksi ala Jenny yang nyata, kita butuh:
1. STT backend yang dapat merekam audio dari user dan mentranskripsikan ke teks
2. TTS backend yang dapat menyintesis teks menjadi suara
3. API endpoints REST + WebSocket untuk real-time streaming
4. Frontend service yang menghubungkan microphone → backend → chat → backend → speaker

## Keputusan

### Lazy Provider Architecture (melihat ADR-023)

STT/TTS providers di-load secara lazy berdasarkan konfigurasi (`STT_PROVIDER`, `TTS_PROVIDER`). Ini menghindari hard dependency pada paket provider-specific.

**STT Providers:**
| Provider | Kondisi | Lazy Import |
|---|---|---|
| `whisper` | whisper.cpp server (HTTP API) | `aiohttp` |
| `openai` | OpenAI Whisper API | `openai` |
| `web_speech` | Browser fallback stub (backend) | tidak perlu |

**TTS Providers:**
| Provider | Kondisi | Lazy Import |
|---|---|---|
| `pyttsx3` | Local offline (Python) | `pyttsx3` |
| `piper` | Piper TTS server (HTTP API) | `aiohttp` |
| `elevenlabs` | ElevenLabs API | `aiohttp` |
| `openai` | OpenAI TTS API | `openai` |

### API Endpoints

**`POST /api/v1/voice/transcribe`**
- Request: `multipart/form-data` dengan field `file` (audio WAV) dan query param `language`
- Response: `VoiceTranscription` (text, confidence, language, duration_ms, alternatives)

**`POST /api/v1/voice/speak`**
- Request: query params `text`, `voice`, `speed`
- Response: `StreamingResponse` (audio WAV/MP3 bytes)

**`GET /api/v1/voice/languages`**
- Response: `{"languages": ["en", "id", ...]}`

**`GET /api/v1/voice/providers`**
- Response: provider info + supported languages

**`WebSocket /api/v1/voice/ws/voice`**
- Real-time voice streaming: binary audio chunks → JSON transcriptions
- Protocol: client sends binary audio, server responds with `{"text": "...", "confidence": 0.x, "final": true/false}`

### Frontend Voice Bridge

`frontend/services/voice.ts` menyediakan:
- `transcribeAudio(blob, language)` — kirim audio ke backend
- `speakTextBrowser(text, lang)` — gunakan browser `speechSynthesis` (fallback)
- `speakText(text, voice, speed)` — gunakan backend TTS (primary)

`chatgpt-page.tsx` mengintegrasikan:
- `navigator.mediaDevices.getUserMedia({ audio: true })` untuk merekam
- `MediaRecorder` untuk mengumpulkan audio chunks
- Kirim ke `/api/v1/voice/transcribe` → dapatkan teks → auto-submit ke chat
- Voice toggle button di header
- Recording indicator saat merekam

## Consequenses

### Positif

- Voice-first interaction yang bekerja di semua browser (backend STT fallback)
- Modular provider architecture — bisa ganti whisper → openai → web_speech tanpa kode berubah
- WebSocket endpoint untuk real-time streaming (latensi rendah)
- Lazy import → tidak pecah jika provider tidak terpasang
- Teraintegrasi dengan cognitive pipeline yang sudah ada (AdaptiveCognitiveRuntime)

### Negatif

- Tambahan `aiohttp` dependency (opsional, lazy import)
- Backend TTS membutuhkan server lokal (whisper.cpp/pyttts) — bisa dijalankan via Docker
- Latency tambahan untuk round-trip audio jika tidak ada caching

### Netral

- Tidak ada perubahan pada Core Runtime
- VoiceAgent tetap backward-compatible (delegates ke service layer)
- Skeleton VisionAgent tidak diubah (hanya VoiceAgent yang diimplementasikan)

## Rancangan Detail

### stt_service.py
```
STTService.transcribe(audio_bytes, language)
  → provider dispatch (whisper / openai / web_speech)
  → TranscriptionResult(text, confidence, language, duration_ms, provider, metadata)
  → to_voice_transcription() → VoiceTranscription
```

### tts_service.py
```
TTSService.speak(text, voice, speed)
  → provider dispatch (pyttsx3 / piper / elevenlabs / openai)
  → SynthesisResult(audio_data, format, sample_rate, provider)
```

### voice_vision_agent.py (updated)
```python
class VoiceAgent:
    async def transcribe(self, audio_data, language) -> VoiceTranscription:
        from backend.app.core.stt_service import stt_service

        result = await stt_service.transcribe(audio_data, language)
        return result.to_voice_transcription()

    async def speak(self, text, voice, speed) -> bytes:
        from backend.app.core.tts_service import tts_service

        result = await tts_service.speak(text, voice, speed)
        return result.audio_data
```

### Config (config.py)
```
STT_PROVIDER, STT_MODEL_PATH, STT_API_KEY, STT_LANGUAGE, STT_WHISPER_HOST
TTS_PROVIDER, TTS_VOICE, TTS_SPEED, TTS_API_KEY, TTS_ELEVENLABS_VOICE_ID, LOCAL_TTS_URL
```

## Referensi

- ADR-023: Voice Provider Architecture
- RFC-0044: Jenny Action Connectors
- RFC-0045: Jenny Safety & Observability
- ADR-001: Core Pipeline Freeze
- ADR-002: Capability Pack Independence
