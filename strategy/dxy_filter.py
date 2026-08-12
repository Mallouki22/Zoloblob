"""
DXY Filter
"""
from data.dxy import DXYData

class DXYFilter:

    def __init__(self):

        self.enabled = True
        self.data = DXYData()

    def get_trend(self):

        df = self.data.latest()

        if len(df) < 50:
            return "UNKNOWN"

        ema20 = df["Close"].ewm(span=20).mean().iloc[-1]
        ema50 = df["Close"].ewm(span=50).mean().iloc[-1]


        if ema20 > ema50:
            return "BULL"

        return "BEAR"

    def allow(self, signal):

        if not self.enabled:
            return True

        trend = self.get_trend()

        print("\n===== DXY FILTER =====")
        print("Trend DXY :", trend)
        print("Signal    :", signal)

        if trend == "UNKNOWN":
            return True

        if trend == "BULL" and signal == "SELL":
            return False

        if trend == "BEAR" and signal == "BUY":
            return False

        return True