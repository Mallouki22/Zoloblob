"""
Market Structure Filter
"""

import pandas as pd


class MarketStructure:

    def __init__(self, lookback=20):

        self.lookback = lookback

    def trend(self, df: pd.DataFrame):

        data = df.tail(self.lookback)

        first_high = data["high"].iloc[0]
        last_high = data["high"].iloc[-1]

        first_low = data["low"].iloc[0]
        last_low = data["low"].iloc[-1]

        if last_high > first_high and last_low > first_low:
            return "BULL"

        if last_high < first_high and last_low < first_low:
            return "BEAR"

        return "RANGE"

    def allow(self, df, signal):

        trend = self.trend(df)

        print("\n===== MARKET STRUCTURE =====")
        print("Trend  :", trend)
        print("Signal :", signal)

        if signal == "BUY":
            return trend == "BULL"

        if signal == "SELL":
            return trend == "BEAR"

        return False