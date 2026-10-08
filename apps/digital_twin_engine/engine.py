"""
Digital Twin Engine — simulation brain for Decision Intelligence.

Provides DigitalTwinEngine for state mirroring, scenario simulation,
adversarial red-team audits, and causal inference by composing
ScenarioSimulatorEngine, AdversarialTestingEngine, and CrossDomainGraphEngine.

Pipeline:
    Decision Request
        ↓
    State Mirror (TwinState)
        ↓
    Scenario Simulator (what-if)
        ↓
    Red Team Agent (adversarial)
        ↓
    Causal Reasoner (causal trace)
        ↓
    TwinStatus + Audit
"""

from __future__ import annotations

import logging
import time
import uuid
from typing import Any

from apps.adversarial_testing.engine import AdversarialTestingEngine
from apps.cross_domain_graph.engine import CrossDomainGraphEngine
from apps.digital_twin_engine.schemas import (
    CausalTrace,
    RedTeamAuditResult,
    TwinState,
    TwinStatus,
)
from apps.digital_twin_engine.schemas import (
    SimulationResult as DT_SimulationResult,
)
from apps.scenario_simulator.engine import ScenarioSimulatorEngine
from apps.scenario_simulator.schemas import ScenarioRequest, SimulationResult

logger = logging.getLogger(__name__)


