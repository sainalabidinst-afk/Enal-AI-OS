"""
Risk Management for Trading Analyst.

Provides position sizing, stop-loss/take-profit calculation, and risk validation.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class PositionSize:
    """Position sizing recommendation."""

    units: float = 0.0
    risk_amount: float = 0.0
    risk_percent: float = 0.0
    kelly_fraction: float = 0.0
    method: str = "fixed_percent"
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class RiskValidation:
    """Pre-trade risk validation result."""

    passed: bool = False
    checks: list[dict[str, Any]] = field(default_factory=list)
    max_risk_score: float = 0.0
    recommendation: str = ""


class RiskManager:
    """Position sizing and risk management utilities."""

    def calculate_position_size(
        self,
        capital: float,
        entry_price: float,
        stop_loss: float,
        risk_percent: float = 0.02,
        win_rate: float | None = None,
        avg_win: float | None = None,
        avg_loss: float | None = None,
    ) -> PositionSize:
        """Calculate position size based on risk parameters."""
        if entry_price <= 0 or stop_loss <= 0 or capital <= 0:
            return PositionSize()
        risk_per_trade = capital * risk_percent
        stop_distance = abs(entry_price - stop_loss)
        if stop_distance == 0:
            return PositionSize()
        units = risk_per_trade / stop_distance
        kelly_fraction = 0.0
        if win_rate is not None and avg_win is not None and avg_loss is not None and avg_loss > 0:
            b = avg_win / avg_loss
            q = 1.0 - win_rate
            kelly = win_rate - (q / b)
            kelly_fraction = max(0.0, min(kelly, 0.25))
        return PositionSize(
            units=units,
            risk_amount=risk_per_trade,
            risk_percent=risk_percent,
            kelly_fraction=kelly_fraction,
            method="kelly" if win_rate else "fixed_percent",
            metadata={
                "capital": capital,
                "entry_price": entry_price,
                "stop_loss": stop_loss,
                "stop_distance": stop_distance,
            },
        )

    def calculate_stop_loss_take_profit(
        self,
        entry_price: float,
        direction: str = "long",
        atr: float | None = None,
        risk_reward_ratio: float = 2.0,
        atr_multiplier: float = 1.5,
    ) -> dict[str, float]:
        """Calculate stop-loss and take-profit levels."""
        if entry_price <= 0:
            return {"stop_loss": 0.0, "take_profit": 0.0}
        stop_distance = atr * atr_multiplier if atr else entry_price * 0.02
        if direction == "long":
            stop_loss = entry_price - stop_distance
            take_profit = entry_price + stop_distance * risk_reward_ratio
        else:
            stop_loss = entry_price + stop_distance
            take_profit = entry_price - stop_distance * risk_reward_ratio
        return {
            "stop_loss": max(stop_loss, 0.0),
            "take_profit": max(take_profit, 0.0),
            "stop_distance": stop_distance,
            "risk_reward_ratio": risk_reward_ratio,
        }

    def validate_trade(
        self, position: PositionSize, max_risk_percent: float = 0.05
    ) -> RiskValidation:
        """Validate a trade against risk limits."""
        checks: list[dict[str, Any]] = []
        passed = True
        if position.risk_percent > max_risk_percent:
            checks.append(
                {
                    "check": "risk_limit",
                    "passed": False,
                    "message": (
                        f"Risk {position.risk_percent:.1%} exceeds max {max_risk_percent:.1%}"
                    ),
                }
            )
            passed = False
        else:
            checks.append(
                {
                    "check": "risk_limit",
                    "passed": True,
                    "message": f"Risk {position.risk_percent:.1%} within limit",
                }
            )
        if position.kelly_fraction > 0.2:
            checks.append(
                {
                    "check": "kelly_caution",
                    "passed": True,
                    "message": (
                        f"Kelly fraction {position.kelly_fraction:.1%} — consider reducing size"
                    ),
                }
            )
        return RiskValidation(
            passed=passed,
            checks=checks,
            max_risk_score=position.risk_percent,
            recommendation="Proceed" if passed else "Reduce position size",
        )
