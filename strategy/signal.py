"""
Signal Generator
"""

import numpy as np


class SignalGenerator:

    def __init__(
        self,
        model,
        threshold=0.60
    ):

        self.model = model
        self.threshold = threshold


    def generate(self, X):

        probabilities = self.model.predict_proba(X)

        signals = []

        for proba in probabilities:

            confidence = np.max(proba)

            prediction = np.argmax(proba)

            if confidence < self.threshold:

                prediction = 1      # WAIT

            signals.append(prediction)

        return np.array(signals)