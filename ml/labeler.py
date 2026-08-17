"""
Event-based trading target generator.

Classes:
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
        atr_multiplier=1.2,
        reward_risk=1.5,
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

        highs = df["high"].to_numpy(
            dtype=np.float64
        )

        lows = df["low"].to_numpy(
            dtype=np.float64
        )

        closes = df["close"].to_numpy(
            dtype=np.float64
        )

        atrs = df["ATR"].to_numpy(
            dtype=np.float64
        )

        for i in range(
            n - self.horizon
        ):

            entry = closes[i]
            atr = atrs[i]

            if not np.isfinite(atr):
                continue

            if atr <= 0:
                continue

            if not np.isfinite(entry):
                continue

            sl_distance = (
                atr
                * self.atr_multiplier
            )

            tp_distance = (
                sl_distance
                * self.reward_risk
            )

            buy_tp = (
                entry
                + tp_distance
            )

            buy_sl = (
                entry
                - sl_distance
            )

            sell_tp = (
                entry
                - tp_distance
            )

            sell_sl = (
                entry
                + sl_distance
            )

            buy_result = None
            sell_result = None

            future_highs = highs[
                i + 1 :
                i + 1 + self.horizon
            ]

            future_lows = lows[
                i + 1 :
                i + 1 + self.horizon
            ]

            for high, low in zip(
                future_highs,
                future_lows,
            ):

                if (
                    buy_result is None
                    and sell_result is None
                ):
                    pass

                # ==============================
                # BUY
                # ==============================

                if buy_result is None:

                    buy_tp_hit = (
                        high >= buy_tp
                    )

                    buy_sl_hit = (
                        low <= buy_sl
                    )

                    if (
                        buy_tp_hit
                        and buy_sl_hit
                    ):
                        buy_result = (
                            "AMBIGUOUS"
                        )

                    elif buy_tp_hit:
                        buy_result = "WIN"

                    elif buy_sl_hit:
                        buy_result = "LOSS"

                # ==============================
                # SELL
                # ==============================

                if sell_result is None:

                    sell_tp_hit = (
                        low <= sell_tp
                    )

                    sell_sl_hit = (
                        high >= sell_sl
                    )

                    if (
                        sell_tp_hit
                        and sell_sl_hit
                    ):
                        sell_result = (
                            "AMBIGUOUS"
                        )

                    elif sell_tp_hit:
                        sell_result = "WIN"

                    elif sell_sl_hit:
                        sell_result = "LOSS"

                # ==============================
                # BOTH SIDES FINISHED
                # ==============================

                if (
                    buy_result is not None
                    and sell_result is not None
                ):
                    break

            # ==============================
            # LABEL DECISION
            # ==============================

            buy_win = (
                buy_result == "WIN"
            )

            sell_win = (
                sell_result == "WIN"
            )

            # Only label a direction when
            # exactly one side wins.

            if (
                buy_win
                and not sell_win
            ):
                labels[i] = 2

            elif (
                sell_win
                and not buy_win
            ):
                labels[i] = 0

            else:
                labels[i] = 1

        df["target"] = labels

        return df