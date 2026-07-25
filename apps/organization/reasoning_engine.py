"""
Reasoning Engine
================

Multi-step reasoning, decision making, and validation engine.

Reasoning Engine mampu:
    - Forward chaining: dari goal → sub-goals → actions
    - Backward chaining: dari desired outcome → required prerequisites
    - Decision making: memilih aksi terbaik berdasarkan evidence
    - Validation: memverifikasi hasil sebelum melanjutkan
    - Constraint propagation: memastikan semua constraint terpenuhi
    - Causal reasoning: memahami cause-effect relationships

Reasoning Engine BUKAN LLM-based reasoning.
Ini adalah symbolic/rule-based reasoning engine yang menggunakan
aturan deterministik dan graph traversal.

Flow:
    Input (goal, context, evidence)
        ↓
    ReasoningEngine.reason()
        ↓
    ├── Analyze context and evidence
    ├── Apply reasoning rules
    ├── Generate conclusions
    ├── Validate against constraints
    └── Return ReasoningResult
"""

import logging
import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum
from typing import Any

from apps.organization.capability_graph import capability_graph
from apps.organization.communication import Event, event_bus

logger = logging.getLogger(__name__)

# ─── Telemetry Events ───

REASONING_STARTED = "ReasoningStarted"
REASONING_COMPLETED = "ReasoningCompleted"
REASONING_FAILED = "ReasoningFailed"
REASONING_RULE_APPLIED = "ReasoningRuleApplied"
REASONING_DECISION_MADE = "ReasoningDecisionMade"

# ─── Enums ───


class ReasoningMethod(str, Enum):
    FORWARD_CHAINING = "forward_chaining"
    BACKWARD_CHAINING = "backward_chaining"
    DECISION_TREE = "decision_tree"
    CONSTRAINT_PROPAGATION = "constraint_propagation"
    CAUSAL_REASONING = "causal_reasoning"


class ReasoningStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    INCONCLUSIVE = "inconclusive"


class EvidenceType(str, Enum):
    FACT = "fact"
    RULE = "rule"
    CONSTRAINT = "constraint"
    OBSERVATION = "observation"
    DERIVED = "derived"


