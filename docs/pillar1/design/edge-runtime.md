# Edge Runtime

## Responsibility
Run a lightweight subset of ECP Cognitive Kernel on edge devices with limited resources.

## Components
- `EdgePerception`
- `EdgeMemory`
- `EdgeDecision`
- `EdgeAction`
- `EdgeStateCache`

## Capabilities
- Perception: basic sensor input processing.
- Memory: Working Memory only (no Long-term/Knowledge).
- Decision: rule-based + lightweight model inference.
- Action: direct hardware/ROS 2 actuation.

## Offline Behavior
- Operate fully autonomously if cloud unreachable.
- Cache state locally in `EdgeStateCache`.
- Sync when connection restored.

## Data Contract
```json
{
  "device_id": "string",
  "status": "online | offline | degraded",
  "capabilities": ["perception", "decision", "action"],
  "latency_ms": 0,
  "battery_percent": 0
}
```

## VS Code Deliverables
- Add `apps/robotics/edge_runtime/`
- Add `apps/robotics/edge_state_cache.py`
- Update `backend/app/core/` to support edge mode.
