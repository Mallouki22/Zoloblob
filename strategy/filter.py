"""Single entry filter shared by live execution and the backtest."""

from __future__ import annotations
from strategy.dxy_filter import DXYFilter

from config.settings import (
    BUY_MIN_CONFIDENCE,
    MAX_OPEN_TRADES,
    MAX_SPREAD,
    SELL_MIN_CONFIDENCE,
)


class TradeFilter:
    def __init__(
        self,
        buy_min_confidence: float = BUY_MIN_CONFIDENCE,
        sell_min_confidence: float = SELL_MIN_CONFIDENCE,
        max_spread: float = MAX_SPREAD,
        max_open_trades: int = MAX_OPEN_TRADES,
    ):
        self.buy_min_confidence = buy_min_confidence
        self.sell_min_confidence = sell_min_confidence
        self.max_spread = max_spread
        self.max_open_trades = max_open_trades
        self.dxy = DXYFilter()

    def required_confidence(self, signal: str) -> float:
        return (
            self.buy_min_confidence if signal == "BUY" else self.sell_min_confidence
        )

    def check(self, prediction, symbol_info, position_manager, symbol):
        signal = prediction["signal"]
        if signal == "WAIT":
            return False, "Signal WAIT"
        print("Confidence =", prediction["confidence"])
        print("Required   =", self.required_confidence(signal))
        if prediction["confidence"] < self.required_confidence(signal):
            return False, "Confiance insuffisante"
        if not self.dxy.allow(signal):
            return False, "DXY ne confirme pas le trade"
        if symbol_info is None:
            return False, "Informations symbole indisponibles"
        if symbol_info.spread > self.max_spread:
            return False, "Spread trop élevé"
        if position_manager.count(symbol) >= self.max_open_trades:
            return False, "Nombre maximal de positions atteint"
        return True, "OK"