class DecisionUrgency(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


# ─── Data Classes ───


@dataclass
class Evidence:
    """A piece of evidence used in reasoning.

    Attributes:
        id: Unique identifier.
        type: Type of evidence.
        description: Human-readable description.
        value: The evidence value/data.
        source: Where this evidence came from.
        confidence: Confidence in this evidence (0.0-1.0).
        metadata: Additional metadata.
    """
    id: str
    type: EvidenceType
    description: str
    value: Any = None
    source: str = ""
    confidence: float = 1.0
    timestamp: datetime = field(default_factory=lambda: datetime.now(UTC))
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class ReasoningRule:
    """A reasoning rule that maps conditions to conclusions.

    Attributes:
        rule_id: Unique identifier.
        name: Human-readable name.
        description: Description of what this rule does.
        conditions: List of condition descriptions that must be true.
        conclusions: List of conclusions when conditions are met.
        confidence: Confidence when this rule fires.
        priority: Priority for conflict resolution.
        metadata: Additional metadata.
    """
    rule_id: str
    name: str
    description: str
    conditions: list[str] = field(default_factory=list)
    conclusions: list[str] = field(default_factory=list)
    confidence: float = 0.8
    priority: int = 5
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class Decision:
    """A decision made by the reasoning engine.

    Attributes:
        decision_id: Unique identifier.
        description: What this decision is about.
        options: Available options considered.
        selected: The selected option.
        confidence: Confidence in this decision.
        reasoning: Explanation of why this decision was made.
        urgency: Urgency level.
        consequences: Expected consequences of this decision.
    """
    decision_id: str
    description: str
    options: list[str] = field(default_factory=list)
    selected: str | None = None
    confidence: float = 0.0
    reasoning: str = ""
    urgency: DecisionUrgency = DecisionUrgency.MEDIUM
    consequences: list[str] = field(default_factory=list)


@dataclass
class Conclusion:
    """A conclusion reached by the reasoning engine.

    Attributes:
        conclusion_id: Unique identifier.
        statement: The conclusion statement.
        confidence: Confidence in this conclusion (0.0-1.0).
        evidence_ids: Evidence that supports this conclusion.
        rule_id: The rule that produced this conclusion.
        derived: Whether this conclusion was derived (vs direct).
    """
    conclusion_id: str
    statement: str
    confidence: float = 0.0
    evidence_ids: list[str] = field(default_factory=list)
    rule_id: str = ""
    derived: bool = False


@dataclass
class ReasoningResult:
    """The output of a reasoning process.

    Attributes:
        reasoning_id: Unique identifier for this reasoning session.
        method: The reasoning method used.
        status: Status of the reasoning process.
        goal: The original goal/question.
        evidence: All evidence collected.
        conclusions: Conclusions reached.
        decisions: Decisions made.
        confidence: Overall confidence in the result.
        explanation: Human-readable explanation of the reasoning.
        execution_time_ms: Time taken.
    """
    reasoning_id: str
    method: ReasoningMethod
    status: ReasoningStatus
    goal: str
    evidence: list[Evidence] = field(default_factory=list)
    conclusions: list[Conclusion] = field(default_factory=list)
    decisions: list[Decision] = field(default_factory=list)
    confidence: float = 0.0
    explanation: str = ""
    execution_time_ms: float = 0.0
    metadata: dict[str, Any] = field(default_factory=dict)


# ─── Reasoning Engine ───


class ReasoningEngine:
    """Multi-step symbolic reasoning engine.

    Uses deterministic rules and graph-based reasoning to:
        - Decompose complex goals
        - Make decisions based on evidence
        - Validate constraints
        - Provide explainable reasoning chains
    """

    def __init__(self):
        self._rules: dict[str, ReasoningRule] = {}
        self._results: dict[str, ReasoningResult] = {}
        self._knowledge_base: dict[str, Evidence] = {}
        self._register_default_rules()

    def _register_default_rules(self) -> None:
        """Register built-in reasoning rules."""
        default_rules = [
            ReasoningRule(
                rule_id="goal-decomposition",
                name="Goal Decomposition",
                description="Decompose complex goals into simpler sub-goals",
                conditions=[
                    "goal is complex",
                    "goal can be split into independent parts",
                ],
                conclusions=[
                    "complex goal should be decomposed",
                    "each sub-goal can be solved independently",
                    "sub-goals should be ordered by dependency",
                ],
                confidence=0.9,
                priority=1,
            ),
            ReasoningRule(
                rule_id="capability-requirement",
                name="Capability Requirement",
                description="Identify required capabilities based on goal",
                conditions=[
                    "goal has specific domain requirements",
                    "capabilities exist for the domain",
                ],
                conclusions=[
                    "required capabilities can be found in catalog",
                    "each capability maps to a workflow or step",
                ],
                confidence=0.85,
                priority=2,
            ),
            ReasoningRule(
                rule_id="dependency-resolution",
                name="Dependency Resolution",
                description="Resolve dependencies between steps",
                conditions=[
                    "multiple steps are required",
                    "steps have input-output relationships",
                ],
                conclusions=[
                    "steps should be ordered by dependency",
                    "independent steps can run in parallel",
                    "dependent steps must run sequentially",
                ],
                confidence=0.9,
                priority=3,
            ),
            ReasoningRule(
                rule_id="constraint-validation",
                name="Constraint Validation",
                description="Validate that all constraints are satisfied",
                conditions=[
                    "constraints are defined for this goal",
                    "evidence exists for each constraint",
                ],
                conclusions=[
                    "constraints must be validated before execution",
                    "unmet constraints block execution",
                ],
                confidence=0.95,
                priority=4,
            ),
            ReasoningRule(
                rule_id="resource-planning",
                name="Resource Planning",
                description="Plan resource allocation based on requirements",
                conditions=[
                    "task requires specific resources or skills",
                    "resources are available in the organization",
                ],
                conclusions=[
                    "resources should be allocated efficiently",
                    "resource conflicts should be resolved",
                ],
                confidence=0.8,
                priority=5,
            ),
            ReasoningRule(
                rule_id="risk-assessment",
                name="Risk Assessment",
                description="Assess risks based on complexity and dependencies",
                conditions=[
                    "task has high complexity",
                    "task has critical dependencies",
                ],
                conclusions=[
                    "high complexity tasks need more validation",
                    "critical dependencies need fallback plans",
                ],
                confidence=0.75,
                priority=6,
            ),
            ReasoningRule(
                rule_id="quality-gate",
                name="Quality Gate",
                description="Ensure quality before proceeding to next step",
                conditions=[
                    "previous step is completed",
                    "quality criteria are defined",
                ],
                conclusions=[
                    "quality must be verified before proceeding",
                    "failed quality gate blocks execution chain",
                ],
                confidence=0.9,
                priority=7,
            ),
        ]

        for rule in default_rules:
            self._rules[rule.rule_id] = rule

    # ─── Rule Management ───

    def register_rule(self, rule: ReasoningRule) -> None:
        """Register a new reasoning rule."""
        self._rules[rule.rule_id] = rule
        logger.info("Rule registered: %s (%s)", rule.rule_id, rule.name)

    def unregister_rule(self, rule_id: str) -> None:
        """Remove a reasoning rule."""
        self._rules.pop(rule_id, None)

    def get_rule(self, rule_id: str) -> ReasoningRule | None:
        """Get a rule by ID."""
        return self._rules.get(rule_id)

    def list_rules(self) -> list[dict[str, Any]]:
        """List all registered rules."""
        return [
            {
                "rule_id": r.rule_id,
                "name": r.name,
                "description": r.description,
                "conditions": r.conditions,
                "conclusions": r.conclusions,
                "confidence": r.confidence,
                "priority": r.priority,
            }
            for r in sorted(self._rules.values(), key=lambda x: x.priority)
        ]

    # ─── Knowledge Base ───

    def add_evidence(self, evidence: Evidence) -> None:
        """Add evidence to the knowledge base."""
        self._knowledge_base[evidence.id] = evidence

    def add_fact(self, description: str, value: Any = None, confidence: float = 1.0) -> Evidence:
        """Add a fact to the knowledge base (convenience method)."""
        evidence = Evidence(
            id=f"ev-{uuid.uuid4().hex[:8]}",
            type=EvidenceType.FACT,
            description=description,
            value=value,
            confidence=confidence,
            source="user",
        )
        self.add_evidence(evidence)
        return evidence

    def get_evidence(self, evidence_id: str) -> Evidence | None:
        """Get evidence by ID."""
        return self._knowledge_base.get(evidence_id)

    def query_evidence(self, description: str) -> list[Evidence]:
        """Find evidence by description (substring match)."""
        return [
            e for e in self._knowledge_base.values()
            if description.lower() in e.description.lower()
        ]

    def clear_evidence(self) -> None:
        """Clear all evidence from the knowledge base."""
        self._knowledge_base.clear()

    # ─── Reasoning Methods ───

    def forward_chaining(
        self,
        goal: str,
        initial_evidence: list[Evidence] | None = None,
    ) -> ReasoningResult:
        """Forward chaining: start from known facts, apply rules to reach conclusions.

        Args:
            goal: The goal to reason about.
            initial_evidence: Initial known facts/evidence.

        Returns:
            ReasoningResult with conclusions and decisions.
        """
        reasoning_id = f"reason-{uuid.uuid4().hex[:12]}"
        start_time = __import__("time").time()

        result = ReasoningResult(
            reasoning_id=reasoning_id,
            method=ReasoningMethod.FORWARD_CHAINING,
            status=ReasoningStatus.IN_PROGRESS,
            goal=goal,
        )

        self._emit_started(reasoning_id, ReasoningMethod.FORWARD_CHAINING, goal)

        # Initialize working memory
        working_memory: list[Evidence] = list(initial_evidence or [])
        applied_rules: set[str] = set()
        conclusions: list[Conclusion] = []
        decisions: list[Decision] = []

        # Add goal as initial evidence
        goal_evidence = Evidence(
            id=f"ev-goal-{uuid.uuid4().hex[:6]}",
            type=EvidenceType.FACT,
            description=f"Goal: {goal}",
            value=goal,
            source="input",
        )
        working_memory.append(goal_evidence)

        # Forward chaining loop
        max_iterations = 20
        iteration = 0
        changed = True

        while changed and iteration < max_iterations:
            changed = False
            iteration += 1

            for rule in sorted(self._rules.values(), key=lambda x: x.priority):
                if rule.rule_id in applied_rules:
                    continue

                # Check if conditions are satisfied
                conditions_satisfied = self._check_conditions(
                    rule.conditions, working_memory
                )

                if conditions_satisfied:
                    # Apply rule
                    applied_rules.add(rule.rule_id)
                    changed = True

                    # Create conclusion
                    for conclusion_stmt in rule.conclusions:
                        conclusion = Conclusion(
                            conclusion_id=f"conc-{uuid.uuid4().hex[:6]}",
                            statement=conclusion_stmt,
                            confidence=rule.confidence,
                            evidence_ids=[e.id for e in working_memory[-3:]],
                            rule_id=rule.rule_id,
                            derived=True,
                        )
                        conclusions.append(conclusion)

                        # Add conclusion as new evidence
                        derived_evidence = Evidence(
                            id=f"ev-derived-{uuid.uuid4().hex[:6]}",
                            type=EvidenceType.DERIVED,
                            description=conclusion_stmt,
                            confidence=rule.confidence,
                            source=f"rule:{rule.rule_id}",
                        )
                        working_memory.append(derived_evidence)

                    self._emit_rule_applied(reasoning_id, rule)

                    # Make decisions based on conclusions
                    if "should be decomposed" in " ".join(rule.conclusions):
                        decisions.append(Decision(
                            decision_id=f"dec-{uuid.uuid4().hex[:6]}",
                            description="Decompose complex goal",
                            options=["decompose", "keep monolithic", "partial decompose"],
                            selected="decompose",
                            confidence=rule.confidence,
                            reasoning=f"Rule '{rule.name}' applied: goal decomposition needed",
                        ))

            # Check for convergence
            if len(conclusions) > 0 and not changed:
                break

        # Build explanation
        explanation_parts = [
            f"Forward chaining reasoning for goal: '{goal}'",
            f"Applied {len(applied_rules)} rules in {iteration} iterations",
            f"Generated {len(conclusions)} conclusions",
            f"Made {len(decisions)} decisions",
            f"Working memory size: {len(working_memory)}",
        ]

        result.evidence = working_memory
        result.conclusions = conclusions
        result.decisions = decisions
        result.confidence = (
            sum(c.confidence for c in conclusions) / len(conclusions)
            if conclusions else 0.0
        )
        result.explanation = "\n".join(explanation_parts)
        result.status = ReasoningStatus.COMPLETED if conclusions else ReasoningStatus.INCONCLUSIVE
        result.execution_time_ms = (__import__("time").time() - start_time) * 1000
        result.metadata = {
            "iterations": iteration,
            "rules_applied": len(applied_rules),
            "working_memory_size": len(working_memory),
        }

        self._results[reasoning_id] = result
        self._emit_completed(result)
        return result

    def backward_chaining(
        self,
        goal: str,
        desired_outcome: str,
        context: dict[str, Any] | None = None,
    ) -> ReasoningResult:
        """Backward chaining: start from desired outcome, find prerequisites.

        Args:
            goal: The original goal.
            desired_outcome: The specific outcome we want to achieve.
            context: Optional context information.

        Returns:
            ReasoningResult with prerequisite conclusions.
        """
        reasoning_id = f"reason-{uuid.uuid4().hex[:12]}"
        start_time = __import__("time").time()

        result = ReasoningResult(
            reasoning_id=reasoning_id,
            method=ReasoningMethod.BACKWARD_CHAINING,
            status=ReasoningStatus.IN_PROGRESS,
            goal=goal,
        )

        self._emit_started(reasoning_id, ReasoningMethod.BACKWARD_CHAINING, goal)

        conclusion = Conclusion(
            conclusion_id=f"conc-{uuid.uuid4().hex[:6]}",
            statement=f"Desired outcome: {desired_outcome}",
            confidence=0.9,
            derived=False,
        )

        prerequisites = self._find_prerequisites(desired_outcome, context or {})

        for prereq in prerequisites:
            prereq_conc = Conclusion(
                conclusion_id=f"conc-prereq-{uuid.uuid4().hex[:6]}",
                statement=f"Prerequisite: {prereq}",
                confidence=0.85,
                derived=True,
                rule_id="backward-chaining",
            )
            result.conclusions.append(prereq_conc)

        result.conclusions.insert(0, conclusion)
        result.confidence = (
            sum(c.confidence for c in result.conclusions) / len(result.conclusions)
            if result.conclusions else 0.0
        )
        result.explanation = f"Backward chaining from '{desired_outcome}': found {len(prerequisites)} prerequisites"
        result.status = ReasoningStatus.COMPLETED
        result.execution_time_ms = (__import__("time").time() - start_time) * 1000

        self._results[reasoning_id] = result
        self._emit_completed(result)
        return result

    def decision_tree(
        self,
        question: str,
        options: list[dict[str, Any]],
        criteria: list[str] | None = None,
    ) -> ReasoningResult:
        """Decision tree reasoning: evaluate options against criteria.

        Args:
            question: The decision question.
            options: List of options, each with attributes.
            criteria: Criteria to evaluate (auto-detected if None).

        Returns:
            ReasoningResult with the best option as a decision.
        """
        reasoning_id = f"reason-{uuid.uuid4().hex[:12]}"
        start_time = __import__("time").time()

        result = ReasoningResult(
            reasoning_id=reasoning_id,
            method=ReasoningMethod.DECISION_TREE,
            status=ReasoningStatus.IN_PROGRESS,
            goal=question,
        )

        self._emit_started(reasoning_id, ReasoningMethod.DECISION_TREE, question)

        # Auto-detect criteria from options
        if criteria is None and options:
            all_keys = set()
            for opt in options:
                all_keys.update(opt.get("attributes", opt).keys())
            criteria = list(all_keys)[:5]

        # Score each option
        scored_options = []
        for option in options:
            score = 0.0
            attr = option.get("attributes", option)
            num_criteria = len(criteria) if criteria else 1

            for criterion in (criteria or []):
                value = attr.get(criterion, 0)
                if isinstance(value, (int, float)):
                    score += float(value)

            avg_score = score / num_criteria if num_criteria > 0 else 0
            scored_options.append((avg_score, option))

        # Sort by score (descending)
        scored_options.sort(key=lambda x: x[0], reverse=True)

        decision = Decision(
            decision_id=f"dec-{uuid.uuid4().hex[:6]}",
            description=f"Decision: {question}",
            options=[str(o.get("name", o.get("id", f"option_{i}"))) for i, (_, o) in enumerate(scored_options)],
            selected=str(scored_options[0][1].get("name", scored_options[0][1].get("id", "best_option"))) if scored_options else None,
            confidence=min(1.0, (scored_options[0][0] / 10.0)) if scored_options else 0.0,
            reasoning=f"Decision tree evaluated {len(options)} options against {len(criteria or [])} criteria. Best option score: {scored_options[0][0] if scored_options else 0:.2f}",
            urgency=DecisionUrgency.MEDIUM,
        )

        result.decisions = [decision]
        result.confidence = decision.confidence
        result.explanation = decision.reasoning
        result.status = ReasoningStatus.COMPLETED if decision.selected else ReasoningStatus.INCONCLUSIVE
        result.execution_time_ms = (__import__("time").time() - start_time) * 1000

        self._results[reasoning_id] = result
        self._emit_completed(result)
        return result

    def constraint_propagation(
        self,
        constraints: list[dict[str, Any]],
        variables: dict[str, Any],
    ) -> ReasoningResult:
        """Constraint propagation: ensure variable assignments satisfy constraints.

        Args:
            constraints: List of constraint definitions.
            variables: Current variable assignments.

        Returns:
            ReasoningResult with constraint satisfaction analysis.
        """
        reasoning_id = f"reason-{uuid.uuid4().hex[:12]}"
        start_time = __import__("time").time()

        result = ReasoningResult(
            reasoning_id=reasoning_id,
            method=ReasoningMethod.CONSTRAINT_PROPAGATION,
            status=ReasoningStatus.IN_PROGRESS,
            goal="Constraint satisfaction",
        )

        self._emit_started(reasoning_id, ReasoningMethod.CONSTRAINT_PROPAGATION, "Constraint satisfaction")

        satisfied = 0
        violated = 0
        violated_constraints: list[str] = []

        for constraint in constraints:
            constraint_expr = constraint.get("expression", "")
            constraint_name = constraint.get("name", constraint_expr)

            # Simple constraint checking
            is_satisfied = self._check_constraint(constraint, variables)

            if is_satisfied:
                satisfied += 1
            else:
                violated += 1
                violated_constraints.append(constraint_name)

        decision = Decision(
            decision_id=f"dec-{uuid.uuid4().hex[:6]}",
            description="Constraint satisfaction check",
            options=["proceed", "block", "renegotiate"],
            selected="block" if violated > 0 else "proceed",
            confidence=1.0 - (violated / max(len(constraints), 1)),
            reasoning=f"Constraints: {satisfied} satisfied, {violated} violated. Violated: {violated_constraints}",
            urgency=DecisionUrgency.HIGH if violated > 0 else DecisionUrgency.LOW,
        )

        result.decisions = [decision]
        conclusion = Conclusion(
            conclusion_id=f"conc-{uuid.uuid4().hex[:6]}",
            statement=f"Constraint check: {satisfied}/{len(constraints)} satisfied",
            confidence=decision.confidence,
            derived=True,
            rule_id="constraint-validation",
        )
        result.conclusions = [conclusion]
        result.confidence = decision.confidence
        result.explanation = decision.reasoning
        result.status = ReasoningStatus.COMPLETED
        result.execution_time_ms = (__import__("time").time() - start_time) * 1000

        self._results[reasoning_id] = result
        self._emit_completed(result)
        return result

    def causal_reasoning(
        self,
        event_description: str,
        context: dict[str, Any] | None = None,
    ) -> ReasoningResult:
        """Causal reasoning: analyze cause-effect relationships.

        Args:
            event_description: The event to analyze.
            context: Optional context.

        Returns:
            ReasoningResult with causal analysis.
        """
        reasoning_id = f"reason-{uuid.uuid4().hex[:12]}"
        start_time = __import__("time").time()

        result = ReasoningResult(
            reasoning_id=reasoning_id,
            method=ReasoningMethod.CAUSAL_REASONING,
            status=ReasoningStatus.IN_PROGRESS,
            goal=f"Analyze causes of: {event_description}",
        )

        self._emit_started(reasoning_id, ReasoningMethod.CAUSAL_REASONING, event_description)

        # Find potential causes from knowledge base
        causes = self.query_evidence(event_description)

        cause_conclusions = []
        if causes:
            for cause in causes:
                conc = Conclusion(
                    conclusion_id=f"conc-cause-{uuid.uuid4().hex[:6]}",
                    statement=f"Potential cause: {cause.description}",
                    confidence=cause.confidence * 0.8,
                    evidence_ids=[cause.id],
                    derived=True,
                    rule_id="causal-reasoning",
                )
                cause_conclusions.append(conc)

        # Generate effects
        effects = [
            "Execution may be blocked or delayed",
            "Dependent steps need re-planning",
            "Resources may need reallocation",
        ]
        for effect in effects:
            conc = Conclusion(
                conclusion_id=f"conc-effect-{uuid.uuid4().hex[:6]}",
                statement=f"Effect: {effect}",
                confidence=0.7,
                derived=True,
                rule_id="causal-reasoning",
            )
            cause_conclusions.append(conc)

        result.conclusions = cause_conclusions
        result.confidence = (
            sum(c.confidence for c in cause_conclusions) / len(cause_conclusions)
            if cause_conclusions else 0.0
        )
        result.explanation = (
            f"Causal analysis of '{event_description}': "
            f"found {len(causes)} potential causes, "
            f"identified {len(effects)} potential effects"
        )
        result.status = ReasoningStatus.COMPLETED if cause_conclusions else ReasoningStatus.INCONCLUSIVE
        result.execution_time_ms = (__import__("time").time() - start_time) * 1000

        self._results[reasoning_id] = result
        self._emit_completed(result)
        return result

    # ─── Main Reasoning Entry Point ───

    def reason(
        self,
        goal: str,
        method: ReasoningMethod = ReasoningMethod.FORWARD_CHAINING,
        context: dict[str, Any] | None = None,
    ) -> ReasoningResult:
        """Main entry point: reason about a goal using the specified method.

        Args:
            goal: The goal or question to reason about.
            method: The reasoning method to use.
            context: Optional context (evidence, constraints, etc.).

        Returns:
            ReasoningResult with conclusions and decisions.
        """
        context = context or {}
        initial_evidence = context.get("evidence")
        desired_outcome = context.get("desired_outcome", "")
        options = context.get("options", [])
        criteria = context.get("criteria")
        constraints = context.get("constraints", [])
        variables = context.get("variables", {})

        if method == ReasoningMethod.FORWARD_CHAINING:
            return self.forward_chaining(goal, initial_evidence)
        elif method == ReasoningMethod.BACKWARD_CHAINING:
            if not desired_outcome:
                desired_outcome = goal
            return self.backward_chaining(goal, desired_outcome, context)
        elif method == ReasoningMethod.DECISION_TREE:
            return self.decision_tree(goal, options, criteria)
        elif method == ReasoningMethod.CONSTRAINT_PROPAGATION:
            return self.constraint_propagation(constraints, variables)
        elif method == ReasoningMethod.CAUSAL_REASONING:
            return self.causal_reasoning(goal, context)
        else:
            return self.forward_chaining(goal, initial_evidence)

    # ─── Result Management ───

    def get_result(self, reasoning_id: str) -> ReasoningResult | None:
        """Get a reasoning result by ID."""
        return self._results.get(reasoning_id)

    def list_results(self) -> list[dict[str, Any]]:
        """List all reasoning results."""
        return [
            {
                "reasoning_id": r.reasoning_id,
                "method": r.method.value,
                "status": r.status.value,
                "goal": r.goal[:80],
                "conclusions": len(r.conclusions),
                "decisions": len(r.decisions),
                "confidence": round(r.confidence, 2),
                "time_ms": round(r.execution_time_ms, 2),
            }
            for r in self._results.values()
        ]

    def clear_results(self) -> None:
        """Clear all reasoning results."""
        self._results.clear()

    # ─── Internal Helpers ───

    def _check_conditions(
        self,
        conditions: list[str],
        working_memory: list[Evidence],
    ) -> bool:
        """Check if conditions are satisfied by the working memory."""
        memory_descriptions = [e.description.lower() for e in working_memory]

        for condition in conditions:
            condition_lower = condition.lower()
            if not any(condition_lower in desc for desc in memory_descriptions):
                return False

        return True

    def _find_prerequisites(
        self,
        desired_outcome: str,
        context: dict[str, Any],
    ) -> list[str]:
        """Find prerequisites for a desired outcome."""
        prerequisites = []

        # Check capability graph for dependencies
        domain = context.get("domain", "")
        if domain:
            cap_ids = capability_graph.get_all_capabilities()
            for cap_id in cap_ids:
                deps = capability_graph.get_dependencies(cap_id)
                if deps:
                    prerequisites.extend(deps)

        # Add generic prerequisites
        generic_prereqs = [
            "Define clear requirements",
            "Identify required resources",
            "Set up development environment",
            "Establish quality criteria",
        ]

        result = list(set(prerequisites + generic_prereqs))
        return result[:5]

    def _check_constraint(
        self,
        constraint: dict[str, Any],
        variables: dict[str, Any],
    ) -> bool:
        """Check if a single constraint is satisfied."""
        var_name = constraint.get("variable", "")
        operator = constraint.get("operator", "exists")
        expected_value = constraint.get("value")

        actual_value = variables.get(var_name)

        if operator == "exists":
            return actual_value is not None
        elif operator == "equals":
            return actual_value == expected_value
        elif operator == "gt":
            return isinstance(actual_value, (int, float)) and isinstance(expected_value, (int, float)) and actual_value > expected_value
        elif operator == "gte":
            return isinstance(actual_value, (int, float)) and isinstance(expected_value, (int, float)) and actual_value >= expected_value
        elif operator == "lt":
            return isinstance(actual_value, (int, float)) and isinstance(expected_value, (int, float)) and actual_value < expected_value
        elif operator == "lte":
            return isinstance(actual_value, (int, float)) and isinstance(expected_value, (int, float)) and actual_value <= expected_value
        elif operator == "in":
            return isinstance(expected_value, list) and actual_value in expected_value
        elif operator == "not_in":
            return isinstance(expected_value, list) and actual_value not in expected_value
        elif operator == "contains":
            return isinstance(actual_value, str) and isinstance(expected_value, str) and expected_value in actual_value
        else:
            return True  # Unknown operators pass by default

    # ─── Telemetry ───

    def _emit_started(self, reasoning_id: str, method: ReasoningMethod, goal: str) -> None:
        event = Event(
            event_type=REASONING_STARTED,
            source="reasoning_engine",
            data={
                "reasoning_id": reasoning_id,
                "method": method.value,
                "goal": goal[:100],
            },
        )
        event_bus.publish(event)

    def _emit_rule_applied(self, reasoning_id: str, rule: ReasoningRule) -> None:
        event = Event(
            event_type=REASONING_RULE_APPLIED,
            source="reasoning_engine",
            data={
                "reasoning_id": reasoning_id,
                "rule_id": rule.rule_id,
                "rule_name": rule.name,
            },
        )
        event_bus.publish(event)

    def _emit_completed(self, result: ReasoningResult) -> None:
        event = Event(
            event_type=REASONING_COMPLETED if result.status == ReasoningStatus.COMPLETED else REASONING_FAILED,
            source="reasoning_engine",
            data={
                "reasoning_id": result.reasoning_id,
                "method": result.method.value,
                "status": result.status.value,
                "conclusions": len(result.conclusions),
                "decisions": len(result.decisions),
                "confidence": round(result.confidence, 2),
                "time_ms": round(result.execution_time_ms, 2),
            },
        )
        event_bus.publish(event)


# ─── Singleton ───

reasoning_engine = ReasoningEngine()

