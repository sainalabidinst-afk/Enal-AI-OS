"""
Backtesting engine for Trading Analyst.

Validates trading strategies against historical data.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class TradeResult:
    """Result of a single backtest trade."""

    entry_price: float = 0.0
    exit_price: float = 0.0
    direction: str = "long"
    pnl: float = 0.0
    pnl_percent: float = 0.0
    duration: int = 0
    win: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class BacktestResult:
    """Aggregated backtest results."""

    total_trades: int = 0
    wins: int = 0
    losses: int = 0
    win_rate: float = 0.0
    total_pnl: float = 0.0
    avg_win: float = 0.0
    avg_loss: float = 0.0
    profit_factor: float = 0.0
    max_drawdown: float = 0.0
    sharpe_ratio: float = 0.0
    trades: list[TradeResult] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def calculate_metrics(self) -> None:
        """Calculate performance metrics from trades."""
        if not self.trades:
            return
        self.total_trades = len(self.trades)
        self.wins = sum(1 for t in self.trades if t.win)
        self.losses = self.total_trades - self.wins
        self.win_rate = self.wins / self.total_trades if self.total_trades > 0 else 0.0
        self.total_pnl = sum(t.pnl for t in self.trades)
        wins_list = [t.pnl for t in self.trades if t.win]
        losses_list = [t.pnl for t in self.trades if not t.win]
        self.avg_win = sum(wins_list) / len(wins_list) if wins_list else 0.0
        self.avg_loss = sum(losses_list) / len(losses_list) if losses_list else 0.0
        gross_profit = sum(wins_list) if wins_list else 0.0
        gross_loss = abs(sum(losses_list)) if losses_list else 0.0
        self.profit_factor = gross_profit / gross_loss if gross_loss > 0 else 0.0


class BacktestEngine:
    """Simple backtesting engine for trading strategies."""

    def run_backtest(
        self,
        ohlcv_data: list[Any],
        strategy,
        initial_capital: float = 10000.0,
        position_size_percent: float = 0.02,
    ) -> BacktestResult:
        """Run a backtest on historical OHLCV data."""
        trades: list[TradeResult] = []
        capital = initial_capital
        position = None
        entry_price = 0.0
        entry_index = 0
        for i, candle in enumerate(ohlcv_data):
            signal = strategy.generate_signal(candle, i, ohlcv_data)
            if signal == "buy" and position is None:
                position = "long"
                entry_price = candle.close
                entry_index = i
            elif signal == "sell" and position == "long":
                pnl = candle.close - entry_price
                pnl_percent = pnl / entry_price * 100 if entry_price > 0 else 0.0
                trade = TradeResult(
                    entry_price=entry_price,
                    exit_price=candle.close,
                    direction="long",
                    pnl=pnl,
                    pnl_percent=pnl_percent,
                    duration=i - entry_index,
                    win=pnl > 0,
                )
                trades.append(trade)
                capital += pnl
                position = None
        result = BacktestResult(
            trades=trades,
            metadata={"initial_capital": initial_capital, "final_capital": capital},
        )
        result.calculate_metrics()
        return result
