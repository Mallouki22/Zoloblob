"""
Trading Label Generator
Version professionnelle
"""

class LabelGenerator:

    def __init__(
        self,
        df,
        lookahead=30,
        atr_multiplier=1.0,
        reward_ratio=1.5
    ):

        self.df = df.copy()

        self.lookahead = lookahead
        self.atr_multiplier = atr_multiplier
        self.reward_ratio = reward_ratio

    def generate(self):

        self.df["target"] = 1      # WAIT

        for i in range(len(self.df) - self.lookahead):

            entry = self.df.at[i, "close"]
            atr = self.df.at[i, "ATR"]

            if atr <= 0:
                continue

            future = self.df.iloc[
                i + 1:
                i + self.lookahead + 1
            ]

            future_high = future["high"].max()
            future_low = future["low"].min()

            up = (future_high - entry) / atr
            down = (entry - future_low) / atr

            if up >= 2.0 and up > down:

                self.df.at[i, "target"] = 2      # BUY

            elif down >= 2.0 and down > up:

                self.df.at[i, "target"] = 0      # SELL

            else:

                self.df.at[i, "target"] = 1      # WAIT

        self.df = (
            self.df
            .iloc[:-self.lookahead]
            .copy()
        )

        self.df = self.df.dropna(subset=["target"])

        self.df["target"] = (
            self.df["target"]
            .astype(int)
        )

        self.df.reset_index(drop=True, inplace=True)

        return self.df