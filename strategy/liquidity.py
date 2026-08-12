"""
Liquidity Sweep
"""

class LiquiditySweep:

    def __init__(self, lookback=20):

        self.lookback = lookback

    def direction(self, df):

        highs = df["high"].tail(self.lookback)
        lows = df["low"].tail(self.lookback)

        previous_high = highs.iloc[:-1].max()
        previous_low = lows.iloc[:-1].min()

        last = df.iloc[-1]

        if last["high"] > previous_high and last["close"] < previous_high:
            return "SELL"

        if last["low"] < previous_low and last["close"] > previous_low:
            return "BUY"

        return "NONE"

    def allow(self, df, signal):

        sweep = self.direction(df)

        print("\n===== LIQUIDITY =====")
        print("Sweep  :", sweep)
        print("Signal :", signal)

        if sweep == "NONE":
            return True

        return sweep == signal