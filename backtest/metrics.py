"""
Performance metrics focused on risk-adjusted robustness.
"""

from __future__ import annotations

import numpy as np


class BacktestMetrics:

    def __init__(
        self,
        trades,
        initial_capital: float,
    ):

        self.trades = trades
        self.initial_capital = initial_capital

    def summary(self):

        if self.trades.empty:

            return {
                "trades": 0,
                "net_profit": 0.0,
                "profit_factor": 0.0,
                "expectancy": 0.0,
                "win_rate": 0.0,
                "max_drawdown": 0.0,
                "return_over_drawdown": 0.0,
                "average_score": 0.0,
            }

        profits = self.trades["profit"]

        gross_profit = profits[profits > 0].sum()

        gross_loss = -profits[profits < 0].sum()

        profit_factor = (
            gross_profit / gross_loss
            if gross_loss
            else float("inf")
        )

        equity = np.r_[
            self.initial_capital,
            self.trades["balance"].to_numpy(),
        ]

        max_drawdown = float(
            -(equity - np.maximum.accumulate(equity)).min()
        )

        average_score = (
            float(self.trades["score"].mean())
            if "score" in self.trades.columns
            else 0.0
        )

        net_profit = float(profits.sum())

        return {

            "trades": int(len(self.trades)),

            "net_profit": net_profit,

            "profit_factor": float(profit_factor),

            "expectancy": float(profits.mean()),

            "win_rate": float((profits > 0).mean() * 100),

            "max_drawdown": max_drawdown,

            "return_over_drawdown": (
                net_profit / max_drawdown
                if max_drawdown
                else 0.0
            ),

            "average_score": average_score,
        }