# Pilar 3 Design Notes — VS Code Artifacts

## Scope
Design and contract artifacts for **Pilar 3: Native Android & Ubiquitous Experience**.

## What this folder contains
- `RFC-0046-ubiquitous-android.md` — overarching RFC.
- `design/hybrid-chat-router.md` — on-device vs backend chat routing contract.
- `design/wake-word-engine.md` — wake-word detection requirements and consent flow.
- `design/live-stream-session.md` — multi-modal stream contract for voice + camera.

## Android Studio Handoff
- Implement `enal-ai-os-android/app/src/main/java/com/enalai/os/android/agent/`
- Implement `enal-ai-os-android/app/src/main/java/com/enalai/os/android/voice/`
- Implement `enal-ai-os-android/app/src/main/java/com/enalai/os/android/camera/`
- Add vendor SDKs per ADR linked from RFC-0046.

## Backend Contracts
- Existing: `POST /api/v1/chat`
- Candidate: `POST /api/v1/chat/live` for stream session metadata
- Existing: `GET /api/v1/observability/logs`, `/api/v1/observability/trace`
