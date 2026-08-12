"""
ADX Trend Filter
"""

import pandas as pd


class ADXFilter:

    def __init__(
        self,
        minimum=25,
    ):

        self.minimum = minimum

    def allow(
        self,
        df: pd.DataFrame,
    ):

        if "ADX" not in df.columns:
            return True

        return df["ADX"].iloc[-1] >= self.minimum