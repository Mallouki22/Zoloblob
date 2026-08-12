"""
Liquidity Map
"""

import pandas as pd


class LiquidityMap:

    def equal_highs(
        self,
        df: pd.DataFrame,
        tolerance=0.15,
    ):

        highs = []

        values = df.high.values

        for i in range(1, len(values)):

            if abs(values[i] - values[i - 1]) <= tolerance:

                highs.append(values[i])

        return highs

    def equal_lows(
        self,
        df: pd.DataFrame,
        tolerance=0.15,
    ):

        lows = []

        values = df.low.values

        for i in range(1, len(values)):

            if abs(values[i] - values[i - 1]) <= tolerance:

                lows.append(values[i])

        return lows