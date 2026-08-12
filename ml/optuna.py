"""Optional parameter search for the conservative backtest.

Run this module explicitly; importing it never starts an expensive study.
"""

from __future__ import annotations

import joblib
import numpy as np
import optuna

from backtest.engine import BacktestEngine
from backtest.metrics import BacktestMetrics
from config.settings import DATASET_PATH, MODEL_PATH
from features.schema import model_input
from ml.dataset import TradingDataset


def objective(trial, test_frame, predictions, confidence):
    engine = BacktestEngine(
        df=test_frame,
        predictions=predictions,
        confidence=confidence,
        atr_multiplier=trial.suggest_float("atr_multiplier", 1.0, 3.0),
        reward_ratio=trial.suggest_float("reward_ratio", 1.0, 3.0),
        confidence_threshold=trial.suggest_float("confidence_threshold", 0.60, 0.90),
    )
    trades = engine.run()
    metrics = BacktestMetrics(trades, engine.initial_capital).summary()
    # Optimise a risk-adjusted score rather than gross capital.
    return metrics["return_over_drawdown"]


def main(n_trials=100):
    dataset = TradingDataset(DATASET_PATH)
    _, test_frame = dataset.split_frame()
    model = joblib.load(MODEL_PATH)
    X_test = model_input(test_frame, getattr(model, "feature_names_in_", None))
    probabilities = model.predict_proba(X_test)
    predictions = model.predict(X_test)
    confidence = np.max(probabilities, axis=1)
    study = optuna.create_study(direction="maximize")
    study.optimize(lambda trial: objective(trial, test_frame, predictions, confidence), n_trials=n_trials)
    print(study.best_value)
    print(study.best_params)


if __name__ == "__main__":
    main()
