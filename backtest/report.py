"""
Backtest Report
"""

from backtest.metrics import BacktestMetrics


class BacktestReport:

    def __init__(
        self,
        trades,
        initial_capital,
        final_capital
    ):

        self.trades = trades

        self.initial_capital = initial_capital

        self.final_capital = final_capital

        self.metrics = BacktestMetrics(trades, initial_capital)

    def print(self):

        print("\n" + "=" * 40)
        print("      BACKTEST REPORT")
        print("=" * 40)

        print(
            f"Initial Capital : {self.initial_capital:.2f}$"
        )

        print(
            f"Final Capital   : {self.final_capital:.2f}$"
        )

        print(
            f"Net Profit      : {self.final_capital-self.initial_capital:.2f}$"
        )

        print()

        for key, value in self.metrics.summary().items():
            print(f"{key:<18}: {value}")

        print("=" * 40)
