# SimplAI Parity Implementation Plan

**Project:** Enal-AI-OS v3.1.0+  
**Objective:** Achieve feature parity with SimplAI platform capabilities  
**Date:** 2026-10-03  
**Status:** Completed ✅

---

## 1. Current State Assessment

### 1.1 Already Implemented ✅

| Feature | Backend | Frontend | Notes |
|---------|---------|----------|-------|
| Decorator SDK | ✅ | ✅ | `backend/app/core/decorators/`, `sdk/` |
| Pipeline Engine | ✅ | ✅ | `backend/app/core/pipeline_engine.py` |
| 7-Layer Memory | ✅ | ✅ | `backend/app/core/memory_layer.py` |
| Voice Agent (basic) | ✅ | ✅ | `backend/app/core/voice_vision_agent.py` + `VoiceAgentBuilder` |
| Consent Manager | ✅ | ✅ | `backend/app/core/consent.py`, `frontend/components/jenny/consent-dialog.tsx` |
| Observability | ✅ | ✅ | Backend tracing + frontend components |
| MCP Registry | ✅ | ✅ | `backend/app/core/mcp_registry.py` + `MCPConnector` |
| Event Bus | ✅ | ✅ | `backend/app/core/event_bus.py` |
| Connectors | ✅ | ✅ | FileSystem, Email, Calendar, SmartHome |
| Document Processing | ✅ | ✅ | PDF, DOCX, CSV |
| Translation | ✅ | ✅ | RFC-0041/ADR-021 |
| Scenario Simulator | ✅ | ✅ | 10 integration tests added |
| Visual Builder Foundation | ✅ | ✅ | ReactFlow canvas, nodes, toolbar |
| Visual Agent Builder | ✅ | ✅ | `AgentBuilder`, `AgentConfigPanel`, `/builder/agent` |
| Visual Tool Builder | ✅ | ✅ | `ToolBuilder`, `StepConfigPanel`, `/builder/tool` |
| Voice Agent Enhancements | ✅ | ✅ | `VoiceAgentBuilder`, STT/TTS, Telephony, LatencyMonitor |
| Guardrails & Safety | ✅ | ✅ | `GuardrailConfig`, `GuardrailEngine`, `/api/v1/guardrails` |
| Marketplace | ✅ | ✅ | `Marketplace`, `TemplateCard`, `CloneWizard`, `ShareDialog`, `/marketplace` |
| A2A/MCP Integration | ✅ | ✅ | `A2AConfig`, `MCPConnector`, `ExternalAgentCard`, `/api/v1/a2a`, `/api/v1/mcp` |
| Bulk/Scheduled/Evaluation | ✅ | ✅ | `BulkRun`, `ScheduleConfig`, `EvaluationDashboard`, `/bulk-evaluation` |

### 1.2 Gaps to Fill 🔴

| Feature | Gap | Priority |
|---------|-----|----------|
| Templates system | Pre-built templates need expansion | Medium |

---

## 2. Implementation Phases

### Phase 1: Visual Builder Foundation (FASE 10)
**Duration:** 2 weeks  
**Goal:** Create the UI/UX foundation for drag-drop builders  
**Status:** Completed ✅

#### 2.1.1 Design System Extensions
- [x] Create `frontend/components/builder/` directory
- [x] Build reusable canvas components:
  - `BuilderCanvas.tsx` — infinite canvas with pan/zoom
  - `BuilderToolbar.tsx` — palette of available nodes
  - `AgentNode.tsx` — draggable agent node
  - `ToolNode.tsx` — draggable tool node
  - `KnowledgeBaseNode.tsx` — knowledge base node
  - `ConditionalNode.tsx` — if/else node
  - `DelayNode.tsx` — delay node
- [x] Add DnD library: `reactflow`
- [x] State management: React state + props

