"""
Trend indicators
"""

import pandas_ta as ta


def add_trend_features(df):

    df = df.copy()


    # Moyennes mobiles

    df["EMA_20"] = ta.ema(
        df["close"],
        length=20
    )


    df["EMA_50"] = ta.ema(
        df["close"],
        length=50
    )


    # MACD

    macd = ta.macd(
        df["close"]
    )


    df = df.join(macd)

    adx = ta.adx(
        high=df["high"],
        low=df["low"],
        close=df["close"],
        length=14,
    )

    df["ADX_14"] = adx["ADX_14"]
    df["DMP_14"] = adx["DMP_14"]
    df["DMN_14"] = adx["DMN_14"]
    # Distance par rapport aux EMA

    df["EMA20_distance"] = (
        df["close"] - df["EMA_20"]
    ) / df["EMA_20"]

    df["EMA50_distance"] = (
        df["close"] - df["EMA_50"]
    ) / df["EMA_50"]


    # Pente des EMA

    df["EMA20_slope"] = df["EMA_20"].diff()

    df["EMA50_slope"] = df["EMA_50"].diff()


    # Croisement EMA

    df["EMA_cross"] = (
        df["EMA_20"] > df["EMA_50"]
    ).astype(int)
    return df