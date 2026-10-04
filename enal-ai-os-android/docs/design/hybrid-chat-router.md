# Hybrid Chat Router

## Responsibility
Route chat requests between on-device SLM and ECP backend.

## States
- `ON_DEVICE_READY`
- `CLOUD_ONLY`
- `HYBRID`

## Decision Rules
- If device offline -> on-device SLM only.
- If request contains complex goal keywords -> backend.
- If on-device confidence below threshold -> backend.
- If user explicitly requests cloud -> backend.

## Data Contract
```json
{
  "route": "on_device | cloud",
  "confidence": 0.0,
  "response": "string",
  "conversation_id": "string",
  "latency_ms": 0
}
```

## VS Code Deliverables
- Update `enal-ai-os-android/app/src/main/java/com/enalai/os/android/agent/HybridChatRouter.kt`
- Add `OnDeviceSlmClient.kt` interface contract.
- Add backend fallback behavior spec.
