# Android Studio Handoff Checklist

## Before Opening Android Studio
- [ ] Install JDK 17
- [ ] Install Android Studio Hedgehog / Iguana
- [ ] Clone repo and open `enal-ai-os-android/` as project
- [ ] Accept Android SDK licenses
- [ ] Create `local.properties` with `sdk.dir`

## Module Setup
- [ ] Sync Gradle with `settings.gradle.kts`
- [ ] Verify `app/build.gradle.kts` compiles
- [ ] Add vendor SDKs after ADR decision:
  - [ ] Wake-word engine
  - [ ] ExecuTorch / MediaPipe LLM Inference
  - [ ] WebRTC / CameraX
  - [ ] Biometric library

## Implementation Order
1. `HybridChatRouter` + `OnDeviceSlmClient`
2. `WakeWordEngine` + `AmbientAgentService`
3. `LiveStreamSession` + `VoiceStreamBridge`
4. Biometric auth in `LoginScreen`
5. Performance tests and QA smoke test

## Acceptance Criteria
- Wake-word latency < 300 ms
- Offline chat response < 1 s
- Cloud handoff < 2 s
- Battery overhead < 5% for ambient idle
