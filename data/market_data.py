"""
Market Data Manager
"""

from data.pipeline import DataPipeline


class MarketDataManager:

    def __init__(self):

        self.pipeline = DataPipeline()

        self.data = None
        self.history_size = 200

    def initialize(self):

        print("📥 Chargement initial...")

        self.data = self.pipeline.run(
            bars=100000
        )

        return self.data

    def latest(self):

        return self.data
    
    def update(self):
        """
        Met à jour les données de marché.
        """

        print("🔄 Mise à jour des données...")

        df = self.pipeline.run(
            bars=300
        )

        self.data = df.tail(
            self.history_size
        ).reset_index(drop=True)

        return self.data