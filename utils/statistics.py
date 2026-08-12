"""
Trading Statistics
"""


class TradingStatistics:

    def __init__(self):

        self.predictions = 0

        self.buy = 0

        self.sell = 0

        self.wait = 0

        self.executed = 0

        self.refused = 0

    def add_prediction(
        self,
        signal
    ):

        self.predictions += 1

        if signal == "BUY":

            self.buy += 1

        elif signal == "SELL":

            self.sell += 1

        else:

            self.wait += 1

    def add_trade(self):

        self.executed += 1

    def add_refused(self):

        self.refused += 1

    def show(self):

        print("\n========== STATISTICS ==========")

        print("Predictions :", self.predictions)

        print("BUY         :", self.buy)

        print("SELL        :", self.sell)

        print("WAIT        :", self.wait)

        print("Executed    :", self.executed)

        print("Refused     :", self.refused)

        print("================================")