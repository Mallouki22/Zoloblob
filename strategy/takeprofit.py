"""
Take Profit Manager
"""


class TakeProfitManager:

    def __init__(
        self,
        ratio=2
    ):

        self.ratio = ratio


    def calculate(
        self,
        signal,
        entry,
        distance
    ):

        if signal == "BUY":

            return entry + distance * self.ratio

        return entry - distance * self.ratio