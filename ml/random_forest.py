from __future__ import annotations

from sklearn.ensemble import RandomForestClassifier


class RandomForestModel:

    def __init__(
        self,
        num_class: int = 3,
    ):

        self.model = RandomForestClassifier(

            n_estimators=500,

            max_depth=14,

            min_samples_leaf=8,

            max_features="sqrt",

            class_weight="balanced",

            random_state=42,

            n_jobs=-1,
        )

    def fit(
        self,
        X,
        y,
    ):

        self.model.fit(
            X,
            y,
        )

        return self

    def predict_proba(self, X):

        return self.model.predict_proba(X)

    def predict(self, X):

        return self.model.predict(X)