#### 2.1.2 Backend Schema Extensions
- [ ] Add `AgentBlueprint` schema to `backend/app/core/schemas.py`
- [ ] Add `ToolBlueprint` schema with step graph model
- [ ] Add `BlueprintRepository` for persistence (JSON/PostgreSQL)
- [ ] Add API endpoints:
  - `POST /api/v1/blueprints/agent` — save agent blueprint
  - `POST /api/v1/blueprints/tool` — save tool blueprint
  - `GET /api/v1/blueprints` — list blueprints
  - `POST /api/v1/blueprints/{id}/deploy` — deploy blueprint

---

### Phase 2: Visual Agent Builder (FASE 11)
**Duration:** 2 weeks  
**Goal:** No-code agent builder UI

#### 2.2.1 Frontend Components
- [ ] `AgentBuilder.tsx` — main builder page
- [ ] `AgentNode.tsx` — agent node on canvas
- [ ] `KnowledgeBaseNode.tsx` — KB attachment node
- [ ] `ToolNode.tsx` — tool attachment node
- [ ] `AgentConfigPanel.tsx` — sidebar for agent config
- [ ] `AgentPreview.tsx` — test agent from builder

#### 2.2.2 Backend Logic
- [ ] `AgentFactory` in `backend/app/core/` — instantiate agent from blueprint
- [ ] `AgentValidator` — validate blueprint before deployment
- [ ] `AgentRuntime` — execute agent from blueprint
- [ ] Integration with existing `DecoratorRegistry` for middleware

#### 2.2.3 Features
- [ ] Drag-drop agent configuration
- [ ] Attach knowledge bases
- [ ] Attach tools
- [ ] Set prompts/instructions
- [ ] Test agent in playground
- [ ] Save/deploy agent

---

### Phase 3: Visual Tool Builder (FASE 12)
**Duration:** 2 weeks  
**Goal:** No-code tool builder with step graph

#### 2.3.1 Frontend Components
- [ ] `ToolBuilder.tsx` — main builder page
- [ ] `StepNode.tsx` — step node on canvas
- [ ] `StepConfigPanel.tsx` — configure step properties
- [ ] `ToolTestRunner.tsx` — test tool execution
- [ ] Step type palette:
  - LLM Call
  - Python Code
  - API Call
  - KB Search
  - Web Scraper
  - Conditional
  - Delay

#### 2.3.2 Backend Logic
- [ ] `ToolEngine` in `backend/app/core/` — execute tool from step graph
- [ ] `StepExecutor` — execute individual step types
- [ ] `StepValidator` — validate step graph
- [ ] `ConditionalEngine` — evaluate conditions
- [ ] Integration with existing `PipelineEngine`

#### 2.3.3 Features
- [ ] Visual step graph editor
- [ ] Connect steps with edges
- [ ] Configure step inputs/outputs
- [ ] Conditional branching
- [ ] Error handling per step
- [ ] Test execution
- [ ] Save/deploy tool

---

### Phase 4: Voice Agent Enhancements (FASE 13)
**Duration:** 1.5 weeks  
**Goal:** Production-ready voice agent with telephony

#### 2.4.1 Frontend Components
- [ ] `VoiceAgentBuilder.tsx` — voice-specific agent config
- [ ] `VoiceCallWidget.tsx` — embedded voice widget
- [ ] `VoiceHistory.tsx` — call recordings + transcripts

#### 2.4.2 Backend Logic
- [ ] `TelephonyIntegration` — Twilio/Plivo integration
- [ ] `STTService` — speech-to-text (Whisper/Deepgram)
- [ ] `TTSService` — text-to-speech (ElevenLabs/Azure)
- [ ] `VoiceQueue` — priority queue for voice runs
- [ ] `LatencyMonitor` — TTFS, P50/P90/P99 tracking
- [ ] `VoiceAgentRuntime` — STT → LLM → TTS pipeline

#### 2.4.3 Features
- [ ] Inbound call handling
- [ ] Outbound dialing
- [ ] Voice-specific guardrails
- [ ] Call recordings + transcripts
- [ ] Sub-second latency optimization
- [ ] Voice agent as workflow node

---

### Phase 5: Guardrails & Safety (FASE 14)
**Duration:** 1.5 weeks  
**Goal:** Comprehensive safety layer

