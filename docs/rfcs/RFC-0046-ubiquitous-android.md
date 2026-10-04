# RFC-0046 — Pilar 3: Native Android & Ubiquitous Experience

## Status
Proposed

## Summary
Define the architecture and implementation boundaries for **Pilar 3: Native Android & Ubiquitous Experience** on top of ECP Core + Stage 2 React Native + Stage 3 native bootstrap.

## Motivation
- Make ECP available offline and hands-free.
- Reduce latency for routine interactions via on-device inference.
- Extend ECP from app-only to ambient assistant across devices.

## Goals
- Deliver always-on wake-word + voice interaction on Android.
- Provide offline-first chat with automatic cloud escalation.
- Enable live multi-modal inspection (voice + camera stream).
- Keep backend as source of truth for complex reasoning.

## Non-Goals
- Full robotics/ROS2 integration (Pilar 1).
- Digital twin simulation at scale (Pilar 2).
- Autonomous capability synthesis (Pilar 4).
- Final Android Studio build/run workflows.

## Architecture

### Layering
- **App Layer:** Jetpack Compose screens.
- **Agent Layer:** Ambient Agent, Hybrid Chat Router.
- **Native Bridge Layer:** Wake-word engine, STT/TTS, Camera/WebRTC bridge.
- **Edge Inference Layer:** On-device SLM.
- **Cloud Layer:** ECP backend `/api/v1/*`.

### Components
- `HybridChatRouter`: route between on-device SLM and backend `/api/v1/chat`.
- `WakeWordEngine`: keyword spotting for "Hey Jenny".
- `AmbientAgentService`: foreground service with consent gate.
- `LiveStreamSession`: camera + audio capture and transport contract.
- `OnDeviceSlmClient`: ExecuTorch/MediaPipe LLM Inference wrapper.

## Contracts

### Chat Routing
- Simple request -> on-device SLM.
- Complex/insufficient -> backend `/api/v1/chat`.
- Response -> same chat UI contract as Stage 2 mobile.

### Voice Trigger
- Wake word detected -> start STT -> send to chat router.
- No wake word -> passive ambient listening disabled.

### Live Stream
- Start/Stop stream from Compose UI.
- Low-latency audio + compressed video frames to backend.
- Consent required before camera activation.

## Implementation Plan

### Phase 1 — Design
- [x] RFC-0046 scope, contracts, and component boundaries.
- [ ] Detail data models for `HybridChatRequest`, `StreamSession`, `SlmCapabilities`.
- [ ] Define consent requirements and risk classification.

### Phase 2 — VS Code Artifacts
- [ ] Update `enal-ai-os-android/` module map with new packages.
- [ ] Add backend stream endpoint contract `/api/v1/chat/live`.
- [ ] Add ADR for on-device SLM vendor selection.
- [ ] Add QA checklist for offline/online handoff.

### Phase 3 — Android Studio Execution
- [ ] Implement `WakeWordEngine` with selected vendor.
- [ ] Implement `HybridChatRouter` + `OnDeviceSlmClient`.
- [ ] Implement `AmbientAgentService` and consent flow.
- [ ] Implement `LiveStreamSession` and backend transport.
- [ ] Performance testing and optimization.

## Risks
- Vendor lock-in for wake-word/SLM runtime.
- Battery impact from always-on microphone/camera.
- Privacy and consent compliance for ambient capture.

## Metrics
- Wake-word latency < 300 ms.
- Offline chat response latency < 1 s.
- Cloud handoff latency < 2 s.
- Battery overhead < 5% for ambient idle state.
