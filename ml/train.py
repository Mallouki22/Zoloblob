"""
Train a probability-calibrated binary trading model.
"""

from __future__ import annotations

import argparse
import joblib

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

    dataset = TradingDataset(
        DATASET_PATH
    )

    (
        X_train,
        X_test,
        y_train,
        y_test,
    ) = dataset.prepare()

    print(
        "\n===== TARGET TRAIN ====="
    )

    print(
        y_train.value_counts()
    )

    print(
        "\n===== TARGET TEST ====="
    )

    print(
        y_test.value_counts()
    )

    # ==============================
    # CHECK
    # ==============================

    train_classes = sorted(
        y_train.unique()
    )

    test_classes = sorted(
        y_test.unique()
    )

    print(
        "\nTrain classes:",
        train_classes,
    )

    print(
        "Test classes:",
        test_classes,
    )

    if train_classes != [0, 1]:

        raise ValueError(
            "Classes invalides : "
            f"{train_classes}"
        )

    # ==============================
    # MODEL
    # ==============================

    base_model = XGBClassifier(

        objective="binary:logistic",

        eval_metric="logloss",

        n_estimators=700,

        max_depth=6,

        learning_rate=0.03,

        subsample=0.8,

        colsample_bytree=0.8,

        min_child_weight=5,

        gamma=0.2,

        reg_alpha=0.1,

        reg_lambda=2,

        tree_method="hist",

        random_state=42,

        n_jobs=1,
    )

    param_grid = {

        "n_estimators": randint(
            300,
            1000,
        ),

        "max_depth": randint(
            4,
            9,
        ),

        "learning_rate": uniform(
            0.01,
            0.07,
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
            2,
            10,
        ),

        "gamma": uniform(
            0,
            0.8,
        ),

        "reg_alpha": uniform(
            0,
            0.3,
        ),

        "reg_lambda": uniform(
            1,
            3,
        ),
    }

    # ==============================
    # TUNING
    # ==============================

    if tune:

        print(
            "\n===== TEMPORAL TUNING ====="
        )

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
        )

        estimator = (
            search.best_estimator_
        )

        print(
            "\nBest temporal CV log-loss:",
            -search.best_score_,
        )

    else:

        estimator = base_model

    # ==============================
    # CALIBRATION
    # ==============================

    print(
        "\n===== FIT MODEL ====="
    )

    model = CalibratedClassifierCV(

        estimator=estimator,

        method="sigmoid",

        cv=_time_series_cv(3),
    )

    model.fit(
        X_train,
        y_train,
    )

    # ==============================
    # SAVE
    # ==============================

    joblib.dump(
        model,
        MODEL_PATH,
    )

    print(
        f"\nModel saved: {MODEL_PATH}"
    )

    # ==============================
    # PREDICTION
    # ==============================

    probabilities = (
        model.predict_proba(
            X_test
        )
    )

    predictions = (
        model.predict(
            X_test
        )
    )

    # ==============================
    # EVALUATION
    # ==============================

    print(
        "\n===== EVALUATION ====="
    )

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

            target_names=[
                "SELL",
                "BUY",
            ],

            zero_division=0,
        )
    )

    # ==============================
    # CONFIDENCE
    # ==============================

    print(
        "\n===== CONFIANCE HORS ÉCHANTILLON ====="
    )

    diagnostics = (
        confidence_diagnostics(
            y_test,
            predictions,
            probabilities,
        )
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