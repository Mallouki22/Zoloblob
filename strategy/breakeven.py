"""
Break Even Manager
"""


class BreakEvenManager:

    def should_move(
        self,
        signal,
        entry,
        current,
        atr,
    ):

        if signal == "BUY":

            return current >= entry + atr

        return current <= entry - atr

    def break_even_price(
        self,
        signal,
        entry,
        spread=0.0,
    ):

        if signal == "BUY":

            return entry + spread

        return entry - spread