"""
Volatility indicators
"""

import pandas as pd
import pandas_ta as ta
import numpy as np

def add_volatility_features(df):

    df = df.copy()


    df["ATR"] = ta.atr(
        high=df["high"],
        low=df["low"],
        close=df["close"],
        length=14
    )
    bb = ta.bbands(
        df["close"],
        length=20
    )

    df = df.join(bb)
    # Variation de l'ATR
    df["ATR_change"] = df["ATR"].diff()

    # ATR relatif au prix
    df["ATR_percent"] = (
        df["ATR"] / df["close"]
    )

    # Largeur des bandes de Bollinger
    if "BBB_20_2.0_2.0" in df.columns:
        df["BB_width"] = df["BBB_20_2.0_2.0"]

    # Position du prix dans les bandes
    if (
        "BBL_20_2.0_2.0" in df.columns
        and "BBU_20_2.0_2.0" in df.columns
    ):
        df["BB_position"] = (
            (df["close"] - df["BBL_20_2.0_2.0"])
            /
            (
                df["BBU_20_2.0_2.0"]
                - df["BBL_20_2.0_2.0"]
            )
        )

    # Distance à la bande haute
    if "BBU_20_2.0_2.0" in df.columns:
        df["Distance_BB_upper"] = (
            df["BBU_20_2.0_2.0"] - df["close"]
        )

    # Distance à la bande basse
    if "BBL_20_2.0_2.0" in df.columns:
        df["Distance_BB_lower"] = (
            df["close"] - df["BBL_20_2.0_2.0"]
        )
        
    highest = df["high"].rolling(14).max()

    lowest = df["low"].rolling(14).min()

    tr = pd.concat(
        [
            df["high"] - df["low"],
            (df["high"] - df["close"].shift()).abs(),
            (df["low"] - df["close"].shift()).abs(),
        ],
        axis=1,
    ).max(axis=1)

    atr_sum = tr.rolling(14).sum()

    df["CHOP"] = (
        100
        * np.log10(
            atr_sum / (highest - lowest)
        )
        / np.log10(14)
    )
    return df