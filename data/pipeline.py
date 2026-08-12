"""
Data Pipeline

Construit le DataFrame prêt pour le modèle ML.
"""

from data.downloader import DataDownloader
from features.pipeline import build_features


class DataPipeline:

    def __init__(self):

        self.downloader = DataDownloader()

    def run(
        self,
        bars=None
    ):

        df = self.downloader.download(
            bars=bars
        )

        return build_features(df)
