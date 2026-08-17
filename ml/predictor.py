from __future__ import annotations

import numpy as np


SELL = 0
WAIT = 1
BUY = 2


class Predictor:

    def __init__(
        self,
        model,
        min_confidence=0.65,
    ):

        self.model = model

        self.min_confidence = (
            min_confidence
        )

    def predict(self, X):

        probabilities = (
            self.model.predict_proba(X)
        )

        prediction = np.argmax(
            probabilities,
            axis=1,
        )

        confidence = probabilities.max(
            axis=1
        )

        signals = np.full(
            len(prediction),
            WAIT,
            dtype=np.int8,
        )

        valid = (
            confidence
            >= self.min_confidence
        )

        signals[
            valid
        ] = prediction[valid]

        return signals

    def predict_one(self, X):

        probabilities = (
            self.model.predict_proba(X)
        )[0]

        prediction = int(
            np.argmax(probabilities)
        )

        confidence = float(
            probabilities.max()
        )

        if confidence < self.min_confidence:

            prediction = WAIT

        return {
            "signal": prediction,
            "confidence": confidence,
            "sell_probability": float(
                probabilities[SELL]
            ),
            "wait_probability": float(
                probabilities[WAIT]
            ),
            "buy_probability": float(
                probabilities[BUY]
            ),
        }