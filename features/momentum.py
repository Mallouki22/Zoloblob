"""
Momentum indicators
"""

import pandas_ta as ta


def add_momentum_features(df):

    df = df.copy()


    df["RSI"] = ta.rsi(
        df["close"],
        length=14
    )
    df["CCI"] = ta.cci(
        high=df["high"],
        low=df["low"],
        close=df["close"],
        length=20
    )

    stoch = ta.stochrsi(
        df["close"]
    )

    df = df.join(stoch)
    
    df["WILLR"] = ta.willr(
        high=df["high"],
        low=df["low"],
        close=df["close"],
        length=14
    )
    # Variation du RSI
    df["RSI_change"] = df["RSI"].diff()

    # Distance du RSI à la zone neutre
    df["RSI_distance_50"] = df["RSI"] - 50

    # Variation du CCI
    df["CCI_change"] = df["CCI"].diff()

    # Variation du Williams %R
    df["WILLR_change"] = df["WILLR"].diff()

    # Variation du Stochastic RSI
    if "STOCHRSIk_14_14_3_3" in df.columns:
        df["STOCH_K_change"] = df["STOCHRSIk_14_14_3_3"].diff()

    if "STOCHRSId_14_14_3_3" in df.columns:
        df["STOCH_D_change"] = df["STOCHRSId_14_14_3_3"].diff()

    # Variation du MACD
    if "MACD_12_26_9" in df.columns:
        df["MACD_change"] = df["MACD_12_26_9"].diff()

    if "MACDh_12_26_9" in df.columns:
        df["MACDh_change"] = df["MACDh_12_26_9"].diff()
    return df