"""
Business Analyst — ROI Calculator.

Quantifies return-on-investment for proposed features or projects.
Calculates NPV, payback period, and ROI percentage.
"""

from __future__ import annotations

import logging
from typing import Any

from apps.business_analyst.schemas import (
    StakeholderInput,
    BusinessContext,
    ROIResult,
)

logger = logging.getLogger(__name__)


class ROICalculator:
    """
    Calculates ROI for proposed investments.

    Usage::

        calc = ROICalculator()
        roi = calc.calculate(inputs, context)
    """

    def calculate(
        self,
        inputs: StakeholderInput,
        context: BusinessContext,
        discount_rate: float = 0.10,
    ) -> ROIResult:
        """
        Calculate ROI for a proposed investment.

        Args:
            inputs: StakeholderInput with requirements and notes.
            context: BusinessContext with project info.
            discount_rate: Annual discount rate for NPV (default 10%).

        Returns:
            ROIResult with NPV, payback period, and ROI percentage.
        """
        # Estimate costs from requirements.
        cost_estimate = self._estimate_cost(inputs, context)

        # Estimate benefits from requirements.
        benefit_estimate = self._estimate_benefits(inputs, context)

        # Calculate NPV over 3 years.
        npv = self._compute_npv(cost_estimate, benefit_estimate, discount_rate, years=3)

        # Calculate payback period.
        payback_months = self._compute_payback(cost_estimate, benefit_estimate)

        # Calculate ROI percentage.
        roi_pct = ((benefit_estimate - cost_estimate) / cost_estimate * 100) if cost_estimate > 0 else 0.0

        return ROIResult(
            npv=round(npv, 2),
            payback_period_months=payback_months,
            roi_percentage=round(roi_pct, 2),
            cost_estimate=round(cost_estimate, 2),
            benefit_estimate=round(benefit_estimate, 2),
            assumptions=[
                f"Discount rate: {discount_rate:.0%}",
                "Benefits estimated from requirement descriptions",
                "Costs based on industry averages per feature",
                "Analysis period: 3 years",
            ],
        )

    def _estimate_cost(self, inputs: StakeholderInput, context: BusinessContext) -> float:
        """Estimate project cost from requirements."""
        req_count = len(inputs.natural_language_requirements)
        note_count = len(inputs.stakeholder_notes)
        constraint_count = len(inputs.technical_constraints)

        # Base cost per requirement type.
        base_cost = 5000.0  # base project cost
        functional_cost = req_count * 8000.0
        non_functional_cost = constraint_count * 5000.0
        overhead = (note_count * 2000.0)

        return base_cost + functional_cost + non_functional_cost + overhead

    def _estimate_benefits(self, inputs: StakeholderInput, context: BusinessContext) -> float:
        """Estimate project benefits from requirements."""
        req_count = len(inputs.natural_language_requirements)

        # Benefit keywords and their estimated value.
        benefit_keywords = {
            "automate": 50000,
            "efficiency": 40000,
            "reduce cost": 60000,
            "increase revenue": 100000,
            "improve": 30000,
            "optimize": 35000,
            "save": 25000,
            "scale": 80000,
            "compliance": 20000,
            "security": 30000,
            "customer": 45000,
            "retention": 50000,
        }

        total_benefit = 0.0
        all_text = " ".join(inputs.natural_language_requirements + inputs.stakeholder_notes).lower()

        for keyword, value in benefit_keywords.items():
            if keyword in all_text:
                total_benefit += value

        # Base benefit for any project.
        total_benefit += req_count * 10000.0

        return total_benefit

    def _compute_npv(
        self,
        initial_cost: float,
        annual_benefit: float,
        discount_rate: float,
        years: int = 3,
    ) -> float:
        """
        Compute Net Present Value.

        Args:
            initial_cost: Upfront investment cost.
            annual_benefit: Annual benefit stream.
            discount_rate: Annual discount rate.
            years: Number of years to project.

        Returns:
            NPV in currency units.
        """
        npv = -initial_cost
        for year in range(1, years + 1):
            discounted_benefit = annual_benefit / ((1 + discount_rate) ** year)
            npv += discounted_benefit
        return npv

    def _compute_payback(self, cost: float, annual_benefit: float) -> int:
        """Compute payback period in months."""
        if annual_benefit <= 0:
            return 999  # no payback
        years = cost / annual_benefit
        return int(years * 12)