#### 2.5.1 Backend Implementation
- [ ] `GuardrailEngine` in `backend/app/core/`
- [ ] Validators:
  - `PIIValidator` — detect PII (email, phone, SSN, credit card)
  - `ToxicLanguageValidator` — detect toxic content
  - `PromptInjectionValidator` — detect injection attacks
  - `BiasCheckValidator` — detect bias in output
  - `LogicCheckValidator` — validate logical consistency
  - `CompetitorCheckValidator` — detect competitor mentions
  - `GibberishValidator` — detect nonsense output
  - `ReadingLevelValidator` — validate reading complexity
- [ ] `CorrectiveAction` enum: FIX, NOOP, EXCEPTION
- [ ] `GuardrailPolicy` — reusable guardrail configurations
- [ ] Integration points:
  - Agent input/output
  - Tool step input/output
  - Voice agent (future)

#### 2.5.2 Frontend Components
- [ ] `GuardrailConfig.tsx` — configure guardrails
- [ ] `GuardrailTest.tsx` — test guardrails on sample input
- [ ] `GuardrailDashboard.tsx` — view guardrail triggers

---

### Phase 6: Marketplace & Templates (FASE 15)
**Duration:** 2 weeks  
**Goal:** Share and discover agents/tools

#### 2.6.1 Backend Implementation
- [ ] `MarketplaceService` in `backend/app/core/`
- [ ] `TemplateRegistry` — pre-built templates
- [ ] `SharingService` — share/unshare agents
- [ ] `CloningService` — clone agents with dependency resolution
- [ ] `AnalyticsService` — track clones, trials, impressions
- [ ] API endpoints:
  - `POST /api/v1/marketplace/share`
  - `POST /api/v1/marketplace/clone`
  - `GET /api/v1/marketplace/templates`
  - `GET /api/v1/marketplace/analytics`

#### 2.6.2 Frontend Components
- [ ] `Marketplace.tsx` — browse templates
- [ ] `TemplateCard.tsx` — template preview
- [ ] `CloneWizard.tsx` — guided cloning flow
- [ ] `ShareDialog.tsx` — share agent
- [ ] `TemplateBuilder.tsx` — create templates

---

### Phase 7: A2A/MCP Integration (FASE 16)
**Duration:** 1.5 weeks  
**Goal:** Agent-to-agent and external tool integration

#### 2.7.1 Backend Implementation
- [ ] `A2ARegistry` — register external A2A agents
- [ ] `A2AInvoker` — invoke external agents
- [ ] `MCPToolRegistry` — register MCP servers
- [ ] `MCPToolProxy` — proxy MCP tool calls
- [ ] Integration with existing `ToolRegistry`

#### 2.7.2 Frontend Components
- [ ] `A2AConfig.tsx` — configure A2A bindings
- [ ] `MCPConnector.tsx` — connect MCP servers
- [ ] `ExternalAgentCard.tsx` — display external agent

---

### Phase 8: Bulk, Scheduled & Evaluation (FASE 17)
**Duration:** 2 weeks  
**Goal:** Batch execution, scheduling, and quality evaluation

#### 2.8.1 Bulk & Scheduled Execution
- [ ] `BulkExecutor` in `backend/app/core/`
- [ ] `SchedulerService` — cron-like scheduling
- [ ] `WebhookService` — webhook triggers
- [ ] `AsyncQueue` — priority queue for async runs
- [ ] Frontend: `BulkRun.tsx`, `ScheduleConfig.tsx`

#### 2.8.2 Evaluation Framework
- [ ] `EvaluatorEngine` in `backend/app/core/`
- [ ] `QualityScorer` — score agent outputs
- [ ] `ScheduledEvaluator` — run evals on schedule
- [ ] `MetricDetails` — per-metric deep-dive
- [ ] Frontend: `EvaluationDashboard.tsx`, `MetricDetails.tsx`

---

## 3. Technology Stack

### Frontend
- **Framework:** Next.js 14 + React 18
- **Language:** TypeScript
- **Styling:** Tailwind CSS
- **State:** Zustand
- **DnD/Canvas:** Reactflow or @dnd-kit
- **Forms:** React Hook Form + Zod
- **API Client:** Axios or fetch

