# ROS 2 Connector

## Responsibility
Translate ECP actions into ROS 2 goals and relay sensor feedback back to ECP.

## Components
- `ROS2Connector`
- `ActionTranslator`
- `FeedbackRelay`

## Mapping
- ECP Action -> ROS 2 Action Goal (Nav2, MoveIt).
- ROS 2 Feedback -> ECP Action Event.
- ROS 2 Service -> ECP Capability Call.

## Flow
1. ECP emits action goal.
2. ActionTranslator converts to ROS 2 goal.
3. ROS 2 executes and streams feedback.
4. FeedbackRelay converts feedback to ECP events.
5. ECP updates workspace state and observability.

## Data Contract
```json
{
  "action_id": "string",
  "type": "navigation | manipulation | inspection",
  "goal": "string",
  "status": "pending | active | succeeded | failed | canceled",
  "feedback": {}
}
```

## VS Code Deliverables
- Add `apps/robotics/ros2_connector.py`
- Add `apps/robotics/action_translator.py`
- Add `apps/robotics/feedback_relay.py`
