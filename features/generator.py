"""
Feature Generator

Ajoute toutes les features techniques.
"""

from features.trend import add_trend_features
from features.momentum import add_momentum_features
from features.volatility import add_volatility_features



class FeatureGenerator:


    def __init__(self, df):

        self.df = df.copy()



    def generate(self):

        print("\n===== FEATURE ENGINEERING =====")


        print("📈 Ajout des indicateurs de tendance...")
        self.df = add_trend_features(self.df)


        print("⚡ Ajout des indicateurs de momentum...")
        self.df = add_momentum_features(self.df)


        print("🌡️ Ajout de la volatilité...")
        self.df = add_volatility_features(self.df)


        return self.df