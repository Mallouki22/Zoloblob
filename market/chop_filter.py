"""
Choppiness Filter
"""

import pandas as pd


class ChopFilter:

    def __init__(
        self,
        maximum=55,
    ):

        self.maximum = maximum

    def allow(
        self,
        df: pd.DataFrame,
    ):

        if "CHOP" not in df.columns:
            return True

        return df["CHOP"].iloc[-1] <= self.maximum