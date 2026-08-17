"""
Trading target generator.

0 = SELL
1 = WAIT
2 = BUY
"""

from __future__ import annotations

import numpy as np
import pandas as pd


class LabelGenerator:

    def __init__(
        self,
        df=None,
        horizon=32,
        atr_multiplier=1.0,
        reward_risk=1.3,
    ):
        self.df = df
        self.horizon = horizon
        self.atr_multiplier = atr_multiplier
        self.reward_risk = reward_risk

    def generate(self, df=None):

        if df is None:
            df = self.df

        if df is None:
            raise ValueError(
                "LabelGenerator: dataframe manquant."
            )

        df = df.copy()

        required = [
            "high",
            "low",
            "close",
            "ATR",
        ]

        missing = [
            c for c in required
            if c not in df.columns
        ]

        if missing:
            raise ValueError(
                f"Colonnes manquantes: {missing}"
            )

        n = len(df)

        labels = np.ones(
            n,
            dtype=np.int8,
        )

        highs = df["high"].to_numpy()
        lows = df["low"].to_numpy()
        closes = df["close"].to_numpy()
        atrs = df["ATR"].to_numpy()

        for i in range(n - self.horizon):

            entry = closes[i]
            atr = atrs[i]

            if not np.isfinite(atr) or atr <= 0:
                continue

            sl = atr * self.atr_multiplier
            tp = sl * self.reward_risk

            buy_tp = entry + tp
            buy_sl = entry - sl

            sell_tp = entry - tp
            sell_sl = entry + sl

            buy_result = None
            sell_result = None

            future_high = highs[
                i + 1:i + 1 + self.horizon
            ]

            future_low = lows[
                i + 1:i + 1 + self.horizon
            ]

            for high, low in zip(
                future_high,
                future_low,
            ):

                # BUY
                if high >= buy_tp and low <= buy_sl:
                    buy_result = "AMBIGUOUS"
                elif high >= buy_tp:
                    buy_result = "WIN"
                elif low <= buy_sl:
                    buy_result = "LOSS"

                # SELL
                if low <= sell_tp and high >= sell_sl:
                    sell_result = "AMBIGUOUS"
                elif low <= sell_tp:
                    sell_result = "WIN"
                elif high >= sell_sl:
                    sell_result = "LOSS"

                if (
                    buy_result is not None
                    and sell_result is not None
                ):
                    break

            # Priorité aux situations non ambiguës
            if buy_result == "WIN" and sell_result != "WIN":
                labels[i] = 2

            elif sell_result == "WIN" and buy_result != "WIN":
                labels[i] = 0

            else:
                labels[i] = 1

        df["target"] = labels

        return df