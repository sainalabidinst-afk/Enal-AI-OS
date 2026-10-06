"""
Digital Twin Engine — Public Contracts (Pydantic schemas).

Defines the input and output contracts for the Digital Twin Engine,
including TwinState, TwinStatus, SimulationRequest, SimulationResult,
CausalTrace, and RedTeamAuditResult.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class TwinState(BaseModel):
    """Mirror of the real-world system state in the digital twin."""

    twin_id: str = Field(..., description="Unique identifier for this digital twin")
    system_state: dict[str, Any] = Field(..., description="Mirrored system state")
    last_sync: str = Field(..., description="ISO timestamp of last synchronization")
    mirror_health: str = Field(
        default="healthy",
        description="Health of the mirror: healthy, degraded, failed",
    )


class TwinStatus(BaseModel):
    """Current health and workload status of the digital twin."""

    twin_id: str = Field(..., description="Unique identifier for this digital twin")
    mirror_health: str = Field(
        default="healthy",
        description="Health of the mirror: healthy, degraded, failed",
    )
    last_sync: str = Field(..., description="ISO timestamp of last synchronization")
    active_simulations: int = Field(default=0, description="Number of running simulations")
    pending_adversarial_tests: int = Field(
        default=0, description="Number of pending adversarial tests"
    )
    audit_history_count: int = Field(default=0, description="Total adversarial audits performed")
    system_state_keys: list[str] = Field(
        default_factory=list, description="Top-level keys in the mirrored state"
    )


class SimulationRequest(BaseModel):
    """Request to run a scenario simulation on the digital twin."""

    simulation_id: str = Field(
        default_factory=lambda: str(__import__("uuid").uuid4()),
        description="Unique request identifier",
    )
    scenario: str = Field(..., description="Natural language scenario description")
    parameters: dict[str, Any] = Field(default_factory=dict, description="Simulation parameters")
    iterations: int = Field(default=100, ge=1, le=10000, description="Monte Carlo iterations")
    time_warp_factor: float = Field(
        default=1.0, ge=0.1, le=100.0, description="Time acceleration factor"
    )
    status: str = Field(default="pending", description="pending | running | completed | failed")


class SimulationResult(BaseModel):
    """Result of a scenario simulation."""

    simulation_id: str = Field(..., description="Unique simulation identifier")
    scenario: str = Field(..., description="Scenario description")
    parameters: dict[str, Any] = Field(default_factory=dict, description="Parameters used")
    iterations: int = Field(default=100, description="Iterations executed")
    success: bool = Field(default=False, description="Whether simulation succeeded")
    outcomes: list[dict[str, Any]] = Field(default_factory=list, description="Simulation outcomes")
    statistics: dict[str, Any] = Field(default_factory=dict, description="Computed statistics")
    recommended_action: str = Field(
        default="proceed", description="Recommended action from simulation"
    )
    confidence: float = Field(default=0.0, ge=0.0, le=1.0, description="Confidence in result")
    raw: dict[str, Any] = Field(default_factory=dict, description="Raw engine output")


class CausalTrace(BaseModel):
    """Result of a causal trace analysis."""

    trace_id: str = Field(..., description="Unique trace identifier")
    treatment: str = Field(..., description="Treatment variable (cause)")
    outcome: str = Field(..., description="Outcome variable (effect)")
    conditions: dict[str, Any] = Field(default_factory=dict, description="Controlling conditions")
    causal_effect: float = Field(default=0.0, description="Estimated causal effect magnitude")
    confidence: float = Field(
        default=0.0, ge=0.0, le=1.0, description="Confidence in causal estimate"
    )
    counterfactual: str = Field(default="", description="Counterfactual explanation or result")
    raw: dict[str, Any] = Field(default_factory=dict, description="Raw engine output")


class RedTeamAuditResult(BaseModel):
    """Result of a red team adversarial audit."""

    audit_id: str = Field(..., description="Unique audit identifier")
    subject: str = Field(..., description="The audited subject")
    subject_type: str = Field(
        default="plan", description="Type of subject: plan, recommendation, architecture"
    )
    vulnerabilities_found: int = Field(default=0, description="Number of vulnerabilities found")
    risk_score: float = Field(default=0.0, description="Aggregate risk score")
    hardening_recommendations: list[str] = Field(
        default_factory=list, description="Recommended hardening actions"
    )
    gate_result: str = Field(default="conditional", description="pass | fail | conditional")
    explanation: str = Field(default="", description="Full explanation chain")
    raw: dict[str, Any] = Field(default_factory=dict, description="Raw engine output")
