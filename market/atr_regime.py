"""
ATR Regime Filter
"""

import pandas as pd


class ATRRegime:

    def score(
        self,
        df: pd.DataFrame,
    ):

        atr = df["ATR"].iloc[-1]

        mean = df["ATR"].tail(100).mean()

        ratio = atr / mean

        if ratio < 0.80:
            return 0

        if ratio < 1.00:
            return 5

        if ratio < 1.20:
            return 10

        if ratio < 1.50:
            return 15

        return 20