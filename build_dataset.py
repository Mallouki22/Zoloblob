import pandas as pd

from data.cleaner import DataCleaner
from features.pipeline import build_features
from ml.labeler import LabelGenerator
from features.ml_market import add_ml_market_features
from features.market_structure_features import (
    add_market_structure_features,
)
INPUT_PATH = (
    "datasets/XAUUSD_15_100k.parquet"
)

OUTPUT_PATH = (
    "datasets/XAUUSD_ML_100k.parquet"
)


def main():

    print(
        "📂 Chargement du dataset..."
    )

    df = pd.read_parquet(
        INPUT_PATH
    )

    print(
        "Lignes :",
        len(df)
    )

    # ==========================================
    # CLEANING
    # ==========================================

    cleaner = DataCleaner(df)

    df = cleaner.run()

    # ==========================================
    # FEATURES
    # ==========================================

    print(
        "\n===== FEATURE ENGINEERING ====="
    )

    df = build_features(df)
    df = add_market_structure_features(df)
    # ==========================================
    # LABELING
    # ==========================================

    print(
        "\n===== TARGET GENERATION ====="
    )

    labeler = LabelGenerator(
        horizon=32,
        atr_multiplier=1.2,
        reward_risk=1.5,
    )

    df = labeler.generate(df)

    # ==========================================
    # REMOVE INVALID ROWS
    # ==========================================

    df = df.dropna(
        subset=["target"]
    ).copy()

    df["target"] = (
        df["target"]
        .astype("int8")
    )

    # ==========================================
    # TARGET REPORT
    # ==========================================

    print(
        "\n===== TARGET ====="
    )

    counts = (
        df["target"]
        .value_counts()
        .sort_index()
    )

    print(counts)

    print(
        "\n===== TARGET % ====="
    )

    print(
        (
            df["target"]
            .value_counts(
                normalize=True
            )
            .sort_index()
            * 100
        ).round(2)
    )

    print(
        "\nSELL :",
        int(
            (df["target"] == 0).sum()
        )
    )

    print(
        "WAIT :",
        int(
            (df["target"] == 1).sum()
        )
    )

    print(
        "BUY  :",
        int(
            (df["target"] == 2).sum()
        )
    )

    # ==========================================
    # SAVE
    # ==========================================

    df.to_parquet(
        OUTPUT_PATH,
        index=False,
    )

    print(
        "\n✅ Dataset ML sauvegardé"
    )

    print(
        df.shape
    )


if __name__ == "__main__":
    main()