"""
Trading Predictor
"""

import joblib

from config.settings import MODEL_PATH
from features.schema import model_input


class Predictor:

    def __init__(self):

        self.model = joblib.load(MODEL_PATH)

        self.feature_names = getattr(
            self.model,
            "feature_names_in_",
            None,
        )

    def predict(self, df):

        last = df.tail(1)

        model_frame = model_input(
            last,
            self.feature_names,
        )

        prediction = int(
            self.model.predict(model_frame)[0]
        )

        probabilities = (
            self.model.predict_proba(model_frame)[0]
        )

        mapping = {
            0: "SELL",
            1: "WAIT",
            2: "BUY",
        }

        confidence = float(
            probabilities[prediction]
        )

        return {

            "signal": mapping[prediction],

            "confidence": confidence,

            "probabilities": {
                "SELL": float(probabilities[0]),
                "WAIT": float(probabilities[1]),
                "BUY": float(probabilities[2]),
            },

            "score": 0,

            "price": float(
                last["close"].iloc[0]
            ),

            "atr": float(
                last["ATR"].iloc[0]
            ),

            "market": last.copy(),

            "time": last["time"].iloc[0],
        }