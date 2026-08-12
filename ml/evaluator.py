"""
Model Evaluator
"""

import pandas as pd


class ModelEvaluator:

    def __init__(self, backtest_results):

        self.results = backtest_results.copy()

    def summary(self):
        if self.results.empty:
            return "Aucun trade."

        total = len(self.results)

        wins = len(
            self.results[
                self.results["result"] == "WIN"
            ]
        )

        losses = total - wins

        win_rate = (
            wins / total * 100
            if total else 0
        )

        profit = self.results["profit"].sum()

        average = (
            self.results["profit"].mean()
            if total else 0
        )

        return {
            "trades": total,
            "wins": wins,
            "losses": losses,
            "win_rate": round(win_rate, 2),
            "net_profit": round(profit, 2),
            "average_profit": round(average, 2)
        }