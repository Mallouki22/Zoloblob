"""Final trade safety filter."""

from __future__ import annotations

from strategy.dxy_filter import DXYFilter

from config.settings import (
    BUY_MIN_CONFIDENCE,
    SELL_MIN_CONFIDENCE,
    MAX_OPEN_TRADES,
    MAX_SPREAD,
)


class TradeFilter:

    def __init__(
        self,
        buy_min_confidence=BUY_MIN_CONFIDENCE,
        sell_min_confidence=SELL_MIN_CONFIDENCE,
        max_spread=MAX_SPREAD,
        max_open_trades=MAX_OPEN_TRADES,
    ):
        self.buy_min_confidence = float(
            buy_min_confidence
        )

        self.sell_min_confidence = float(
            sell_min_confidence
        )

        self.max_spread = float(max_spread)
        self.max_open_trades = int(max_open_trades)

        self.dxy = DXYFilter()

    def required_confidence(self, signal):

        if signal == "BUY":
            return self.buy_min_confidence

        if signal == "SELL":
            return self.sell_min_confidence

        return 1.0

    def check(
        self,
        prediction,
        symbol_info,
        position_manager,
        symbol,
    ):

        signal = prediction.get("signal")

        if signal == "WAIT":
            return False, "Signal WAIT"

        confidence = float(
            prediction.get("confidence", 0.0)
        )

        required = self.required_confidence(
            signal
        )

        if confidence < required:
            return False, "Confiance insuffisante"

        if not self.dxy.allow(signal):
            return False, "DXY ne confirme pas"

        if symbol_info is None:
            return False, "Informations symbole indisponibles"

        spread = float(
            getattr(symbol_info, "spread", 0)
        )

        if spread > self.max_spread:
            return False, "Spread trop élevé"

        if (
            position_manager.count(symbol)
            >= self.max_open_trades
        ):
            return False, "Nombre maximal de positions atteint"

        return True, "OK"