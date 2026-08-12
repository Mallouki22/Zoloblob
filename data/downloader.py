"""
Data Downloader

Télécharge les données historiques depuis MetaTrader 5
et les transforme en DataFrame pandas.
"""

import pandas as pd
import MetaTrader5 as mt5

from mt5.client import MT5Client
from config.settings import (
    DEFAULT_SYMBOL,
    DEFAULT_TIMEFRAME,
    DEFAULT_BARS,
    DATASET_DIR
)
from config.constants import TIMEFRAMES


class DataDownloader:

    def __init__(self):

        self.client = MT5Client()

        self.symbol = DEFAULT_SYMBOL

        self.timeframe = TIMEFRAMES[DEFAULT_TIMEFRAME]

        self.bars = DEFAULT_BARS


    def download(self, bars=None):
        """
        Télécharge les données historiques.
        """

        self.client.initialize()

        symbol = self.client.find_symbol(
            self.symbol
        )

        if bars is None:
            bars = self.bars

        print(f"📊 Symbole utilisé : {symbol}")
        print("Symbol :", symbol)
        print("Timeframe :", self.timeframe)
        print("Bars :", bars)

        rates = self.client.get_rates(
            symbol,
            self.timeframe,
            bars
        )

        df = pd.DataFrame(rates)

        df["time"] = pd.to_datetime(
            df["time"],
            unit="s"
        )

        df = (
            df
            .sort_values("time")
            .reset_index(drop=True)
        )

        return df
    
    def download_latest(self):
            """
            Télécharge uniquement la dernière bougie.
            """

            self.client.initialize()

            symbol = self.client.find_symbol(
                self.symbol
            )

            rates = self.client.get_rates(
                symbol,
                self.timeframe,
                2
            )

            df = pd.DataFrame(rates)

            df["time"] = pd.to_datetime(
                df["time"],
                unit="s"
            )

            df = (
                df
                .sort_values("time")
                .reset_index(drop=True)
            )

            return df
    def save(self, df, filename=None):
        """
        Sauvegarde un DataFrame en format Parquet.
        """

        if filename is None:
            filename = (
                f"{self.symbol}_"
                f"{self.timeframe}_100k"
                ".parquet"
            )


        path = DATASET_DIR / filename


        df.to_parquet(
            path,
            engine="pyarrow"
        )


        print(f"💾 Données sauvegardées : {path}")

        return path