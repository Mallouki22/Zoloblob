from __future__ import annotations

import numpy as np
import pandas as pd


def add_market_structure_features(
    df: pd.DataFrame,
) -> pd.DataFrame:

    df = df.copy()

    high = df["high"]
    low = df["low"]
    close = df["close"]
    open_ = df["open"]

    atr = df["ATR"].replace(0, np.nan)

    # ==========================================
    # TREND
    # ==========================================

    df["ms_trend"] = np.select(
        [
            df["EMA_20"] > df["EMA_50"],
            df["EMA_20"] < df["EMA_50"],
        ],
        [1, -1],
        default=0,
    )

    df["ms_trend_strength"] = (
        (df["EMA_20"] - df["EMA_50"]) / atr
    )

    # ==========================================
    # BOS
    # ==========================================

    swing_high = (
        high
        .rolling(20)
        .max()
        .shift(1)
    )

    swing_low = (
        low
        .rolling(20)
        .min()
        .shift(1)
    )

    df["bos_up"] = (
        close > swing_high
    ).astype("int8")

    df["bos_down"] = (
        close < swing_low
    ).astype("int8")

    df["distance_swing_high"] = (
        (swing_high - close) / atr
    )

    df["distance_swing_low"] = (
        (close - swing_low) / atr
    )

    # ==========================================
    # LIQUIDITY
    # ==========================================

    previous_high = high.shift(1)
    previous_low = low.shift(1)

    df["equal_high"] = (
        (high - previous_high).abs()
        <= atr * 0.15
    ).astype("int8")

    df["equal_low"] = (
        (low - previous_low).abs()
        <= atr * 0.15
    ).astype("int8")

    df["liquidity_sweep_high"] = (
        (high > swing_high)
        & (close < swing_high)
    ).astype("int8")

    df["liquidity_sweep_low"] = (
        (low < swing_low)
        & (close > swing_low)
    ).astype("int8")

    # ==========================================
    # FVG
    # ==========================================

    bullish_fvg = (
        low > high.shift(2)
    )

    bearish_fvg = (
        high < low.shift(2)
    )

    df["bullish_fvg"] = (
        bullish_fvg
    ).astype("int8")

    df["bearish_fvg"] = (
        bearish_fvg
    ).astype("int8")

    df["fvg_size"] = np.where(
        bullish_fvg,
        (low - high.shift(2)) / atr,
        np.where(
            bearish_fvg,
            (low.shift(2) - high) / atr,
            0,
        ),
    )

    # ==========================================
    # ORDER BLOCK APPROXIMATION
    # ==========================================

    previous_bearish = (
        close.shift(1)
        < open_.shift(1)
    )

    previous_bullish = (
        close.shift(1)
        > open_.shift(1)
    )

    df["bullish_ob"] = (
        previous_bearish
        & (close > high.shift(1))
    ).astype("int8")

    df["bearish_ob"] = (
        previous_bullish
        & (close < low.shift(1))
    ).astype("int8")

    # ==========================================
    # PREMIUM / DISCOUNT
    # ==========================================

    range_high = (
        high
        .rolling(40)
        .max()
    )

    range_low = (
        low
        .rolling(40)
        .min()
    )

    midpoint = (
        range_high + range_low
    ) / 2

    df["premium_discount"] = (
        (close - midpoint)
        / (range_high - range_low)
    )

    df["discount_zone"] = (
        close < midpoint
    ).astype("int8")

    df["premium_zone"] = (
        close > midpoint
    ).astype("int8")

    # ==========================================
    # MARKET STRUCTURE SCORE
    # ==========================================

    df["market_structure_score"] = (
        df["ms_trend"]
        + df["bos_up"]
        - df["bos_down"]
        + df["liquidity_sweep_low"]
        - df["liquidity_sweep_high"]
        + df["bullish_fvg"]
        - df["bearish_fvg"]
        + df["bullish_ob"]
        - df["bearish_ob"]
    )

    # ==========================================
    # CLEAN
    # ==========================================

    df = df.replace(
        [np.inf, -np.inf],
        np.nan,
    )

    return df