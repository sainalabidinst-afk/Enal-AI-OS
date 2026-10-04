# Pilar 1 — VS Code Artifacts

## Scope
Design and contract artifacts for **Pilar 1: Physical & Autonomous Robotics Integration**.

## What this folder contains
- `RFC-0048-robotics-edge-integration.md` — overarching RFC.
- `design/edge-runtime.md` — lightweight edge runtime subset.
- `design/ros2-connector.md` — ROS 2 integration contract.
- `design/vision-engine.md` — computer vision inference pipeline.
- `design/smart-agri-connector.md` — IoT agriculture/poultry automation.

## Implementation Roadmap
1. Edge Runtime + Edge State Cache
2. ROS 2 Connector + Action Translator
3. Vision Engine + Inference Pipeline
4. Smart Agri Connector
5. Edge device testing and optimization

## Acceptance Criteria
- Edge decision latency < 100 ms
- ROS 2 action latency < 50 ms
- Vision inference latency < 30 ms on Jetson Nano
- Edge offline autonomy >= 4 hours
- MQTT message latency < 10 ms
