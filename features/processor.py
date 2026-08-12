"""
Feature Processor

Prépare les données pour le Machine Learning.
"""


class FeatureProcessor:

    def __init__(self, df):

        self.df = df.copy()

    def add_price_features(self):

        df = self.df

        # Corps de la bougie
        df["body"] = df["close"] - df["open"]

        # Taille totale
        df["range"] = df["high"] - df["low"]

        # Mèche haute
        df["upper_wick"] = (
            df["high"]
            - df[["open", "close"]].max(axis=1)
        )

        # Mèche basse
        df["lower_wick"] = (
            df[["open", "close"]].min(axis=1)
            - df["low"]
        )

        # Rendement
        df["return"] = df["close"].pct_change()

        self.df = df

    def remove_nan(self):

        before = len(self.df)

        self.df = (
            self.df
            .dropna()
            .reset_index(drop=True)
        )

        after = len(self.df)

        print(
            f"🧹 Lignes supprimées (NaN) : {before-after}"
        )

    def run(self, drop_na=True):

        print("\n===== PROCESSING =====")

        print("💰 Ajout des Price Action Features...")
        self.add_price_features()

        if drop_na:
            self.remove_nan()

        print(
            f"Dataset final : {len(self.df)} lignes"
        )

        return self.df
