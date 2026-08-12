import pandas as pd

from data.cleaner import DataCleaner
from features.pipeline import build_features
from ml.labeler import LabelGenerator


def main():

    print("📂 Chargement du dataset...")

    df = pd.read_parquet(
        "datasets/XAUUSD_15_100k.parquet"
    )

    print("Lignes :", len(df))

    cleaner = DataCleaner(df)
    df = cleaner.run()

    df = build_features(df)
    labeler = LabelGenerator(df)
    df = labeler.generate()

    print("\n===== TARGET =====")
    print(df["target"].value_counts())
    print(df["target"].isna().sum())
    print(df["target"].value_counts(dropna=False))
    df.to_parquet(
        "datasets/XAUUSD_ML_100k.parquet",
        index=False
    )

    print("\n✅ Dataset ML sauvegardé")
    print(df.shape)


if __name__ == "__main__":
    main()
