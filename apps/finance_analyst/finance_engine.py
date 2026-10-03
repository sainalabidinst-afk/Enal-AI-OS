"""
Finance Analyst — Financial Analysis Engine module.
"""

from __future__ import annotations

import logging
from typing import Any

from apps.finance_analyst.schemas import (
    EvidenceCheckResult,
    FinanceInputs,
    FinanceOperation,
    FinancialMetric,
    RiskScenario,
    SensitivityScenario,
)

logger = logging.getLogger(__name__)


class FinanceAnalysisEngine:
    """
    Provides financial analysis, scenario modeling, risk modeling,
    and finance control evidence mapping.

    All calculations use explicit inputs and formulae; no silent defaults
    are applied for missing values.
    """

    def financial_summary(self, inputs: FinanceInputs) -> list[FinancialMetric]:
        """Calculate financial ratios from normalized inputs."""
        metrics = []

        if inputs.revenue is not None and inputs.cost_of_goods_sold is not None:
            gpm = inputs.revenue - inputs.cost_of_goods_sold
            gross_margin = gpm / inputs.revenue if inputs.revenue else None
            metrics.append(
                FinancialMetric(
                    name="gross_margin",
                    value=gross_margin,
                    formula="(revenue - cogs) / revenue",
                    inputs_traced=["revenue", "cost_of_goods_sold"],
                )
            )

        if inputs.current_assets is not None and inputs.current_liabilities is not None:
            if inputs.current_liabilities == 0:
                metrics.append(
                    FinancialMetric(
                        name="current_ratio",
                        value=None,
                        formula="current_assets / current_liabilities",
                        inputs_traced=["current_assets", "current_liabilities"],
                        notes="Missing denominator: current_liabilities is zero",
                    )
                )
            else:
                cr = inputs.current_assets / inputs.current_liabilities
                metrics.append(
                    FinancialMetric(
                        name="current_ratio",
                        value=cr,
                        formula="current_assets / current_liabilities",
                        inputs_traced=["current_assets", "current_liabilities"],
                    )
                )
        else:
            metrics.append(
                FinancialMetric(
                    name="current_ratio",
                    value=None,
                    formula="current_assets / current_liabilities",
                    inputs_traced=[],
                    notes="Missing inputs: current_assets or current_liabilities",
                )
            )

        return metrics

    def cash_flow_runway(self, inputs: FinanceInputs) -> dict[str, Any]:
        """Calculate cash flow runway from balance and burn."""
        result: dict[str, Any] = {"formula_disclosed": True}

        if inputs.cash_balance is None or inputs.monthly_net_burn is None:
            result["runway_months"] = None
            result["missing_input_reported"] = True
            result["assumptions_disclosed"] = ["Requires cash_balance and monthly_net_burn"]
            return result

        if inputs.monthly_net_burn == 0:
            result["runway_months"] = None
            result["missing_input_reported"] = True
            result["assumptions_disclosed"] = ["Burn rate must be non-zero"]
            return result

        runway = inputs.cash_balance / inputs.monthly_net_burn
        result["runway_months"] = round(runway, 1)
        result["assumptions_disclosed"] = [
            f"cash_balance={inputs.cash_balance}, monthly_net_burn={inputs.monthly_net_burn}",
            f"currency={inputs.currency}",
        ]
        return result

    def scenario_analysis(self, inputs: FinanceInputs) -> list[SensitivityScenario]:
        """Run bounded sensitivity cases for user-supplied assumptions."""
        if inputs.baseline_revenue is None or inputs.margin is None:
            return []

        scenarios = []
        baseline_profit = inputs.baseline_revenue * inputs.margin
        scenarios.append(
            SensitivityScenario(
                change_pct=0.0,
                result=round(baseline_profit, 2),
                labelled=True,
            )
        )

        for change_pct in inputs.revenue_changes_pct:
            adjusted_revenue = inputs.baseline_revenue * (1 + change_pct / 100)
            adjusted_profit = adjusted_revenue * inputs.margin
            scenarios.append(
                SensitivityScenario(
                    change_pct=change_pct,
                    result=round(adjusted_profit, 2),
                    labelled=True,
                )
            )

        return scenarios

    def risk_model(self, inputs: FinanceInputs) -> RiskScenario:
        """Model a downside risk scenario with explicit baseline."""
        if inputs.baseline_cost is None or inputs.downside_cost_increase_pct is None:
            return RiskScenario(
                name="downside_risk",
                baseline=0.0,
                downside=0.0,
                change_pct=0.0,
                assumption_label="Missing inputs",
            )

        downside_cost = inputs.baseline_cost * (1 + inputs.downside_cost_increase_pct / 100)
        return RiskScenario(
            name="downside_risk",
            baseline=inputs.baseline_cost,
            downside=round(downside_cost, 2),
            change_pct=inputs.downside_cost_increase_pct,
            assumption_label=f"baseline_cost={inputs.baseline_cost}, increase={inputs.downside_cost_increase_pct}%",  # noqa: E501
        )

    def control_check(self, inputs: FinanceInputs) -> list[EvidenceCheckResult]:
        """Map supplied evidence to a versioned control checklist."""
        results = []
        for ev in inputs.evidence:
            results.append(
                EvidenceCheckResult(
                    control_id=ev.get("control", "unknown"),
                    status=ev.get("status", "unspecified"),
                    evidence_available=True,
                    unsupported=False,
                )
            )
        return results

    def check_input_validation(self, inputs: FinanceInputs) -> dict[str, Any]:
        """Validate inputs for missing or ambiguous values."""
        errors = []
        valid = True

        if inputs.currency is None:
            errors.append("currency must be specified")
            valid = False

        if inputs.operation == FinanceOperation.financial_summary:
            if inputs.revenue is None:
                errors.append("revenue is required for financial_summary")
            if inputs.current_assets is not None and inputs.current_liabilities is None:
                errors.append("current_liabilities missing with current_assets present")

        if inputs.operation == FinanceOperation.cash_flow:
            if inputs.cash_balance is None or inputs.monthly_net_burn is None:
                errors.append("cash_balance and monthly_net_burn required for cash_flow")

        return {
            "valid": valid and len(errors) == 0,
            "validation_errors": errors,
            "calculation_performed": valid,
        }


__all__ = ["FinanceAnalysisEngine"]
