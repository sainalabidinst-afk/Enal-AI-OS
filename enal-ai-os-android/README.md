# Enal AI OS — Native Android Stage 3

## Project
- Package: `com.enalai.os.android`
- Min SDK: 26
- Target SDK: 34
- Language: Kotlin
- UI: Jetpack Compose + Material 3

## Module Highlights
- `data/remote`: Retrofit + Moshi API client
- `data/local`: DataStore session persistence
- `domain`: repository contracts + use cases
- `ui/screen`: Compose screens for login, chat, observability, settings
- `voice`: native STT/TTS wrappers
- `consent`: Android notification-based consent channel
- `offline`: placeholder offline model cache module
- `observability`: bootstrap for native tracing/logging

## Next Steps
- Wire Retrofit login to UI
- Connect chat screen to `/api/v1/chat`
- Add biometric auth
- Add WorkManager for background sync
- Add Firebase Crashlytics/Performance
