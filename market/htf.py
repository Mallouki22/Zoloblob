"""
Higher Time Frame Filter
"""

import MetaTrader5 as mt5

from data.market_data import MarketData


class HTFTrend:

    def __init__(self):

        self.market = MarketData()

    def direction(
        self,
        symbol,
    ):

        df = self.market.get_rates(
            symbol=symbol,
            timeframe=mt5.TIMEFRAME_H1,
            bars=300,
        )

        if df is None or len(df) < 60:
            return "RANGE"

        ema20 = df["EMA_20"].iloc[-1]
        ema50 = df["EMA_50"].iloc[-1]

        if ema20 > ema50:
            return "BUY"

        if ema20 < ema50:
            return "SELL"

        return "RANGE"

    def validate(
        self,
        symbol,
        signal,
    ):

        trend = self.direction(symbol)

        return trend == signal