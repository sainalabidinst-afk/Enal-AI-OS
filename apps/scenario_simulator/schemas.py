"""
Scenario Simulator — Public Contracts (Pydantic schemas).

Defines the input (ScenarioRequest) and output (SimulationResult) contracts
for the Scenario Simulator Capability Pack, plus all supporting types.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field, field_validator


class VariableType(str, Enum):
    """Types of variables that can participate in a simulation scenario."""

    FLOAT = "float"
    INT = "int"
    BOOLEAN = "boolean"
    ENUM = "enum"
    STRING = "string"


class ChangeType(str, Enum):
    """How a variable changes in a scenario."""

    ABSOLUTE_DELTA = "absolute_delta"
    PERCENT_DELTA = "percent_delta"
    SET_VALUE = "set_value"


class DistributionType(str, Enum):
    """Probability distributions for Monte Carlo iterations."""

    FIXED = "fixed"
    UNIFORM = "uniform"
    NORMAL = "normal"
    TRIANGULAR = "triangular"
    BETA = "beta"


class OutcomeType(str, Enum):
    """Outcome scenarios from simulation."""

    BEST_CASE = "best_case"
    WORST_CASE = "worst_case"
    MOST_LIKELY = "most_likely"


# ---------------------------------------------------------------------------
# Input models
# ---------------------------------------------------------------------------


class BaseVariable(BaseModel):
    """A base variable in the current state."""

    name: str = Field(..., description="Variable name, e.g. 'interest_rate'")
    value: float | int | bool | str | None = Field(default=None, description="Current value")
    type: VariableType = Field(default=VariableType.FLOAT, description="Variable type")
    unit: str | None = Field(default=None, description="Unit of measurement")


class VariableChange(BaseModel):
    """A change applied to a variable during simulation."""

    variable: str = Field(..., description="Name of the variable to change")
    change_type: ChangeType = Field(..., description="How the variable changes")
    value: float = Field(..., description="Magnitude of change")
    distribution: DistributionType = Field(default=DistributionType.FIXED, description="Distribution for Monte Carlo")
    range_min: float | None = Field(default=None, description="Minimum value for distribution range")
    range_max: float | None = Field(default=None, description="Maximum value for distribution range")
    stddev: float | None = Field(default=None, description="Standard deviation for normal distribution")
    mode: float | None = Field(default=None, description="Mode for triangular distribution")


class ScenarioRequest(BaseModel):
    """Input contract for a scenario simulation request."""

    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique request identifier")
    title: str = Field(..., description="Scenario name/title")
    description: str = Field(..., description="What-if description in natural language")
    base_state: dict[str, Any] = Field(default_factory=dict, description="Base state variables")
    variable_changes: list[VariableChange] = Field(default_factory=list, description="Variables to change")
    iterations: int = Field(default=100, ge=1, le=10000, description="Number of Monte Carlo iterations")
    sandbox_enabled: bool = Field(default=True, description="Whether to run sandbox experiments")
    sandbox_code: str | None = Field(default=None, description="Optional code/logic to execute in sandbox")
    context: dict[str, Any] = Field(default_factory=dict, description="Additional context from capability packs")
    seed: int | None = Field(default=None, description="Random seed for reproducibility")


# ---------------------------------------------------------------------------
# Output models
# ---------------------------------------------------------------------------


@dataclass
class HistogramBucket:
    """A single histogram bucket."""

    bucket_label: str
    count: int
    range_start: float | None = None
    range_end: float | None = None


@dataclass
class OutcomeResult:
    """A single outcome scenario (best/worst/most-likely)."""

    outcome_type: OutcomeType
    value: float
    variables: dict[str, Any]
    explanation: str
    iteration_index: int | None = None


@dataclass
class DistributionStats:
    """Statistical summary of simulation outcomes."""

    mean: float = 0.0
    median: float = 0.0
    std_dev: float = 0.0
    min_value: float = 0.0
    max_value: float = 0.0
    p5: float = 0.0
    p25: float = 0.0
    p75: float = 0.0
    p95: float = 0.0
    histogram: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class SimulationResult:
    """Output contract for a simulation result."""

    request_id: str
    title: str
    description: str
    iterations_run: int
    outcomes: dict[str, Any] = field(default_factory=dict)
    distribution: DistributionStats = field(default_factory=DistributionStats)
    assumptions: list[str] = field(default_factory=list)
    key_drivers: list[str] = field(default_factory=list)
    confidence: float = 0.0
    explanation_chain: dict[str, Any] = field(default_factory=dict)
    sandbox_logs: list[dict[str, Any]] = field(default_factory=list)
    raw: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable dict."""
        return {
            "request_id": self.request_id,
            "title": self.title,
            "description": self.description,
            "iterations_run": self.iterations_run,
            "outcomes": self.outcomes,
            "distribution": {
                "mean": self.distribution.mean,
                "median": self.distribution.median,
                "std_dev": self.distribution.std_dev,
                "min": self.distribution.min_value,
                "max": self.distribution.max_value,
                "p5": self.distribution.p5,
                "p25": self.distribution.p25,
                "p75": self.distribution.p75,
                "p95": self.distribution.p95,
                "histogram": self.distribution.histogram,
            },
            "assumptions": self.assumptions,
            "key_drivers": self.key_drivers,
            "confidence": self.confidence,
            "explanation_chain": self.explanation_chain,
            "sandbox_logs": self.sandbox_logs,
            "raw": self.raw,
        }
