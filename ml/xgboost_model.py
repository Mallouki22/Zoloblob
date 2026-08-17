from __future__ import annotations

from xgboost import XGBClassifier


class XGBoostModel:

    def __init__(
        self,
        num_class: int = 3,
    ):

        self.model = XGBClassifier(

            objective="multi:softprob",

            num_class=num_class,

            eval_metric="mlogloss",

            n_estimators=600,

            learning_rate=0.03,

            max_depth=5,

            min_child_weight=8,

            subsample=0.85,

            colsample_bytree=0.85,

            gamma=0.2,

            reg_alpha=0.2,

            reg_lambda=3.0,

            tree_method="hist",

            random_state=42,

            n_jobs=-1,
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