class DigitalTwinEngine:
    """
    Orchestrates scenario simulation, adversarial testing, and causal inference.

    Composes existing engines (per ADR-004) and exposes a unified digital twin
    API for Decision Intelligence.

    Public API::

        engine = DigitalTwinEngine()
        twin = engine.mirror_state(system_state)
        result = engine.run_simulation("What if X increases 10%?", params, iterations=100)
        audit = engine.run_red_team("plan-A", subject_type="plan")
        trace = engine.run_causal_trace("treatment-X", "outcome-Y", conditions={...})
        status = engine.get_status()
    """

    def __init__(self) -> None:
        self.scenario_engine = ScenarioSimulatorEngine()
        self.adversarial_engine = AdversarialTestingEngine()
        self.cross_domain_engine = CrossDomainGraphEngine()
        self._twin_id = str(uuid.uuid4())
        self._state: dict[str, Any] = {}
        self._last_sync: str = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        self._active_simulations: int = 0
        self._pending_adversarial_tests: int = 0
        self._audit_history: list[dict[str, Any]] = []

    # ------------------------------------------------------------------
    # State Mirroring
    # ------------------------------------------------------------------

    def mirror_state(self, system_state: dict[str, Any]) -> TwinState:
        """
        Create or update the digital twin state mirror.

        Args:
            system_state: Current real-world system state to mirror.

        Returns:
            TwinState representing the mirrored state.
        """
        self._state = dict(system_state)
        self._last_sync = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        return TwinState(
            twin_id=self._twin_id,
            system_state=system_state,
            last_sync=self._last_sync,
            mirror_health="healthy",
        )

    # ------------------------------------------------------------------
    # Scenario Simulation
    # ------------------------------------------------------------------

    def run_simulation(
        self, scenario: str, parameters: dict[str, Any], iterations: int = 100
    ) -> DT_SimulationResult:
        """
        Orchestrate a scenario simulation via ScenarioSimulatorEngine.

        Args:
            scenario: Natural language scenario description.
            parameters: Scenario parameters (base_state, variable_changes, etc.).
            iterations: Number of Monte Carlo iterations.

        Returns:
            SimulationResult with outcomes, risk scores, and recommended actions.
        """
        self._active_simulations += 1
        try:
            base_state = parameters.get("base_state", self._state)
            variable_changes = parameters.get("variable_changes", [])
            seed = parameters.get("seed")
            sandbox_enabled = parameters.get("sandbox_enabled", False)
            sandbox_code = parameters.get("sandbox_code")

            request = ScenarioRequest(
                title=parameters.get("title", f"DT Simulation: {scenario[:50]}"),
                description=scenario,
                base_state=base_state or {},
                variable_changes=variable_changes,
                iterations=iterations,
                seed=seed,
                sandbox_enabled=sandbox_enabled,
                sandbox_code=sandbox_code,
                context=parameters.get("context", {}),
            )

            result: SimulationResult = self.scenario_engine.run_simulation(request)
            stats = result.to_dict().get("distribution", {})
            return DT_SimulationResult(
                simulation_id=str(uuid.uuid4()),
                scenario=scenario,
                parameters=parameters,
                iterations=iterations,
                success=result.iterations_run > 0,
                outcomes=result.outcomes,
                statistics=stats,
                recommended_action=stats.get("recommended_action", "proceed"),
                confidence=stats.get("confidence", 0.0),
                raw=result.to_dict(),
            )
        finally:
            self._active_simulations = max(0, self._active_simulations - 1)

    # ------------------------------------------------------------------
    # Red Team Adversarial Testing
    # ------------------------------------------------------------------

    def run_red_team(self, subject: str, subject_type: str = "plan") -> RedTeamAuditResult:
        """
        Orchestrate adversarial testing via AdversarialTestingEngine.

        Args:
            subject: The plan/strategy/recommendation to attack.
            subject_type: Type of subject (plan, recommendation, architecture, etc.).

        Returns:
            RedTeamAuditResult with vulnerabilities, gate result, and recommendations.
        """
        self._pending_adversarial_tests += 1
        try:
            result = self.adversarial_engine.test(
                subject=subject,
                subject_type=subject_type,
            )
            audit_id = str(uuid.uuid4())
            audit_entry = {
                "audit_id": audit_id,
                "subject": subject,
                "subject_type": subject_type,
                "gate_result": result.gate_result.value,
                "pass_score": result.pass_score,
                "vulnerabilities_found": len(result.vulnerabilities_found),
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            }
            self._audit_history.append(audit_entry)
            return RedTeamAuditResult(
                audit_id=audit_id,
                subject=subject,
                subject_type=subject_type,
                vulnerabilities_found=len(result.vulnerabilities_found),
                risk_score=result.pass_score,
                hardening_recommendations=[
                    rec.get("recommendation", "") for rec in result.hardening_recommendations
                ],
                gate_result=result.gate_result.value,
                explanation=result.explanation_chain.get("summary", ""),
                raw=result.to_dict(),
            )
        finally:
            self._pending_adversarial_tests = max(0, self._pending_adversarial_tests - 1)

    # ------------------------------------------------------------------
    # Causal Inference
    # ------------------------------------------------------------------

    def run_causal_trace(
        self, treatment: str, outcome: str, conditions: dict[str, Any] | None = None
    ) -> CausalTrace:
        """
        Orchestrate causal inference via CrossDomainGraphEngine.

        Args:
            treatment: The treatment variable (cause).
            outcome: The outcome variable (effect).
            conditions: Optional controlling conditions.

        Returns:
            CausalTrace with causal effect estimate, confidence, and counterfactual.
        """
        conditions = conditions or {}
        query = (
            f"What is the causal effect of {treatment} on {outcome} given conditions {conditions}?"
        )

        try:
            inference = self.cross_domain_engine.query(query)
            causal_effect = inference.confidence if hasattr(inference, "confidence") else 0.0
            counterfactual = inference.answer if hasattr(inference, "answer") else str(inference)
            return CausalTrace(
                trace_id=str(uuid.uuid4()),
                treatment=treatment,
                outcome=outcome,
                conditions=conditions,
                causal_effect=causal_effect,
                confidence=causal_effect,
                counterfactual=counterfactual,
                raw=inference.to_dict() if hasattr(inference, "to_dict") else {},
            )
        except Exception as exc:
            logger.warning("Causal trace query failed: %s", exc)
            return CausalTrace(
                trace_id=str(uuid.uuid4()),
                treatment=treatment,
                outcome=outcome,
                conditions=conditions,
                causal_effect=0.0,
                confidence=0.0,
                counterfactual=f"Query failed: {exc}",
                raw={},
            )

    # ------------------------------------------------------------------
    # Status & Telemetry
    # ------------------------------------------------------------------

    def get_status(self) -> TwinStatus:
        """
        Return the current digital twin health and active workload.

        Returns:
            TwinStatus with mirror_health, active_simulations, pending_adversarial_tests, etc.
        """
        mirror_health = "healthy"
        if self._active_simulations > 10 or self._pending_adversarial_tests > 5:
            mirror_health = "degraded"
        return TwinStatus(
            twin_id=self._twin_id,
            mirror_health=mirror_health,
            last_sync=self._last_sync,
            active_simulations=self._active_simulations,
            pending_adversarial_tests=self._pending_adversarial_tests,
            audit_history_count=len(self._audit_history),
            system_state_keys=list(self._state.keys()),
        )
