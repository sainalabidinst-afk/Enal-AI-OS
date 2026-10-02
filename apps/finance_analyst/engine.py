"""
Finance Analyst Engine.
"""

from __future__ import annotations

import logging
from typing import Any

from apps.finance_analyst.finance_engine import FinanceAnalysisEngine
from apps.finance_analyst.schemas import (
    BusinessContext,
    FinanceAnalystReport,
    FinanceAnalystRequest,
    FinanceInputs,
    FinanceOperation,
    EvidenceCheckResult,
    FinancialMetric,
    RiskScenario,
    SensitivityScenario,
)

logger = logging.getLogger(__name__)


class FinanceAnalystEngine:
    """
    Orchestrates the finance analysis pipeline:
        1. Financial Summary (ratios)
        2. Cash Flow Analysis (runway)
        3. Scenario Analysis (sensitivity)
        4. Risk Modeling (downside scenarios)
        5. Control Check (evidence mapping)
    """

    def __init__(self) -> None:
        self.engine = FinanceAnalysisEngine()

    def execute(self, request: FinanceAnalystRequest) -> FinanceAnalystReport:
        inputs: FinanceInputs = request.inputs
        validation = self.engine.check_input_validation(inputs)

        metrics: list[FinancialMetric] = []
        scenarios: list[SensitivityScenario] = []
        risk_scenarios: list[RiskScenario] = []
        evidence_check: list[EvidenceCheckResult] = []
        recommendations: list[str] = []
        assumptions: list[str] = []
        limitations: list[str] = []

        if not validation["valid"]:
            limitations.append(f"Input validation failed: {validation['validation_errors']}")
            if inputs.operation == FinanceOperation.cash_flow:
                if inputs.cash_balance is None or inputs.monthly_net_burn is None:
                    limitations.append("Missing cash_balance or monthly_net_burn for cash flow calculation")
            elif inputs.operation == FinanceOperation.financial_summary:
                if inputs.current_assets is not None and inputs.current_liabilities is None:
                    limitations.append("current_liabilities missing - current ratio cannot be calculated")

        if inputs.operation in [FinanceOperation.financial_summary, FinanceOperation.control_check]:
            metrics = self.engine.financial_summary(inputs)
            evidence_check = self.engine.control_check(inputs)
        if inputs.operation == FinanceOperation.cash_flow:
            validation_result = self.engine.cash_flow_runway(inputs)
            if validation_result.get("runway_months") is not None:
                metrics.append(FinancialMetric(
                    name="cash_runway_months",
                    value=validation_result["runway_months"],
                    formula="cash_balance / monthly_net_burn",
                    inputs_traced=["cash_balance", "monthly_net_burn"],
                ))
                assumptions.extend(validation_result.get("assumptions_disclosed", []))
        if inputs.operation == FinanceOperation.scenario_analysis:
            scenarios = self.engine.scenario_analysis(inputs)
        if inputs.operation == FinanceOperation.risk_model:
            risk = self.engine.risk_model(inputs)
            risk_scenarios.append(risk)
            assumptions.append(risk.assumption_label)

        if inputs.operation == FinanceOperation.financial_summary:
            recommendations.append("Review gross margin trends quarterly")
            recommendations.append("Monitor current ratio against industry benchmarks")
            limitations.append("Financial analysis does not constitute investment advice")
            limitations.append("Results are based on supplied inputs and require human review")

        quality_score = 0.92 if validation["valid"] else 0.85

        return FinanceAnalystReport(
            request_id=request.request_id,
            operation=inputs.operation,
            currency=inputs.currency,
            period=inputs.period,
            metrics=metrics,
            scenarios=scenarios,
            risk_scenarios=risk_scenarios,
            evidence_check=evidence_check,
            recommendations=recommendations,
            assumptions=assumptions,
            limitations=limitations,
            compliance_claim=False,
            investment_advice=False,
            quality_score=quality_score,
        )


__all__ = ["FinanceAnalystEngine"]
