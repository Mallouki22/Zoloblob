"""
Market Trend Filter
"""

import pandas as pd


class TrendFilter:

    def __init__(
        self,
        fast=20,
        slow=50,
    ):

        self.fast = fast
        self.slow = slow

    def direction(self, df: pd.DataFrame):

        ema_fast = df["EMA_20"].iloc[-3:].mean()

        ema_slow = df["EMA_50"].iloc[-3:].mean()

        if ema_fast > ema_slow:

            return "BULL"

        if ema_fast < ema_slow:

            return "BEAR"

        return "RANGE"

    def validate(
        self,
        signal,
        df
    ):

        trend = self.direction(df)

        if signal == "BUY":

            return trend == "BULL"

        if signal == "SELL":

            return trend == "BEAR"

        return True