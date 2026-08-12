"""
Professional Trade Planner
"""

import pandas as pd


class TradePlanner:

    def __init__(
        self,
        rr1=1.0,
        rr2=2.0,
        rr3=4.0,
        atr_buffer=0.30,
        swing_window=10,
    ):

        self.rr1 = rr1
        self.rr2 = rr2
        self.rr3 = rr3

        self.atr_buffer = atr_buffer
        self.swing_window = swing_window

    def _buy_sl(
        self,
        df,
        entry,
        atr,
    ):

        swing = (
            df["low"]
            .tail(self.swing_window)
            .min()
        )

        sl = min(
            swing,
            entry - atr,
        )

        sl -= atr * self.atr_buffer

        return sl

    def _sell_sl(
        self,
        df,
        entry,
        atr,
    ):

        swing = (
            df["high"]
            .tail(self.swing_window)
            .max()
        )

        sl = max(
            swing,
            entry + atr,
        )

        sl += atr * self.atr_buffer

        return sl

    def build(
        self,
        df: pd.DataFrame,
        signal,
    ):

        if signal == 0:
            return None

        row = df.iloc[-1]

        entry = row["close"]

        atr = row["ATR"]

        if atr <= 0:
            return None

        atr_mean = df["ATR"].tail(100).mean()

        ratio = atr / atr_mean

        if ratio < 0.80:

            sl_mult = 0.90

            rr1 = 1.30
            rr2 = 2.00
            rr3 = 3.00

        elif ratio < 1.10:

            sl_mult = 1.00

            rr1 = 1.50
            rr2 = 2.50
            rr3 = 4.00

        elif ratio < 1.40:

            sl_mult = 1.20

            rr1 = 2.00
            rr2 = 3.50
            rr3 = 5.00

        else:

            sl_mult = 1.50

            rr1 = 2.50
            rr2 = 4.00
            rr3 = 6.00

        if signal == 1:

            sl = max(
                self._buy_sl(
                    df,
                    entry,
                    atr,
                ),
                entry - atr * sl_mult,
            )

            risk = entry - sl

            tp1 = entry + risk * rr1
            tp2 = entry + risk * rr2
            tp3 = entry + risk * rr3

        else:

            sl = min(
                self._sell_sl(
                    df,
                    entry,
                    atr,
                ),
                entry + atr * sl_mult,
            )

            risk = sl - entry

            tp1 = entry - risk * rr1
            tp2 = entry - risk * rr2
            tp3 = entry - risk * rr3

        return {

            "entry": entry,

            "sl": sl,

            "tp1": tp1,

            "tp2": tp2,

            "tp3": tp3,

            "risk": risk,

            "reward1": abs(tp1 - entry),

            "reward2": abs(tp2 - entry),

            "reward3": abs(tp3 - entry),

            "rr1": rr1,

            "rr2": rr2,

            "rr3": rr3,

            "atr": atr,

            "atr_ratio": ratio,
        }