"""Evaluate the saved model with the same rules used by live execution."""

import joblib
import numpy as np

from backtest.engine import BacktestEngine
from backtest.metrics import BacktestMetrics
from config.settings import MODEL_PATH, DATASET_PATH
from features.schema import model_input
from ml.confidence import confidence_diagnostics
from ml.dataset import TradingDataset


def main():

    dataset = TradingDataset(DATASET_PATH)

    _, test_frame = dataset.split_frame()

    artifact = joblib.load(MODEL_PATH)

    if not isinstance(artifact, dict):
        raise TypeError(
            "Model artifact invalide : dict attendu."
        )

    ensemble = artifact["ensemble"]
    features = artifact["features"]
    threshold = artifact.get(
        "threshold",
        0.65,
    )

    X_test = model_input(
        test_frame,
        expected_columns=features,
    )

    probabilities = ensemble.predict_proba(
        X_test
    )

    predictions = ensemble.predict(
        X_test
    )

    confidence = np.max(
        probabilities,
        axis=1,
    )

    print(
        "===== MODEL ====="
    )

    print(
        "Features :",
        len(features),
    )

    print(
        "Threshold :",
        threshold,
    )

    print(
        "Confidence moyenne :",
        round(float(confidence.mean()), 4),
    )

    print(
        "Confidence max :",
        round(float(confidence.max()), 4),
    )

    print(
        "Confidence min :",
        round(float(confidence.min()), 4),
    )

    print(
        "\n===== DIAGNOSTIC DE CONFIANCE (hors échantillon) ====="
    )

    diagnostics = confidence_diagnostics(
        test_frame["target"].to_numpy(),
        predictions,
        probabilities,
    )

    print(
        diagnostics.to_string(
            index=False
        )
    )

    engine = BacktestEngine(
        test_frame,
        predictions,
        confidence,
        confidence_threshold=threshold,
    )

    trades = engine.run()

    print(
        "\n===== BACKTEST PRUDENT ====="
    )

    print(
        BacktestMetrics(
            trades,
            engine.initial_capital,
        ).summary()
    )

    print(
        "Rejets :",
        engine.rejections,
    )


if __name__ == "__main__":
    main()