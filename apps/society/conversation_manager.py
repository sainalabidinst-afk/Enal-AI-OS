"""
Conversation Layer
==================

Bridges the ECP pipeline with the Chat API.

Responsibilities:
- Manage conversation state and history
- Route user messages through SocietyRuntime
- Emit streaming progress events
- Persist conversation memory
- Handle follow-up context
"""

import logging
import uuid
from collections.abc import AsyncGenerator
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from apps.society.society import SocietyRuntime, create_society

try:
    from backend.app.core.memory import conversation_store as _memory
    _MEMORY_AVAILABLE = True
except Exception:
    _MEMORY_AVAILABLE = False

logger = logging.getLogger(__name__)


@dataclass
class ConversationTurn:
    role: str
    content: str
    timestamp: datetime = field(default_factory=datetime.utcnow)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class ConversationState:
    conversation_id: str
    turns: list[ConversationTurn] = field(default_factory=list)
    current_domain: str | None = None
    context: dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)


class ConversationManager:
    """Manages conversation lifecycle and memory."""

    def __init__(self):
        self._society: SocietyRuntime | None = None
        self._states: dict[str, ConversationState] = {}
        self._local_memory: dict[str, list[dict[str, Any]]] = {}

    def _get_society(self) -> SocietyRuntime:
        if self._society is None:
            self._society = create_society("Enal AI OS")
        return self._society

    async def get_state(self, conversation_id: str) -> ConversationState:
        if conversation_id not in self._states:
            stored = await self._get_conversation(conversation_id)
            turns = []
            for msg in stored:
                turns.append(ConversationTurn(
                    role=msg.get("role", "user"),
                    content=msg.get("content", ""),
                    timestamp=datetime.fromisoformat(msg.get("timestamp", datetime.utcnow().isoformat())),
                    metadata=msg.get("metadata", {}),
                ))
            state = ConversationState(conversation_id=conversation_id, turns=turns)
            if turns:
                state.current_domain = turns[-1].metadata.get("domain")
            self._states[conversation_id] = state
        return self._states[conversation_id]

    async def send_message(self, conversation_id: str, user_message: str, context: dict[str, Any] | None = None) -> dict[str, Any]:
        state = await self.get_state(conversation_id)
        context = context or {}

        if state.current_domain:
            context["previous_domain"] = state.current_domain
        if len(state.turns) > 0:
            context["history"] = [
                {"role": t.role, "content": t.content} for t in state.turns[-6:]
            ]

        events: list[dict[str, Any]] = []
        events.append({"type": "status", "message": "Understanding your request..."})

        society = self._get_society()
        result = await society.process_user_request(user_message, context={
            "conversation_id": conversation_id,
            "history": context.get("history", []),
            "previous_domain": context.get("previous_domain"),
        })

        intent_domain = result.get("intent", {}).get("domain", "general")
        state.current_domain = intent_domain

        results_raw = result.get("result", {})
        if isinstance(results_raw, dict):
            results_list = results_raw.get("results", [])
        else:
            results_list = []
        if results_list:
            first = results_list[0]
            if hasattr(first, "result"):
                assistant_message = first.result or ""
            elif isinstance(first, dict):
                assistant_message = first.get("result", "")
            else:
                assistant_message = str(first)
        else:
            assistant_message = str(results_raw)

        analysis_payload = await self._maybe_analyze_attachments(user_message, context)

        user_turn = ConversationTurn(
            role="user",
            content=user_message,
            metadata={"domain": intent_domain},
        )
        assistant_turn = ConversationTurn(
            role="assistant",
            content=assistant_message,
            metadata={
                "domain": intent_domain,
                "intent": result.get("intent"),
                "task_plan": result.get("task_plan"),
                "execution_plan": result.get("execution_plan"),
                "team_size": result.get("team_size"),
                "analysis": analysis_payload,
            },
        )
        state.turns.extend([user_turn, assistant_turn])
        state.updated_at = datetime.utcnow()

        await self._persist_turn(conversation_id, user_turn)
        await self._persist_turn(conversation_id, assistant_turn)

        events.append({"type": "status", "message": "Done"})
        response = {
            "message": assistant_turn.content,
            "conversation_id": conversation_id,
            "domain": intent_domain,
            "events": events,
            "metadata": assistant_turn.metadata,
        }
        if analysis_payload:
            response["analysis"] = analysis_payload
        return response

    async def stream_message(self, conversation_id: str, user_message: str, context: dict[str, Any] | None = None) -> AsyncGenerator[dict[str, Any], None]:
        state = await self.get_state(conversation_id)
        context = context or {}

        if state.current_domain:
            context["previous_domain"] = state.current_domain
        if len(state.turns) > 0:
            context["history"] = [
                {"role": t.role, "content": t.content} for t in state.turns[-6:]
            ]

        lowered = user_message.lower()
        if any(keyword in lowered for keyword in ["what can you do", "capabilities", "list capability", "apa yang bisa"]):
            yield {"type": "capabilities", "capabilities": self._get_capability_summary()}
            return

        yield {"type": "status", "message": "Understanding your request..."}

        society = self._get_society()
        result = await society.process_user_request(user_message, context={
            "conversation_id": conversation_id,
            "history": context.get("history", []),
            "previous_domain": context.get("previous_domain"),
        })

        intent_domain = result.get("intent", {}).get("domain", "general")
        state.current_domain = intent_domain

        intent = result.get("intent", {})
        task_plan = result.get("task_plan", {})
        execution_plan = result.get("execution_plan", {})

        results_raw = result.get("result", {})
        if isinstance(results_raw, dict):
            results_list = results_raw.get("results", [])
        else:
            results_list = []
        if results_list:
            first = results_list[0]
            if hasattr(first, "result"):
                assistant_message = first.result or ""
            elif isinstance(first, dict):
                assistant_message = first.get("result", "")
            else:
                assistant_message = str(first)
        else:
            assistant_message = str(results_raw)

        artifact = {
            "conversation_id": conversation_id,
            "domain": intent_domain,
            "intent": intent,
            "task_plan": task_plan,
            "execution_plan": execution_plan,
            "result": results_raw,
            "timestamp": __import__("datetime").datetime.utcnow().isoformat(),
        }
        await self._persist_artifact(conversation_id, artifact)

        if task_plan:
            subtask_count = len(task_plan.get("subtasks", []))
            yield {"type": "plan", "subtasks": subtask_count, "strategy": task_plan.get("strategy")}
            for subtask in task_plan.get("subtasks", []):
                yield {"type": "status", "message": "Working on: " + subtask.get("name", "")}

        if execution_plan:
            for stage in execution_plan.get("stages", []):
                yield {"type": "stage", "mode": stage.get("mode"), "subtasks": stage.get("subtasks", [])}

        analysis_payload = await self._maybe_analyze_attachments(user_message, context)
        if analysis_payload:
            yield {"type": "analysis_progress", "message": "Analyzing attachments..."}
            yield {"type": "analysis", "analysis": analysis_payload}

        user_turn = ConversationTurn(
            role="user",
            content=user_message,
            metadata={"domain": intent_domain},
        )
        assistant_turn = ConversationTurn(
            role="assistant",
            content=assistant_message,
            metadata={
                "domain": intent_domain,
                "intent": intent,
                "task_plan": task_plan,
                "execution_plan": execution_plan,
                "team_size": result.get("team_size"),
                "artifact_id": artifact.get("id"),
                "analysis": analysis_payload,
            },
        )
        state.turns.extend([user_turn, assistant_turn])
        state.updated_at = datetime.utcnow()

        await self._persist_turn(conversation_id, user_turn)
        await self._persist_turn(conversation_id, assistant_turn)

        yield {
            "type": "final",
            "message": assistant_turn.content,
            "conversation_id": conversation_id,
            "domain": intent_domain,
            "intent": intent,
            "task_plan": task_plan,
            "execution_plan": execution_plan,
            "team_size": result.get("team_size"),
            "artifact": artifact,
            "metadata": assistant_turn.metadata,
        }

    def _get_capability_summary(self) -> dict[str, Any]:
        try:
            from apps.organization.capability_graph import capability_graph
            from apps.society.intent_router import intent_router
            domains = {}
            for domain, pack in intent_router._capability_packs.items():
                if domain.value == "general":
                    continue
                templates = capability_graph.get_subtask_templates(domain.value)
                domains[domain.value] = {
                    "description": pack.description,
                    "capabilities": pack.capabilities,
                    "workers": pack.workers,
                    "subtasks": [t.name for t in templates],
                }
            return {
                "domains": list(domains.keys()),
                "details": domains,
                "total": len(domains),
            }
        except Exception:
            return {
                "domains": ["network", "code", "research", "devops", "trading", "self-development"],
                "total": 6,
            }

    async def get_history(self, conversation_id: str) -> list[dict[str, Any]]:
        state = await self.get_state(conversation_id)
        return [
            {
                "role": t.role,
                "content": t.content,
                "timestamp": t.timestamp.isoformat(),
                "metadata": t.metadata,
            }
            for t in state.turns
        ]

    async def clear_history(self, conversation_id: str) -> None:
        if conversation_id in self._states:
            del self._states[conversation_id]
        self._local_memory.pop(conversation_id, None)
        if _MEMORY_AVAILABLE:
            try:
                await _memory.clear_conversation(conversation_id)
            except Exception:
                pass

    async def _get_conversation(self, conversation_id: str) -> list[dict[str, Any]]:
        if not _MEMORY_AVAILABLE:
            return self._local_memory.get(conversation_id, [])
        try:
            return await _memory.get_conversation(conversation_id)
        except Exception:
            return self._local_memory.get(conversation_id, [])

    async def _persist_turn(self, conversation_id: str, turn: ConversationTurn) -> None:
        message = {
            "role": turn.role,
            "content": turn.content,
            "timestamp": turn.timestamp.isoformat(),
            "metadata": turn.metadata,
        }
        if not _MEMORY_AVAILABLE:
            self._local_memory.setdefault(conversation_id, []).append(message)
            return
        try:
            await _memory.append_message(conversation_id, message)
        except Exception:
            self._local_memory.setdefault(conversation_id, []).append(message)

    async def _persist_artifact(self, conversation_id: str, artifact: dict[str, Any]) -> None:
        artifact_id = "artifact-" + uuid.uuid4().hex[:8]
        artifact["id"] = artifact_id
        if not _MEMORY_AVAILABLE:
            return
        try:
            msg = {
                "role": "system",
                "content": artifact_id,
                "metadata": artifact,
            }
            await _memory.append_message(conversation_id, msg)
        except Exception:
            pass

    async def _maybe_analyze_attachments(self, user_message: str, context: dict[str, Any]) -> dict[str, Any] | None:
        lowered = user_message.lower()
        attachment_triggers = ["audit", "analyze", "analysis", "review", "cek", "periksa", "upload", "file", "config", "configuration"]
        if not any(trigger in lowered for trigger in attachment_triggers):
            return None

        files = context.get("files") or []
        if not files:
            return None

        try:
            from backend.app.core.attachments.analyzer import analyze_multi

            items = []
            uploads = files if isinstance(files, list) else [files]
            for upload in uploads:
                if hasattr(upload, "read"):
                    content = await upload.read()
                    filename = getattr(upload, "filename", "uploaded")
                elif isinstance(upload, dict):
                    content = upload.get("content", b"")
                    filename = upload.get("filename", "uploaded")
                else:
                    continue
                items.append((filename, content))

            compliance = [value for value in context.get("compliance_frameworks", []) if value in {"cis", "nist_csf", "zero_trust", "vendor_best_practice"}]
            analysis = analyze_multi(items, compliance_frameworks=compliance or None)

            payload = analysis.ast.to_dict()
            payload["summary"] = analysis.summary
            payload["risk_score"] = analysis.risk_score
            payload["recommendations"] = analysis.recommendations
            if analysis.analysis_error:
                payload["analysis_error"] = analysis.analysis_error
            return payload
        except Exception as exc:
            logger.warning("Attachment analysis failed: %s", exc)
            return None


conversation_manager = ConversationManager()
