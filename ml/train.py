from __future__ import annotations

import joblib
import numpy as np

from sklearn.utils.class_weight import compute_sample_weight

from config.settings import DATASET_PATH, MODEL_PATH
from ml.dataset import TradingDataset
from ml.features import prepare_features
from ml.lightgbm_model import LightGBMModel
from ml.xgboost_model import XGBoostModel
from ml.random_forest import RandomForestModel
from ml.ensemble import EnsembleModel
from ml.evaluator import evaluate, confidence_report


def main():

    # ==========================================
    # DATA
    # ==========================================

    dataset = TradingDataset(
        DATASET_PATH
    )

    (
        X_train,
        X_test,
        y_train,
        y_test,
    ) = dataset.prepare()

    X_train = prepare_features(
        X_train
    )

    X_test = prepare_features(
        X_test
    )

    print("\n===== DATA =====")

    print(
        "Train:",
        X_train.shape
    )

    print(
        "Test :",
        X_test.shape
    )

    print("\n===== TARGET TRAIN =====")
    print(
        y_train.value_counts()
        .sort_index()
    )

    print("\n===== TARGET TEST =====")
    print(
        y_test.value_counts()
        .sort_index()
    )

    # ==========================================
    # WEIGHTS
    # ==========================================

    sample_weight = (
        compute_sample_weight(
            class_weight="balanced",
            y=y_train,
        )
    )

    # ==========================================
    # LIGHTGBM
    # ==========================================

    print(
        "\n===== LIGHTGBM ====="
    )

    lgbm = LightGBMModel()

    lgbm.fit(
        X_train,
        y_train,
        sample_weight=sample_weight,
    )

    # ==========================================
    # XGBOOST
    # ==========================================

    print(
        "\n===== XGBOOST ====="
    )

    xgb = XGBoostModel()

    xgb.fit(
        X_train,
        y_train,
        sample_weight=sample_weight,
    )

    # ==========================================
    # RANDOM FOREST
    # ==========================================

    print(
        "\n===== RANDOM FOREST ====="
    )

    rf = RandomForestModel()

    rf.fit(
        X_train,
        y_train,
    )

    # ==========================================
    # INDIVIDUAL EVALUATION
    # ==========================================

    print(
        "\n===== LIGHTGBM TEST ====="
    )

    lgbm_result = evaluate(
        lgbm,
        X_test,
        y_test,
    )

    print(
        "\n===== XGBOOST TEST ====="
    )

    xgb_result = evaluate(
        xgb,
        X_test,
        y_test,
    )

    print(
        "\n===== RANDOM FOREST TEST ====="
    )

    rf_result = evaluate(
        rf,
        X_test,
        y_test,
    )

    # ==========================================
    # ENSEMBLE
    # ==========================================

    print(
        "\n===== ENSEMBLE ====="
    )

    models = [
        lgbm,
        xgb,
        rf,
    ]

    ensemble = EnsembleModel(
        models=models,
        weights=[
            1.0,
            1.0,
            1.0,
        ],
    )

    result = evaluate(
        ensemble,
        X_test,
        y_test,
    )

    probabilities = (
        result["probabilities"]
    )

    confidence_report(
        y_test,
        probabilities,
    )

    # ==========================================
    # SAVE
    # ==========================================

    artifact = {

        "ensemble": ensemble,

        "features": list(
            X_train.columns
        ),

        "classes": [
            0,
            1,
            2,
        ],

        "threshold": 0.65,
    }

    joblib.dump(
        artifact,
        MODEL_PATH,
    )

    print(
        f"\nModel saved: {MODEL_PATH}"
    )


if __name__ == "__main__":

    main()