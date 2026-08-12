"""
Stop Loss Manager
"""


class StopLossManager:

    def __init__(
        self,
        multiplier=2
    ):

        self.multiplier = multiplier


    def calculate(
        self,
        signal,
        entry,
        atr
    ):

        distance = atr * self.multiplier

        if signal == "BUY":

            sl = entry - distance

        else:

            sl = entry + distance

        return sl, distance