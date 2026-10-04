# Live Stream Session

## Responsibility
Transport low-latency voice + camera frames to ECP backend.

## Requirements
- Start/Stop from Compose UI.
- Consent before camera/mic activation.
- Compressed audio and video frames.
- Backend endpoint candidate: `/api/v1/chat/live`.

## Data Contract
```json
{
  "session_id": "string",
  "status": "idle | active | ended",
  "audio_format": "opus",
  "video_format": "h264",
  "backend_url": "string"
}
```

## VS Code Deliverables
- Update `enal-ai-os-android/app/src/main/java/com/enalai/os/android/camera/LiveStreamSession.kt`
- Update `enal-ai-os-android/app/src/main/java/com/enalai/os/android/voice/VoiceStreamBridge.kt`
- Add backend endpoint requirements doc.
