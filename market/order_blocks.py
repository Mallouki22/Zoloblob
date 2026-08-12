"""
Order Blocks
"""

import pandas as pd


class OrderBlocks:

    def bullish(
        self,
        df: pd.DataFrame,
        lookback=40,
    ):

        candles = df.tail(lookback)

        bearish = candles[candles.close < candles.open]

        if bearish.empty:
            return None

        row = bearish.iloc[-1]

        return {

            "low": row.low,

            "high": row.high,

            "time": row.time,
        }

    def bearish(
        self,
        df: pd.DataFrame,
        lookback=40,
    ):

        candles = df.tail(lookback)

        bullish = candles[candles.close > candles.open]

        if bullish.empty:
            return None

        row = bullish.iloc[-1]

        return {

            "low": row.low,

            "high": row.high,

            "time": row.time,
        }

    def inside(
        self,
        price,
        block,
    ):

        if block is None:
            return False

        return block["low"] <= price <= block["high"]