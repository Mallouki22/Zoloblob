class SignalFilter:

    def validate(self, row, signal):

        # BUY
        if signal == 1:

            if row["EMA_20"] < row["EMA_50"]:
                return False

            if row["ADX_14"] < 25:
                return False

            if row["RSI"] < 55:
                return False

            return True

        # SELL
        if signal == -1:

            if row["EMA_20"] > row["EMA_50"]:
                return False

            if row["ADX_14"] < 25:
                return False

            if row["RSI"] > 45:
                return False

            return True

        return False