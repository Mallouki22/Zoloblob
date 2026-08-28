"""
Final signal generation.

ML + confidence gate.
"""

import numpy as np


SELL = "SELL"
WAIT = "WAIT"
BUY = "BUY"


class SignalGenerator:

    def __init__(
        self,
        model,
        buy_threshold=0.70,
        sell_threshold=0.70,
    ):
        self.model = model
        self.buy_threshold = float(buy_threshold)
        self.sell_threshold = float(sell_threshold)

    def generate_one(self, X):

        probabilities = self.model.predict_proba(X)[0]

        sell_probability = float(probabilities[0])
        wait_probability = float(probabilities[1])
        buy_probability = float(probabilities[2])

        if (
            buy_probability >= self.buy_threshold
            and buy_probability > sell_probability
        ):
            signal = BUY
            confidence = buy_probability

        elif (
            sell_probability >= self.sell_threshold
            and sell_probability > buy_probability
        ):
            signal = SELL
            confidence = sell_probability

        else:
            signal = WAIT
            confidence = max(
                sell_probability,
                wait_probability,
                buy_probability,
            )

        return {
            "signal": signal,
            "confidence": confidence,
            "sell_probability": sell_probability,
            "wait_probability": wait_probability,
            "buy_probability": buy_probability,
        }