"""Threshold sensitivity report; it does not optimise on the training set."""

import joblib
import numpy as np
import pandas as pd

from backtest.engine import BacktestEngine
from backtest.metrics import BacktestMetrics
from backtest.analysis import period_stability
from config.settings import DATASET_PATH, MODEL_PATH
from features.schema import model_input
from ml.confidence import DEFAULT_THRESHOLDS
from ml.dataset import TradingDataset


def main():
    dataset = TradingDataset(DATASET_PATH)
    _, test_frame = dataset.split_frame()
    model = joblib.load(MODEL_PATH)
    X_test = model_input(test_frame, getattr(model, "feature_names_in_", None))
    probabilities = model.predict_proba(X_test)
    predictions = model.predict(X_test)
    confidence = np.max(probabilities, axis=1)

    rows = []
    for threshold in DEFAULT_THRESHOLDS:
        engine = BacktestEngine(test_frame, predictions, confidence, confidence_threshold=threshold)
        trades = engine.run()
        rows.append({"threshold": threshold, **BacktestMetrics(trades, engine.initial_capital).summary()})
    print(pd.DataFrame(rows).to_string(index=False))
    for threshold in DEFAULT_THRESHOLDS:
        print(f"\n===== Stabilité hors échantillon — seuil {threshold:.0%} =====")
        print(period_stability(test_frame, predictions, confidence, threshold).to_string(index=False))


if __name__ == "__main__":
    main()
