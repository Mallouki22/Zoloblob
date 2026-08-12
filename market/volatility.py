"""
Volatility Filter
"""


class VolatilityFilter:

    def allow(
        self,
        df,
    ):

        atr = df["ATR"].iloc[-1]

        atr_mean = df["ATR"].tail(150).mean()

        return 0.75 <= atr / atr_mean <= 1.80