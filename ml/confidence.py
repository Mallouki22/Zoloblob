"""Out-of-sample diagnostics for model probability quality."""

from __future__ import annotations

import numpy as np
import pandas as pd


DEFAULT_THRESHOLDS = (0.60, 0.65, 0.70, 0.75, 0.80, 0.85, 0.90)


def confidence_diagnostics(y_true, predictions, probabilities, thresholds=DEFAULT_THRESHOLDS):
    """Measure directional precision and coverage at each confidence level.

    Class ``1`` is WAIT; only directional predictions are candidates for an
    order.  This deliberately reports BUY and SELL separately.
    """
    y_true = np.asarray(y_true)
    predictions = np.asarray(predictions)
    confidence = np.max(np.asarray(probabilities), axis=1)
    rows = []
    for threshold in thresholds:
        accepted = (predictions != 1) & (confidence >= threshold)
        buy = accepted & (predictions == 2)
        sell = accepted & (predictions == 0)
        rows.append({
            "threshold": threshold,
            "signals": int(accepted.sum()),
            "coverage_pct": round(float(accepted.mean() * 100), 2),
            "directional_precision_pct": round(float((predictions[accepted] == y_true[accepted]).mean() * 100), 2) if accepted.any() else 0.0,
            "buy_signals": int(buy.sum()),
            "buy_precision_pct": round(float((predictions[buy] == y_true[buy]).mean() * 100), 2) if buy.any() else 0.0,
            "sell_signals": int(sell.sum()),
            "sell_precision_pct": round(float((predictions[sell] == y_true[sell]).mean() * 100), 2) if sell.any() else 0.0,
        })
    return pd.DataFrame(rows)
