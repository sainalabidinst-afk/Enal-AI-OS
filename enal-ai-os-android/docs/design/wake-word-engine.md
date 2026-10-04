# Wake-Word Engine

## Responsibility
Detect wake phrase and trigger ambient agent flow.

## Requirements
- Always-on low-power keyword spotting.
- Local-only audio processing before wake phrase.
- Consent required before microphone activation.
- Foreground service notification when ambient agent is active.

## Flow
1. Passive listening in foreground service.
2. Wake phrase detected.
3. Request runtime microphone consent if missing.
4. Start STT.
5. Send transcript to chat router.
6. Return to passive listening.

## VS Code Deliverables
- Update `enal-ai-os-android/app/src/main/java/com/enalai/os/android/voice/WakeWordEngine.kt`
- Add `AmbientAgentService.kt` contract.
- Add consent flow note for Android 13+ notification/mic permissions.
