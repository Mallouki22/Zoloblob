"""
Trailing Stop Manager
"""


class TrailingStopManager:

    def calculate(
        self,
        signal,
        current_price,
        atr,
    ):

        if signal == "BUY":

            return current_price - atr

        return current_price + atr

    def should_update(
        self,
        signal,
        current_sl,
        new_sl,
    ):

        if signal == "BUY":

            return new_sl > current_sl

        return new_sl < current_sl