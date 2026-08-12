"""
Dataset Loader

Charge les données historiques sauvegardées.
"""

import pandas as pd

from config.settings import DATASET_DIR


class DataLoader:


    def __init__(self, filename):

        self.path = DATASET_DIR / filename



    def load(self):

        if not self.path.exists():

            raise FileNotFoundError(
                f"Dataset introuvable : {self.path}"
            )


        df = pd.read_parquet(
            self.path
        )


        print(
            f"📂 Dataset chargé : {self.path}"
        )


        print(
            f"Nombre de lignes : {len(df)}"
        )


        return df