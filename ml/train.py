"""
Train XGBoost 3-class trading model.

Classes:
    0 = SELL
    1 = WAIT
    2 = BUY
"""

from __future__ import annotations

import argparse
import joblib
import numpy as np

from scipy.stats import randint, uniform

from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    log_loss,
)
from sklearn.model_selection import (
    RandomizedSearchCV,
    TimeSeriesSplit,
)
from sklearn.utils.class_weight import compute_sample_weight

from xgboost import XGBClassifier

from config.settings import DATASET_PATH, MODEL_PATH
from ml.confidence import confidence_diagnostics
from ml.dataset import TradingDataset


LOOKAHEAD_GAP = 30
SEARCH_ITERATIONS = 6


def _time_series_cv(n_splits=4):

    return TimeSeriesSplit(
        n_splits=n_splits,
        gap=LOOKAHEAD_GAP,
    )


def train(tune=False):

    dataset = TradingDataset(DATASET_PATH)

    (
        X_train,
        X_test,
        y_train,
        y_test,
    ) = dataset.prepare()

    print("\n===== TARGET TRAIN =====")
    print(y_train.value_counts().sort_index())

    print("\n===== TARGET TEST =====")
    print(y_test.value_counts().sort_index())

    train_classes = sorted(
        y_train.unique()
    )

    test_classes = sorted(
        y_test.unique()
    )

    print("\nTrain classes:", train_classes)
    print("Test classes :", test_classes)

    expected = [0, 1, 2]

    if train_classes != expected:
        raise ValueError(
            f"Train classes invalides: {train_classes}. "
            "Expected [0, 1, 2]."
        )

    if test_classes != expected:
        raise ValueError(
            f"Test classes invalides: {test_classes}. "
            "Expected [0, 1, 2]."
        )

    # ==========================================
    # CLASS WEIGHTS
    # ==========================================

    print("\n===== CLASS WEIGHTS =====")

    sample_weights = compute_sample_weight(
        class_weight="balanced",
        y=y_train,
    )

    for cls in expected:

        mask = y_train == cls

        if mask.any():

            print(
                f"class {cls}: "
                f"{sample_weights[mask].mean():.3f}"
            )

    # ==========================================
    # MODEL
    # ==========================================

    base_model = XGBClassifier(

        objective="multi:softprob",

        num_class=3,

        eval_metric="mlogloss",

        n_estimators=700,

        max_depth=5,

        learning_rate=0.03,

        subsample=0.85,

        colsample_bytree=0.85,

        min_child_weight=8,

        gamma=0.2,

        reg_alpha=0.2,

        reg_lambda=3,

        tree_method="hist",

        random_state=42,

        n_jobs=1,
    )

    # ==========================================
    # TUNING
    # ==========================================

    if tune:

        print("\n===== TEMPORAL TUNING =====")

        param_grid = {

            "n_estimators": randint(
                300,
                1000,
            ),

            "max_depth": randint(
                3,
                8,
            ),

            "learning_rate": uniform(
                0.01,
                0.05,
            ),

            "subsample": uniform(
                0.75,
                0.25,
            ),

            "colsample_bytree": uniform(
                0.75,
                0.25,
            ),

            "min_child_weight": randint(
                3,
                15,
            ),

            "gamma": uniform(
                0,
                0.8,
            ),

            "reg_alpha": uniform(
                0,
                0.5,
            ),

            "reg_lambda": uniform(
                1,
                4,
            ),
        }

        search = RandomizedSearchCV(

            estimator=base_model,

            param_distributions=param_grid,

            n_iter=SEARCH_ITERATIONS,

            scoring="neg_log_loss",

            cv=_time_series_cv(),

            verbose=2,

            random_state=42,

            n_jobs=1,
        )

        search.fit(
            X_train,
            y_train,
            sample_weight=sample_weights,
        )

        estimator = search.best_estimator_

        print(
            "\nBest temporal CV log-loss:",
            -search.best_score_,
        )

    else:

        estimator = base_model

    # ==========================================
    # TRAIN
    # ==========================================

    print("\n===== FIT MODEL =====")

    estimator.fit(
        X_train,
        y_train,
        sample_weight=sample_weights,
    )

    # ==========================================
    # CALIBRATION
    # ==========================================

    print("\n===== CALIBRATION =====")

    model = CalibratedClassifierCV(
        estimator=estimator,
        method="sigmoid",
        cv=_time_series_cv(3),
    )

    model.fit(
        X_train,
        y_train,
    )

    # ==========================================
    # SAVE
    # ==========================================

    joblib.dump(
        model,
        MODEL_PATH,
    )

    print(
        f"\nModel saved: {MODEL_PATH}"
    )

    # ==========================================
    # PREDICTION
    # ==========================================

    probabilities = model.predict_proba(X_test)

    predictions = model.predict(X_test)

    # ==========================================
    # EVALUATION
    # ==========================================

    print("\n===== EVALUATION =====")

    print(
        "Out-of-sample log-loss:",
        log_loss(
            y_test,
            probabilities,
        ),
    )

    print(
        "Out-of-sample accuracy:",
        accuracy_score(
            y_test,
            predictions,
        ),
    )

    print(
        classification_report(

            y_test,

            predictions,

            labels=[0, 1, 2],

            target_names=[
                "SELL",
                "WAIT",
                "BUY",
            ],

            zero_division=0,
        )
    )

    # ==========================================
    # PROBABILITY DISTRIBUTION
    # ==========================================

    max_probability = probabilities.max(axis=1)

    print("\n===== PROBABILITY DISTRIBUTION =====")

    print(
        "Min :",
        round(float(max_probability.min()), 4),
    )

    print(
        "Mean:",
        round(float(max_probability.mean()), 4),
    )

    print(
        "Max :",
        round(float(max_probability.max()), 4),
    )

    for threshold in [
        0.50,
        0.55,
        0.60,
        0.65,
        0.70,
        0.75,
        0.80,
        0.85,
        0.90,
    ]:

        count = int(
            (max_probability >= threshold).sum()
        )

        print(
            f">= {threshold:.2f}: "
            f"{count} "
            f"({count / len(max_probability) * 100:.2f}%)"
        )

    # ==========================================
    # CONFIDENCE
    # ==========================================

    print(
        "\n===== CONFIANCE HORS ÉCHANTILLON ====="
    )

    diagnostics = confidence_diagnostics(
        y_test,
        predictions,
        probabilities,
    )

    print(
        diagnostics.to_string(
            index=False
        )
    )

    return model


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--tune",
        action="store_true",
    )

    args = parser.parse_args()

    train(
        tune=args.tune
    )