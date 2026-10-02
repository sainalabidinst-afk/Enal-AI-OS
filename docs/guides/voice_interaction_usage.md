# Voice Interaction Pack — Usage Guide

## Overview

The Voice Interaction capability pack provides speech-to-text (STT) and text-to-speech (TTS)
services with multi-provider fallback, language detection, and conversation turn management.

## Quick Start

### Python Backend

```python
from apps.voice_interaction import get_app

app = get_app()
result = await app.run("transcribe my voice memo", {
    "operation": "transcribe",
    "audio_data": "<base64-encoded-audio>",
    "source_language": "auto",
    "stt_provider": "whisper",
})
```

### Synchronous Execution

```python
from apps.voice_interaction.worker import VoiceInteractionWorker

worker = VoiceInteractionWorker()
result = worker.execute({
    "operation": "synthesize",
    "text": "Hello from Jenny, your AI assistant.",
    "target_language": "en",
    "tts_provider": "pyttsx3",
})
print(result["syntheses"])
```

## Operations

| Operation | Description | Key Fields |
|-----------|-------------|------------|
| `transcribe` | Speech-to-text via STT service | `audio_data`, `source_language`, `stt_provider` |
| `synthesize` | Text-to-speech via TTS service | `text`, `target_language`, `tts_voice`, `tts_speed` |
| `conversation` | Multi-turn voice conversation | `audio_data`, `text`, `source_language`, `target_language` |

## STT Providers

| Provider | Status | Notes |
|----------|--------|-------|
| `whisper` | Primary | High accuracy, local deployment |
| `openai` | Fallback 1 | Cloud API, requires API key |
| `web_speech` | Fallback 2 | Browser-based, no setup needed |

## TTS Providers

| Provider | Status | Notes |
|----------|--------|-------|
| `pyttsx3` | Primary | Offline, Python-native |
| `piper` | Fallback 1 | Neural, low-latency |
| `elevenlabs` | Fallback 2 | Cloud, high quality |
| `openai` | Fallback 3 | Cloud TTS with neural voices |

## Supported Languages (22)

en, id, es, fr, de, zh, ja, ar, pt, ru, ko, hi, th, vi, tl, nl, it, tr, pl, uk, ca, ms

## API Endpoints

```
GET  /api/voice/languages     — List supported languages
GET  /api/voice/providers     — List available providers
POST /api/voice/transcribe    — Transcribe audio
GET  /api/voice/speak         — Synthesize text to speech
WS   /ws/voice               — Real-time streaming voice
```

## Frontend Integration

```typescript
import { transcribeAudio, speakText, getSupportedLanguages } from '@/services/voice';

// Transcribe audio file
const transcript = await transcribeAudio(audioBlob, 'auto', 'whisper');

// Synthesize speech
await speakText("Hello from Jenny", 'en', 'pyttsx3');
```

## Benchmark

```bash
python benchmarks/voice_interaction_benchmark.py
```

Expected result: **Grade A** (≥90% overall score)
