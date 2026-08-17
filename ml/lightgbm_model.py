from __future__ import annotations

import lightgbm as lgb


class LightGBMModel:

    def __init__(
        self,
        num_class: int = 3,
    ):

        self.model = lgb.LGBMClassifier(

            objective="multiclass",

            num_class=num_class,

            n_estimators=600,

            learning_rate=0.03,

            num_leaves=31,

            max_depth=7,

            min_child_samples=40,

            subsample=0.85,

            colsample_bytree=0.85,

            reg_alpha=0.2,

            reg_lambda=2.0,

            random_state=42,

            n_jobs=-1,

            verbosity=-1,
        )

    def fit(
        self,
        X,
        y,
        sample_weight=None,
    ):

        self.model.fit(
            X,
            y,
            sample_weight=sample_weight,
        )

        return self

    def predict_proba(self, X):

        return self.model.predict_proba(X)

    def predict(self, X):

        return self.model.predict(X)