### Backend
- **Framework:** FastAPI
- **Language:** Python 3.11+
- **Schemas:** Pydantic v2
- **Database:** PostgreSQL (existing)
- **Cache:** Redis (existing)
- **Queue:** Celery or ARQ (new)
- **Telephony:** Twilio SDK or Plivo
- **STT/TTS:** Whisper/Deepgram + ElevenLabs/Azure

---

## 4. File Structure Plan

```
frontend/
├── components/
│   ├── builder/
│   │   ├── Canvas.tsx
│   │   ├── Node.tsx
│   │   ├── Edge.tsx
│   │   ├── Toolbar.tsx
│   │   ├── AgentBuilder.tsx
│   │   ├── ToolBuilder.tsx
│   │   ├── VoiceAgentBuilder.tsx
│   │   └── ...
│   ├── marketplace/
│   │   ├── Marketplace.tsx
│   │   ├── TemplateCard.tsx
│   │   └── CloneWizard.tsx
│   ├── guardrails/
│   │   ├── GuardrailConfig.tsx
│   │   └── GuardrailTest.tsx
│   └── ...
├── app/
│   ├── builder/
│   │   ├── agent/
│   │   ├── tool/
│   │   └── voice/
│   ├── marketplace/
│   └── ...

backend/app/core/
├── schemas.py (extend with blueprints)
├── agent_factory.py (new)
├── tool_engine.py (new)
├── guardrail_engine.py (new)
├── telephony_integration.py (new)
├── stt_service.py (new)
├── tts_service.py (new)
├── marketplace_service.py (new)
├── a2a_registry.py (new)
├── mcp_tool_registry.py (new)
├── bulk_executor.py (new)
├── scheduler_service.py (new)
├── evaluator_engine.py (new)
├── webhook_service.py (new)
└── ...
```

---

## 5. Dependencies & Risks

### Dependencies
- Reactflow or @dnd-kit for canvas (frontend)
- Twilio/Plivo SDK for telephony (backend)
- Whisper/Deepgram for STT (backend)
- ElevenLabs/Azure for TTS (backend)
- Celery/ARQ for async queues (backend)

### Risks
1. **Complexity:** Visual builders are complex; start with MVP
2. **Performance:** Canvas rendering with many nodes can be slow
3. **Latency:** Voice agent sub-second latency is challenging
4. **Security:** Guardrails must be robust to avoid bypasses
5. **Scalability:** Marketplace features need multi-tenant support

---

## 6. Success Criteria

| Feature | Success Metric |
|---------|---------------|
| Visual Agent Builder | Can create and deploy agent in < 5 min via UI |
| Visual Tool Builder | Can create tool with 3+ steps via UI |
| Voice Agent | < 500ms TTFS, 99% uptime |
| Guardrails | 95%+ detection rate for known threats |
| Marketplace | 10+ pre-built templates, 50+ clones |
| A2A/MCP | Support 5+ external integrations |
| Bulk/Scheduled | 1000+ batch runs/day |
| Evaluation | 90%+ correlation with human judgment |

---

## 7. Next Steps

1. **Week 1:** Set up Reactflow, create Canvas/Node/Edge components
2. **Week 2:** Build Agent Builder MVP (basic agent config)
3. **Week 3:** Build Tool Builder MVP (step graph)
4. **Week 4:** Voice Agent telephony integration
5. **Week 5:** Guardrails implementation
6. **Week 6+:** Marketplace, A2A, Bulk/Scheduled, Evaluation

---

## 8. Open Questions

1. Should we use Reactflow or @dnd-kit for the canvas? (Reactflow is more feature-rich)
2. Should we support both SimplAI-style no-code AND code-based builders? (Yes)
3. Should we support multi-tenant from day 1? (Yes, for marketplace)
4. Which telephony provider to use? (Twilio is most popular)
5. Which STT/TTS providers to support? (Start with OpenAI Whisper + ElevenLabs)

---

**Approved by:**  
**Date:**  

**Next Review:** 2026-10-10
