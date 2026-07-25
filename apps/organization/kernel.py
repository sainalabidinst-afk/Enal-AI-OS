"""
Organization Kernel
====================

The central authority of the AI Workforce.
Enforces the Constitution, manages lifecycle, resolves conflicts,
tracks productivity, allocates budget, and manages resources.

Analogy: Linux Kernel manages processes, threads, and scheduling.
Organization Kernel manages organizations, teams, and workers.
"""

import logging
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any

from apps.organization.communication import Event, event_bus

logger = logging.getLogger(__name__)


class OrgEventType(str, Enum):
    WORKER_CREATED = "worker_created"
    WORKER_ASSIGNED = "worker_assigned"
    WORKER_COMPLETED = "worker_completed"
    WORKER_FAILED = "worker_failed"
    WORKER_RETIRED = "worker_retired"
    TEAM_FORMED = "team_formed"
    PROJECT_STARTED = "project_started"
    PROJECT_COMPLETED = "project_completed"
    CONFLICT_DETECTED = "conflict_detected"
    CONFLICT_RESOLVED = "conflict_resolved"
    BUDGET_ALLOCATED = "budget_allocated"
    RESOURCE_REQUESTED = "resource_requested"
    CONSTITUTION_VIOLATION = "constitution_violation"


@dataclass
class Budget:
    total: float = 0.0
    allocated: float = 0.0
    spent: float = 0.0
    currency: str = "USD"
    period_start: datetime = field(default_factory=datetime.utcnow)
    period_end: datetime | None = None


@dataclass
class ResourceRequest:
    id: str
    requester_id: str
    resource_type: str
    description: str
    estimated_cost: float = 0.0
    status: str = "pending"
    approved_by: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class ConflictRecord:
    id: str
    level: int
    parties: list[str]
    description: str
    status: str = "open"
    resolution: str = ""
    resolved_by: str | None = None
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class ProductivityMetrics:
    worker_id: str
    tasks_completed: int = 0
    tasks_failed: int = 0
    avg_completion_time_seconds: float = 0.0
    total_cost: float = 0.0
    quality_score: float = 0.0
    collaboration_score: float = 0.0
    last_updated: datetime = field(default_factory=datetime.utcnow)


