"""
Break Of Structure
"""

class BOS:

    def __init__(self, lookback=10):

        self.lookback = lookback

    def direction(self, df):

        highs = df["high"].tail(self.lookback)
        lows = df["low"].tail(self.lookback)

        last_close = df["close"].iloc[-1]

        previous_high = highs.iloc[:-1].max()
        previous_low = lows.iloc[:-1].min()

        if last_close > previous_high:
            return "BULL"

        if last_close < previous_low:
            return "BEAR"

        return "NONE"

    def allow(self, df, signal):

        bos = self.direction(df)

        print("\n===== BOS =====")
        print("Direction :", bos)
        print("Signal    :", signal)

        if signal == "BUY":
            return bos == "BULL"

        if signal == "SELL":
            return bos == "BEAR"

        return False