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
    model = joblib.load(MODEL_PATH)
    X_test = model_input(test_frame, getattr(model, "feature_names_in_", None))
    probabilities = model.predict_proba(X_test)
    predictions = model.predict(X_test)
    confidence = np.max(probabilities, axis=1)

    print("===== DIAGNOSTIC DE CONFIANCE (hors échantillon) =====")
    print(confidence_diagnostics(test_frame["target"].map({-1: 0, 0: 1, 1: 2}), predictions, probabilities).to_string(index=False))

    engine = BacktestEngine(test_frame, predictions, confidence)
    trades = engine.run()
    print("===== BACKTEST PRUDENT =====")
    print(BacktestMetrics(trades, engine.initial_capital).summary())
    print("Rejets :", engine.rejections)


if __name__ == "__main__":
    main()
