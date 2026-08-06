# Society Capability

## Overview

Society capability simulates multi-agent social dynamics, conversation management, executive decision-making, and intent routing within ENAL AI OS.

## Architecture

### Modules

- `agent.py` — Base agent implementation
- `conversation_manager.py` — Conversation state and turn management
- `executive.py` — Executive decision-making and oversight
- `intent_router.py` — Intent classification and routing
- `society.py` — Society simulation and coordination

## Contracts

- Agent creation and lifecycle
- Conversation initiation and management
- Intent resolution and routing
- Executive oversight and intervention

## Observability

Society exposes metrics for agent interactions, conversation flow, and executive decisions.

## Limitations

- Simplified social model; complex societal dynamics are not fully represented
- Conversation depth is limited by context window constraints
