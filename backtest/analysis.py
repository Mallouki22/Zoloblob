"""Out-of-sample stability reports for threshold experiments."""

from __future__ import annotations

import numpy as np
import pandas as pd

from backtest.engine import BacktestEngine
from backtest.metrics import BacktestMetrics


def period_stability(df, predictions, confidence, threshold: float, periods: int = 4):
    """Evaluate contiguous chronological slices without mixing their outcomes."""
    bounds = np.linspace(0, len(df), periods + 1, dtype=int)
    rows = []
    for index, (start, stop) in enumerate(zip(bounds[:-1], bounds[1:]), start=1):
        engine = BacktestEngine(
            df.iloc[start:stop].reset_index(drop=True),
            predictions[start:stop],
            confidence[start:stop],
            confidence_threshold=threshold,
        )
        trades = engine.run()
        rows.append({"period": index, **BacktestMetrics(trades, engine.initial_capital).summary()})
    return pd.DataFrame(rows)
