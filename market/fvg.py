"""
Fair Value Gap
"""

import pandas as pd


class FairValueGap:

    def detect(
        self,
        df: pd.DataFrame,
    ):

        gaps = []

        for i in range(2, len(df)):

            prev = df.iloc[i - 2]
            cur = df.iloc[i]

            if prev.high < cur.low:

                gaps.append({

                    "type": "BULL",

                    "low": prev.high,

                    "high": cur.low,

                    "index": i,
                })

            elif prev.low > cur.high:

                gaps.append({

                    "type": "BEAR",

                    "low": cur.high,

                    "high": prev.low,

                    "index": i,
                })

        return gaps

    def nearest(
        self,
        price,
        gaps,
    ):

        if not gaps:
            return None

        return min(

            gaps,

            key=lambda g: abs(

                ((g["low"] + g["high"]) / 2)

                - price
            ),
        )

    def inside(
        self,
        price,
        gap,
    ):

        if gap is None:
            return False

        return gap["low"] <= price <= gap["high"]