"""
Data Cleaner

Nettoyage des données historiques.
"""


class DataCleaner:


    def __init__(self, df):

        self.df = df.copy()



    def remove_duplicates(self):

        before = len(self.df)


        self.df = (
            self.df
            .drop_duplicates()
        )


        after = len(self.df)


        print(
            f"Doublons supprimés : {before-after}"
        )



    def remove_missing(self):

        before = len(self.df)


        self.df = (
            self.df
            .dropna()
        )


        after = len(self.df)


        print(
            f"Lignes avec valeurs manquantes supprimées : {before-after}"
        )



    def check_ohlc(self):

        condition = (

            (self.df["high"] >= self.df["open"]) &
            (self.df["high"] >= self.df["close"]) &
            (self.df["low"] <= self.df["open"]) &
            (self.df["low"] <= self.df["close"])

        )


        invalid = (~condition).sum()


        if invalid > 0:

            print(
                f"⚠️ Bougies invalides : {invalid}"
            )

            self.df = self.df[condition]


        else:

            print(
                "Bougies OHLC valides ✅"
            )



    def run(self):

        print("\n===== CLEANING =====")


        self.remove_duplicates()

        self.remove_missing()

        self.check_ohlc()


        self.df = (
            self.df
            .sort_values("time")
            .reset_index(drop=True)
        )


        return self.df