"""
DXY Data
"""

import yfinance as yf


class DXYData:

    SYMBOL = "DX-Y.NYB"

    def latest(self, period="5d", interval="15m"):

        df = yf.download(
            self.SYMBOL,
            period=period,
            interval=interval,
            progress=False,
            auto_adjust=True,
        )

        if df.empty:
            return df

        if hasattr(df.columns, "nlevels") and df.columns.nlevels > 1:
            df.columns = df.columns.get_level_values(0)

        return df