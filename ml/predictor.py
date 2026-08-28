import joblib
import numpy as np
import pandas as pd


class Predictor:

    def __init__(self, model):
        if isinstance(model, str):
            model = joblib.load(model)

        self.model_data = model

        if isinstance(model, dict):
            self.model = model["ensemble"]
            self.features = model["features"]
            self.classes = model["classes"]
            self.threshold = model.get("threshold", 0.50)
        else:
            self.model = model
            self.features = None
            self.classes = [0, 1, 2]
            self.threshold = 0.50

    def predict(self, df):

        data = df.copy()

        if self.features is not None:
            missing = [
                col for col in self.features
                if col not in data.columns
            ]

            if missing:
                raise ValueError(
                    f"Features manquantes: {missing}"
                )

            X = data[self.features]

        else:
            X = data

        X = X.replace(
            [np.inf, -np.inf],
            np.nan
        ).ffill().bfill()

        probabilities = self.model.predict_proba(X)

        probabilities = np.asarray(probabilities)

        predictions = np.argmax(
            probabilities,
            axis=1
        )

        confidence = np.max(
            probabilities,
            axis=1
        )

        prediction = int(predictions[-1])
        confidence_value = float(confidence[-1])

        row = data.iloc[-1]

        signal_map = {
            0: -1,
            1: 0,
            2: 1,
        }

        return {
            "signal": signal_map[prediction],
            "class": prediction,
            "confidence": confidence_value,
            "probabilities": probabilities[-1],
            "atr": float(row["ATR"]),
            "price": float(row["close"]),
            "time": row["time"],
        }