class OrganizationKernel:
    """Central authority for the AI Workforce."""

    def __init__(self):
        self._budget = Budget()
        self._resource_requests: dict[str, ResourceRequest] = {}
        self._conflicts: dict[str, ConflictRecord] = {}
        self._productivity: dict[str, ProductivityMetrics] = {}
        self._worker_lifecycle: dict[str, list[dict[str, Any]]] = {}
        self._constitution_events: list[dict[str, Any]] = []
        self._register_event_handlers()

    def set_budget(self, total: float, currency: str = "USD") -> None:
        self._budget = Budget(total=total, currency=currency)
        logger.info("Budget set: %s %s", total, currency)

    def allocate_budget(self, amount: float, recipient_id: str, purpose: str) -> bool:
        if self._budget.allocated + amount > self._budget.total:
            logger.warning("Budget exceeded: requested %s, available %s", amount, self._budget.total - self._budget.allocated)
            return False
        self._budget.allocated += amount
        self._publish_event(OrgEventType.BUDGET_ALLOCATED, {
            "amount": amount,
            "recipient_id": recipient_id,
            "purpose": purpose,
        })
        logger.info("Budget allocated: %s to %s for %s", amount, recipient_id, purpose)
        return True

    def record_expense(self, amount: float, worker_id: str, task_id: str) -> None:
        self._budget.spent += amount
        metrics = self._productivity.get(worker_id)
        if metrics:
            metrics.total_cost += amount

    def request_resource(self, requester_id: str, resource_type: str, description: str, estimated_cost: float = 0.0) -> ResourceRequest:
        request_id = f"res-{uuid.uuid4().hex[:8]}"
        request = ResourceRequest(
            id=request_id,
            requester_id=requester_id,
            resource_type=resource_type,
            description=description,
            estimated_cost=estimated_cost,
        )
        self._resource_requests[request_id] = request
        self._publish_event(OrgEventType.RESOURCE_REQUESTED, {
            "request_id": request_id,
            "requester_id": requester_id,
            "resource_type": resource_type,
        })
        logger.info("Resource requested: %s by %s", resource_type, requester_id)
        return request

    def approve_resource(self, request_id: str, approver_id: str) -> ResourceRequest | None:
        request = self._resource_requests.get(request_id)
        if not request:
            return None
        if request.status != "pending":
            return None
        request.status = "approved"
        request.approved_by = approver_id
        self._publish_event(OrgEventType.BUDGET_ALLOCATED, {
            "request_id": request_id,
            "approved_by": approver_id,
        })
        logger.info("Resource approved: %s by %s", request_id, approver_id)
        return request

    def detect_conflict(self, level: int, parties: list[str], description: str) -> ConflictRecord:
        conflict_id = f"conflict-{uuid.uuid4().hex[:8]}"
        conflict = ConflictRecord(
            id=conflict_id,
            level=level,
            parties=parties,
            description=description,
        )
        self._conflicts[conflict_id] = conflict
        self._publish_event(OrgEventType.CONFLICT_DETECTED, {
            "conflict_id": conflict_id,
            "level": level,
            "parties": parties,
            "description": description,
        })
        logger.warning("Conflict detected: %s (level %d)", description, level)
        return conflict

    def resolve_conflict(self, conflict_id: str, resolution: str, resolved_by: str) -> ConflictRecord | None:
        conflict = self._conflicts.get(conflict_id)
        if not conflict:
            return None
        conflict.status = "resolved"
        conflict.resolution = resolution
        conflict.resolved_by = resolved_by
        self._publish_event(OrgEventType.CONFLICT_RESOLVED, {
            "conflict_id": conflict_id,
            "resolution": resolution,
            "resolved_by": resolved_by,
        })
        logger.info("Conflict resolved: %s by %s", conflict_id, resolved_by)
        return conflict

    def track_productivity(self, worker_id: str, task_completed: bool, completion_time_seconds: float = 0.0, quality_score: float = 0.0) -> None:
        if worker_id not in self._productivity:
            self._productivity[worker_id] = ProductivityMetrics(worker_id=worker_id)
        metrics = self._productivity[worker_id]
        if task_completed:
            metrics.tasks_completed += 1
            metrics.avg_completion_time_seconds = (
                (metrics.avg_completion_time_seconds * (metrics.tasks_completed - 1) + completion_time_seconds) / metrics.tasks_completed
            )
        else:
            metrics.tasks_failed += 1
        metrics.quality_score = quality_score
        metrics.last_updated = datetime.utcnow()

    def get_productivity(self, worker_id: str) -> ProductivityMetrics | None:
        return self._productivity.get(worker_id)

    def get_budget_status(self) -> dict[str, Any]:
        return {
            "total": self._budget.total,
            "allocated": self._budget.allocated,
            "spent": self._budget.spent,
            "available": self._budget.total - self._budget.allocated,
            "utilization": (self._budget.spent / self._budget.total * 100) if self._budget.total > 0 else 0,
        }

    def get_conflicts(self, status: str | None = None) -> list[ConflictRecord]:
        conflicts = list(self._conflicts.values())
        if status:
            conflicts = [c for c in conflicts if c.status == status]
        return conflicts

    def get_resource_requests(self, status: str | None = None) -> list[ResourceRequest]:
        requests = list(self._resource_requests.values())
        if status:
            requests = [r for r in requests if r.status == status]
        return requests

    def _publish_event(self, event_type: OrgEventType, data: dict[str, Any]) -> None:
        event = Event(event_type=event_type.value, source="organization_kernel", data=data)
        event_bus.publish(event)

    def _register_event_handlers(self) -> None:
        event_bus.subscribe(OrgEventType.WORKER_CREATED.value, self._on_worker_created)
        event_bus.subscribe(OrgEventType.WORKER_COMPLETED.value, self._on_worker_completed)
        event_bus.subscribe(OrgEventType.WORKER_FAILED.value, self._on_worker_failed)
        event_bus.subscribe(OrgEventType.PROJECT_COMPLETED.value, self._on_project_completed)

    def _on_worker_created(self, event: Any) -> None:
        data = event.data if hasattr(event, "data") else event
        worker_id = data.get("worker_id", "")
        self._worker_lifecycle.setdefault(worker_id, []).append({
            "event": "created",
            "timestamp": datetime.utcnow().isoformat(),
        })

    def _on_worker_completed(self, event: Any) -> None:
        data = event.data if hasattr(event, "data") else event
        worker_id = data.get("worker_id", "")
        self._worker_lifecycle.setdefault(worker_id, []).append({
            "event": "completed",
            "timestamp": datetime.utcnow().isoformat(),
        })

    def _on_worker_failed(self, event: Any) -> None:
        data = event.data if hasattr(event, "data") else event
        worker_id = data.get("worker_id", "")
        self._worker_lifecycle.setdefault(worker_id, []).append({
            "event": "failed",
            "timestamp": datetime.utcnow().isoformat(),
        })

    def _on_project_completed(self, event: Any) -> None:
        data = event.data if hasattr(event, "data") else event
        project_id = data.get("project_id", "")
        self._publish_event(OrgEventType.PROJECT_COMPLETED, {
            "project_id": project_id,
            "budget_spent": self._budget.spent,
            "workers_active": len(self._productivity),
        })


organization_kernel = OrganizationKernel()
