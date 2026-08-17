from __future__ import annotations

import pandas as pd


EXCLUDED_COLUMNS = {
    "time",
    "target",
}


def prepare_features(
    df: pd.DataFrame,
) -> pd.DataFrame:

    features = df.drop(
        columns=[
            c
            for c in EXCLUDED_COLUMNS
            if c in df.columns
        ]
    ).copy()

    features = features.select_dtypes(
        include=["number"]
    )

    features = features.replace(
        [float("inf"), float("-inf")],
        pd.NA,
    )

    features = features.ffill()

    features = features.fillna(0.0)

    return features