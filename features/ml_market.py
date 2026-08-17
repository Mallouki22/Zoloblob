from __future__ import annotations

import numpy as np
import pandas as pd


def add_ml_market_features(
    df: pd.DataFrame,
) -> pd.DataFrame:

    df = df.copy()

    # ==========================================
    # RETURN / VOLATILITY
    # ==========================================

    for n in [1, 3, 5, 10, 20]:

        df[f"return_{n}"] = (
            df["close"]
            .pct_change(n)
        )

    df["atr_pct"] = (
        df["ATR"]
        / df["close"]
    )

    # ==========================================
    # CANDLE STRUCTURE
    # ==========================================

    candle_range = (
        df["high"]
        - df["low"]
    )

    candle_range = candle_range.replace(
        0,
        np.nan,
    )

    df["body_pct"] = (
        (df["close"] - df["open"])
        / candle_range
    )

    df["upper_wick_pct"] = (
        (
            df["high"]
            - df[["open", "close"]].max(axis=1)
        )
        / candle_range
    )

    df["lower_wick_pct"] = (
        (
            df[["open", "close"]].min(axis=1)
            - df["low"]
        )
        / candle_range
    )

    # ==========================================
    # PRICE / EMA
    # ==========================================

    df["close_ema20_distance"] = (
        (df["close"] - df["EMA_20"])
        / df["ATR"]
    )

    df["close_ema50_distance"] = (
        (df["close"] - df["EMA_50"])
        / df["ATR"]
    )

    # ==========================================
    # EMA SLOPE
    # ==========================================

    df["ema20_slope_5"] = (
        df["EMA_20"]
        - df["EMA_20"].shift(5)
    ) / df["ATR"]

    df["ema50_slope_5"] = (
        df["EMA_50"]
        - df["EMA_50"].shift(5)
    ) / df["ATR"]

    # ==========================================
    # TREND ALIGNMENT
    # ==========================================

    df["trend_alignment"] = np.select(
        [
            (
                (df["EMA_20"] > df["EMA_50"])
                & (df["close"] > df["EMA_20"])
            ),
            (
                (df["EMA_20"] < df["EMA_50"])
                & (df["close"] < df["EMA_20"])
            ),
        ],
        [
            1,
            -1,
        ],
        default=0,
    )

    # ==========================================
    # RSI REGIME
    # ==========================================

    df["rsi_bull"] = (
        df["RSI"] > 55
    ).astype("int8")

    df["rsi_bear"] = (
        df["RSI"] < 45
    ).astype("int8")

    # ==========================================
    # ADX REGIME
    # ==========================================

    df["adx_strong"] = (
        df["ADX_14"] >= 25
    ).astype("int8")

    df["adx_very_strong"] = (
        df["ADX_14"] >= 35
    ).astype("int8")

    # ==========================================
    # DIRECTIONAL MOVEMENT
    # ==========================================

    df["dm_direction"] = np.select(
        [
            df["DMP_14"] > df["DMN_14"],
            df["DMP_14"] < df["DMN_14"],
        ],
        [
            1,
            -1,
        ],
        default=0,
    )

    # ==========================================
    # ATR REGIME
    # ==========================================

    atr_mean = (
        df["ATR"]
        .rolling(100)
        .mean()
    )

    df["atr_regime"] = (
        df["ATR"]
        / atr_mean
    )

    # ==========================================
    # BREAKOUT FEATURES
    # ==========================================

    previous_high = (
        df["high"]
        .rolling(20)
        .max()
        .shift(1)
    )

    previous_low = (
        df["low"]
        .rolling(20)
        .min()
        .shift(1)
    )

    df["breakout_up"] = (
        df["close"]
        > previous_high
    ).astype("int8")

    df["breakout_down"] = (
        df["close"]
        < previous_low
    ).astype("int8")

    df["distance_previous_high"] = (
        (previous_high - df["close"])
        / df["ATR"]
    )

    df["distance_previous_low"] = (
        (df["close"] - previous_low)
        / df["ATR"]
    )

    # ==========================================
    # LIQUIDITY SWEEP
    # ==========================================

    df["sweep_high"] = (
        (
            df["high"] > previous_high
        )
        &
        (
            df["close"] < previous_high
        )
    ).astype("int8")

    df["sweep_low"] = (
        (
            df["low"] < previous_low
        )
        &
        (
            df["close"] > previous_low
        )
    ).astype("int8")

    # ==========================================
    # NORMALIZATION
    # ==========================================

    df = df.replace(
        [np.inf, -np.inf],
        np.nan,
    )

    return df