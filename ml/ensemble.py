from __future__ import annotations

import numpy as np


class EnsembleModel:

    def __init__(
        self,
        models,
        weights=None,
    ):
        self.models = models

        if weights is None:
            weights = np.ones(len(models))

        self.weights = np.asarray(
            weights,
            dtype=np.float64,
        )

        self.weights = (
            self.weights
            / self.weights.sum()
        )

    def predict_proba(self, X):

        combined = None

        for model, weight in zip(
            self.models,
            self.weights,
        ):

            proba = np.asarray(
                model.predict_proba(X),
                dtype=np.float64,
            )

            # Sécurité : normalisation
            row_sums = proba.sum(
                axis=1,
                keepdims=True,
            )

            row_sums[
                row_sums <= 0
            ] = 1.0

            proba = (
                proba / row_sums
            )

            if combined is None:
                combined = (
                    weight * proba
                )
            else:
                combined += (
                    weight * proba
                )

        # Normalisation finale
        combined = (
            combined
            / combined.sum(
                axis=1,
                keepdims=True,
            )
        )

        return combined

    def predict(self, X):

        probabilities = (
            self.predict_proba(X)
        )

        return np.argmax(
            probabilities,
            axis=1,
        )

    def confidence(self, X):

        probabilities = (
            self.predict_proba(X)
        )

        return probabilities.max(
            axis=1,
        )

    def direction(self, X):

        probabilities = (
            self.predict_proba(X)
        )

        return np.argmax(
            probabilities,
            axis=1,
        )